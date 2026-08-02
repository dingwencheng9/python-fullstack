"""示例代码：基础加密算法识别与调用"""
import base64
import hashlib
import hmac


def decode_base64(encoded: str) -> str:
    """Base64 解码。"""
    return base64.b64decode(encoded).decode("utf-8")


def compute_md5(text: str) -> str:
    """MD5 哈希。"""
    return hashlib.md5(text.encode()).hexdigest()


def compute_hmac_sha256(key: str, message: str) -> str:
    """HMAC-SHA256 签名。"""
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()


def identify_cipher(ciphertext: str) -> str:
    """识别加密类型。
    
    常见特征：
    - Base64: 长度 % 4 == 0, 字符集 A-Za-z0-9+/
    - MD5: 32 位十六进制
    - SHA256: 64 位十六进制
    - HMAC: 64 位十六进制
    """
    if len(ciphertext) == 32 and all(c in "0123456789abcdef" for c in ciphertext.lower()):
        return "MD5"
    if len(ciphertext) == 64 and all(c in "0123456789abcdef" for c in ciphertext.lower()):
        return "SHA256 or HMAC-SHA256"
    return "Unknown"


if __name__ == "__main__":
    print("基础加密识别示例")
