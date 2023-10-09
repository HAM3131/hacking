from pwn import *

# EXE = ELF("./onebyte")

# GET FUNCTION ADDRESS
# func_address = EXE.symbols['func']
# # GET GLOBAL OFFSET TABLE ENTRY
# lib_call_address = EXE.got['lib']

def conn(useEXE=True):
    if useEXE:
        # r = process([EXE.path])
        pass
    else:
        r = remote("chall.pwnoh.io", 13370)
    return r

# context.binary = EXE
context.log_level = "DEBUG"

io = conn(False)

# io.recvline()
surrogate_pair = "Hello 世"
io.sendline(surrogate_pair)
io.interactive()

io.close()