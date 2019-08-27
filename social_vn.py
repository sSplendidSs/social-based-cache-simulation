from statsmodels.tsa.arima_model import ARMA
#from sklearn.preprocessing import scale
import matplotlib.pyplot as plt
import numpy as np
import math
import os

w=50*1024*1024*8
p=300*1024*1024*8
alpha=1.2
capacity=5000
times=1
x_num=1
file_num=1000
people=1900
day=527
interval=day
Cbuf=2
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
class user:
	def __init__(self):
		self.watched = set()
		self.wait_watch = set()
		self.wait_buf = set()
		self.Iij=[]
		self.interaction = []
		self.model=[0]*people
		self.connect = [0]*people
		self.edge = [0]*people
		self.active=[0]*day
		self.bandwidth=np.random.normal(2.5,0.5)


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

	with open('CollegeMsg.txt','r') as f:
		edge=f.read().split()
		i=0
		while i+1<len(edge):
			#day
			timestamp=int((int(edge[i+2]))/60/60/24)
			users[int(edge[i])].interaction[timestamp].append(int(edge[i+1]))
			users[int(edge[i])].connect[int(edge[i+1])]+=1	
			i+=3
	for i in range(people):
		for j in range(people):
			if 	users[i].connect[j]>1:
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
					users[i].Iij[who][j]=contact_num/total
				index+=contact_num
	
	for d in range(day):
		m=0
		for i in range(people):	
			if len(users[i].interaction[d])>m:
				m=len(users[i].interaction[j])
		if m==0:
			m=1
		for i in range(people):
			users[i].active[d]=len(users[i].interaction[d])/m

	'''for i in range(people):
		if users[72].connect[i]>20:
			test=list()
			for j in range(day):
				if j<7:
					test.append(0)
				else:
					try:
						model = ARMA(users[72].Iij[i][j-7:j], order=(5,0,0))
						model = model.fit(disp=0)
						out = model.forecast()[0]
						if out>1:
							out=1
						if out<0:
							out=0
						test.append(out)
					except:
						test.append(0)
			plt.plot(test,'b')
			plt.plot(users[72].Iij[i],"g")
			plt.show()'''


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

n1=[0]*interval
n2=[0]*interval
n3=[0]*interval
n4=[0]*interval
t=range(day)
x=range(x_num)
init()
def update_graph_route(day):
	for a in range(people):
		for b in range(people):
			book=dict()
			for b in range(people):
				if users[a].connect[b]>1:
					if users[a].Iij[b][day]>0:
						book[b]=users[a].Iij[b][day]
			graph[a]=book

	for a in range(people):
		for b in range(people):
			if a!=b:
				table[a][b]=possible(a,b)
