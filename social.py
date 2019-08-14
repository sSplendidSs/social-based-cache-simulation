from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pyplot as plt
import numpy as np
import math
import os

w=50*1024*1024*8
alpha=1.2
capacity=500
interval=193
times=1
x_num=2
file_num=400
people=146

class request:
	def __init__(self,name,source):
		self.name=name
		self.source=source
class file:
	def __init__(self, file_name):
		self.file_name = file_name
		self.count = 0
		self.score = 0
		self.realcount = 0
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
		self.online=set()


graph=dict()
table=list()
users=list()
requests=list()
interaction=list()
#init
def init():
	for i in range(people):
		users.append(user())
		table.append([])
		for j in range(people):
			users[i].interaction.append([])
			table[i].append([])

	with open('email-Eu-core-temporal-Dept4.txt','r') as f:
		edge=f.read().split()
		i=0
		while i+1<len(edge):
			#hour
			timestamp=int((int(edge[i+2]))/60/60)
			users[int(edge[i])].interaction[int(edge[i+1])].append(timestamp)
			users[int(edge[i])].connect[int(edge[i+1])]+=1
			users[int(edge[i])].online.add(int(timestamp/24))
			i+=3

	for i in range(people):
		for j in range(people):
			if users[i].connect[j]>10:
				y=list()
				buf=list()
				index=0
				for k in range(12583):
					if k in users[i].interaction[j]:
						buf.append(1)

					if index==24:
						y.append(sum(buf))
						index=0
						buf=[]
					index+=1

				m=max(y)
				print(i,j)
				for k in range(len(y)):
					y[k]*=2
					y[k]/=m
				#Ci,j(day)
				users[i].interaction[j]=y
				model = ARIMA(y, order=(3,0,0))
				users[i].model[j] = model.fit(disp=0)

def possible(source , destination):

	result=list()

	def BFS(source , destination , path):
		if len(path)>3:
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

#our
cache_list=set()
#most popular
cache_list2=set()
n1=list()
n2=list()
n3=list()
n4=list()
n5=list()
t=range(interval)
'''x=list()

for i in range(x_num):
	x.append(1.2+i*0.1)
'''
x=range(x_num)
init()

