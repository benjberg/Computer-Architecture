#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
#grab args
if len(sys.argv) != 2:
    sys.exit(1)
# TODO load opcodes in to memory
print(sys.argv[1])
cpu.load(sys.argv[1])
cpu.run()