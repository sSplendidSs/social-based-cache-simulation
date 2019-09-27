import matplotlib.pyplot as plt
import operator
x=list()
#y=[0]*336
y=list()
popularity=dict()
user=list()
#14天
#16337人
#9343人
#84602個
#598人
#4513
with open('youtube.parsed.012908.S1.dat') as f:
	edge=f.read().split('\n')
	for i in range(len(edge)):
		edge[i]=edge[i].split()
		#秒
		#edge[i][0]=int(float(edge[i][0])-1201639675)
	count=0
	for e in edge:
		if e[2] not in user:
			count+=1
			user.append(e[2])
	print(count)
	'''for e in edge:
		if e[4] not in popularity:
			popularity[e[4]]=1
		else:
			popularity[e[4]]+=1
	sorted_x = sorted(popularity.items(), key=lambda kv: kv[1])
	print(sorted_x)
	for e in popularity.values():
		y.append(e)
	y.sort(reverse=True)
	print(len(y))'''
	#print(y)
	'''for i in range(len(edge)-1):
		try:
			y[int(edge[i][0]/3600)]+=1
		except:
			pass'''
plt.xlabel("hour")
plt.ylabel("number of requests")
plt.plot(y,"g",)
plt.show()