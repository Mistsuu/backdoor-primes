def dbl_xz(P, A, B, H_D):
    '''
    From http://hyperelliptic.org/EFD/g1p/auto-shortw-xz.html#doubling-dbl-2002-it-2
    '''
    X1, Z1 = P

    T1 = X1**2 % H_D
    T2 = Z1**2 % H_D
    T3 = A*T2 % H_D
    T4 = T1-T3
    T5 = T4**2 % H_D
    T6 = B*T2 % H_D
    T7 = X1*Z1 % H_D
    T8 = T6*T7 % H_D
    T9 = 8*T8
    X3 = T5-T9
    T10 = T1+T3
    T11 = T7*T10 % H_D
    T12 = T6*T2 % H_D
    T13 = T11+T12
    Z3 = 4*T13

    return X3, Z3

def add_xz(P1, P2, X1, A, B, H_D):
    '''
    From http://hyperelliptic.org/EFD/g1p/auto-shortw-xz.html#diffadd-mdadd-2002-it-3
    '''
    X2, Z2 = P1
    X3, Z3 = P2

    T1 = X2*X3 % H_D
    T2 = Z2*Z3 % H_D
    T3 = X2*Z3 % H_D
    T4 = Z2*X3 % H_D
    T5 = A*T2 % H_D
    T6 = T1-T5
    T7 = T6**2 % H_D
    T8 = B*T2 % H_D
    T9 = 4*T8
    T10 = T3+T4
    T11 = T9*T10 % H_D
    T12 = T7-T11
    X5 = T12
    T13 = T3-T4
    T14 = T13**2 % H_D
    Z5 = X1*T14 % H_D

    return X5, Z5

def mul_x1(x0, _1, n, A, B, H_D):
    x1, z1 = x0, _1
    x2, z2 = dbl_xz((x1, z1), A, B, H_D)
    R = [(x1, z1), (x2, z2)]

    l = n.nbits()
    for i in range(2, l+1):
        bit = (n >> (l-i)) & 1
        R[1-bit] = add_xz(R[0], R[1], x0, A, B, H_D)
        R[bit] = dbl_xz(R[bit], A, B, H_D)

    return R[0]

def mul_x1_with_bar(x0, _1, n, A, B, H_D):
    from tqdm import trange
    
    x1, z1 = x0, _1
    x2, z2 = dbl_xz((x1, z1), A, B, H_D)
    R = [(x1, z1), (x2, z2)]

    l = n.nbits()
    for i in trange(2, l+1):
        bit = (n >> (l-i)) & 1
        R[1-bit] = add_xz(R[0], R[1], x0, A, B, H_D)
        R[bit] = dbl_xz(R[bit], A, B, H_D)

    return R[0]