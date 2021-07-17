#!/usr/bin/python

import socket, struct

a = "100.0.0.1"
aInt = socket.inet_aton(a)
aLong = struct.unpack("!L", aInt)[0]
aLong2 = socket.htonl(aLong)
aInt2 = struct.pack("!L", aLong2)
b = socket.inet_ntoa(aInt)
c = socket.inet_ntoa(aInt2)

print b # this is 100.0.0.1
print c # this is 1.0.0.100



