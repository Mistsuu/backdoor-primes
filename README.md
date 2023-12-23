# Backdoor Primes

Factor composite `n=p*q`, with `p` in the form `DV^2 + 1`, where `D` is a non-square.

## Branches

- `master`: Uses only one threads, requires minimal setup.
- `ntl-upgrade`: Uses local `C` functions of `libntl`, which supports multithreading for arithmetics calculations.

## Prerequisites

- `sagemath`: Tested & worked with version `9.5`.
  
To run `attackverbose.py`, you also need to install `tqdm` package in `Python`.

## Run `setup`

The scripts cannot run unless you have all the files needed.

In order to get the files, you need to run:

```bash
cd setup && chmod +x ./setup.py && ./setup.py
```
