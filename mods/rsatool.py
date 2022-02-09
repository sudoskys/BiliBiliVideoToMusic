# _*_ coding: utf-8 _*_
"""
__project__ = 'BiliBiliVideoToMusic'
__file_name__ = 'rsa'
__author__ = 'sudoskys'
__time__ = '2022/2/9 下午12:23'
__product_name__ = 'PyCharm'
__version__ = '2月091223'
# code is far away from bugs with the god，author here https://github.com/sudoskys
    ____  _
   / __ \(_)___ _____  ____ _
  / / / / / __ `/ __ \/ __ `/
 / /_/ / / /_/ / / / / /_/ /
/_____/_/\__,_/_/ /_/\__,_/
"""
import base64
import rsa
from rsa import common

class RsaUtil(object):
    # 初始化key
    def __init__(self, mode="File", **alice):
        """选择密钥传入方式
            :param mode  模式
            :param alice 参数表
        """
        self.mode = mode
        if mode == 'STR':
            if alice.get('pub'):
                self.company_public_key = rsa.PublicKey.load_pkcs1(alice.get('pub').encode('utf-8'))
            if alice.get('pri'):
                self.company_private_key = rsa.PrivateKey.load_pkcs1(alice.get('pri').encode('utf-8'))

        elif mode == 'FILE':
            if alice.get('pub'):
                with open(alice.get('pub'), "rb") as x:
                    key = x.read()
                    # self.company_public_key = rsa.PublicKey.load_pkcs1_openssl_pem(key)
                    self.company_public_key = rsa.PublicKey.load_pkcs1(key)
            if alice.get('pri'):
                with open(alice.get('pri'), "rb") as x:
                    key = x.read()
                    self.company_private_key = rsa.PrivateKey.load_pkcs1(key)
        else:
            raise Exception("NO MODE SELECTED?")

    def get_max_length(self, rsa_key, encrypt=True):
        """加密内容过长时 需要分段加密 换算每一段的长度.
            :param rsa_key: 钥匙.
            :param encrypt: 是否是加密.
        """
        blocksize = common.byte_size(rsa_key.n)
        reserve_size = 11  # 预留位为11
        if not encrypt:  # 解密时不需要考虑预留位
            reserve_size = 0
        maxlength = blocksize - reserve_size
        return maxlength

    # 加密 支付方公钥
    def encrypt_by_public_key(self, message):
        """使用公钥加密.
            :param message: 需要加密的内容,FILE为byte字符.
            加密之后需要对接过进行base64转码
        """
        if self.mode == 'STR':
            message = message.encode('utf-8')
        else:
            pass
        encrypt_result = b''
        max_length = self.get_max_length(self.company_public_key)
        while message:
            input = message[:max_length]
            message = message[max_length:]
            # print(self.company_public_key)
            out = rsa.encrypt(input, self.company_public_key)
            encrypt_result += out
        encrypt_result = base64.b64encode(encrypt_result)
        return encrypt_result

    def decrypt_by_private_key(self, message):
        """使用私钥解密.
            :param message: 需要加密的内容.FILE为byte字符.
            解密之后的内容直接是字符串，不需要在进行转义
        """
        if self.mode == 'STR':
            message = message.encode('utf-8')
        else:
            pass
        decrypt_result = b""

        max_length = self.get_max_length(self.company_private_key, False)
        decrypt_message = base64.b64decode(message)
        while decrypt_message:
            input = decrypt_message[:max_length]
            decrypt_message = decrypt_message[max_length:]
            out = rsa.decrypt(input, self.company_private_key)
            decrypt_result += out
        return decrypt_result.decode('utf-8')

    # 签名 商户私钥 base64转码
    def sign_by_private_key(self, data):
        """私钥签名.
            :param data: 需要签名的内容.
            使用SHA-1 方法进行签名（也可以使用MD5）
            签名之后，需要转义后输出
        """
        signature = rsa.sign(str(data), priv_key=self.company_private_key, hash='SHA-1')
        return base64.b64encode(signature)

    def verify_by_public_key(self, message, signature):
        """公钥验签.
            :param message: 验签的内容.
            :param signature: 对验签内容签名的值（签名之后，会进行b64encode转码，所以验签前也需转码）.
        """
        signature = base64.b64decode(signature)
        return rsa.verify(message, signature, self.company_public_key)
