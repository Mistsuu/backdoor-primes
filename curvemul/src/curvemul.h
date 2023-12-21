#ifndef __CURVEMUL_H__
#define __CURVEMUL_H__

#include <NTL/ZZ_pX.h>
#include <NTL/ZZ.h>
#include <NTL/ZZX.h>
#include <NTL/BasicThreadPool.h>
#include <signal.h>
#include <sstream>
#include <cstring>

using namespace std;
using namespace NTL;

void curveinit(
    const char* A_str,
    const char* B_str,
    const char* H_D_str,
    const char* n_str,
    int n_threads,
    int show_progress_bar
) ;

void curvemul(
    char** pXk_str, char** pZk_str, // These should not be init-ed
    char*  X0_str,  char*  k_str
);

void curvefree(
    char* Xk_str,
    char* Zk_str
);

#endif