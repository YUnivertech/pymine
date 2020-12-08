import random, time
l = []
li = []
ls = []
for i in range(10000000):
    l.append(random.random()*100)
print('list made')

a = time.time()
for i in range(len(l)):
    ls.append(str(l[i]))
print('string coversion time(milliseconds):', (time.time()-a)*1000)

b = time.time()
for i in range(len(l)):
    li.append(int(l[i]))
print('int coversion time(milliseconds):', (time.time()-b)*1000)
