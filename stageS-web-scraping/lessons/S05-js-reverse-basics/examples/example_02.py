"""示例代码：签名算法逆向分析框架"""
from dataclasses import dataclass
from typing import Any


@dataclass
class SignResult:
    algorithm: str
    signature: str
    params: dict[str, Any]


class SignAnalyzer:
    """签名算法分析工具。"""
    
    def analyze(self, params: dict[str, str]) -> SignResult:
        """分析请求参数中的签名字段。
        
        常见签名位置：
        - sign, signature, token
        - _token, appKey, timestamp + sign
        - Authorization Bearer token
        """
        sign_field = params.get("sign") or params.get("signature") or params.get("token")
        if not sign_field:
            raise ValueError("未找到签名字段")
        
        # 常见签名算法检测
        if len(sign_field) == 32:
            algo = "MD5"
        elif len(sign_field) == 64:
            algo = "SHA256"
        else:
            algo = "Unknown"
        
        return SignResult(algorithm=algo, signature=sign_field, params=params)


if __name__ == "__main__":
    print("签名算法逆向示例")
