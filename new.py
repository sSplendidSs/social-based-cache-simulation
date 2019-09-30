import numpy as np
#import tensorflow as tf
import scipy.stats as stats
import matplotlib.pyplot as plt

people=1005
alpha=0.56
file_num=1000
capacity=150
x_n=7
bound=np.arange(1, file_num)
weights=bound**(-alpha)
weights/=weights.sum()
bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(bound, weights))
#print(bounded_zipf.rvs(size=1000))
class user:
	def __init__(self):
		self.wait_watch=set()
		self.wait_buf=set()
		#self.watched=set()
		self.connect=[0]*people
		self.friends=dict()
		#self.active=0
class file:
	def __init__(self, file_name):
		self.id=file_name
		self.count=0
		self.score=0

#init
def init():
	for i in range(people):
		users.append(user())
	for i in range(1, file_num+1):
		files.append(file(i))

n1=list()
n2=list()
for abcdefg in range(x_n):
	users=list()
	files=list()
	init()
	with open('email-Eu-core-temporal.txt','r') as f:
		hit1=0
		hit2=0
		hit3=0
		hit4=0
		occupation1=0
		occupation2=0
		occupation3=0
		occupation4=0
		edge=f.read().split()
		ii=0
		day=0
		requests=0
		while ii+1<len(edge):
			timestamp=int((int(edge[ii+2]))/60/60/24)
			users[int(edge[ii])].connect[int(edge[ii+1])]+=1
			users[int(edge[ii])].friends[int(edge[ii+1])]=0
			ii+=3
			#evaluate&update at time slot=1 hour
			if timestamp>day:
				CL1=list()
				CL2=list()
				CL3=list()
				CL4=list()
				#determine cache
				buf=sorted(files, key=lambda x: x.score, reverse=True)
				for e in buf:
					if occupation1>capacity:
						break
					CL1.append(e.id)
					occupation1+=1
				buf=sorted(files, key=lambda x: x.count, reverse=True)
				for e in buf:
					if occupation2>capacity:
						break
					CL2.append(e.id)
					occupation2+=1
				
				#calculate importance
				for i in range(people):
					if len(users[i].friends)>1:
						for k in users[i].friends.keys():
							users[i].friends[k]=users[i].connect[k]
						sorted_f = sorted(users[i].friends.items(), key=lambda kv: kv[1])
						#print(sorted_f)
						ma=sorted_f[-1][0]
						mi=sorted_f[0][0]
						if ma!=mi:
							for j in range(people):
								users[i].connect[j]=(users[i].connect[j]-mi)/ma
					else:
						for j in range(people):
							users[i].connect[j]=0
				#pour			
				for i in range(people):
					users[i].wait_watch|=users[i].wait_buf
					users[i].wait_buf=set()

				#watch shared
				for i in range(people):
					for e in users[i].wait_watch:
						files[e].count+=1
						files[e].score+=sum(users[i].connect)
						if e in CL1:
							hit1+=1
						if e in CL2:
							hit2+=1
						if e in CL3:
							hit3+=1
						if e in CL4:
							hit4+=1
						requests+=1

						#seen by friends
						if len(users[i].friends)>1:
							for f in users[i].friends:
								if np.random.rand()<users[i].connect[f]*users[f].connect[i]:
									users[f].wait_buf.add(a)					

				#self watch
				for i in range(people):
					if np.random.rand()<0.01:
						a=bounded_zipf.rvs()
						files[a].count+=1
						files[a].score+=sum(users[i].connect)
						if a in CL1:
							hit1+=1
						if a in CL2:
							hit2+=1
						if a in CL3:
							hit3+=1
						if a in CL4:
							hit4+=1
						requests+=1
						#seen by friends
						if len(users[i].friends)>1:
							for f in users[i].friends:
								if np.random.rand()<users[i].connect[f]*users[f].connect[i]:
									users[f].wait_watch.add(a)
				print(day)
				print(requests)

				for e in users:
					e.connect=[0]*people
					e.friends=dict()
				occupation1=0
				occupation2=0
				occupation3=0
				occupation4=0
				day+=1

				if day>100:
					print(hit1/requests)
					print(hit2/requests)
					break
	n1.append(hit1/requests)
	n2.append(hit2/requests)
	alpha+=1
plt.plot(range(x_n),n1,"go",)
plt.plot(range(x_n),n2,"bo",)
plt.show()