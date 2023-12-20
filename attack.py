from sage.all import Zmod, randrange, gcd, ZZ, pari
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
    # Although we're supposed to divide A & B 
    # by 1728-j in Zn[j] / H_D, we can cheat 
    # by setting
    #        R = rand * (1728-j)
    #
    # Since A is mutliplied by R^2,
    #       B is multiplied by R^3,
    # 
    # We can just multiply 
    #       A with (1728-j)
    #       B with (1728-j)^2
    # 
    # This also helps reduce runtime
    # for scalar multiplication later
    # since A & B are low-degree :-)
    R = Zn(randrange(1, n))
    A = 3*j*R**2*(1728-j)    % H_D
    B = 2*j*R**3*(1728-j)**2 % H_D

    # Convert to PARI object
    # as it has built-in gcd
    # polynomials -- and it's
    # fast as well + gives us
    # error message during 
    # inversion failed :>
    pari_H_D = pari.Mod(H_D.change_ring(ZZ), n)

    while True:
        # Create point (x, .)
        x = Znj(randrange(1, n))
        _1 = Znj(1)

        # Multiply (x/1, .) with n
        X, Z = mul_x1(x, _1, n, A, B, H_D)

        # It's likely that Z is equivalent to 0
        # mod p (but not mod q), hence j is the 
        # root of Z(j) mod p, but since it's also
        # root of H_D(j) mod p,

        # For low-degree H_D polynomials, we can use
        # resultant method.
        if H_D.degree() < 2:
            kp = int(H_D.resultant(Z))
            if 1 < (p := (gcd(kp, n))) < n:
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