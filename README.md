# Backdoor Primes

Factor composite `n=p*q`, with `p` in the form `DV^2 + 1`, where `D` is a non-square.

## Branches

- `master`: Uses only one threads, requires minimal setup.
- `ntl-upgrade`: Uses local `C` functions of `libntl`, which supports multithreading for arithmetics calculations.

## Prerequisites

- `libntl-dev`: Tested & worked with version `11.5.1-1`.
- `sagemath`: Tested & worked with version `9.5`.
  
## Run `setup`

The scripts cannot run unless you have all the files needed.

In order to get the files, you need to run:

```bash
cd setup && chmod +x ./setup.py && ./setup.py
```
