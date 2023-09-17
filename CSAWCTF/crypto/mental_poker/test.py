from math import gcd
import os
from Crypto.Util.number import getPrime
from tqdm import tqdm

class PRNG:
	def __init__(self, seed = int(os.urandom(8).hex(),16)):
		self.seed = int(os.urandom(8).hex(),16)
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

p = getPrime(300)
q = getPrime(300)
phi = (p-1)*(q-1)
N = p*q
possibleED = set()

for i in tqdm(range(20000000)):
    e, d = -1, 0
    rng = PRNG()
    while e < 2 or d < 1:
        e_array = []
        for _ in range(6):
            e_array.append(str(rng.getnum()))
            e = int(''.join(e_array))
            if gcd(e, phi) == 1:
                d = pow(e,-1,phi)
    possibleED.add((e, d))
    if i % 100000 == 0:
        print(f'iteration {i} - length {len(possibleED)}')