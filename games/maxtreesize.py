import sys
from parse import *

maxsize = 0
for line in sys.stdin[::-1]:
    line = parse("{:d} {} {:d}", line.strip())
    maxsize = max(line[2], maxsize)

print(maxsize)