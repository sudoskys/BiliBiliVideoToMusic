# _*_ coding: utf-8 _*_
"""
__project__ = 'BiliBiliVideoToMusic'
__file_name__ = 'tokenaes'
__author__ = 'sudoskys'
__time__ = '2022/2/9 上午11:02'
__product_name__ = 'PyCharm'
__version__ = '2月091102'
# code is far away from bugs with the god，author here https://github.com/sudoskys
    ____  _                  
   / __ \(_)___ _____  ____ _
  / / / / / __ `/ __ \/ __ `/
 / /_/ / / /_/ / / / / /_/ / 
/_____/_/\__,_/_/ /_/\__,_/                    
"""
# -*- coding: UTF-8 -*-
# reference codes: https://www.jianshu.com/p/7a4645691c68
'''
import rsa

public, private = rsa.newkeys(1024)  # 生成公钥、私钥

private = private.save_pkcs1()  # 保存为 .key 格式
a = open("private.key", "wb")
a.write(private)  # 保存私钥
print(private)
a.close()

public = public.save_pkcs1()  # 保存为 .cer 格式
a = open("public.cer", "wb")
a.write(public)  # 保存公钥
print(public)
a.close()
'''

# 使用 rsa库进行RSA签名和加解密
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


def go():
    from O365 import Account
    credentials = (input("YOUR ID:"), input("YOUR KEY:"))
    account = Account(credentials=credentials)
    if account.authenticate(scopes=['offline_access', 'files.readwrite']):
        print('Authenticated!')
        gogo(account)


def gogo(accounts):
    storage = accounts.storage()  # here we get the storage instance that handles all the storage options.
    my_drive = storage.get_default_drive()  # or get_drive('drive-id')
    root_folder = my_drive.get_root_folder()
    # 详见源码
    # attachments_folder = my_drive.get_special_folder('MUSIC')
    # paths = my_drive.get_item_by_path('/share')
    # folder = paths.get_items()
    # print(list(folder))
    # iterate over the first 25 items on the root folder
    for item in root_folder.get_items(limit=25):
        if item.is_folder:
            print(list(item.get_items(2)))  # print the first to element on this folder.
        elif item.is_file:
            if item.is_photo:
                print(item.camera_model)  # print some metadata of this photo
            elif item.is_image:
                print(item.dimensions)  # print the image dimensions
            else:
                # regular file:
                print(item.mime_type)  # print the mime type

    import rsa
    public, private = rsa.newkeys(1024)  # 生成公钥、私钥
    private = private.save_pkcs1()
    public = public.save_pkcs1()
    print(public.decode('utf-8'))
    print(private.decode('utf-8'))
    with open("public.cer", 'w+') as f:
        f.write(public.decode('utf-8'))
    with open("private.key", 'w+') as f:
        f.write(private.decode('utf-8'))

    alice_call = {
        'pub': public.decode('utf-8'),
        'pri': private.decode('utf-8'),
    }
    # base64加密token后放在这里...

    with open('o365_token.txt', 'r', encoding='utf-8') as f:
        token = f.read()
    import base64
    print(token)
    print(type(token))
    x = str(base64.b64encode(token.encode("utf-8")), "utf-8")
    data = RsaUtil(mode="STR", **alice_call)
    strs = data.encrypt_by_public_key(x)
    with open("o365_token.txt", 'w+') as f:
        f.write(strs.decode('utf-8'))

    tar = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
    shutil.move(os.getcwd() + "/o365_token.txt", tar + "/o365_token.txt")
    shutil.move(os.getcwd() + "/public.cer", tar + "/data/public.cer")
    os.remove(os.getcwd() + "/private.key")
    print('收好你的私钥：\n\n' + private.decode('utf-8'))


import os
import shutil

try:
    go()
except BaseException as arg:
    os.remove(os.getcwd() + "/private.key")
    os.remove(os.getcwd() + "/public.cer")
    os.remove(os.getcwd() + "/o365_token.txt")
    print('Failed ' + '\nException:' + str(arg))
    # mLog("err", "Fail " + n + '  -' + u).wq()

