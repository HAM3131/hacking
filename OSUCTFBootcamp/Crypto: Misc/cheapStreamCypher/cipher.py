import sys
import random

key = int(sys.argv[1])
if not (0 <= key < 2 ** 16):
    raise ValueError("Key out of bounds")

rng = random.Random(key)

for byte in sys.stdin.buffer.read():
    b = bytes([byte ^ rng.getrandbits(8)])
    sys.stdout.buffer.write(b)
