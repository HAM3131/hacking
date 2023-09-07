import Crypto.Util.number as cun
import Crypto.Random.random as crr


"""
By Lagrange's Theorem, the order of any subgroup must be a divisor of the order
of the group.

Since the integers modulo p all fall within the interval [1, p - 1], the order
of the group is p - 1.

We will pick a p so that the only factors of (p - 1) are {1, 2, q, p - 1}.
By observation, we know that:
- The only element that generates a subgroup of order 1 is 1
- The only element that generates a subgroup of order 2 is p - 1
- All other elements generate a subgroup of order q or p - 1, which is 2q.

In production, we will pick q to be very large so that we don't run out of IDs.
"""


def gen_safe_prime():
    while True:
        q = cun.getRandomInteger(128)
        if not cun.isPrime(q):
            continue

        p = 2 * q + 1
        if cun.isPrime(p):
            return p


def gen_g(p):
    """
    Elements in the interval [2, p - 1) all generate large subgroups.
    Randomly pick one to be the generator element `g`.
    """
    return crr.randrange(2, p - 1)


def gen_e(p):
    """
    Randomly pick a starting exponent. Just in case ANYONE manages to find `g`.
    """
    return crr.randrange(1, p)


def gen_id(p, g, e):
    """
    Generate an ID from the parameters.
    `e` should be incremented after calling this.
    """
    return pow(g, e, p)
