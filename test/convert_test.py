import random
import struct
from typing import Literal

# floatlist = [random.random() for _ in range(10**5)]
# buf = struct.pack('%sf' % len(floatlist), *floatlist)

# fl = struct.unpack('f', buf)
# print(fl)

def longlist2bytes(array):
    a = b''
    for i in array:
        bytes = i.to_bytes(8, byteorder="little", signed=True) 
        a += bytes
    return a

def longbytes2list(arrayb):
    list = []
    length = len(arrayb)
    i = 0
    while length > 0:
        bytes = arrayb[i : i + 8]
        long = int.from_bytes(bytes, "little", signed=True)
        length -= 8
        i += 8
        list.append(long)
    print(list)

array = [1, 20000, 300000, -1]

arrayb = longlist2bytes(array)
longbytes2list(arrayb)