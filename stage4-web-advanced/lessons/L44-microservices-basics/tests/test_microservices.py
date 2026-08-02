# tests/test_microservices.py
"""
L44 微服务架构测试
"""

from __future__ import annotations

import pytest


# ==================== 测试数据模型 ====================


class MockConsul:
    """测试用模拟 Consul"""

    def __init__(self):
        self._services = {}
        self._instances = {}

    def register(self, service_name, instance_id, host, port, **kwargs):
        self._instances[instance_id] = {
            "service_name": service_name,
            "instance_id": instance_id,
            "host": host,
            "port": port,
            "healthy": True,
        }
        if service_name not in self._services:
            self._services[service_name] = []
        self._services[service_name].append(instance_id)
        return True

    def deregister(self, instance_id):
        if instance_id not in self._instances:
            return False
        instance = self._instances[instance_id]
        service = self._services.get(instance["service_name"], [])
        if instance_id in service:
            service.remove(instance_id)
        del self._instances[instance_id]
        return True

    def discover(self, service_name):
        instances = self._services.get(service_name, [])
        healthy = [i for i in instances if self._instances.get(i, {}).get("healthy")]
        if healthy:
            return self._instances[healthy[0]]
        return None

    def set_health(self, instance_id, healthy):
        if instance_id in self._instances:
            self._instances[instance_id]["healthy"] = healthy


class TestServiceDiscovery:
    """测试服务发现"""

    def test_register_service(self):
        """测试服务注册"""
        consul = MockConsul()

        result = consul.register(
            service_name="user-service", instance_id="user-1", host="localhost", port=8001
        )

        assert result is True
        assert "user-1" in consul._instances
        assert "user-service" in consul._services

    def test_discover_service(self):
        """测试服务发现"""
        consul = MockConsul()

        # 注册服务
        consul.register("user-service", "user-1", "localhost", 8001)
        consul.register("user-service", "user-2", "localhost", 8002)

        # 发现服务
        instance = consul.discover("user-service")

        assert instance is not None
        assert instance["service_name"] == "user-service"
        assert instance["instance_id"] in ["user-1", "user-2"]

    def test_deregister_service(self):
        """测试服务注销"""
        consul = MockConsul()

        consul.register("user-service", "user-1", "localhost", 8001)
        result = consul.deregister("user-1")

        assert result is True
        assert "user-1" not in consul._instances

    def test_discover_nonexistent_service(self):
        """测试发现不存在的服务"""
        consul = MockConsul()

        instance = consul.discover("nonexistent-service")

        assert instance is None

    def test_health_check(self):
        """测试健康检查"""
        consul = MockConsul()

        consul.register("user-service", "user-1", "localhost", 8001)
        consul.set_health("user-1", False)

        instance = consul.discover("user-service")

        assert instance is None


class CircuitBreaker:
    """测试用断路器"""

    def __init__(self, failure_threshold=3):
        self.failure_threshold = failure_threshold
        self._state = "closed"
        self._consecutive_failures = 0
        self._call_count = 0

    def call(self, func):
        self._call_count += 1
        try:
            result = func()
            self._consecutive_failures = 0
            return result
        except Exception:
            self._consecutive_failures += 1
            if self._consecutive_failures >= self.failure_threshold:
                self._state = "open"
            raise

    @property
    def state(self):
        return self._state

    def reset(self):
        self._state = "closed"
        self._consecutive_failures = 0


class TestCircuitBreaker:
    """测试断路器"""

    def test_normal_operation(self):
        """测试正常操作"""
        cb = CircuitBreaker(failure_threshold=3)

        def succeed():
            return "success"

        result = cb.call(succeed)

        assert result == "success"
        assert cb.state == "closed"

    def test_circuit_opens_after_failures(self):
        """测试连续失败后断路器打开"""
        cb = CircuitBreaker(failure_threshold=3)

        def fail():
            raise ConnectionError("Failed")

        for _ in range(3):
            with pytest.raises(ConnectionError):
                cb.call(fail)

        assert cb.state == "open"

    def test_circuit_stays_closed_with_success(self):
        """测试成功后重置失败计数"""
        cb = CircuitBreaker(failure_threshold=3)

        def sometimes_fail():
            if cb._call_count % 2 == 0:
                raise ConnectionError("Failed")
            return "success"

        for _ in range(6):
            try:
                cb.call(sometimes_fail)
            except ConnectionError:
                pass

        # 不会打开，因为有成功
        assert cb.state == "closed"


class RateLimiter:
    """测试用限流器"""

    def __init__(self, rate=5, window=60):
        self.rate = rate
        self.window = window
        self._requests = {}

    def is_allowed(self, client_id):
        import time

        now = time.time()
        cutoff = now - self.window

        if client_id not in self._requests:
            self._requests[client_id] = []

        # 清理过期请求
        self._requests[client_id] = [t for t in self._requests[client_id] if t > cutoff]

        return len(self._requests[client_id]) < self.rate

    def record_request(self, client_id):
        import time

        if client_id not in self._requests:
            self._requests[client_id] = []
        self._requests[client_id].append(time.time())


class TestRateLimiter:
    """测试限流器"""

    def test_allows_requests_under_limit(self):
        """测试限额内允许请求"""
        limiter = RateLimiter(rate=5)

        for i in range(5):
            assert limiter.is_allowed("client-1") is True
            limiter.record_request("client-1")

    def test_blocks_requests_over_limit(self):
        """测试超过限额拒绝请求"""
        limiter = RateLimiter(rate=3)

        # 前 3 个请求允许
        for i in range(3):
            limiter.record_request("client-1")

        # 第 4 个请求拒绝
        assert limiter.is_allowed("client-1") is False

    def test_different_clients_independent(self):
        """测试不同客户端独立限流"""
        limiter = RateLimiter(rate=2)

        # 每个客户端独立计数
        limiter.record_request("client-1")
        limiter.record_request("client-1")
        assert limiter.is_allowed("client-1") is False

        # client-2 不受影响
        assert limiter.is_allowed("client-2") is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
