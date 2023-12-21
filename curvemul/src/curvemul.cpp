#include "curvemul.h"
#include "ex_assert.h"
#include "progressbar.h"

using namespace std;
using namespace NTL;

/*
    curvemul.cpp:
        Mutliply points on curve in residue ring:
               Zn[j] / H_D(j)
*/
ZZ_pXMultiplier A;      // Weierstrass Curve's A
ZZ_pXMultiplier B;      // Weierstrass Curve's B
ZZ_pXModulus    H_D;    // Curve's modulus
ZZ              n;      // Modulus of Zn
ZZ_pX           _1;     // Fast cache for number 1.
bool            is_curve_init = false;
int             enable_progbar = 0;

void curveinit(
    const char* A_str,
    const char* B_str,
    const char* H_D_str,
    const char* n_str,
    int n_threads,
    int show_progress_bar
) 
{
    n = conv<ZZ>(n_str);
    ZZ_p::init(n);

    H_D = ZZ_pXModulus(conv<ZZ_pX>(H_D_str));
    A = ZZ_pXMultiplier(conv<ZZ_pX>(A_str), H_D);
    B = ZZ_pXMultiplier(conv<ZZ_pX>(B_str), H_D);
    _1 = conv<ZZ_pX>("[1]");

    SetNumThreads((long)n_threads);
    enable_progbar = show_progress_bar;
    is_curve_init = true;
}


ZZ_pX T1;
ZZ_pX T2;
ZZ_pX T3;
ZZ_pX T4;
ZZ_pX T5;
ZZ_pX T6;
ZZ_pX T7;
ZZ_pX T8;
ZZ_pX T9;
ZZ_pX T10;
ZZ_pX T11;
ZZ_pX T12;
ZZ_pX T13;
ZZ_pX T14;

void add_xz(
    ZZ_pX& X5, ZZ_pX& Z5, // P+Q
    ZZ_pX X2, ZZ_pX Z2,   // P
    ZZ_pX X3, ZZ_pX Z3,   // Q
    ZZ_pX X1              // P-Q
)
{
    // T1 = X2*X3
    MulMod(T1, X2, X3, H_D);
    // T2 = Z2*Z3
    MulMod(T2, Z2, Z3, H_D);
    // T3 = X2*Z3
    MulMod(T3, X2, Z3, H_D);
    // T4 = Z2*X3
    MulMod(T4, Z2, X3, H_D);
    // T5 = A*T2
    MulMod(T5, T2, A, H_D);
    // T6 = T1-T5
    sub(T6, T1, T5);
    // T7 = T6**2
    SqrMod(T7, T6, H_D);
    // T8 = B*T2
    MulMod(T8, T2, B, H_D);
    // T9 = 4*T8
    mul(T9, T8, 4);
    // T10 = T3+T4
    add(T10, T3, T4);
    // T11 = T9*T10
    MulMod(T11, T9, T10, H_D);
    // X5 = T7-T11
    sub(X5, T7, T11);
    // T13 = T3-T4
    sub(T13, T3, T4);
    // T14 = T13**2
    SqrMod(T14, T13, H_D);
    // Z5 = X1*T14
    MulMod(Z5, X1, T14, H_D);
}

void dbl_xz(
    ZZ_pX& X3, ZZ_pX& Z3, // 2P
    ZZ_pX X1, ZZ_pX Z1    // P
)
{
    // T1 = X1**2
    SqrMod(T1, X1, H_D);
    // T2 = Z1**2
    SqrMod(T2, Z1, H_D);
    // T3 = A*T2
    MulMod(T3, T2, A, H_D);
    // T4 = T1-T3
    sub(T4, T1, T3);
    // T5 = T4**2
    SqrMod(T5, T4, H_D);
    // T6 = B*T2
    MulMod(T6, T2, B, H_D);
    // T7 = X1*Z1
    MulMod(T7, X1, Z1, H_D);
    // T8 = T6*T7
    MulMod(T8, T6, T7, H_D);
    // T9 = 8*T8
    mul(T9, T8, 8);
    // X3 = T5-T9
    sub(X3, T5, T9);
    // T10 = T1+T3
    add(T10, T1, T3);
    // T11 = T7*T10
    MulMod(T11, T7, T10, H_D);
    // T12 = T6*T2
    MulMod(T12, T6, T2, H_D);
    // T13 = T11+T12
    add(T13, T11, T12);
    // Z3 = 4*T13
    mul(Z3, T13, 4);
}

ZZ_pX R[4];

void mul_x1(
    ZZ_pX& Xk, ZZ_pX& Zk,    // P*k
    ZZ_pX  X0, ZZ     k      // P, k
)
{

    R[0] = X0; R[1] = _1;           // R[0,1] = P
    dbl_xz(R[2], R[3], X0, _1);     // R[2,3] = 2P

    long i;
    long l;
    long b;
    l = NumBits(k);

    for (i = 2; i <= l; ++i) {
        b = bit(k, l-i);
        add_xz(
            R[2-2*b], R[3-2*b], 
            R[0], R[1], 
            R[2], R[3], 
            X0
        );
        dbl_xz(
            R[2*b], R[2*b+1],
            R[2*b], R[2*b+1]
        );
    }

    Xk = R[0]; Zk = R[1];
}

void mul_x1_with_bar(
    ZZ_pX& Xk, ZZ_pX& Zk,    // P*k
    ZZ_pX  X0, ZZ     k      // P, k
)
{

    R[0] = X0; R[1] = _1;           // R[0,1] = P
    dbl_xz(R[2], R[3], X0, _1);     // R[2,3] = 2P

    long i;
    long l;
    long b;
    l = NumBits(k);

    progressbar *bar = progressbar_new("Processing", l-2);
    for (i = 2; i <= l; ++i) {
        b = bit(k, l-i);
        add_xz(
            R[2-2*b], R[3-2*b], 
            R[0], R[1], 
            R[2], R[3], 
            X0
        );
        dbl_xz(
            R[2*b], R[2*b+1],
            R[2*b], R[2*b+1]
        );
        progressbar_inc(bar);
    }
    progressbar_finish(bar);

    Xk = R[0]; Zk = R[1];

}

void user_interrupt_handler(
    int signum
)
{
    printf("[libcurvemul] Caught SIGINT (signum = %d)! Exiting in peace...\n", signum);
    exit(-1);
}

void curvemul(
    char** pXk_str, char** pZk_str, // These should not be init-ed
    char*  X0_str,  char*  k_str
)
{
    assertf(
        is_curve_init,
        "Curve is not initialized! Please call init_curve first!"
    );

    // Register user's interrupt :)
    signal(SIGINT, user_interrupt_handler);

    // Convert X0 & k and multiply :-)
    ZZ_pX Xk, Zk, X0;
    ZZ k;

    X0 = conv<ZZ_pX>(X0_str);
    k = conv<ZZ>(k_str);

    if (enable_progbar)
        mul_x1_with_bar(Xk, Zk, X0, k);
    else
        mul_x1(Xk, Zk, X0, k);

    // Convert output back to char*
    stringstream ss;
    string tmp;

    ss.str(std::string());
    ss.clear();
    ss << Xk;
    tmp = ss.str();

    *pXk_str = (char*)malloc(tmp.length() + 1);
    strcpy(*pXk_str, tmp.c_str());

    ss.str(std::string());
    ss.clear();
    ss << Zk;
    tmp = ss.str();

    *pZk_str = (char*)malloc(tmp.length() + 1);
    strcpy(*pZk_str, tmp.c_str());
}

void curvefree(
    char* Xk_str,
    char* Zk_str
)
{
    free(Xk_str);
    free(Zk_str);
}