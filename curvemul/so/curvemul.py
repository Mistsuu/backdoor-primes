import os
import sys

libcurvemul_path = os.path.join(os.path.dirname(__file__), 'libcurvemul.so')
assert os.path.exists(libcurvemul_path), \
    ValueError("You need to compile libcurvemul.so first!")

import ctypes
libcurvemul = ctypes.CDLL(libcurvemul_path)

# ============================== Exposed functions ==============================
"""
void curveinit(
    const char* A_str,
    const char* B_str,
    const char* H_D_str,
    const char* n_str
);
"""
curveinit = libcurvemul._Z9curveinitPKcS0_S0_S0_
curveinit.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
]

"""
void curvemul(
    char** pXk_str, char** pZk_str, // These should not be init-ed
    char*  X0_str,  char*  k_str
);
"""
curvemul = libcurvemul._Z8curvemulPPcS0_S_S_
curvemul.argtypes = [
    ctypes.POINTER(ctypes.c_char_p),
    ctypes.POINTER(ctypes.c_char_p),
    ctypes.c_char_p,
    ctypes.c_char_p,
]

"""
void curvefree(
    char* Xk_str,
    char* Zk_str
);
"""
curvefree = libcurvemul._Z9curvefreePcS_
curvefree.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
]

# ============================== API Call ==============================
def tostr(f):
    fstr = '['
    flen = f.degree() + 1
    for i in range(flen):
        fstr += f'{f[i]}'
        if i < flen - 1:
            fstr += ' '
    return fstr + ']'

def mul_x1_ntl(X0, k, A, B, H_D): # TODO: Add thread
    # Extract n from H_D
    n = H_D.base_ring().cardinality()

    # Prepare parameters
    A_str = tostr(A).encode() + b'\0'
    B_str = tostr(B).encode() + b'\0'
    H_D_str = tostr(H_D).encode() + b'\0'
    n_str = str(n).encode() + b'\0'
    X0_str = tostr(X0).encode() + b'\0'
    k_str = str(k).encode() + b'\0'
    Xk_str = ctypes.c_char_p()
    Zk_str = ctypes.c_char_p()

    # Call!
    curveinit(
        A_str,
        B_str,
        H_D_str,
        n_str
    )

    curvemul(
        ctypes.byref(Xk_str),
        ctypes.byref(Zk_str),
        X0_str,
        k_str,
    )

    # Extract values!
    print(Xk_str.value)
    print(Zk_str.value)

    # Free memory
    curvefree(
        Xk_str,
        Zk_str
    )

if __name__ == '__main__':
    pass