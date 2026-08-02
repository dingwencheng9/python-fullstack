"""示例代码：电商签名算法逆向"""
from typing import Any


def reconstruct_sign(params: dict[str, Any], secret: str) -> str:
    """重构电商接口签名。
    
    常见签名模式：
    - 字典排序后拼接 + secret + MD5/SHA256
    - JSON 序列化 + HMAC
    - 自定义拼接规则 + MD5
    """
    import hashlib
    
    # 方法 1: URL 参数排序拼接
    sorted_params = sorted((k, v) for k, v in params.items() if k != "sign")
    query = "&".join(f"{k}={v}" for k, v in sorted_params)
    sign_str = f"{query}{secret}"
    
    # 方法 2: JSON 排序
    import json
    json.dumps(params, sort_keys=True, separators=(",", ":"))
    
    return hashlib.md5(sign_str.encode()).hexdigest()


if __name__ == "__main__":
    print("电商签名逆向示例")
