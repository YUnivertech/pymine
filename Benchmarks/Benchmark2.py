import random, time
l1 = []
l2 = []
for i in range(10000000):
    l1.append(random.random()*100)
    l2.append(random.random()*100)
print('lists made')

c1 = 0
c2 = 0

a = time.time()
for i in range(len(l1)):
    if l1[i] == l2[i]:
        c1 = c1 + 1
print('== comparing time(milliseconds):', (time.time()-a)*1000)

b = time.time()
for i in range(len(l1)):
    if l1[i] is l2[i]:
        c2 = c2 + 1
print('is comparing time(milliseconds):', (time.time()-b)*1000)
