import numpy as np
import math
Ninact = []
Peoinact = []
tinact = []
s = []

#initialize
for i in range(10):
    Peoinact.append([])
#print(Peoinact)
for i in range(10):
    Ninact.append(int(np.random.chisquare(2)))

for i in range(10):
    tinact.append([])
    for j in range(10):
        tinact[i].append([])

#everyone's people interact distribution
for i in range(0,10):
    for j in range(Ninact[i]):
        temp = np.random.randint(0,10)
        if (temp not in Peoinact[i]) and (temp != i):
            Peoinact[i].append(temp)
#print(Peoinact)

#address multi problem
for i in range(10):
    for j in range(10):
        if (i in Peoinact[j]) and (j not in Peoinact[i]):
            Peoinact[i].append(j)
            Ninact[i]+=1
print(Ninact)
#sort
for i in range(10):
    Peoinact[i].sort()
print(Peoinact)

#message time record
for i in range(10):
    for j in range(i+1,10):
        if j in Peoinact[i]:
            a = np.random.chisquare(abs(np.random.normal(2)),100)
            for k in range(len(a)):
                if a[k]>5.:
                    tinact[i][j].append(k)
                    tinact[j][i].append(k)
#show
for i in range(10):
    for j in range(10):
        print('user '+str(i)+' user '+str(j))
        print(tinact[i][j])

#count
for i in range(10):
    count = 0
    for j in range(10):
        if len(tinact[i][j])>0:
            for k in range(len(tinact[i][j])):
                count+=math.exp(-tinact[i][j][k]/350)
    count=math.sqrt(count)
    s.append(count*Ninact[i]*Ninact[i])
print(s)