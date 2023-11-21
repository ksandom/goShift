#!/usr/bin/env python3
"""
Another basic prototype to practise python and follow some curiosity.

Usage:
 cat inputFile | ./ps.py method 'key' > outputFile

 Method
 * 'e' - Encrypt.
 * 'd' - Decrypt.

 Key can be a string. No length limit has been set, but there will be a limit somewhere. It's likely a long way past what is practical.
"""

import sys
from pyShift import *

### Get args.
# TODO Try argparse: https://stackoverflow.com/a/42929351
count = len(sys.argv)
if count < 3:
    print("Expected 2 parameters.")
    sys.exit(1)

method = sys.argv[1]
key = sys.argv[2]

### Get the pyShift class up and running.
ps = PyShift(method, key)

### Do it.
ps.doStdInOut()

