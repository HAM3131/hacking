import os
from Crypto.Cipher import AES
import Crypto.Util.number as cun
from key import key
import subprocess


def pkcs7_unpad(ct):
    return ct[: -(ct[-1])]


def decrypt(ct):
    iv = ct[:16]
    ct = ct[16:]
    return AES.new(key, AES.MODE_CBC, iv).decrypt(ct)


print("Welcome to flop.")

for i in range(64):
    try:
        enc_cmd = cun.long_to_bytes(int(input("ctf@flop$ "), 16))
        cmd = pkcs7_unpad(decrypt(enc_cmd))
    except EOFError:
        break
    except ValueError:
        print("Invalid command")
        continue

    print(subprocess.check_output(["/bin/bash", "-c", cmd]).decode(), flush=True)
