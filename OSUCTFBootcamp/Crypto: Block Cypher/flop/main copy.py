import os
from Crypto.Cipher import AES
import Crypto.Util.number as cun
import subprocess
from pwn import *

key = b'1'*16
IV = b'1'*16

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def pkcs7_unpad(ct):
    print(ct[-1])
    return ct[: -(ct[-1])]

def decrypt(ct):
    iv = ct[:16]
    ct = ct[16:]
    return AES.new(key, AES.MODE_CBC, iv).decrypt(ct)

print("Welcome to flop.")

cipher = AES.new(key, AES.MODE_CBC, IV)
padding = 0x0e
plaintext = b'ls'+p8(padding)*padding
ciphertext = cipher.encrypt(plaintext)
cmd = pkcs7_unpad(decrypt(IV+ciphertext))
print(cmd)

iv = IV
exCmd = ciphertext
padding = 0x04
newCmd = b'cat flag.txt'+p8(padding)*padding
xored = byte_xor(plaintext, iv)
xored = byte_xor(xored, newCmd)
# print(decrypt(xored+exCmd))
cmd = pkcs7_unpad(decrypt(xored+exCmd))
print(cmd)


# for i in range(64):
#     try:
#         enc_cmd = cun.long_to_bytes(int(input("ctf@flop$ "), 16))
#         cmd = pkcs7_unpad(decrypt(enc_cmd))
#         print(cmd)
#     except EOFError:
#         break
#     except ValueError:
#         print("Invalid command")
#         continue
