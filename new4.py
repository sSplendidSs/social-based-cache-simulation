import math
import numpy as np
#import tensorflow as tf
from scipy import stats
import matplotlib.pyplot as plt
people=1005
alpha=0.9
Thb=20
file_num=1000
capacity=100
interval=431
#b=3
qa=0.25
qb=0.25
qc=0.1
qd=0.4
x_n=14
times=50

class user:
	def __init__(self):
		self.wait_watch=set()
		self.wait_buf=set()
		self.watched=dict()
		self.connect=[0]*people
		self.friends=dict()
		self.active=0
		self.downloading=False
		self.remaining=300
		self.cached=0
		self.bt_1=0
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
	QoE1=0
	QoE2=0
	QoE3=0
	QoE4=0
	count=0
	bound=np.arange(1, file_num)
	weights=bound**(-alpha)
	weights/=weights.sum()
	bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(bound, weights))
	for wxyz in range(times):
		#init
		users=list()
		files=list()
		for i in range(people):
			users.append(user())
		for i in range(1, file_num+1):
			files.append(file(i))

		with open('email-Eu-core-temporal.txt','r') as f:
			q1=list()
			q2=list()
			q3=list()
			q4=list()

			occupation3=0
			occupation4=0
			edge=f.read().split()
			ii=0
			day=0
			CL1=list()
			CL2=list()
			CL3=dict()
			CL4=list()
			#CL4=list(bounded_zipf.rvs(size=capacity))

			while ii+1<len(edge):
				timestamp=int((int(edge[ii+2]))/60/60/24)
				users[int(edge[ii])].connect[int(edge[ii+1])]+=1
				users[int(edge[ii])].friends[int(edge[ii+1])]=0
				users[int(edge[ii])].active+=1
				ii+=3

				#evaluate&update at time slot=1 hour
				if timestamp>day:
					
					#calculate importance
					for i in range(people):
						if len(users[i].friends)>1:
							m=max(users[i].connect)
							for k in users[i].friends.keys():
								users[i].friends[k]=users[i].connect[k]/m	
					
					
					requests=list()					
					#pour			
					for i in range(people):
						users[i].wait_watch|=users[i].wait_buf
						users[i].wait_buf=set()	
					#watch shared
					for i in range(people):
						if users[i].active==0:
							users[i].wait_watch=set()
							continue
						for e in users[i].wait_watch:
							if e not in users[i].watched:
								users[i].watched[e]=3
								files[e].count+=1
								files[e].score=1+sum(v for v in users[i].friends.values())
								requests.append(e)
								count+=1
								
								#seen by friends
								if len(users[i].friends)>1:
									for f in users[i].friends:
										if np.random.rand()<users[i].friends[f]*users[i].friends[f]:
											users[f].wait_buf.add(a)
					#self watch
					for i in range(people):
						if np.random.rand()<0.01:
							a=bounded_zipf.rvs()
							if a not in users[i].watched:
								users[i].watched[a]=3
								files[a].count+=1
								files[a].score=1+sum(v for v in users[i].friends.values())
								requests.append(a)
								count+=1

								#seen by friends
								if len(users[i].friends)>1:
									for f in users[i].friends:
										if np.random.rand()<users[i].friends[f]*users[i].friends[f]:
											users[f].wait_watch.add(a)	
					#print(len(requests))

					#evaluate
					for e in requests:
						bt_1=stats.rice.rvs(3)
						bt=stats.rice.rvs(3)
						b=bt_1+(bt-bt_1)/3
						#print(abs(b-bt_1))
						if e in CL1:
							hit1+=1
							QoE1+=(qa*math.log(b)-qb*abs(b-bt_1)-qc*0.25)
							ava=float(Thb)/len(requests)/2
							if ava>b:
								QoE1+=1
							else:
								QoE1+=min(1,0.5*ava/(b-ava))
						if e in CL2:
							hit2+=1
							QoE2+=(qa*math.log(b)-qb*abs(b-bt_1)-qc*0.25)
							ava=float(Thb)/len(requests)/2
							if ava>b:
								QoE2+=1
							else:
								QoE2+=min(1,0.5*ava/(b-ava))
						if e in CL3:
							hit3+=1
							CL3[e]+=1
							QoE3+=(qa*math.log(b)-qb*abs(b-bt_1)-qc*0.25)
							ava=float(Thb)/len(requests)/2
							if ava>b:
								QoE3+=1
							else:
								QoE3+=min(1,0.5*ava/(b-ava))
						if e in CL4:
							hit4+=1
							QoE4+=(qa*math.log(b)-qb*abs(b-bt_1)-qc*0.25)
							ava=float(Thb)/len(requests)/2
							if ava>b:
								QoE4+=1
							else:
								QoE4+=min(1,0.5*ava/(b-ava))

					#determine cache
					if occupation3>=capacity:
						sortedLFU=sorted(CL3.items(), key=lambda kv: kv[1])
						CL3.pop(sortedLFU[0][0])
						occupation3-=1

					if occupation4>=capacity:
						CL4.pop(np.random.randint(len(CL4)))
						occupation4-=1

					occupation1=0
					occupation2=0					
					CL1=[]
					CL2=[]
					
					buf=sorted(files, key=lambda x: x.score, reverse=True)
					for e in buf:
						if occupation1>=capacity:
							break
						CL1.append(e.id)
						occupation1+=0.5

					for e in buf:
						if occupation3>=capacity:
							break 
						if e not in CL3:
							CL3[e.id]=0
							occupation3+=1
					for e in buf:
						if occupation4>=capacity:
							break
						if e not in CL4:
							CL4.append(e.id)
							occupation4+=1		

					buf=sorted(files, key=lambda x: x.count, reverse=True)
					for e in buf:
						if occupation2>=capacity:
							break
						CL2.append(e.id)
						occupation2+=1			

					#update parameter every time slot
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
						e.active=0

					day+=1
					#print(day)
					if day==67:
						day=72
					if day>interval:
						break
					#print(len(CL4))

	print(abcde)
	n1.append(float(QoE1)/count)
	n2.append(float(QoE2)/count)
	n3.append(float(QoE3)/count)
	n4.append(float(QoE4)/count)
	Thb+=10
x=list()
for i in range(x_n):
	x.append(20+i*10)

plt.plot(x,n1,"go",)
plt.plot(x,n2,"bo",)
plt.plot(x,n3,"ro",)
plt.plot(x,n4,"yo",)
plt.plot(x,n1,"g",label='proposed')
plt.plot(x,n2,"b",label='most popular')
plt.plot(x,n3,"r",label='LFU')
plt.plot(x,n4,"y",label='random')
#plt.xlabel("alpha")
plt.xlabel("backhaul capacity (MB/s)")
plt.ylabel("QoE")
#plt.ylabel("hit rate")
plt.legend()
plt.savefig('QoE-backhaul-all.png',dpi=300)
plt.show()
