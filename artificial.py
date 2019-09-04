from statsmodels.tsa.arima_model import ARIMA
#from sklearn.preprocessing import scale
from scipy import optimize as op
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import os

w=1
p=75
RTTf=10
RTTB=70
alpha=1.2
capacity=0
interval=200
times=1
x_num=20
file_num=1000
people=1005+1900
day=805
Cbuf=1
qa=0.5
qb=0.5
qc=0.5

class request:
	def __init__(self,name,source):
		self.name=name
		self.source=source
class file:
	def __init__(self, file_name):
		self.file_name = file_name
		self.count = 0
		self.score = 0
		a=np.random.normal(11.7,4)
		while a<0 or a>20:
			a=np.random.normal(11.7,4)
		self.V=a*60
class user:
	def __init__(self):
		self.wait_watch = set()
		self.wait_buf = set()
		self.online=set()
		self.Iij=[]
		self.interaction = []
		self.model=[0]*people
		self.connect = [0]*people
		self.edge = [0]*people
		self.active=0
		self.count=0
		self.social_factor=0
		self.bandwidth=np.random.normal(3,0.5)


graph=dict()
table=list()
users=list()
#init
def init():
	for i in range(people):
		users.append(user())
		table.append([])
		for j in range(people):
			users[i].Iij.append([])
			table[i].append([])
		for j in range(day):
			users[i].interaction.append([])

	with open('email-Eu-core-temporal.txt','r') as f:
		edge=f.read().split()
		i=0
		while i+1<len(edge):
			timestamp=int((int(edge[i+2]))/60/60/24)
			users[int(edge[i])].interaction[timestamp].append(int(edge[i+1]))
			users[int(edge[i])].connect[int(edge[i+1])]+=1	
			users[int(edge[i])].online.add(timestamp)
			users[int(edge[i])].count+=1
			i+=3
	
	with open('CollegeMsg.txt','r') as f:
		edge=f.read().split()
		i=0
		while i+1<len(edge):
			timestamp=int((int(edge[i+2])-1082040961)/60/60/24)
			users[int(edge[i])+1005].interaction[timestamp].append(int(edge[i+1])+1005)
			users[int(edge[i])+1005].connect[int(edge[i+1])+1005]+=1
			users[int(edge[i])+1005].online.add(timestamp)	
			users[int(edge[i])+1005].count+=1
			i+=3

	for i in range(people):
		for j in range(people):
			if users[i].connect[j]>1:
				users[i].Iij[j]=[0]*day

	for i in range(people):
		for j in range(day):
			users[i].interaction[j].sort()
			total=len(users[i].interaction[j])
			index=0
			while index<total:
				who=users[i].interaction[j][index]
				contact_num=users[i].interaction[j].count(who)
				if users[i].connect[who]>1:
					users[i].Iij[who][j]=float(contact_num)/total
				index+=contact_num
	
	for i in range(1005):
		users[i].active=float(users[i].count)/527
	for i in range(1005,1900):
		users[i].active=float(users[i].count)/180

	for i in range(people):
		m=max(users[i].connect)
		if m==0:
			continue
		for j in range(people):
			if users[i].connect[j]>1:
				users[i].edge[j]=float(users[i].connect[j])/m
		users[i].social_factor=sum(users[i].edge)

	'''for i in range(people):
		book=dict()
		for j in range(people):
			if users[i].connect[j]>1:
				book[j]=users[i].edge[j]
		graph[i]=book
	
	for a in range(people):
		for b in range(people):
			if a!=b:
				table[a][b]=possible(a,b)'''

def possible(source , destination):

	result=list()

	def BFS(source , destination , path):
		if len(path)>2:
			return
		if destination in graph[source]:
			path.append(destination)
			result.append(path)
			return 

		else:
			for e in graph[source]:
				if e not in path:
					BFS(e , destination ,path + [e])
	BFS(source , destination , [source])
	return result

'''n1=[0]*interval
n2=[0]*interval
n3=[0]*interval
n4=[0]*interval'''
n1=list()
n2=list()
n3=list()
n4=list()
t=range(interval)
x=list()
for i in range(x_num):
	x.append(1+i*0.05)
init()

