# examples/01_service_discovery.py
"""
服务发现实现 - 使用 Consul 进行服务注册与发现

本模块演示微服务架构中的服务发现问题。
"""

from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass, field
from datetime import datetime

# ==================== 数据模型 ====================


@dataclass
class ServiceInstance:
    """服务实例"""

    service_name: str
    instance_id: str
    host: str
    port: int
    health_check_url: str
    metadata: dict = field(default_factory=dict)
    registered_at: datetime = field(default_factory=datetime.now)
    healthy: bool = True


@dataclass
class ServiceInfo:
    """服务信息"""

    name: str
    instances: list[ServiceInstance] = field(default_factory=list)

    def healthy_instances(self) -> list[ServiceInstance]:
        """获取健康实例"""
        return [i for i in self.instances if i.healthy]

    def random_instance(self) -> ServiceInstance | None:
        """随机获取一个健康实例"""
        healthy = self.healthy_instances()
        return random.choice(healthy) if healthy else None


# ==================== 模拟 Consul ====================


class MockConsul:
    """
    模拟 Consul 服务注册中心

    提供服务注册、注销、健康检查和发现功能。
    """

    def __init__(self):
        self._services: dict[str, ServiceInfo] = {}
        self._instance_map: dict[str, ServiceInstance] = {}

    def register(
        self,
        service_name: str,
        instance_id: str,
        host: str,
        port: int,
        health_check_url: str = "",
        metadata: dict = None,
    ) -> bool:
        """注册服务实例"""
        instance = ServiceInstance(
            service_name=service_name,
            instance_id=instance_id,
            host=host,
            port=port,
            health_check_url=health_check_url,
            metadata=metadata or {},
        )

        self._instance_map[instance_id] = instance

        if service_name not in self._services:
            self._services[service_name] = ServiceInfo(name=service_name)

        self._services[service_name].instances.append(instance)
        print(f"  [Consul] 注册服务: {service_name}/{instance_id} -> {host}:{port}")
        return True

    def deregister(self, instance_id: str) -> bool:
        """注销服务实例"""
        if instance_id not in self._instance_map:
            return False

        instance = self._instance_map[instance_id]
        service = self._services.get(instance.service_name)

        if service:
            service.instances = [i for i in service.instances if i.instance_id != instance_id]

        del self._instance_map[instance_id]
        print(f"  [Consul] 注销服务: {instance_id}")
        return True

    def discover(self, service_name: str) -> ServiceInstance | None:
        """发现服务 - 负载均衡（随机）"""
        service = self._services.get(service_name)
        if not service:
            print(f"  [Consul] 服务不存在: {service_name}")
            return None

        healthy = service.healthy_instances()
        if not healthy:
            print(f"  [Consul] 无健康实例: {service_name}")
            return None

        instance = random.choice(healthy)
        print(f"  [Consul] 发现服务: {service_name} -> {instance.host}:{instance.port}")
        return instance

    def discover_all(self, service_name: str) -> list[ServiceInstance]:
        """获取所有健康实例"""
        service = self._services.get(service_name)
        if not service:
            return []
        return service.healthy_instances()

    def set_health(self, instance_id: str, healthy: bool):
        """设置实例健康状态"""
        if instance_id in self._instance_map:
            self._instance_map[instance_id].healthy = healthy
            status = "健康" if healthy else "不健康"
            print(f"  [Consul] 设置健康状态: {instance_id} -> {status}")


# ==================== 服务客户端 ====================


class ServiceClient:
    """服务客户端 - 使用服务发现"""

    def __init__(self, consul: MockConsul):
        self.consul = consul
        self._cache: dict[str, ServiceInstance] = {}
        self._cache_ttl = 30

    async def call_service(self, service_name: str, path: str = "/health") -> dict | None:
        """调用远程服务"""
        # 发现服务
        instance = self.consul.discover(service_name)

        if not instance:
            return {"error": f"服务不可用: {service_name}"}

        # 模拟 HTTP 调用
        await asyncio.sleep(0.05)
        return {
            "service": service_name,
            "instance": instance.instance_id,
            "host": instance.host,
            "port": instance.port,
            "path": path,
            "status": "ok",
        }

    async def call_with_retry(
        self, service_name: str, path: str = "/health", max_retries: int = 3
    ) -> dict | None:
        """带重试的服务调用"""
        for attempt in range(max_retries):
            result = await self.call_service(service_name, path)
            if result and "error" not in result:
                return result

            if attempt < max_retries - 1:
                print(f"  重试... (尝试 {attempt + 2}/{max_retries})")
                await asyncio.sleep(0.5)

        return {"error": f"服务调用失败: {service_name}"}


