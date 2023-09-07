from pwn import *
from Crypto.Util.Padding import pad, unpad

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

context.log_level = 'debug'

exampleBytes = pack(0x4d7953757065725365637572655f49569c044d435f555343cffca09faf780fcd, 256, 'big', False)
exCmd = exampleBytes[16:]
iv = exampleBytes[:16]
newCmd = b'cat flag.txt'+p8(0x04)*4
padding = 0x0e
xored = byte_xor(b'ls'+p8(padding)*padding, iv)
newIV = byte_xor(newCmd, xored)
payload = (newIV + exCmd).hex()


conn = remote('flop.pwn.osucyber.club', 13396)

conn.recvuntil(b'ctf@flop$ ')
conn.send(payload.encode() + b'\n')
conn.recvline()
conn.interactive()

# conn.recvuntil(b' ', drop=True)

# conn.recvline()

conn.close()