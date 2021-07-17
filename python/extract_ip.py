#!/usr/bin/python3

import sys, re

fileName = sys.argv[1]
print("extract ips from %s" % fileName)
fh = open(fileName, "r")
if not fh:
    print("Cannot open file\n")
    exit(1)
ips = set([])
while True:
    line = fh.readline()
    if not line:
        break
    m = re.findall("(\d+\.\d+\.\d+\.\d+)", line)
    for e in m:
        if len(e) < 20:
            ips.add(e)
fh.close()

for ip in ips:
    print(ip)

