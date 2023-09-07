import Crypto.Util.number as cun

e = 3

while True:
    p = cun.getPrime(1024)
    q = cun.getPrime(1024)
    phi = (p - 1) * (q - 1)
    d = cun.inverse(e, phi)
    if d != 1:
        break

n = p * q

flag = b"osuctf{??????????????????}"
flag = cun.bytes_to_long(flag)

ciphertext = pow(flag, e, n)
print(f"ciphertext = {ciphertext}")
print(f"n = {n}")
print(f"e = {e}")

decryption = pow(ciphertext, d, n)
assert decryption == flag
