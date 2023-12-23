import os
import hashlib

def hash(x):
    return hashlib.sha256(x.encode()).hexdigest()[:30]

def hilbert_classpoly_coefs(D, n, verbose=False):
    """
        Using classpoly tool to create
        Hilbert Class Polynomial mod n.
    """

    def run_classpoly(H_D_poly_filepath):
        if not verbose:
            os.system(f"CLASSPOLY_PHI_FILES=\"./phi_files\" ./classpoly {D} 0 {n} 2> /dev/null")
        else:
            print('-------------------------- classpoly output --------------------------')
            os.system(f"CLASSPOLY_PHI_FILES=\"./phi_files\" ./classpoly {D} 0 {n}")
            print('----------------------------------------------------------------------')

        # If H_D file doesn't exist,
        # it means that classpoly
        # has failed to find the poly.
        if not os.path.exists(f'H_{D}.txt'):
            return False
        if verbose:
            print(f'[i] The generated polynomial is written to \"{H_D_poly_filepath}\".')
        os.rename(f'H_{D}.txt', H_D_poly_filepath)
        
        return True
    
    # Autocorrect D to positive if found negative.
    D = abs(D)

    # Hash filename to store it somewhere else.
    H_D_poly_filename = hash(f'{D}_{n}') + '.txt'
    H_D_poly_filepath = os.path.join('./hilbertout', H_D_poly_filename)
    if not os.path.exists(H_D_poly_filepath):
        if not run_classpoly(H_D_poly_filepath):
            return
    else:
        polyfile = open(H_D_poly_filepath, "r")
        _I = int(polyfile.readline().strip().split('=')[1])
        _D = int(polyfile.readline().strip().split('=')[1])
        _P = int(polyfile.readline().strip().split('=')[1])
        if _I != 0 or abs(_D) != abs(D) or abs(_P) != abs(n):
            if not run_classpoly(H_D_poly_filepath):
                return
        polyfile.close()

    # Read polyfile.    
    polyfile = open(H_D_poly_filepath, "r")
    for _ in range(3):
        polyfile.readline()  # I=... => D=... => P=... =>

    # Extract coefficients from file.
    polycoefs = []
    while True:
        line = polyfile.readline().strip()
        coef = int(line.split('*')[0])
        polycoefs.append(coef)
        if not line.endswith('+'):
            break

    return polycoefs

class Module:
    def __init__(self):
        if not os.path.exists('./classpoly'):
            print("[!] The modified \"classpoly\" binary provided by https://github.com/ph4r05/class-poly must be presented!")
            exit(-1)
        
        if not os.path.exists('./phi_files'):
            print("[!] The \"phi_files\" directory must exist and hold phi_j_*.txt files!")
            exit(-1)
        
        if not os.path.isdir('./phi_files'):
            print(f'[!] "phi_files" must be a directory!')
            exit(-1)

        for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199]:
            phi_filename = f'phi_j_{p}.txt'
            phi_filepath = os.path.join('./phi_files', phi_filename)
            if not os.path.exists(phi_filepath):
                print(f'[!] Missing phi_j file "{phi_filepath}"! Consider re-running setup file?')
                exit(-1)

        if not os.path.exists('./hilbertout'):
            os.mkdir("./hilbertout")

        if not os.path.isdir('./hilbertout'):
            print(f'[!] "hilbertout" must be a folder!')
            exit(-1)

    def __del__(self):
        pass

___module___ = Module()