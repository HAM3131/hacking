from pwn import *

conn = remote('ftp.ubuntu.com',21)

conn.recvline()

conn.send(b'USER anonymous\r\n')

conn.recvuntil(b' ', drop=True)

conn.recvline()

conn.close()