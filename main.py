# -*- coding: utf-8 -*-
import base64
import time
import ecdsa
import hashlib
import requests

import binascii

# Private Key PEM format: openssl ecparam -genkey -name secp256k1 -rand /dev/urandom -out priv.key
pemPrivateKey = open("priv.key", "r").read()

timestamp = str(time.time()).split('.')[0]

# Load key
signingKey = ecdsa.SigningKey.from_pem(pemPrivateKey)


# Receive X - sign for request
def gen_sign(url_path: str):
    data = (timestamp + url_path).encode('utf-8')
    sign = signingKey.sign(data, hashfunc=hashlib.sha256)
    signB64 = base64.b64encode(sign)
    return signB64


# Receive Public Key
publicKey = signingKey.get_verifying_key()
publicKeyB64 = base64.b64encode(publicKey.to_pem())

# Receive X - KeyId for request
uncompressedPublicKey = bytearray([0x04]) + (bytearray(publicKey.to_string()))
digests = hashlib.sha1()
digests.update(uncompressedPublicKey)
keyID = binascii.hexlify(digests.digest())

print("X-Time:        ", timestamp)
# print("X-Permissions: ", permissions)
# print("X-Sign:        ", signB64)
print("X-Key-Id:      ", keyID)
print("Public Key:    ", publicKeyB64)

request_url = "https://api.monobank.ua/personal/auth/registration"


def request_corp(name, description, contactPerson, phone, email, picturePath):
    print("request_corp")

    with open(picturePath, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read())

    headers = {
        "X-Time": timestamp,
        "X-Sign": gen_sign("/personal/auth/registration").decode(encoding='utf-8'),
    }

    payload = {
        "pubkey": publicKeyB64.decode(encoding='utf-8'),
        "name": name,
        "description": description,
        "contactPerson": contactPerson,
        "phone": phone,
        "email": email,
        "logo": encoded_logo.decode(encoding='utf-8'),
    }
    request = requests.request("POST", request_url, headers=headers, json=payload)
    print("Code: ", request.status_code)
    print(request.text)


def check_status():
    print("check_status")
    headers = {
        "X-Time": timestamp,
        "X-Sign": gen_sign("/personal/auth/registration/status").decode(encoding='utf-8'),
    }
    payload = {
        "pubkey": publicKeyB64.decode(encoding='utf-8'),
    }
    request = requests.request("POST", "https://api.monobank.ua/personal/auth/registration/status", headers=headers,
                               json=payload)
    print("Code: ", request.status_code)
    print(request.text)


def initialize_access():
    print("initialize_access")

    headers = {
        "X-Key-Id": keyID,
        "X-Time": timestamp,
        "X-Sign": gen_sign("/personal/auth/request").decode(encoding='utf-8'),
        # TODO use your webhook URL
        "X-Callback": "https://webhook.site/a115bae7-c789-4635-adb0-a1bf33723cc9",
    }
    request = requests.request("POST", "https://api.monobank.ua/personal/auth/request", headers=headers, )
    print("Code: ", request.status_code)
    print(request.text)


def register_webhook():
    print("register_webhook")

    headers = {
        "X-Key-Id": keyID,
        "X-Time": timestamp,
        "X-Sign": gen_sign("/personal/corp/webhook").decode(encoding='utf-8'),
        "X-Request-Id": "aDTecAywEnvNaLxV3AxHzlQ",
    }
    payload = {
        # TODO use your webhook URL
        "webHookUrl": "https://webhook.site/a115bae7-c789-4635-adb0-a1bf33723cc9",
    }
    request = requests.request("POST", "https://api.monobank.ua/personal/corp/webhook", headers=headers, json=payload)
    print("Code: ", request.status_code)
    print(request.text)


def corp_settings():
    print("corp_settings")

    headers = {
        "X-Key-Id": keyID,
        "X-Time": timestamp,
        "X-Sign": gen_sign("/personal/corp/settings").decode(encoding='utf-8'),
        "X-Request-Id": "awKANWFw6TMu126qONm2fug",
    }

    request = requests.request("GET", "https://api.monobank.ua/personal/corp/settings", headers=headers)
    print("Code: ", request.status_code)
    print("Json: ", request.json())
    print(request.text)


if __name__ == '__main__':

    request_corp(
        name="",
        description="",
        contactPerson="",
        phone="",
        email="",
        picturePath="",
    )
    # corp_settings()
    # register_webhook()
    # initialize_access()
