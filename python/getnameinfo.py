#!/usr/bin/python
import sys
import socket
import time

fh = open(sys.argv[1], "r")
if not fh:
    print("Cannot open file")
    exit(1)

ipStrs = {}
while True:
    line = fh.readline()
    if not line:
        break
    ipStrs[line.strip()] = None
fh.close()

print("total ip adds to look up %s" % len(ipStrs))

r = socket.getnameinfo(("54.240.8.86", 0), 8)
print("Sanity check result %s" % str(r))

clockStartTime = time.clock()
wallStartTime = time.time()
count = 0.0

for ipStr in ipStrs:
    sockAddr = (ipStr, 0)
    try:
        r = socket.getnameinfo(sockAddr, 8)
        ipStrs[ipStr] = r[0]
        count += 1
        if count % 100 == 0:
            elapseTime = time.time() - wallStartTime
            elapseClock = time.clock() - clockStartTime
            print("count %s, wall time used %s, clock used %s, "
                  "avg wall time per lookup %.6f, clock per lookup %.6f" % (
                      count, elapseTime, elapseClock, elapseTime/count,
                      elapseClock/count))
    except socket.gaierror, ex:
        print("Failed %s: %s" % (ipStr, ex))

clockEndTime = time.clock()
wallEndTime = time.time()

for ipStr in ipStrs:
    if ipStrs[ipStr] is not None:
        print("%s : %s" % (ipStr, ipStrs[ipStr]))

print("Avg time per lookup wall elapse time %.6f, clock %.6f" % (
    (wallEndTime - wallStartTime)/count,
    (clockEndTime - clockStartTime)/count))
