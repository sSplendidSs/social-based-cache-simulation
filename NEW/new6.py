import math
import numpy as np
#import tensorflow as tf
from scipy import stats
import matplotlib.pyplot as plt
people=1005
alpha=0.9
Thb=20
file_num=1000
capacity=50
interval=431
#b=3
qa=0.25
qb=0.25
qc=0.1
qd=0.4
x_n=1
times=4

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

for abcde in range(x_n):
	bt1=0
	bt2=0
	bt3=0
	ft1=0
	ft2=0
	ft3=0
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
			edge=f.read().split()
			ii=0
			day=0
			CL1=list()
			CL11=list()
			CL2=list()

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
					mp5=list()
					for e in requests:
						if stats.rice.rvs(3)<1.75:
							bt3+=2
						else:
							ft3+=1.25
							bt3+=1

						if e in CL1 or e in CL11:
							ft1+=1.5
							if e not in mp5 and np.random.rand()<=0.5:
								ft1+=1.5
								mp5.append(e)
						else:
							bt1+=1
							ft1+=1.5

						if e in CL2:
							ft2+=1
						else:
							ft2+=1.5
							bt2+=1
							

					#determine cache
					occupation1=0
					occupation11=0
					occupation2=0				
					CL1=[]
					CL2=[]
					

					buf=sorted(files, key=lambda x: x.score, reverse=True)
					for e in buf:
						if np.random.rand()<=0.5:
							if occupation1<capacity:
								CL1.append(e.id)
								occupation1+=1
							else:
								if occupation11<capacity:
									CL11.append(e.id)
									occupation11+=1
						else:
							if occupation11<capacity:
								CL11.append(e.id)
								occupation11+=1
							else:
								if occupation1<capacity:
									CL1.append(e.id)
									occupation1+=1
						if occupation1>=capacity and occupation11>=capacity:
							break

					for e in buf:
						if occupation2>capacity:
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
					if day==67:
						day=72
					if day>interval:
						break		


	print(abcde)
	'''co.append(float(bt1)/count)
	co.append(float(ft1)/count)
	noco.append(float(bt2)/count)
	noco.append(float(ft2)/count)'''
	print(float(bt1)/count,float(bt2)/count,float(bt3)/count)
	print(ft1/count,ft2/count,ft3/count)

	Thb+=10
'''x=['backhaul','fronthaul']
plt.bar(x,co,align="edge",width=-0.35)
plt.bar(x,noco,align="edge",width=0.35)
plt.ylabel("average traffic (MB/s)")
plt.legend()
plt.savefig('traffic-conoco.png',dpi=300)
plt.show()'''