for n in range(x_num):
	h1=list()
	h2=list()
	h3=list()
	h4=list()
	h5=list()
	occupation3=0
	occupation4=0
	occupation5=0
	#random
	cache_list3=set()
	#LFU
	cache_list4=set()

	for u in range(times):

		for i in range(interval):

			for a in range(people):
				for b in range(people):
					if users[a].connect[b]>10:
						users[a].edge[b]=users[a].model[b].predict(start=i, end=i)[0]*2
				book=dict()
				for b in range(people):
					if users[a].edge[b]>0:
						book[b]=users[a].edge[b]
				graph[a]=book
			#print(graph)
			if i==0:
				for a in range(people):
					for b in range(people):
						if a!=b:
							table[a][b]=possible(a,b)
				print(table)

				#users[a].social_factor=sum(users[a].edge)
			occupation=0
			occupation2=0
			
			#creat files
			files=list()
			for j in range(file_num):
				new_file=file(j)
				files.append(new_file)

			#update requests
			requests=list()
			for j in range(people):
				if len(users[j].online)>30:
					a=np.random.zipf(alpha)
					while a>=file_num or a<0 or a in users[j].watched:
						a=np.random.randint(2,file_num)

					requests.append(request(a,j))
					users[j].iswatching=True
					users[j].watched.add(a)

					if occupation3<capacity and (str(a) not in cache_list3):
						cache_list3.add(str(a))
						occupation3+=100

					if occupation4<capacity and (a not in cache_list4):
						cache_list4.add(a)
						occupation4+=100

					for k in range(people):
						if users[j].connect[k]>10:
							#if np.random.rand() <= users[j].interaction[k][int(i/24)]:
							users[k].wait_watch.add(str(a))

			#score
			for e in requests:
				files[e.name].count+=1
				files[e.name].realcount+=1

				for i in range(people):
					if table[e.name][i]!=0 and e.name!=i:
						p_know=list()
						for e in table[e.name][i]:
							multip=1
							for index in range(1,len(e)):
								multip*=graph[index-1][index]
							p_know.append(1-multip)
						donknow=1
						for e in p_know:
							donknow*=e
						print((1-donknow))
						files[e.name].score+=(1-donknow)
			
			print(len(requests))
			#wait_watch and spread
			while 1:
				star=len(requests)
				for j in range(people):
					num=len(users[j].wait_watch)
					#print(num)
					if num>0:
						for e in range(num):
							try:
								a = int(users[j].wait_watch.pop())
								requests.append(request(a,j))
								users[j].iswatching=True
								users[j].watched.add(a)
								for k in range(people):
									if users[j].connect[k]>10:
										if np.random.rand() <= users[j].interaction[k][int(i/24)]:
											users[k].wait_buf.add(str(a))
							except:
								break
				
				for j in range(people):
					num=len(users[j].wait_buf)
					if num>0:
						for e in range(num):
							try:
								a = int(users[j].wait_buf.pop())
								requests.append(request(a,j))
								users[j].iswatching=True
								users[j].watched.add(a)
							except:
								break

				if len(requests)-star==0:
					break

			for e in requests:
				files[e.name].realcount+=1

			#determine cache
			files.sort(key=lambda x: x.score, reverse=True)
			for e in files:
				if occupation <capacity:
					if e.file_name not in cache_list:
						cache_list.add(e.file_name)
						occupation+=100

						'''if e.realcount*2.5>(150):
							cache_list.add(e.file_name)
							occupation += 100
						else:
							cache_list.add(e.file_name)
							occupation += 40'''
				else:
					break

			files.sort(key=lambda x: x.count, reverse=True)

			for e in files:
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

			r_num=len(requests)
			print(r_num)
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

			h1.append(float(hit1)/(r_num+1))
			h2.append(float(hit2)/(r_num+1))
			h3.append(float(hit3)/(r_num+1))
			h4.append(float(hit4)/(r_num+1))
			'''h1.append(bitrate1)
			h2.append(bitrate2)
			h3.append(bitrate3)
			h4.append(bitrate4)'''
			cache_list=set()
			cache_list2=set()

			#init
			for j in range(people):
				users[j].iswatching=False
				users[j].wait_watch=set()
				users[j].watched=set()

			files.sort(key=lambda x: x.score, reverse=False)

			if capacity!=0 and len(cache_list3)>0:
				cache_list3.pop()
				occupation3-=100
			files.sort(key=lambda x: x.realcount, reverse=False)
			for e in files:
				if e.file_name in cache_list4:
					cache_list4.remove(e.file_name)
					occupation4-=100
					break

			for e in files:
				if e.file_name in cache_list4:
					cache_list4.remove(e.file_name)
					occupation4-=100
					break

	capacity += 100
	#alpha+=0.1
	n1.append(float(sum(h1))/interval/times)
	n2.append(float(sum(h2))/interval/times)
	n3.append(float(sum(h3))/interval/times)
	n4.append(float(sum(h4))/interval/times)
	n5.append(float(sum(h5))/interval/times)
	#time series
	'''plt.plot(t,h1,"g")
	plt.plot(t,h2,"b")
	plt.plot(t,h3,"r")
	plt.plot(t,h4,"y")
	plt.xlabel("time")
	plt.ylabel("QoE")
	plt.legend()'''
plt.plot(x,n1,"go",)
plt.plot(x,n2,"bo",)
plt.plot(x,n3,"ro",)
plt.plot(x,n4,"yo",)
plt.plot(x,n1,"g",label='proposed')
plt.plot(x,n2,"b",label='most popular')
plt.plot(x,n3,"r",label='random')
plt.plot(x,n4,"y",label='LFU')
plt.xlabel("cache size")
plt.ylabel("hit rate")
plt.legend()
plt.show()
