#include <iostream>

#include <NTL/ZZ_pX.h>
#include <NTL/ZZ.h>
#include <NTL/ZZX.h>
#include <NTL/BasicThreadPool.h>

using namespace std;
using namespace NTL;

int main(int argc, char const *argv[])
{
    SetNumThreads(4);   
    return 0;
}