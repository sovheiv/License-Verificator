import hashlib
import random
import string

import rsa


def gen_pass(size=32, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def hash_key(key, salt):
    return hashlib.sha256(str.encode(key + salt)).hexdigest()


def encrypt_msg(msg: str, key_text: str):
    key_text = key_text.join(("-----BEGIN RSA PUBLIC KEY-----\n", "\n-----END RSA PUBLIC KEY-----"))
    key = rsa.PublicKey.load_pkcs1(key_text)
    return rsa.encrypt(msg.encode(), key)


def gen_rsa_keys(nbits=512):
    public_key, private_key = rsa.newkeys(nbits)

    pbkey_text = public_key.save_pkcs1().decode()
    pbkey_text = (
        pbkey_text.replace("\n", "")
        .replace("-----BEGIN RSA PUBLIC KEY-----", "")
        .replace("-----END RSA PUBLIC KEY-----", "")
    )

    prkey_text = private_key.save_pkcs1().decode()
    prkey_text = (
        prkey_text.replace("\n", "")
        .replace("-----BEGIN RSA PRIVATE KEY-----", "")
        .replace("-----END RSA PRIVATE KEY-----", "")
    )
    return pbkey_text, prkey_text
