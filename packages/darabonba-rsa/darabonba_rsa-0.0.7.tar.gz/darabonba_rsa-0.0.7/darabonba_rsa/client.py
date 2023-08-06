import base64
import uuid
from time import time

from Crypto.Hash import SHA1
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5


class Client:

    @staticmethod
    def sha_sign(message: bytes, private_key: str) -> bytes:
        private_key = RSA.import_key(private_key)
        signer = PKCS1_v1_5.new(private_key)
        digest = SHA1.new(message)
        sign = signer.sign(digest)

        return sign

    @staticmethod
    def encrypt(public_key: str, data: bytes) -> bytes:
        """
        通过公钥加密数据
        :param public_key:
        :param data:
        :return:
        """
        public_key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(public_key)
        data = cipher.encrypt(data)
        return data

    @staticmethod
    def decrypt(private_key: str, data: bytes) -> bytes:
        """
        通过私钥解密数据
        :param private_key: 
        :param data:
        :return:
        """
        privateKey = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(privateKey)
        data = cipher.decrypt(data)
        return data

    @staticmethod
    def b_decode(s: bytes) -> bytes:
        return base64.b64decode(s)

    @staticmethod
    def b_encode(s: bytes) -> bytes:
        return base64.b64encode(s)

    @staticmethod
    def gen_ts() -> int:
        return round(time() * 1000)

    @staticmethod
    def uuid() -> str:
        return str(uuid.uuid1())