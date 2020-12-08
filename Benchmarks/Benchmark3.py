import time
from math import e
a = time.time()
for i in range(10000000):
    x = e/100
print('time taken to compute e/100(milliseconds):', (time.time()-a)*1000)
b = time.time()
for i in range(10000000):
    y = e*0.01
print('time taken to compute e*0.01(milliseconds):', (time.time()-b)*1000)
c = time.time()
for i in range(10000000):
    z = e/100.0
print('time taken to compute e/100.0(milliseconds):', (time.time()-c)*1000)
