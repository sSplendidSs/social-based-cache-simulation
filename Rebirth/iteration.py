import numpy as np
ThF=175
users=25
x=[0.8,1.5,4,7.5,12]
bandwidth=np.random.normal(1.25*8,0.5*8,users)
bitrate=[0]*users
for i in range(users):
	index=0
	diff=100
	for j in range(len(x)):
		if abs(bandwidth[i]-x[j])<diff:
			diff=abs(bandwidth[i]-x[j])
			index=j
	bitrate[i]=x[index]

QoS=dict()
for i in range(users):
		if bitrate[i]>bandwidth[i]:
			bitrate[i]=x[x.index(bitrate[i])-1]
print(sum(bitrate))
optimal=False
while not optimal:
	for i in range(users):
		if sum(bitrate)<ThF:
			optimal=True
			break
		else:
			print('hi')
			bitrate[i]=x[x.index(bitrate[i])-1]
