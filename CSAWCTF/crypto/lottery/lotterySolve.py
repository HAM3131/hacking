from pwn import *

def generateLists(i):
    base = [[1,2,3,4,9,10],
            [1,2,5,6,13,14],
            [1,2,7,8,11,12],
            [3,4,5,6,11,12],
            [3,4,7,8,13,14],
            [5,6,7,8,9,10],
            [9,10,11,12,13,14]]
    newVal = [[i+x for x in y] for y in base]
    return newVal

sendLists = []

for i in range(5):
    sendLists += generateLists(i*14)
print(sendLists)
print(len(sendLists))

conn = remote('crypto.csaw.io',5000)
gotten = conn.recvuntil(b'>> ', drop=True)
conn.send(b'35\n')
for x in range(35):
    for y in range(6):
        gah = conn.recvuntil(">> ")
        print(str(sendLists[x][y]))
        conn.send((str(sendLists[x][y]) + "\n").encode())
    print(x)

try:
    while True:
        gotten = conn.recvline()
        print(gotten)
except:
    print("[!] Hit end of file")



conn.close()