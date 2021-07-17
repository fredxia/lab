#!/usr/bin/python

import sys
import pdb
import email.parser

fh = open(sys.argv[1], "r")
parser = email.parser.Parser()
r = parser.parse(fh)

pdb.set_trace()

print r.as_string()
