from sage.all import Zmod, randrange, gcd, ZZ, pari, PolynomialRing
from curvexz  import mul_x1_with_bar
from genprime import gen_backdoor_params
from hilbert  import hilbert_classpoly_coefs

import time
import re

def attack(n, D):
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
        print('[i] Multiplying point...')
        start = time.time()        
        X, Z = mul_x1_with_bar(x, _1, n, A, B, H_D)
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
    # D, p, q, n = gen_backdoor_params(upper_D=20_000)
    D = 12963
    p = 7283792041131875884449632282560514764722828469630329188813462890152105245685629147248455541883453738590382081354339129409725231808748184304988105465498947621964992319761872846969077412459341606361558695496543740024072687144948999180864332290034483176825976653117868741379337168326644516054854087602726837
    q = 77789478336742296558106407819056053203451973672855044922293138530718799385104317987843330150382675996463972300357671977500217903465636571331578685644572255549040867926943026867493696825137871511981751702236206924863457901149449725442529276459412115247279293943318856410114846556321324945094582789481101890299
    n = 566602383192964013794530548046072242748551368835918296031577431844876498511346856636212421912865148616080760016343450473032427908042934035080509139286471487312929115714068583636348779352776579605399608189457503880120844293631160705981683030948213946645095191901651946549941072241884538816383729002567217937039576699394360365968521050737702863808898790422072961987683832728986832541779125480551824359720657150656257841463329151858796869730799997244774516200594852123169063807335857727149161534550168844308887987159073188463559212354390115495163402406762627836106246539507823761836758704357548768907215627637254263

    print(f'[i] Testing with case: ')
    print(f'{D = }')
    print(f'{p = }')
    print(f'{q = }')
    print(f'{n = }')

    print(f'[i] Try recover: ')
    recovered_p = attack(n, D)
    print(f'{recovered_p = }')