#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import string
import random
import hashlib
import time
import struct
from Crypto.Cipher import AES
import xml.etree.cElementTree as ET
import socket


class FormatException(Exception):
    pass


def throw_exception(message, exception_class=FormatException):
    raise exception_class(message)


class SHA1:
    def getSHA1(self, token, timestamp, nonce, encrypt):
        try:
            sortlist = [token, timestamp, nonce, encrypt]
            sortlist.sort()
            sha = hashlib.sha1()
            sha.update("".join(sortlist).encode('utf-8'))
            return 0, sha.hexdigest()
        except Exception as e:
            print(e)
            return -1, None


class XMLParse:
    AES_TEXT_RESPONSE_TEMPLATE = """<xml>
<Encrypt><![CDATA[%(msg_encrypt)s]]></Encrypt>
<MsgSignature><![CDATA[%(msg_signaturet)s]]></MsgSignature>
<TimeStamp>%(timestamp)s</TimeStamp>
<Nonce><![CDATA[%(nonce)s]]></Nonce>
</xml>"""

    def extract(self, xmltext):
        try:
            xml_tree = ET.fromstring(xmltext)
            encrypt = xml_tree.find("Encrypt")
            return 0, encrypt.text
        except Exception as e:
            print(e)
            return -1, None

    def generate(self, encrypt, signature, timestamp, nonce):
        resp_dict = {
            'msg_encrypt': encrypt,
            'msg_signaturet': signature,
            'timestamp': timestamp,
            'nonce': nonce,
        }
        resp_xml = self.AES_TEXT_RESPONSE_TEMPLATE % resp_dict
        return resp_xml


class PKCS7Encoder():
    block_size = 32

    def encode(self, text):
        if isinstance(text, str):
            text = text.encode('utf-8')
        text_length = len(text)
        amount_to_pad = self.block_size - (text_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        pad = bytes([amount_to_pad])
        return text + pad * amount_to_pad

    def decode(self, decrypted):
        pad = decrypted[-1]
        if pad < 1 or pad > 32:
            pad = 0
        return decrypted[:-pad]


class Prpcrypt(object):
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    def encrypt(self, text, receiveid):
        if isinstance(text, str):
            text = text.encode('utf-8')
        if isinstance(receiveid, str):
            receiveid = receiveid.encode('utf-8')
        text = self.get_random_str() + struct.pack("I", socket.htonl(len(text))) + text + receiveid
        pkcs7 = PKCS7Encoder()
        text = pkcs7.encode(text)
        cryptor = AES.new(self.key[:32].encode('utf-8') if isinstance(self.key, str) else self.key[:32], self.mode, self.key[:16].encode('utf-8') if isinstance(self.key, str) else self.key[:16])
        try:
            ciphertext = cryptor.encrypt(text)
            return 0, base64.b64encode(ciphertext).decode('utf-8')
        except Exception as e:
            print(e)
            return -1, None

    def decrypt(self, text, receiveid):
        try:
            key = self.key[:32].encode('utf-8') if isinstance(self.key, str) else self.key[:32]
            iv = self.key[:16].encode('utf-8') if isinstance(self.key, str) else self.key[:16]
            cryptor = AES.new(key, self.mode, iv)
            plain_text = cryptor.decrypt(base64.b64decode(text))
        except Exception as e:
            print(e)
            return -1, None
        try:
            pad = plain_text[-1]
            content = plain_text[16:-pad]
            xml_len = socket.ntohl(struct.unpack("I", content[:4])[0])
            xml_content = content[4:xml_len + 4]
            from_receiveid = content[xml_len + 4:]
        except Exception as e:
            print(e)
            return -1, None
        if isinstance(from_receiveid, bytes):
            from_receiveid = from_receiveid.decode('utf-8')
        if isinstance(receiveid, bytes):
            receiveid = receiveid.decode('utf-8')
        if from_receiveid != receiveid:
            return -1, None
        return 0, xml_content.decode('utf-8') if isinstance(xml_content, bytes) else xml_content

    def get_random_str(self):
        rule = string.ascii_letters + string.digits
        r = random.sample(rule, 16)
        return "".join(r).encode('utf-8')


class WXBizMsgCrypt(object):
    def __init__(self, token, encoding_aes_key, corp_id):
        self.token = token
        self.corp_id = corp_id
        self.key = base64.b64decode(encoding_aes_key + "=")
        self.pc = Prpcrypt(self.key)
        self.sha1 = SHA1()
        self.parse = XMLParse()

    def _sign(self, timestamp, nonce, encrypt, msg_signature=None):
        if msg_signature:
            return msg_signature
        sortlist = [self.token, timestamp, nonce, encrypt]
        sortlist.sort()
        sha = hashlib.sha1()
        sha.update("".join(sortlist).encode('utf-8'))
        return sha.hexdigest()

    def VerifyURL(self, msg_signature, timestamp, nonce, echostr):
        ret, signature = self.sha1.getSHA1(self.token, timestamp, nonce, echostr)
        if ret != 0:
            return ret, None
        if signature != msg_signature:
            return -1, None
        ret, encrypt = self.pc.decrypt(echostr, self.corp_id)
        return ret, encrypt

    def DecryptMsg(self, post_data, msg_signature, timestamp, nonce):
        ret, encrypt = self.parse.extract(post_data)
        if ret != 0:
            return ret, None
        signature = self._sign(timestamp, nonce, encrypt, msg_signature)
        if signature != msg_signature:
            return -1, None
        ret, xml_content = self.pc.decrypt(encrypt, self.corp_id)
        return ret, xml_content

    def EncryptMsg(self, reply_msg, nonce, timestamp=None):
        if not timestamp:
            timestamp = str(int(time.time()))
        ret, encrypt = self.pc.encrypt(reply_msg, self.corp_id)
        if ret != 0:
            return ret, None
        signature = self._sign(timestamp, nonce, encrypt)
        resp_xml = self.parse.generate(encrypt, signature, timestamp, nonce)
        return 0, resp_xml
