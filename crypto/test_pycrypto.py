# encoding: utf-8
"""
-------------------------------------------------
Description:    test_pycrypto
date:       2021/9/9 15:11
author:     lixueji
-------------------------------------------------
"""
# 实例2： 使用AES算法加密，解密一段数据
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

# 加密与解密所使用的密钥，长度必须是16的倍数
secret_key = "SecretKey_LBESec"
print(len(secret_key))
# 要加密的明文数据，长度必须是16的倍数
plain_data = "Hello,World123!"
# IV参数，长度必须是16的倍数 CBC模式
iv_param = 'This is an IV456'


# 补齐
def pad(text: str):
    while len(text) % 16 != 0:
        text += ' '
    return text


# 数据加密
def encrypt(plaintext):
    aes1 = AES.new(secret_key, AES.MODE_ECB)
    cipher_data = aes1.encrypt(pad(plaintext).encode('utf8'))
    cipher_text = b2a_hex(cipher_data)
    cipher_text = str(cipher_text)[2:-1]
    print('cipher_text：', type(cipher_text))
    print('cipher_text：', cipher_text)
    return cipher_text

# cipher_text = '354338bdbea4d7f5452b50d56723250f'


# 数据解密
def decrypt(cipher_text):
    aes2 = AES.new(secret_key, AES.MODE_ECB, 'This is an IV456')
    plain_data2 = aes2.decrypt(a2b_hex(cipher_text))  # 解密后的明文数据
    plaintext = plain_data2.decode('utf8')
    print('plain text：', plaintext)
    return plaintext


text = encrypt(" 1")
plain = decrypt(text)





