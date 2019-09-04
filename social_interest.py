import matplotlib.pyplot as plt
import operator
x=list()
#y=[0]*336
y=list()
popularity=dict()
users=list()
userbook=dict()
#14天
#16337人
class user:
	def __init__(self):
		self.history=list()
		self.interest=[0]*16337

with open('youtube.parsed.061807.24.dat') as f:
	edge=f.read().split('\n')
	count=0
	for i in range(len(edge)):
		edge[i]=edge[i].split()
		#edge[i][0]=int(float(edge[i][0])-1201639675)
		if edge[i][2] not in userbook:
			userbook[edge[i][2]]=count
			count+=1
			user.append(user())
		users[userbook[edge[i][2]]].history.append(edge[i][4])
	for i in range(len(users)):
		for j in range(len(users)):
			a=len(users[i].history)
			b=len(users[j].history)
			similar=0
			for e in users[i].history:
				if e in users[j].history:
					similar+=1
			users[i].interest[j]=similar
	for i in range(len(users)):
		print(users[i].interest)


plt.xlabel("hour")
plt.ylabel("number of requests")
plt.plot(y,"g",)
plt.show()