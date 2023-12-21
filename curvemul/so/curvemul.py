import os
import sys
sys.path.append(os.path.dirname(__file__))

assert os.path.exists('./libcurvemul.so'), \
    ValueError("You need to compile libcurvemul.so first!")

import ctypes
libcurvemul = ctypes.CDLL('./libcurvemul.so')

