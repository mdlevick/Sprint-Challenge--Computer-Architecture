"""Main."""

import sys
from cpu import *

args = sys.argv

if len(args) < 2:
    print("you forgot the argument")
    sys.exit(1)

program = args[1]

cpu = CPU()

cpu.load(program)
cpu.run()