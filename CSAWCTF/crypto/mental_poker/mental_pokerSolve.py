from math import gcd
import random
import os
from Crypto.Util.number import long_to_bytes, bytes_to_long
from tqdm import tqdm
from pwn import *

class PRNG:
	def __init__(self, seed = int(os.urandom(8).hex(), 16)):
		self.seed = int(os.urandom(8).hex(), 16)
		self.state = [self.seed]
		self.index = 64
		for i in range(63):
			self.state.append((3 * (self.state[i] ^ (self.state[i-1] >> 4)) + i+1)%64)
	
	def __str__(self):
		return f"{self.state}"
	
	def getnum(self):
		if self.index >= 64:
			for i in range(64):
				y = (self.state[i] & 0x20) + (self.state[(i+1)%64] & 0x1f)
				val = y >> 1
				val = val ^ self.state[(i+42)%64]
				if y & 1:
					val = val ^ 37
				self.state[i] = val
			self.index = 0
		seed = self.state[self.index]
		self.index += 1
		return (seed*15 + 17)%(2**6)


# IO
context.log_level = 'debug'
while True:
    try:
        io = remote('crypto.csaw.io', 5001)
        io.recvuntil(b'--> ')
        p = int(io.recvuntil(b', ', drop=True))
        q = int(io.recvline())

        # My RSA scheme
        myP = p
        myQ = q
        myPhi = (myP-1)*(myQ-1)
        myN = myP*myQ
        myE = 19051
        myD = pow(myE,-1,myPhi)

        io.recvline()
        io.sendline(str(myE))
        io.recvline()
        io.sendline(str(myD))

        io.recvuntil(b'[')
        data = io.recvuntil(b']', drop=True).split(b', ')

        phi = (p-1)*(q-1)
        N = p*q
        possibleED = set()

        for i in tqdm(range(10000)):
            e, d = -1, 0
            rng = PRNG()
            for i in range(64): 
                rng.getnum()
            while e < 2 or d < 1:
                e_array = []
                for _ in range(6):
                    e_array.append(str(rng.getnum()))
                    e = int(''.join(e_array))
                    if gcd(e, phi) == 1:
                        d = pow(e,-1,phi)
            possibleED.add((e, d))

        encCard = int(data[0])
        CORRECT_D = -1
        CORRECT_E = -1

        for e, d in possibleED:
            card = long_to_bytes(pow(pow(encCard,d,N),myD,N))
            if b' of ' in card:
                print("Found")
                print(card)
                CORRECT_D = d
                CORRECT_E = e

        if CORRECT_D < 0 or CORRECT_E < 0:
            raise ValueError("Didn't find correct private exponent")

        # io.interactive()
        break
    except:
        continue


suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
card_rank_dict = {0: "Zero", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Jack", 12: "Queen", 13: "King", 14: "Ace", 15: "Joker"}
for i in range(10):
    deck_str = set()
    send_order = []    
    for suit in suits:
        for i in range(16):
            deck_str.add(card_rank_dict[i] + " of " + suit)

    for suit in suits:
        card = card_rank_dict[0] + " of " + suit
        deck_str.remove(card)
        send_order.append(card)
    card = card_rank_dict[1] + " of " + suits[0]
    deck_str.remove(card)
    send_order.append(card)

    for suit in suits:
        card = card_rank_dict[15] + " of " + suit
        deck_str.remove(card)
        send_order.append(card)
    card = card_rank_dict[14] + " of " + suits[0]
    deck_str.remove(card)
    send_order.append(card)

    for card in deck_str:
        send_order.append(card)

    for card in send_order:
         payload = str(pow(pow(bytes_to_long(str(card).encode()),CORRECT_E,N),myE,N))
         io.sendlineafter(b'>> ', payload)

    # For debugging
    # io.interactive()

io.recvuntil("HAHAHAHA!!!!\r\n")
data = io.recvline()

print('\n\n')
print(data)
print(f'D : {CORRECT_D}')
print(f'N : {N}')

#Finally, decrypt the above with RSA
