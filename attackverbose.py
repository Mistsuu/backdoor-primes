from sage.all import Zmod, randrange, gcd, ZZ, pari, PolynomialRing
from curvexz  import mul_x1_with_bar
from genprime import gen_backdoor_params
from hilbert  import hilbert_classpoly_coefs

import time
import re

# NTL supports multithreading!
from curvemul.so.curvemul import mul_x1_ntl

def attack(n, D, n_threads = 4):
    # Change to ZZ's sage
    n = ZZ(n)
    D = ZZ(D)

    # Create ring
    Zn = Zmod(n)
    Znj = PolynomialRing(Zn, 'x', implementation="NTL")
    j = Znj.gen()    
    H_D = Znj(hilbert_classpoly_coefs(D, n, verbose=True))
    assert H_D, ValueError(f"Cannot generate the Hilbert Class Polynomial with D={D}!")

    # Create curve A, B
    R = Zn(randrange(1, n))            # R = rand * (1728-j)
    A = 3*j*R**2*(1728-j)    % H_D     # removes the need for inversion
    B = 2*j*R**3*(1728-j)**2 % H_D     # makes A&B low degree -> faster computation.

    # PARI object has built in GCD
    # function for polynomials.
    # It's fast & gives us error messages
    # during inversion fails :>
    pari_H_D = pari.Mod(H_D.change_ring(ZZ), n)

    while True:
        # Create point (x, .)
        x = Znj(randrange(1, n))

        # Multiply (x/1, .) with n
        print('[i] Multiplying point...')
        start = time.time()        
        X, Z = mul_x1_ntl(x, n, A, B, H_D, 
                          n_threads=n_threads,
                          show_progress_bar=True)
        print(f'[i] Takes {time.time() - start} seconds.')

        # It's likely that Z is equivalent to 0
        # mod p (but not mod q), hence j is the 
        # root of Z(j) mod p, but since it's also
        # root of H_D(j) mod p,

        # For low-degree H_D polynomials, we can use
        # resultant method.
        print('[i] Attempt to GCD to leak p...')
        start = time.time()
        if H_D.degree() < 2:
            kp = int(H_D.resultant(Z))
            if 1 < (p := (gcd(kp, n))) < n:
                print(f'[i] Found {p = }')
                print(f'[i] Takes {time.time() - start} seconds.')
                return p
            continue

        # But it's also so likely that
        # gcd these 2 polynomials would arrive
        # into an error, where we try to invert
        # a zero-divisor of n! Which then we
        # can read from error message to derive p.
        pari_Z = pari.Mod(Z.change_ring(ZZ), n)

        # This way it's used for high degree
        # H_D, since it's much much faster than
        # the resultant method.
        try:
            pari.gcd(pari_H_D, pari_Z)
        except Exception as err:
            try:
                kp = int(re.findall(r'\d+', str(err))[0])
                if 1 < (p := gcd(kp, n)) < n:
                    print(f'[i] Found {p = }')
                    print(f'[i] Takes {time.time() - start} seconds.')
                    return p
            except:
                pass

    
if __name__ == '__main__':
    D, p, q, n = gen_backdoor_params(upper_D=20_000_000_000)

    print(f'[i] Testing with case: ')
    print(f'{D = }')
    print(f'{p = }')
    print(f'{q = }')
    print(f'{n = }')

    print(f'[i] Try recover: ')
    recovered_p = attack(n, D)
    print(f'{recovered_p = }')