from math import log

n1 = int(input())
n2 = int(input())

if n2 < 2:
    result = log(n1)
else:
    result = log(n1, n2)

print(round(result, 2))