for n in range(x_num):
	
	for u in range(times):
		b1=list()
		b2=list()
		b3=list()
		b4=list()
		Ti1=list()
		Ti2=list()
		Ti3=list()
		Ti4=list()

		h1=list()
		h2=list()
		h3=list()
		h4=list()		

		occupation3=0
		occupation4=0
		#our
		#cache_list=dict()
		cache_list=set()	
		#most popular
		cache_list2=set()
		#random
		cache_list3=list()
		#LFU
		cache_list4=set()
		real=list()
		for name in range(1,file_num+1):
			new_file=file(name)
			real.append(new_file)

		for i in range(day):
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
				done4=False
				for j in range(people):
					if np.random.rand()<=np.random.poisson(users[j].active[i]):
						#a=np.random.zipf(alpha)
						a=np.random.randint(1,file_num)
						'''swhile a>=file_num or a<=0:
							a=np.random.zipf(alpha)
							if a<100:
								a=-1'''
						requests.append(request(a,j))
						users[j].watched.add(a)

						if occupation4<capacity and (a not in cache_list4) and not done4:
							cache_list4.add(a)
							occupation4+=100
							done4=True

						for k in range(people):
							if users[j].connect[k]>1 and np.random.rand()<=np.random.poisson(users[j].Iij[k][i]):
								users[k].wait_watch.add(a)

				if occupation3<capacity:
					a=np.random.zipf(alpha)
					while a>=file_num or a<=0 or a in cache_list3:
						a=np.random.zipf(alpha)
					cache_list3.append(a)
					occupation3+=100

			def update_cache():
				global occupation
				global occupation2
				#score
				for e in requests:
					real[e.name].count+=1
					for i in range(people):
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
							real[e.name].score+=(1-donknow)
					
				'''for a,b in cache_list.items():
					cache_list[a]-=1
					if b<=0:
						cache_list.pop(a) 
						occupation-=40'''

				#determine cache
				buf=sorted(real, key=lambda x: x.score, reverse=True)
				i=0
				for e in buf:
					if occupation <capacity:
						if e.file_name not in cache_list:
							cache_list.add(e.file_name)
							#cache_list[e.file_name]=0
							occupation+=50
						i+=1
					else:
						break
				
				buf=sorted(real, key=lambda x: x.count, reverse=True)	
				for e in buf:					
					if occupation2 <capacity:
						if e.file_name not in cache_list2:
							cache_list2.add(e.file_name)
							occupation2 += 100
					else:
						break

				'''print(cache_list)
				print(cache_list2)
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
								i#f a not in users[j].watched:
								requests.append(request(a,j))
								users[j].watched.add(a)
								for k in range(people):
									if users[j].connect[k]>1:
										if np.random.rand()<=np.random.poisson(users[j].Iij[k][i]):
											users[k].wait_buf.add(a)
							except e:
								print(e)
								break
			
			def evaluate():

				'''w1=w
				w2=w
				w3=w
				w4=w'''
				init1=0
				init2=0
				init3=0
				init4=0
				global hit1
				global hit2
				global hit3
				global hit4
				'''global Q1
				global Q2
				global Q3
				global Q4'''

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
					'''if e.name in cache_list:
						hit1+=1
						init1+=1/10/1000
						init1+=Cbuf/users[e.source].bandwidth
						init1+=Cbuf/p
					else:
						init1+=1/10/1000
						init1+=1/70/1000
						init1+=Cbuf/users[e.source].bandwidth
						init1+=Cbuf/w

					if e.name in cache_list2:
						hit2+=1
						init2+=1/10/1000
						init2+=Cbuf/users[e.source].bandwidth
						init2+=Cbuf/p						
					else:
						init2+=1/10/1000
						init2+=1/70/1000
						init2+=Cbuf/users[e.source].bandwidth
						init2+=Cbuf/w						
					if e.name in cache_list3:
						hit3+=1
						init3+=1/10/1000
						init3+=Cbuf/users[e.source].bandwidth
						init3+=Cbuf/p						
					else:
						init3+=1/10/1000
						init3+=1/70/1000
						init3+=Cbuf/users[e.source].bandwidth
						init3+=Cbuf/w						
					if e.name in cache_list4:
						hit4+=1
						init4+=1/10/1000
						init4+=Cbuf/users[e.source].bandwidth
						init4+=Cbuf/p						
					else:
						init4+=1/10/1000
						init4+=1/70/1000
						init4+=Cbuf/users[e.source].bandwidth
						init4+=Cbuf/w	'''					

				'''print(w/(len(requests)+1-hit2)/1024/1024/8)
		
				if w/(r_num-hit1)/1024/1024/8 >2.5:
					w1=2.5
				if w/(r_num-hit2)/1024/1024/8 >2.5:
					w2=2.5
				if w/(r_num-hit3)/1024/1024/8 >2.5:
					w3=2.5
				if w/(r_num-hit4)/1024/1024/8 >2.5:
					w4=2.5

								
				bitrate1=math.log((hit1*2.5*1024*1024*8 + w)/r_num)
				bitrate2=math.log((hit2*2.5*1024*1024*8 + w)/r_num)
				bitrate3=math.log((hit3*2.5*1024*1024*8 + w)/r_num)
				bitrate4=math.log((hit4*2.5*1024*1024*8 + w)/r_num)
				Q1=qa*bitrate1-qb*init1
				Q2=qa*bitrate2-qb*init2
				Q3=qa*bitrate3-qb*init3
				Q4=qa*bitrate4-qb*init4'''
			update_graph_route(i)
			requests=[]
			share()
			r_num=len(requests)
			print('shared',r_num)
			evaluate()	
			requests=[]
			cache_list=set()
			cache_list2=set()
			self_watch()
			print('self',len(requests))
			update_cache()
			if i%1==0:
				for j in range(people):
					users[j].watched=set()
			print(i)

			h1.append(float(hit1)/(r_num+1))
			h2.append(float(hit2)/(r_num+1))
			h3.append(float(hit3)/(r_num+1))
			h4.append(float(hit4)/(r_num+1))
			'''if i>0:
				h1.append(Q1)
				h2.append(Q2)
				h3.append(Q3)
				h4.append(Q4)'''
			if i>int(capacity/100):
				if capacity!=0 and len(cache_list3)>0:
					cache_list3.pop(np.random.randint(len(cache_list3)))
					occupation3-=100

				buf=sorted(real,key=lambda x: x.count, reverse=False)
				
				for e in buf:
					if e.file_name in cache_list4:
						cache_list4.remove(e.file_name)
						occupation4-=100
						break
			for e in real:
				e.score=0

	'''capacity += 100
	#alpha+=0.1
	n1.append(float(sum(h1))/interval/times)
	n2.append(float(sum(h2))/interval/times)
	n3.append(float(sum(h3))/interval/times)
	n4.append(float(sum(h4))/interval/times)
	n5.append(float(sum(h5))/interval/times)'''
	#time series
	for i in range(interval):
		n1[i]+=h1[i]
		n2[i]+=h2[i]
		n3[i]+=h3[i]
		n4[i]+=h4[i]
for i in range(interval):
	n1[i]/=x_num
	n2[i]/=x_num
	n3[i]/=x_num
	n4[i]/=x_num
'''n1=scale(n1)
n2=scale(n2)
n3=scale(n3)
n4=scale(n4)'''
plt.plot(t,n1,"g",label='proposed')
plt.plot(t,n2,"b",label='most popular')
plt.plot(t,n3,"r",label='random')
plt.plot(t,n4,"y",label='LFU')
plt.xlabel("time slot")
#plt.ylabel("QoE")
plt.ylabel("hitrate")
plt.legend()
'''plt.plot(x,n1,"go",)
plt.plot(x,n2,"bo",)
plt.plot(x,n3,"ro",)
plt.plot(x,n4,"yo",)
plt.plot(x,n1,"g",label='proposed')
plt.plot(x,n2,"b",label='most popular')
plt.plot(x,n3,"r",label='random')
plt.plot(x,n4,"y",label='LFU')
plt.xlabel("cache size")
plt.ylabel("hit rate")
plt.legend()'''
plt.show()