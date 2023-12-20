import os

def hilbert_classpoly_coefs(D, n, verbose=False):
    """
        Using classpoly tool to create
        Hilbert Class Polynomial mod n.
    """
    # Autocorrect D to positive if found negative.
    D = abs(D)

    # Running command
    if not verbose:
        os.system(f"CLASSPOLY_PHI_FILES=\"./phi_files\" ./classpoly {D} 0 {n} 2> /dev/null")
    else:
        print('-------------------------- classpoly output --------------------------')
        os.system(f"CLASSPOLY_PHI_FILES=\"./phi_files\" ./classpoly {D} 0 {n}")
        print('----------------------------------------------------------------------')

    # Read lines from H_<D>.txt file.
    H_D_poly_filename = f'H_{D}.txt'
    if not os.path.exists(H_D_poly_filename):
        return None
    
    # Append filename to global cleanup object.
    global ___module___
    ___module___.d_filenames.append(H_D_poly_filename)

    # Read polyfile.    
    polyfile = open(H_D_poly_filename, "r")
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
        # Create a variable containing 
        # all the D files created,
        # so after this the destructor 
        # can remove it later...
        self.d_filenames = []

        if not os.path.exists('./classpoly'):
            print("[!] The modified classpoly binary provided by https://github.com/ph4r05/class-poly must be presented!")
            exit(-1)
        
        if not os.path.exists('./phi_files'):
            print("[!] The phi_files directory must exist and hold phi_j_*.txt files!")
            exit(-1)
        
        if not os.path.isdir('./phi_files'):
            print(f'[!] phi_files must be a directory!')
            exit(-1)

    def __del__(self):
        for filename in self.d_filenames:
            if os.path.exists(filename):
                os.remove(filename)

___module___ = Module()