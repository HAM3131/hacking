from tqdm import tqdm
p = 234146428696455141502482141719214063107
ID1 = 188553448758859508628339656160735886461
ID2 = 166919641008352110337771506945818223491

# Python program for the extended Euclidean algorithm
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x
 
 
if __name__ == '__main__':
 
    gcd, x, y = extended_gcd(ID1, p)
    # print('The GCD is', gcd)
    # print(f'x = {x}, y = {y}')
    # print("The Modular Inverse if ID1 is: ", p+x)
    ID1ModInverse = p+x
    g = (ID2 * ID1ModInverse) % p
    # print("g = ",g)
    gcd, x, y, = extended_gcd(g, p)
    # print("The Modular Inverse of g is: ", p+x)
    gModInverse = p+x
    backtrack = ID2 * gModInverse % p
    ids = [(ID1*pow(gModInverse, i, p) % p) for i in range(93)]
    # print(ids)
    print("The real answer: https://mpaste.pwn.osucyber.club/p/" + str(ids[92]))
