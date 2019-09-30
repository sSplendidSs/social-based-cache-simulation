import numpy as np
#import tensorflow as tf
import scipy.stats as stats
import matplotlib.pyplot as plt

people=1005
alpha=0.56
file_num=10000
capacity=0

users=list()
files=list()
bound=np.arange(1, file_num+1)
weights=bound**(-alpha)
weights/=weights.sum()
bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(bound, weights))
#print(bounded_zipf.rvs(size=1000))
class user:
	def __init__(self):
		self.wait_watch=set()
		self.wait_buf=set()
		self.connect=[0]*people
		self.friends=set()
class file:
	def __init__(self, file_name):
		self.file_name=file_name
		self.count=0
		self.score=0

#init
def init():
	for i in range(people):
		users.append(user())
	for i in range(file_num):
		files.append(file(i))
init()

with open('email-Eu-core-temporal.txt','r') as f:
	CL1=list()
	CL2=list()
	CL3=list()
	CL4=list()
	hit1=0
	hit2=0
	hit3=0
	hit4=0
	occupation1=0
	occupation2=0
	occupation3=0
	occupation4=0
	edge=f.read().split()
	i=0
	day=0
	while i+1<len(edge):
		timestamp=int((int(edge[i+2]))/60/60/24)
		print(int(edge[i]))
		print(int(edge[i+1]))
		print(int(edge[i+2]))
		users[int(edge[i])].connect[int(edge[i+1])]+=1
		users[int(edge[i])].friends.add(int(edge[i+1]))
		i+=3
		#time slot=1 hour
		if timestamp>day:

			#determine cache
			buf=sorted(files, key=lambda x: x.score, reverse=True)
			for e in buf:
				if occupation1>capacity:
					break
				CL1.append(e)
			buf=sorted(files, key=lambda x: x.count, reverse=True)
			for e in buf:
				if occupation2>capacity:
					break
				CL2.append(e)

			#calculate importance
			for i in range(people):
				m=max(users[i].connect)
				if m>0:
					for j in range(people):
						users[i].connect[j]/=m
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

					#seen by friends
					for f in users[i].friends:
						if np.random.rand()<users[i].connect[f]:
							users[f].wait_buf.add(a)					


			#self watch
			for i in range(people):
				if np.random.rand()<0.1:
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

					#seen by friends
					for f in users[i].friends:
						if np.random.rand()<users[i].connect[f]:
							users[f].wait_watch.add(a)
			print(hit1)
			print(hit2)

			for e in users:
				e.connect=[0]*people
			day+=1
		
