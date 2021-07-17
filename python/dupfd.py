#!/usr/bin/env python3

import os, sys

def readFile():
    print("is tty: {}".format(sys.stdin.isatty()))
    lines = sys.stdin.readlines()
    print(lines)

fh = open(sys.argv[1], "r")
os.dup2(fh.fileno(), sys.stdin.fileno())
readFile()