# ==================== 模拟服务 ====================


class Microservice:
    """模拟微服务"""

    def __init__(self, name: str, consul: MockConsul, port: int):
        self.name = name
        self.consul = consul
        self.port = port
        self.instance_id = f"{name}-{port}"
        self.running = False

    async def start(self):
        """启动服务"""
        self.consul.register(
            service_name=self.name,
            instance_id=self.instance_id,
            host="localhost",
            port=self.port,
            health_check_url=f"http://localhost:{self.port}/health",
            metadata={"version": "1.0"},
        )
        self.running = True
        print(f"  [服务] 启动: {self.name} (端口 {self.port})")

    async def stop(self):
        """停止服务"""
        self.consul.deregister(self.instance_id)
        self.running = False
        print(f"  [服务] 停止: {self.name}")


# ==================== 演示 ====================


async def demo_basic_discovery():
    """演示基础服务发现"""
    print("\n" + "=" * 60)
    print("基础服务发现演示")
    print("=" * 60)

    # 初始化
    consul = MockConsul()
    client = ServiceClient(consul)

    # 启动服务
    user_service = Microservice("user-service", consul, 8001)
    order_service = Microservice("order-service", consul, 8002)

    await user_service.start()
    await order_service.start()

    # 服务发现
    print("\n[1] 调用用户服务")
    result = await client.call_service("user-service")
    print(f"    结果: {result}")

    print("\n[2] 多次调用订单服务（观察负载均衡）")
    for i in range(3):
        result = await client.call_service("order-service")
        print(f"    第{i + 1}次: instance={result.get('instance') if result else 'error'}")

    # 停止服务
    await user_service.stop()


async def demo_service_failover():
    """演示服务故障转移"""
    print("\n" + "=" * 60)
    print("服务故障转移演示")
    print("=" * 60)

    consul = MockConsul()
    client = ServiceClient(consul)

    # 启动多个订单服务实例
    instances = []
    for port in [8010, 8011, 8012]:
        service = Microservice("order-service-v2", consul, port)
        await service.start()
        instances.append(service)

    # 调用服务
    print("\n[1] 正常调用")
    result = await client.call_service("order-service-v2")
    print(f"    结果: instance={result.get('instance') if result else 'error'}")

    # 模拟一个实例故障
    print("\n[2] 模拟实例故障")
    consul.set_health("order-service-v2-8010", False)

    # 再次调用
    print("\n[3] 再次调用（故障实例已排除）")
    for i in range(3):
        result = await client.call_service("order-service-v2")
        instance = result.get("instance") if result else "error"
        print(f"    第{i + 1}次: instance={instance}")

    # 恢复实例
    print("\n[4] 恢复故障实例")
    consul.set_health("order-service-v2-8010", True)

    # 清理
    for service in instances:
        await service.stop()


async def demo_retry_mechanism():
    """演示重试机制"""
    print("\n" + "=" * 60)
    print("服务调用重试机制演示")
    print("=" * 60)

    consul = MockConsul()
    client = ServiceClient(consul)

    # 启动服务
    service = Microservice("payment-service", consul, 8020)
    await service.start()

    # 正常调用
    print("\n[1] 正常调用")
    result = await client.call_with_retry("payment-service")
    print(f"    结果: {result}")

    # 停止服务
    await service.stop()

    # 调用不可用服务
    print("\n[2] 调用不可用服务（带重试）")
    result = await client.call_with_retry("payment-service", max_retries=2)
    print(f"    结果: {result}")


async def main():
    """主函数"""
    await demo_basic_discovery()
    await demo_service_failover()
    await demo_retry_mechanism()

    print("\n" + "=" * 60)
    print("服务发现演示完成！")
    print("=" * 60)
    print("\n关键点:")
    print("  1. 服务注册：启动时向 Consul 注册")
    print("  2. 健康检查：定期检查服务健康状态")
    print("  3. 负载均衡：随机选择一个健康实例")
    print("  4. 故障转移：自动排除不健康实例")
    print("  5. 重试机制：失败时自动重试")


if __name__ == "__main__":
    asyncio.run(main())
