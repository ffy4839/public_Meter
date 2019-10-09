import random
import time
import pprint

# def ranges(data):
#     # data = (0.00001,1,5)
#     if isinstance(data, tuple) and len(data) == 3:
#         n = data[-1]
#         n1 = int(round(data[0], n) * 10 ** n)
#         n2 = int(round(data[1], n) * 10 ** n)
#         if n1 > n2:
#             n1, n2 = n2, n1
#         x = random.choice(range(n1, n2))
#         return round(float(x / (10 ** n)), n)
#     else:
#         return False
#
# def make_up_temperature(self, temp):
#     pass
#
# def rangess():
#     a = (0.123456,1,5)
#     xx =0
#     for i in range(100):
#         x = []
#         n = 0
#         while True:
#             for i in range(0,100):
#                 x.append(ranges(a))
#             n += 1
#             if len(list(set(x))) != 100:
#                 break
#             x = []
#         if n>xx:
#             xx=n
#     return xx
# res = {}
# for i in range(100):
#     r = str(rangess())
#     try:
#         res[r] += 1
#     except:
#         res[r] = 1
# pprint.pprint(res)


def random_parameter(n=1, r=1):
    # 流量波动 ranges = (0.00001,1,5)
    pn = 1
    if random.randint(1, 10) <= 5:
        pn = -1
    tn = 1000 ** n
    tr = r * tn
    res = pn * round(float(random.randint(1, tr) / tn), n)
    return res

for i in range(9):
    print(random_parameter(n=i,r = 1))