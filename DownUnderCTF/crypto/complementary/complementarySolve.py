from pwn import *
import math

def int_to_bytes(integer_in: int) -> bytes:
    """Convert an integer to bytes"""
    # Calculates the least amount of bytes the integer can be fit into
    length = math.ceil((math.log(integer_in)+1)/math.log(256))

    return integer_in.to_bytes(length, 'little')


output = 6954494065942554678316751997792528753841173212407363342283423753536991947310058248515278
testFlag = 1
print(math.log(int(math.sqrt(output))))

# while True:
#     temp = int_to_bytes(testFlag)
#     m1 = int.from_bytes(temp[:len(temp)//2], 'little')
#     m2 = int.from_bytes(temp[len(temp)//2:], 'little')
#     n = m1 * m2
#     if n == output:
#         print("Flag = ", testFlag)
#         break
#     if(testFlag % 1000000 == 0):
#         print("Tested: ", testFlag)
#     testFlag += 1