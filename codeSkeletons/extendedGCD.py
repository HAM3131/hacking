# Python program for the extended Euclidean algorithm - Finds modular inverse and GCD
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x
 
 
if __name__ == '__main__':
    a = 22
    b = 12392
    gcd, x, y = extended_gcd(a, b)
    print('The GCD is', gcd)
    print(f'x = {x}, y = {y}')
    print(x*a % b)
    print("The the Modular Inverse is: ", b+x)