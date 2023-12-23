from sage.all import Zmod, randrange, gcd, ZZ, pari, PolynomialRing
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
    D, p, q, n = gen_backdoor_params(upper_D=20_000)
    D = 14779
    p = 88478115065938598674286631301091061017901095337872504685116313724968535078645117547096282998788454032452238009437512996467238285664695328236141436236868475434419749457322095871807619360211616689854421490130185898477847736768476230869415179530766710403595532692726922631489300490732653367365646640087847630819
    q = 13761556018427461211380633872497369146597533367054856061037223521430743069962785710875151695153915885202214817811994325162806125837521145158089230537418815284190151631012249402275850560835941883934883949828110374948357843774910411046912611554497918526770445789395558775241579378705563159809643949171292042859
    n = 1217596536884784751651377238648246447404528942666732646168445363234191087876451908213202493595600684519594258870920010295352425607826220863059369322721533795939699897395082209392254820765152094879847558989125583815615612811821038309529245856638657816596368142414700633322461982825657873637511729384453105184286496421069763313274265250280481603344028432641115129116402637178018914742338418881650059095506193166910512879560773085859673409430713417787958688363373987500525546377503301261156347793318894923241775022836138058306436552741160938518213219298078897467504330175786832455722728026213076145766208134309757271521

    print(f'[i] Testing with case: ')
    print(f'{D = }')
    print(f'{p = }')
    print(f'{q = }')
    print(f'{n = }')

    print(f'[i] Try recover: ')
    recovered_p = attack(n, D)
    print(f'{recovered_p = }')