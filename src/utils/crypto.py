import base64
from Crypto.Cipher import AES
import time

def get_random_str():
    """生成16位随机字符串"""
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    random_str = ''
    for i in range(16):
        index = int(time.time() * 1000) % len(chars)
        random_str += chars[index]
        time.sleep(0.0001)
    return random_str

def aes_encrypt(text: str, key: str, iv: str) -> str:
    """AES加密
    Args:
        text: 要加密的文本
        key: 密钥
        iv: 初始化向量
    Returns:
        加密后的base64字符串
    """
    # 确保文本是字节类型
    if isinstance(text, str):
        text = text.encode('utf-8')
    
    # 计算需要填充的字节数
    pad_length = 16 - (len(text) % 16)
    # 使用PKCS7填充
    text = text + bytes([pad_length] * pad_length)
    
    # 创建AES加密器
    encryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    # 加密
    encrypt_text = encryptor.encrypt(text)
    # Base64编码
    encrypt_text = base64.b64encode(encrypt_text)
    
    return encrypt_text.decode('utf-8')
