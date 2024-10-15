import base64
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def md5_str(s):
    # 1、将文本（字符串类型）数据转换为二进制格式得
    s_byte = s.encode('utf-8')
    # 2、使用hashlib模块里面得MD5函数进行加密--结果是字符串类型二代
    return hashlib.md5(s_byte).hexdigest()

def res_str(data):
    # 读取公钥信息内容
    public_key_str = open('E:\\daily\\Encrypt\\rsa_public_key.pem').read()
    # 导入公钥信息，返回公钥对象
    public_key = RSA.importKey(public_key_str)
    # 基于公钥创建RSA加密器对象
    pk = PKCS1_v1_5.new(public_key)
    # 进行加密（加密前数据转换为二进制格式）
    rsa_data = pk.encrypt(data.encode('utf-8'))
    # 进行base64编码
    base64_data = base64.b64encode(rsa_data)
    # 把数据由二进制转换为文本类型的
    return base64_data.decode('utf-8')