for n in range(x_num):

	h1=list()
	h2=list()
	h3=list()
	h4=list()

	for u in range(times):		

		occupation3=0
		occupation4=0
		#our
		cache_list=dict()
		#most popular
		cache_list2=set()
		#random
		cache_list3=set()
		cache_list4=set()
		real=list()
		for name in range(1,file_num+1):
			new_file=file(name)
			real.append(new_file)

		while occupation4<capacity:
			a=np.random.zipf(1.1)
			while a>=file_num or a<=0:
				a=np.random.zipf(alpha)
				if a<100:
					a=-1
			if a not in cache_list4:
				cache_list4.add(a)
				occupation4+=real[a].V

		while occupation3<capacity:
			a=np.random.randint(1,file_num)
			if a not in cache_list3:
				cache_list3.add(a)
				occupation3+=real[a].V

		for i in range(interval):
			hit1=0
			hit2=0
			hit3=0
			hit4=0
			Q1=0
			Q2=0
			Q3=0
			Q4=0
			occupation=0	
			occupation2=0

			def self_watch():
				global occupation3
				global occupation4
				for j in range(people):
					if np.random.rand()<=0.1*users[j].active+0.9*(i in users[j].online):
						a=np.random.zipf(alpha)
						while a>=file_num or a<=0:
							a=np.random.zipf(alpha)
							if a<100:
								a=-1

						requests.append(request(a,j))

						for k in range(people):
							if users[j].connect[k]>1:
								if float(np.random.poisson(5))/10<=users[j].Iij[k][i]:
									users[k].wait_watch.add(a)
						if occupation4<capacity:
							if a not in cache_list4:
								cache_list4.add(a)
								occupation4+=real[a].V							
						
			def update_cache():
				global occupation
				global occupation2
				#score
				for e in requests:
					real[e.name].count+=1
					real[e.name].score+=1
					'''for i in range(people):
						if len(table[e.source][i])>0 and e.source!=i:
							p_know=list()
							for d in table[e.source][i]:
								multip=1
								for index in range(1,len(d)):
									multip*=graph[d[index-1]][d[index]]
								p_know.append(1-multip)
							donknow=1
							for d in p_know:
								donknow*=d
								print(donknow)
							real[e.name].score+=(1-donknow)'''

				#determine cache
				buf=sorted(real, key=lambda x: x.count, reverse=True)
				objective=list()
				subjective=[[]]
				B_ub=np.array([capacity])
				SP1_name=list()
				for e in buf:
					if e.count>0:
						objective.append(e.count)
						subjective[0].append(e.V)
						SP1_name.append(e.file_name)
					else:
						break
				ratio=tuple([(0.01,0.67)]*len(objective))
				res=op.linprog(-np.array(objective),np.array(subjective),B_ub,bounds=ratio)
				print(res)
				for index in range(len(objective)):
					if res['x'][index]>0.01:
						cache_list[SP1_name[index]]=res['x'][index]
				
				#buf=sorted(real, key=lambda x: x.count, reverse=True)	
				for e in buf:					
					if occupation2 <capacity:
						if e.file_name not in cache_list2:
							cache_list2.add(e.file_name)
							occupation2+=e.V
					else:
						break
				'''
				print(cache_list)
				print(len(cache_list))
				print(cache_list2)
				print(len(cache_list2))
				print(cache_list3)
				print(cache_list4)'''

			def share():
				for j in range(people):
					users[j].wait_watch=users[j].wait_watch|users[j].wait_buf
					users[j].wait_buf=set()
				#wait_watch and spread
				for j in range(people):
					num=len(users[j].wait_watch)
					if num>0:
						for e in range(num):
							try:
								a = int(users[j].wait_watch.pop())
								requests.append(request(a,j))
								for k in range(people):
									if users[j].connect[k]>1:
										if float(np.random.poisson(5))/10<=users[j].Iij[k][i]:
											users[k].wait_buf.add(a)
							except:
								break
			def evaluate_QoE():
				Q1=[0]*3
				Q2=[0]*3
				Q3=[0]*3
				Q4=[0]*3
				global QoE1
				global QoE2
				global QoE3
				global QoE4
				QoE1=0
				QoE2=0
				QoE3=0
				QoE4=0
				for e in requests:
					real[e.name].count+=1
					if e.name in cache_list:
						Q1[0]+=math.log(users[e.source].bandwidth)
						Q1[1]-=RTTf/1000
						Q1[1]-=Cbuf/users[e.source].bandwidth
						Q1[1]-=Cbuf/p
						Q1[2]+=min(1,cache_list[e.name]*(1+w/(users[e.source].bandwidth-w)))
					else:
						Q1[0]+=math.log(w)
						Q1[1]-=RTTf/1000
						Q1[1]-=RTTB/1000
						Q1[1]-=Cbuf/users[e.source].bandwidth
						Q1[1]-=Cbuf/w

					if e.name in cache_list2:
						Q2[0]+=math.log(users[e.source].bandwidth)
						Q2[1]-=RTTf/1000
						Q2[1]-=Cbuf/users[e.source].bandwidth
						Q2[1]-=Cbuf/p
						Q2[2]+=1			
					else:
						Q2[0]+=math.log(w)
						Q2[1]-=RTTf/1000
						Q2[1]-=RTTB/1000
						Q2[1]-=Cbuf/users[e.source].bandwidth
						Q2[1]-=Cbuf/w
					if e.name in cache_list3:
						Q3[0]+=math.log(users[e.source].bandwidth)
						Q3[1]-=RTTf/1000
						Q3[1]-=Cbuf/users[e.source].bandwidth
						Q3[1]-=Cbuf/p
						Q3[2]+=1					
					else:
						Q3[0]+=math.log(w)
						Q3[1]-=RTTf/1000
						Q3[1]-=RTTB/1000
						Q3[1]-=Cbuf/users[e.source].bandwidth
						Q3[1]-=Cbuf/w		
					if e.name in cache_list4:
						Q4[0]+=math.log(users[e.source].bandwidth)
						Q4[1]-=RTTf/1000
						Q4[1]-=Cbuf/users[e.source].bandwidth
						Q4[1]-=Cbuf/p
						Q4[2]+=1
					else:
						Q4[0]+=math.log(w)
						Q4[1]-=RTTf/1000
						Q4[1]-=RTTB/1000
						Q4[1]-=Cbuf/users[e.source].bandwidth
						Q4[1]-=Cbuf/w
								
				QoE1=float(Q1[0]+Q1[1]+Q1[2])/(len(requests)+1)
				QoE2=float(Q2[0]+Q2[1]+Q2[2])/(len(requests)+1)
				QoE3=float(Q3[0]+Q3[1]+Q3[2])/(len(requests)+1)
				QoE4=float(Q4[0]+Q4[1]+Q4[2])/(len(requests)+1)
			def evaluate_hit():

				global hit1
				global hit2
				global hit3
				global hit4

				for e in requests:
					real[e.name].count+=1
					if e.name in cache_list:
						hit1+=1
					if e.name in cache_list2:
						hit2+=1
					if e.name in cache_list3:
						hit3+=1
					if e.name in cache_list4:
						hit4+=1
			if i>0:
				requests=[]
				share()
				r_num=len(requests)
				print('shared',r_num)
				#evaluate_QoE()	
				evaluate_hit()
				h1.append(float(hit1)/(r_num+1))
				h2.append(float(hit2)/(r_num+1))
				h3.append(float(hit3)/(r_num+1))
				h4.append(float(hit4)/(r_num+1))
				'''h1.append(QoE1)
				h2.append(QoE2)
				h3.append(QoE3)
				h4.append(QoE4)'''
			requests=[]
			cache_list=dict()
			cache_list2=set()
			self_watch()
			update_cache()

			print('self',len(requests))
			print(i)

			buf=sorted(real,key=lambda x: x.count, reverse=False)
				
			for e in buf:
				if e.file_name in cache_list4:
					cache_list4.remove(e.file_name)
					occupation4-=real[e.file_name].V
					break

		for i in range(people):
			users[i].wait_watch=set()
			users[i].wait_buf=set()

	capacity += 10*1024
	#alpha+=0.1
	n1.append(float(sum(h1))/interval/times)
	n2.append(float(sum(h2))/interval/times)
	n3.append(float(sum(h3))/interval/times)
	n4.append(float(sum(h4))/interval/times)
	print(n1)
	#time series
	'''for i in range(interval):
			n1[i]+=h1[i]
			n2[i]+=h2[i]
			n3[i]+=h3[i]
			n4[i]+=h4[i]
for i in range(interval):
	n1[i]/=x_num
	n2[i]/=x_num
	n3[i]/=x_num
	n4[i]/=x_num'''
'''plt.plot(t,n1,"g",label='proposed')
plt.plot(t,n2,"b",label='most popular')
plt.plot(t,n3,"r",label='random')
plt.plot(t,n4,"y",label='LFU')
plt.xlabel("time slot")
#plt.ylabel("QoE")
plt.ylabel("hitrate")
plt.legend()'''
plt.plot(x,n1,"go",)
plt.plot(x,n2,"bo",)
plt.plot(x,n3,"ro",)
plt.plot(x,n4,"yo",)
plt.plot(x,n1,"g",label='proposed')
plt.plot(x,n2,"b",label='most popular')
plt.plot(x,n3,"r",label='random')
plt.plot(x,n4,"y",label='LFU')
#plt.xlabel("alpha")
plt.xlabel("cache size")
#plt.ylabel("QoE")
plt.ylabel("hit rate")
plt.legend()
plt.show()