from pwn import *

EXE = ELF("./onebyte")

def conn(remote=True):
	if not remote:
		r = process([EXE.path])
	else:
		r = remote("2023.ductf.dev", 30018)
	return r

context.binary = EXE
context.log_level = "DEBUG"

conn = remote('ftp.ubuntu.com',21)

conn.recvline()

conn.send(b'USER anonymous\r\n')

conn.recvuntil(b' ', drop=True)

conn.recvline()

conn.close()