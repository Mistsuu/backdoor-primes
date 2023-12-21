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

void init_curve(
    const char* A_str,
    const char* B_str,
    const char* H_D_str,
    const char* n_str
);

#endif