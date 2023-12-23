# Backdoor Primes

Factor composite `n=p*q`, with `p` in the form `DV^2 + 1`, where `D` is a non-square.


Based on the code of [https://github.com/cryptolu/primes-backdoor], with some modifications to ensure we can run the algorithm for `D ~ 2^32` in a reasonable amount of time and space.

## Quick Usages
```py

# You should have the script in the same
# folder as the files in this folder.
from attack import attack

"""
attack(
    <the non-square D used to generate p>,
    <composite we want to factor>
)
"""

# Example:
attack(
    7344031099,
    415878402787678439447760706119314176604738739883541911842156052231487981386787767772275067511145093302048309999662070264662971252310338819361034078270272220348571419132086188132621562742647162045568973386601882934099713057585905088722339560038386968479347776866758776241948408448941558903631566110377870674301431984512084090947673301722264257688579962682461489771712067573730097610637179632812845750704151603939735179977069369731736458775750633499966090697655909500108561903396263710554403479746866219105900552583697062519116546598145506746936638500230211243196508105597021806395415553828025810196953896324977680717
)
```

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
