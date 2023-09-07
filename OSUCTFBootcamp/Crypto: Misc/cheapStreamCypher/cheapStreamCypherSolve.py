import random

# PNG file have what are sometimes known as 'magic bytes' at their header, denoting file type.
# We will test various keys until the encodedd file is properly decoded to the expected png header. 
PNGMAGICBYTES = bytes.fromhex('89504E470D0A1A0A')
# Set REALKEY to a dummy value until we find it in the loop
REALKEY = -1

for key in range(2 ** 16):
    rng = random.Random(key)

    # Open the encoded png file to read the binary and take the first 8 bytes
    f = open("OSUCTFBootcamp/Crypto: Misc/cheapStreamCypher/flag.png.enc", "rb")
    magicbytes = f.read(8)
    f.close()
    
    # Decode the header of the png file `magicbytes` with the key for this iteration
    binary = b''
    for i in range(8):
        byte = magicbytes[i]
        xor = byte ^ rng.getrandbits(8)
        binary += xor.to_bytes(1, 'big')
    # Check if the png magic bytes are decoded properly, and if so quit the loop and change the value of REALKEY
    if binary == PNGMAGICBYTES:
        REALKEY = key
        print(key)
        break

# Check if the REALKEY was found, else quit with the assertion
if not (0 <= REALKEY < 2 ** 16):
    raise ValueError("No key found")
# Decode the whole file
with open("OSUCTFBootcamp/Crypto: Misc/cheapStreamCypher/flag.png.enc", "rb") as file:
    image = file.read()
    b = bytearray(image)

rng = random.Random(REALKEY)
writeFile = open("OSUCTFBootcamp/Crypto: Misc/cheapStreamCypher/flag.png", "wb")
for byte in b:
    byte = byte ^ rng.getrandbits(8)
    writeFile.write(byte.to_bytes(1, 'big'))
