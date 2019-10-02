import numpy as np
#import tensorflow as tf
import scipy.stats as stats
import matplotlib.pyplot as plt

people=1005
alpha=0.7
file_num=2000
capacity=50
interval=50
x_n=20
times=10
bound=np.arange(1, file_num)
weights=bound**(-alpha)
weights/=weights.sum()
bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(bound, weights))
class user:
	def __init__(self):
		self.wait_watch=set()
		self.wait_buf=set()
		self.watched=dict()
		self.connect=[0]*people
		self.friends=dict()
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
n3=list()
n4=list()
for abcde in range(x_n):
	hit1=0
	hit2=0
	hit3=0
	hit4=0
	requests=0
	for wxyz in range(times):
		#init
		users=list()
		files=list()
		for i in range(people):
			users.append(user())
		for i in range(1, file_num+1):
			files.append(file(i))

		with open('email-Eu-core-temporal.txt','r') as f:
			occupation3=0
			occupation4=0
			edge=f.read().split()
			ii=0
			day=0
			CL3=dict()
			CL4=list()
			while ii+1<len(edge):
				timestamp=int((int(edge[ii+2]))/60/60/24)
				users[int(edge[ii])].connect[int(edge[ii+1])]+=1
				users[int(edge[ii])].friends[int(edge[ii+1])]=0
				ii+=3
				#evaluate&update at time slot=1 hour
				if timestamp>day:
					occupation1=0
					occupation2=0
					CL1=list()
					CL2=list()

					#determine cache
					buf=sorted(files, key=lambda x: x.score, reverse=True)
					for e in buf:
						if occupation1>capacity:
							break
						CL1.append(e.id)
						occupation1+=0.5
					buf=sorted(files, key=lambda x: x.count, reverse=True)
					for e in buf:
						if occupation2>=capacity:
							break
						CL2.append(e.id)
						occupation2+=1
					#calculate importance
					for i in range(people):
						if len(users[i].friends)>1:
							for k in users[i].friends.keys():
								users[i].friends[k]=users[i].connect[k]
							sorted_f = sorted(users[i].friends.items(), key=lambda kv: kv[1])
							ma=sorted_f[-1][1]
							mi=sorted_f[0][1]
							if ma!=mi:
								for j in range(people):
									users[i].connect[j]=(users[i].connect[j]-mi)/ma
						else:
							for k in users[i].friends.keys():
								users[i].connect[k]=0
					#pour			
					for i in range(people):
						users[i].wait_watch|=users[i].wait_buf
						users[i].wait_buf=set()

					#watch shared
					for i in range(people):
						for e in users[i].wait_watch:
							if e not in users[i].watched:
								users[i].watched[e]=7
								files[e].count+=1
								files[e].score+=sum(users[i].connect)
								if e in CL1:
									hit1+=1
								if e in CL2:
									hit2+=1
								if e in CL3:
									hit3+=1
									CL3[e]+=1
								if e in CL4:
									hit4+=1
								requests+=1

								#seen by friends
								if len(users[i].friends)>1:
									for f in users[i].friends:
										if np.random.rand()<users[i].connect[f]:
											users[f].wait_buf.add(a)					
					
					if occupation3>=capacity:
						sortedLFU = sorted(CL3.items(), key=lambda kv: kv[1])
						CL3.pop(sortedLFU[0][0])
						occupation3-=1

					if occupation4>=capacity:
						CL4.pop(np.random.randint(len(CL4)))
						occupation4-=1

					#self watch
					for i in range(people):
						if np.random.rand()<0.01:
							a=bounded_zipf.rvs()
							if a not in users[i].watched:
								users[i].watched[a]=7
								files[a].count+=1
								files[a].score+=sum(users[i].connect)
								if occupation3<capacity and a not in CL3:
									CL3[a]=0
									occupation3+=1
								if occupation4<capacity and a not in CL4:
									CL4.append(a)
									occupation4+=1
								if a in CL1:
									hit1+=1
								if a in CL2:
									hit2+=1
								if a in CL3:
									hit3+=1
									CL3[a]+=1
								if a in CL4:
									hit4+=1
								requests+=1

								#seen by friends
								if len(users[i].friends)>1:
									for f in users[i].friends:
										if np.random.rand()<users[i].connect[f]:
											users[f].wait_watch.add(a)
					#print(day)
					#print(requests)
					for m in users:
						execu=list()
						for n in m.watched:
							m.watched[n]-=1
							if m.watched[n]<=0:
								execu.append(n)
						for o in execu:
							m.watched.pop(o)

					for e in users:
						e.connect=[0]*people
						e.friends=dict()

					day+=1
					if day>interval:
						break


			print(len(CL3))
	print(hit1/requests)
	print(hit2/requests)	
	print(hit3/requests)
	print(hit4/requests)	
	n1.append(hit1/requests)
	n2.append(hit2/requests)
	n3.append(hit3/requests)
	n4.append(hit4/requests)
	#alpha+=0.1
	capacity+=10
plt.plot(range(x_n),n1,"g",)
plt.plot(range(x_n),n2,"b",)
plt.plot(range(x_n),n3,"r",)
plt.plot(range(x_n),n4,"y",)
plt.show()