'''
import rsa
 
data='dsfasfasdfasdfasdfadfadfasfafdadfasdf'                #需要传输的数据
data_encode = data.encode("utf-8")                          #将数据进行utf8编码
 
with open("private.key", "rb") as x:
    private_key = x.read()
    private_key = rsa.PrivateKey.load_pkcs1(private_key)    # 加载私钥
with open("public.cer", "rb") as x:
    public_cer = x.read()
    public_cer = rsa.PublicKey.load_pkcs1(public_cer)       # 加载公钥
 
public_date = rsa.encrypt(data_encode, public_cer)          # 使用公钥加密
#print(public_date.encode("utf-8"))
print(public_date)               #加密后的数据
 
data = rsa.decrypt(public_date, private_key)                # 使用私钥解密
print(data)
print(data.decode('utf-8'))     #解密后的数据
 
sign = rsa.sign(data_encode, private_key, "SHA-256")        # 使用私钥进行'sha256'签名
verify = rsa.verify(data_encode, sign, public_cer)          # 使用公钥验证签名
print(verify)
'''
'''
import rsa
public, private = rsa.newkeys(1024)  # 生成公钥、私钥
private = private.save_pkcs1()  # 保存为 .key 格式
a = open("private.key", "wb")
a.write(private)  # 保存私钥
print(private)
a.close()

public = public.save_pkcs1()  # 保存为 .cer 格式
a = open("public.cer", "wb")
a.write(public)  # 保存公钥
print(public)
a.close()

'''
'''
# -*- coding:utf-8 -*-
import rsa
import base64
 
 
 
def getRSAKey(keySize=1024):
    """
    获取一对公私钥
    :param keySize: 生成密钥的长度默认1024
    :return:publicKey,privateKey
    """
    (publicKey, privateKey) = rsa.newkeys(keySize)
    print "生成一对公私钥长度为%s字节"%(keySize)
    print "公钥为：%s"%(publicKey)
    print "私钥为：%s"%(privateKey)
    return publicKey,privateKey
 
def getRSAKeyFile(filePath=".",publicKeyFileName="publicKey.pem",privateKeyFileName="privateKey.pem",keySize=1024):
    """
    获取公私钥文件
    :param filePath：文件路径
    :param publicKeyFileName: 公钥文件名称
    :param privateKeyFileName: 私钥文件名
    :param keysize: 密钥长度默认1024字节
    :return:
    """
    publicKey,privateKey = getRSAKey(keySize)
    publicKeyFile = filePath+"/"+publicKeyFileName
    privateKeyFile = filePath + "/" + privateKeyFileName
    #创建文件
    pubfile = open(publicKeyFile, 'w+')
    #save_pkcs1会将密钥进行base64进行加密
    pubfile.write(publicKey.save_pkcs1())
    pubfile.close()
    print "生成公钥文件：%s"%(publicKeyFile)
    prifile = open(privateKeyFile, 'w+')
    prifile.write(privateKey.save_pkcs1())
    prifile.close()
    print "生成私钥文件：%s" % (privateKeyFile)
    return publicKeyFile,privateKeyFile
 
def readPublicKey(file):
    """
    读取公钥文件
    :param file: 文件
    :return: publicKey
    """
    key = open(file)
    pubkey = key.read()
    publicKey = rsa.PublicKey.load_pkcs1(pubkey)
    key.close()
    print "读取公钥为：%s"%(publicKey)
    return publicKey
 
def readPrivteKey(file):
    """
    读取私钥文件
    :param file: 文件
    :return: privateKey
    """
    key =  open(file)
    prikey = key.read()
    privateKey = rsa.PrivateKey.load_pkcs1(prikey)
    key.close()
    print "读取私钥为：%s"%(privateKey)
    return  privateKey
 
def encodeByPublicKey(message="",publicKey="",isBase64="1"):
    """
    使用未加密的公钥加密数据
    :param message: 加密数据
    :param publicKey: 公钥
    :param isBase64 数据加密后转换为base64 0-是  1-否
    :return:
    """
    enMessage = rsa.encrypt(message, publicKey)
    if isBase64 == "0":
        enMessage = base64.b64encode(enMessage)
    return enMessage
 
def decodeByPrivateKey(enMessage="",privateKey="",isBase64="1"):
    """
    未加密的私钥解密数据
    :param enMessage: 解密数据
    :param privateKey:私钥
    :param isBase64 数据转换为base64解密 0-是  1-否
    :return:
    """
    if isBase64 == "0":
        enMessage = base64.b64decode(enMessage)
    message = rsa.decrypt(enMessage, privateKey)
    return message
 
def signByPrivateKey(message="",privteKey="",hash_method="SHA-1",isBase64="1"):
    """
    用私钥签名认证
    :param message: 加签的数据
    :param privteKey: 私钥
    :param hash_method 加签的方式 SHA-1，SHA-224，SHA-224，SHA-256，SHA-384，SHA-512，MD5
    :param isBase64: 加签后的数据是否base64加密 0-是 1-否
    :return:signMessage 加签数据,hash_method :加签的方式
    """
    signMessage = rsa.sign(message, privteKey, hash_method)
    if isBase64 == "0":
        signMessage = base64.b64encode(signMessage)
    return signMessage,hash_method
 
 
 
def verifyByPublicKey(message="",signMessage="",publicKey="",hash_method="SHA-1",isBase64="1"):
    """
    用公钥进行验签
    :param message: 验签参照数据
    :param signMessage: 验签的数据
    :param publicKey: 公钥
    :param hash_method: 验签的方式
    :param isBase64:  验签的数据为bae64加密数据
    :return: boolean 验签结果  method 数据加签的方式
    """
    if isBase64 == "0":
        signMessage = base64.b64decode(signMessage)
    method = rsa.verify(message, signMessage, publicKey)
    if method == hash_method:
        return True,method
    else:
        print "验签失败：加签方式为%s"%method
        return False,method
 
 
 
if __name__=="__main__":
 
    print "测试获取密钥"
    pub,pri = getRSAKey()
 
    print "测试获取密钥文件"
    getRSAKeyFile()
 
    print "测试获取公钥"
    readPublicKey("publicKey.pem")
    readPrivteKey("privateKey.pem")
 
    print "测试加解密"
    message = "1111"
    enM = encodeByPublicKey(message,pub,"0")
    print "加密后：%s"%enM
    me = decodeByPrivateKey(enM,pri,"0")
    print "解密后：%s"%me
 
 
    print "测试加签验签"
    message = "1234567890"
    signMessage,signMethod = signByPrivateKey(message,pri,isBase64="0")
    print "加签后的数据:%s"%(signMessage)
    print verifyByPublicKey(message,signMessage,pub,isBase64="0")
 
 

'''
