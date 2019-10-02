import numpy as np
#import tensorflow as tf
from scipy import stats
import matplotlib.pyplot as plt
people=1005
alpha=0.7
file_num=2000
capacity=50
interval=220
x_n=10
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
		self.active=0
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
	count=0
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
			CL1=list()
			CL2=list()
			CL3=dict()
			CL4=list(bounded_zipf.rvs(size=capacity))

			while ii+1<len(edge):
				timestamp=int((int(edge[ii+2]))/60/60/24)
				users[int(edge[ii])].connect[int(edge[ii+1])]+=1
				users[int(edge[ii])].friends[int(edge[ii+1])]=0
				users[int(edge[ii])].active+=1
				ii+=3

				#evaluate&update at time slot=1 hour
				if timestamp>day:
					occupation1=0
					occupation2=0
					
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
								users[i].watched[e]=14
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
								users[i].watched[a]=14
								files[a].count+=1
								files[a].score=1+sum(v for v in users[i].friends.values())
								requests.append(a)
								count+=1

								#seen by friends
								if len(users[i].friends)>1:
									for f in users[i].friends:
										if np.random.rand()<users[i].friends[f]*users[i].friends[f]:
											users[f].wait_watch.add(a)	

					#evaluate
					for e in requests:
						if a in CL1:
							hit1+=1
						if a in CL2:
							hit2+=1
						if a in CL3:
							hit3+=1
							CL3[a]+=1
						if a in CL4:
							hit4+=1

					#determine cache
					full=True
					execu=list()
					for k,v in CL3.items():
						if v==0:
							execu.append(k)
							full=False
					for e in execu:
						CL3.pop(e)
						occupation3-=1
					if occupation3>=capacity and full:
						sortedLFU=sorted(CL3.items(), key=lambda kv: kv[1])
						CL3.pop(sortedLFU[0][0])
						occupation3-=1

					'''if occupation4>=capacity:
						CL4.pop(np.random.randint(len(CL4)))
						occupation4-=1'''
					
					CL1=list()
					CL2=list()
					
					buf=sorted(files, key=lambda x: x.score, reverse=True)
					for e in buf:
						if occupation1>capacity or e.count==0:
							break
						CL1.append(e.id)
						occupation1+=0.5
					while occupation1<capacity:	
						o=bounded_zipf.rvs()
						while 1:
							if o not in CL1:
								CL1.append(o)
								occupation1+=0.5
								break
							o=bounded_zipf.rvs()

					buf=sorted(files, key=lambda x: x.count, reverse=True)
					for e in buf:
						if occupation2>capacity or e.count==0:
							break
						CL2.append(e.id)
						occupation2+=1
					
					while occupation2<capacity:	
						o=bounded_zipf.rvs()
						while 1:
							if o not in CL2:
								CL2.append(o)
								occupation2+=1
								break
							o=bounded_zipf.rvs()

					'''for a in requests:
							if occupation3<capacity and a not in CL3:
								CL3[a]=0
								occupation3+=1
							if occupation4<capacity and a not in CL4:
								CL4.append(a)
								occupation4+=1'''
					while occupation3<capacity:	
						o=bounded_zipf.rvs()
						while 1:
							if o not in CL3:
								CL3[o]=0
								occupation3+=1
								break
							o=bounded_zipf.rvs()

					#print(day)
					#print(len(requests))
					#print(len(CL3))

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
					#print(len(CL1))
					#print(len(CL3))
					#print(len(CL4))
					if day==67:
						day=72
					if day>interval:
						break


	print(float(hit1)/count)
	print(float(hit2)/count)
	print(float(hit3)/count)
	print(float(hit4)/count)
	n1.append(float(hit1)/count)
	n2.append(float(hit2)/count)
	n3.append(float(hit3)/count)
	n4.append(float(hit4)/count)
	#alpha+=0.1
	capacity+=10
plt.plot(range(x_n),n1,"g",)
plt.plot(range(x_n),n2,"b",)
plt.plot(range(x_n),n3,"r",)
plt.plot(range(x_n),n4,"y",)
plt.show()
