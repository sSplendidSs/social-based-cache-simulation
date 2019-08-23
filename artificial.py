from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pyplot as plt
import numpy as np
import math
import os

w=50*1024*1024*8
alpha=1.2
capacity=500
interval=30
times=1
x_num=1
file_num=1000
people=143

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
		self.interaction = []
		self.model=[0]*people
		self.connect = [0]*people
		self.edge = [0]*people
		self.social_factor=0


graph=dict()
table=list()
users=list()
#init
def init():
	for i in range(people):
		users.append(user())
		table.append([])
		for j in range(people):
			users[i].interaction.append([])
			table[i].append([])

	for i in range(people):
		N_inte=np.random.randint(0,people,np.random.poisson(7))
		for e in N_inte:
			if e!=i:
				users[i].connect[e]=np.random.poisson(0.4)


def possible(source , destination):

	result=list()

	def BFS(source , destination , path):
		if len(path)>5:
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

n1=list()
n2=list()
n3=list()
n4=list()
n5=list()
t=range(interval)
x=range(x_num)
init()

for n in range(x_num):
	h1=list()
	h2=list()
	h3=list()
	h4=list()
	h5=list()
	occupation=0
	occupation3=0
	occupation4=0
	occupation5=0
	#our
	#cache_list=dict()
	cache_list=set()	
	#most popular
	cache_list2=set()
	#random
	cache_list3=set()
	#LFU
	cache_list4=set()
	real=list()
	for name in range(file_num):
		new_file=file(name)
		real.append(new_file)
	
	for u in range(times):

		for i in range(interval):

			for a in range(people):
				for b in range(people):
					if users[a].connect[b]>0:
						users[a].edge[b]=users[a].connect[b]+np.random.normal(0,0)
				book=dict()
				for b in range(people):
					if users[a].edge[b]>0:
						book[b]=users[a].edge[b]
				graph[a]=book

			for a in range(people):
				for b in range(people):
					if a!=b:
						table[a][b]=possible(a,b)
				#users[a].social_factor=sum(users[a].edge)
			
			#creat files
			files=list()
			for name in range(file_num):
				new_file=file(name)
				files.append(new_file)

			occupation2=0	
			occupation=0					

			requests=[]
			cache_list=set()
			cache_list2=set()
			#update requests
			for j in range(people):
				if np.random.rand()<np.random.poisson(0.2):
					a=np.random.zipf(alpha)
					while a>=file_num or a<=0 or a in users[j].watched:
						a=np.random.randint(100,file_num)

					requests.append(request(a,j))
					users[j].watched.add(a)

					if occupation3<capacity and (str(a) not in cache_list3):
						cache_list3.add(str(a))
						occupation3+=100

					if occupation4<capacity and (a not in cache_list4):
						cache_list4.add(a)
						occupation4+=100

					for k in range(people):
						if np.random.rand()<=users[j].connect[k]:
							users[k].wait_watch.add(str(a))

			#score
			for e in requests:
				files[e.name].count+=1
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
						files[e.name].score+=(1-donknow)
				
			'''for a,b in cache_list.items():
				cache_list[a]-=1
				if b<=0:
					cache_list.pop(a) 
					occupation-=40'''

			#determine cache
			files.sort(key=lambda x: x.score, reverse=True)
			i=0
			for e in files:
				if occupation <capacity:
					if e.file_name not in cache_list:
						cache_list.add(e.file_name)
						#cache_list[e.file_name]=0
						occupation+=100
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

			print(cache_list)
			print(cache_list2)
			print(cache_list3)
			print(cache_list4)

			requests=[]
			#wait_watch and spread
			for j in range(people):
				num=len(users[j].wait_watch)
				if num>0:
					for e in range(num):
						try:
							a = int(users[j].wait_watch.pop())
							requests.append(request(a,j))
							users[j].watched.add(a)
						except:
							break

			for e in requests:
				real[e.name].count+=1

			print(len(requests))

			#evaluate
			hit1=0
			hit2=0
			hit3=0
			hit4=0

			for e in requests:
				if e.name in cache_list:
					hit1+=1
				if e.name in cache_list2:
					hit2+=1
				if str(e.name) in cache_list3:
					hit3+=1
				if e.name in cache_list4:
					hit4+=1

			print(i)

			#print(w/(r_num-hit2)/1024/1024/8)
			'''
			w1=w
			w2=w
			w3=w
			w4=w	
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
			bitrate4=math.log((hit4*2.5*1024*1024*8 + w)/r_num)'''
			#stalling1=w1/float(w)
			#stalling2=w2/float(w)
			#stalling3=w3/float(w)
			#stalling4=w4/float(w)
			#print(stalling1)
			#print(stalling2)
			#print(stalling3)
			#print(stalling4)

			h1.append(float(hit1)/(len(requests)))
			h2.append(float(hit2)/(len(requests)))
			h3.append(float(hit3)/(len(requests)))
			h4.append(float(hit4)/(len(requests)))
			'''h1.append(bitrate1)
			h2.append(bitrate2)
			h3.append(bitrate3)
			h4.append(bitrate4)'''

			#init
			for j in range(people):
				users[j].watched=set()

			files.sort(key=lambda x: x.count, reverse=False)

			if capacity!=0 and len(cache_list3)>0:
				cache_list3.pop()
				occupation3-=100
			
			for e in files:
				if e.file_name in cache_list4:
					cache_list4.remove(e.file_name)
					occupation4-=100
					break

	'''capacity += 100
	#alpha+=0.1
	n1.append(float(sum(h1))/interval/times)
	n2.append(float(sum(h2))/interval/times)
	n3.append(float(sum(h3))/interval/times)
	n4.append(float(sum(h4))/interval/times)
	n5.append(float(sum(h5))/interval/times)'''
	#time series
	plt.plot(t,h1,"g")
	plt.plot(t,h2,"b")
	plt.plot(t,h3,"r")
	plt.plot(t,h4,"y")
	plt.xlabel("time")
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