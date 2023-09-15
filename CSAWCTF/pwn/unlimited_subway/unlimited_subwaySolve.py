from pwn import *

path_to_binary = "./challenge/unlimited_subway"
EXE = ELF(path_to_binary)

def conn(use_exe = False):
	if use_exe:
		r = process([EXE.path])
	else:
		r = remote("pwn.csaw.io", 7900)
	return r

context.binary = EXE
context.log_level = "DEBUG"

conn = conn(True)

conn.recvline()

conn.send(b'USER anonymous\r\n')

conn.recvuntil(b' ', drop=True)

conn.recvline()

conn.close()