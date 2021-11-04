import math

a = int(input())
area = 2 * math.sqrt(3) * math.pow(a, 2)
volume = (1 / 3) * (math.sqrt(2) * math.pow(a, 3))
print(round(area, 2), round(volume, 2))
