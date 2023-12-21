from sage.all import Zmod, randrange, gcd, ZZ, pari, ntl
from curvexz  import mul_x1
from genprime import gen_backdoor_params
from hilbert  import hilbert_classpoly_coefs

import re

def attack(n, D):
    # Change to ZZ's sage
    n = ZZ(n)
    D = ZZ(D)

    # Create ring
    Zn = Zmod(n)
    Znj = Zn['j']
    j = Znj.gen()    
    H_D = Znj(hilbert_classpoly_coefs(D, n))
    assert H_D, ValueError(f"Cannot generate the Hilbert Class Polynomial with D={D}!")

    # Create curve A, B
    R = Zn(randrange(1, n))            # R = rand * (1728-j)
    A = 3*j*R**2*(1728-j)    % H_D     # removes the need for inversion
    B = 2*j*R**3*(1728-j)**2 % H_D     # makes A&B low degree -> faster computation.

    # PARI object has built-in support
    # for GCD of polynomials in Zn[X].
    pari_H_D = pari.Mod(H_D.change_ring(ZZ), n)

    while True:
        # Create point (x, .)
        x = Znj(randrange(1, n))
        _1 = Znj(1)

        # Multiply (x/1, .) with n
        X, Z = mul_x1(x, _1, n, A, B, H_D)

        # Use resulant method 
        # for low degree H_D.
        if H_D.degree() < 2:
            kp = int(H_D.resultant(Z))
            if 1 < (p := (gcd(kp, n))) < n:
                return p
            continue
        
        # For high-degree H_D, use GCD
        # since it's faster.
        pari_Z = pari.Mod(Z.change_ring(ZZ), n)
        try:
            pari.gcd(pari_H_D, pari_Z)
        except Exception as err:
            try:
                kp = int(re.findall(r'\d+', str(err))[0])
                if 1 < (p := gcd(kp, n)) < n:
                    return p
            except:
                pass

    
if __name__ == '__main__':
    D, p, q, n = gen_backdoor_params(upper_D=2_000_000_000)

    print(f'[i] Testing with case: ')
    print(f'{D = }')
    print(f'{p = }')
    print(f'{q = }')
    print(f'{n = }')

    print(f'[i] Try recover: ')
    recovered_p = attack(n, D)
    print(f'{recovered_p = }')