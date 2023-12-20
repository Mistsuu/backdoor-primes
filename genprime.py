from sage.all import getrandbits, is_prime, randrange, ZZ, random_prime

def gen_prime_with_backdoor(D, pbits):
    Dbits = int(D).bit_length()
    Vbits = (pbits + 2 - Dbits) // 2
    for _ in range(pbits * 3): # Limit since sometimes we can run forever :v
        V = getrandbits(Vbits) | 0x1
        t = V**2 * D + 1
        if t % 4 == 0 and is_prime(t // 4):
            return t // 4
    
def get_nonsquare(upper_limit = 10**4):
    while True:
        D = randrange(3, upper_limit)
        if not ZZ(D).is_square():
            return D
        
def gen_backdoor_params(upper_D = 10**4):
    while True:
        D = get_nonsquare(upper_D)
        p = gen_prime_with_backdoor(D, 1024)
        if p != None:
            break
            
    q = random_prime(2**1024)
    n = p*q

    return D, p, q, n
