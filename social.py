import matplotlib.pyplot as plt
import os
import numpy as np
import math
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
		self.watching = False
		self.watched = set()
		self.wait_watch = set()
		self.wait2 = set()
		self.interaction = [0]*1900
		self.iswatching = False
users=list()
requests=list()
interaction=list()
social_factor=list()
#init
def init():
	for i in range(1900):
		users.append(user())
	with open('CollegeMsg.txt','r') as f:
		edge=f.read().split()
		i=0
		while i+1<len(edge):
			users[int(edge[i])].interaction[int(edge[i+1])] += 1
			users[int(edge[i+1])].interaction[int(edge[i])] += 1
			i+=3
		for i in range(1900):
			m=float(max(users[i].interaction))
			if m==0:
				continue
			for j in range(1900):
				users[i].interaction[j]/=m
		for i in range(1900):
			social_factor.append(sum(users[i].interaction))

w=600*1024*1024*8
capacity=0
interval=10
times=11
file_num=100
#our
cache_list=list()
#most popular
cache_list2=list()
#random
cache_list3=list()
n1=list()
n2=list()
n3=list()
n4=list()
n5=list()
buf=list()
for i in range(file_num):
	buf.append(file(i))
t=range(interval)
x=range(times)
init()

for n in range(times):
	h1=list()
	h2=list()
	h3=list()
	h4=list()
	h5=list()
	occupation4=0
	occupation5=0
	#LFU
	cache_list4=list()
	#greedy
	cache_list5=list()

	for i in range(interval):
		occupation=0
		occupation2=0
		occupation3=0
		#creat files
		files=list()
		for j in range(file_num):
			new_file=file(j)
			files.append(new_file)

		#update requests
		requests=list()
		for j in range(1900):
			if np.random.rand()<=0.1:
				a=np.random.zipf(1.2)
				#if a>100:
				#	continue
				while a>=100 or a<0 or a in users[j].watched:
					a=np.random.randint(2,100)
					if occupation3<capacity and (a not in cache_list3):
						cache_list3.append(a)
						occupation3+=100

				requests.append(request(a,j))
				users[j].iswatching=True
				users[j].watched.add(a)
				
				if occupation4<capacity and (a not in cache_list4):
					cache_list4.append(a)
					occupation4+=100

				for k in range(1900):
					if users[k].interaction[j] !=0:
						if np.random.rand() <= users[k].interaction[j]:
							if (a not in users[k].watched) and (a not in users[k].wait_watch):
								users[k].wait_watch.add(str(a))
		#score
		for e in requests:
			files[e.name].count+=1
			files[e.name].score+=social_factor[e.source]
			files[e.name].realcount+=1
		#print(len(requests))

		#wait_watch and spread
		for j in range(1900):
			num=len(users[j].wait_watch)
			#print(num)
			if num>0:
				dice = np.random.poisson(3)
				for e in range(num):
					try:
						a = int(users[j].wait_watch.pop())
						requests.append(request(a,j))
						users[j].iswatching=True
						users[j].watched.add(a)

					except:
						break
		for e in requests:
			files[e.name].realcount+=1

		#determine cache
		files.sort(key=lambda x: x.score, reverse=True)
		for e in files:
			if occupation <capacity:
				if e.file_name not in cache_list:
					if e.realcount*2.5>(150):
						#print('hit')
						cache_list.append(e.file_name)
						occupation += 100
					else:
						cache_list.append(e.file_name)
						occupation += 35
			else:
				break
		for e in files:
			if occupation5 <capacity:
				if e.file_name not in cache_list5:
					cache_list5.append(e.file_name)
					occupation5 += 100
					break

		files.sort(key=lambda x: x.count, reverse=True)

		for e in files:
			if occupation2 <capacity:
				if e.file_name not in cache_list2:
					cache_list2.append(e.file_name)
					occupation2 += 100
			else:
				break

		cache_list.sort()
		cache_list2.sort()
		cache_list3.sort()
		cache_list4.sort()
		cache_list5.sort()
		print(cache_list)
		print(cache_list2)
		print(cache_list3)
		print(cache_list4)
		print(cache_list5)

		#evaluate
		hit1=0
		hit2=0
		hit3=0
		hit4=0
		hit5=0

		for e in requests:
			if e.name in cache_list:
				hit1+=1
			if e.name in cache_list2:
				hit2+=1
			if e.name in cache_list3:
				hit3+=1
			if e.name in cache_list4:
				hit4+=1
			if e.name in cache_list5:
				hit5+=1
		r_num=len(requests)
		print(r_num)
		print(n)
		'''print(w/(r_num-hit2)/1024/1024/8)
		bitrate1=math.log((hit1*2.5*1024*1024*8 + w)/r_num)
		bitrate2=math.log((hit2*2.5*1024*1024*8 + w)/r_num)
		bitrate3=math.log((hit3*2.5*1024*1024*8 + w)/r_num)
		bitrate4=math.log((hit4*2.5*1024*1024*8 + w)/r_num)
		bitrate5=math.log((hit5*2.5*1024*1024*8 + w)/r_num)
		print(bitrate1)
		print(bitrate2)
		print(bitrate3)
		print(bitrate4)
		print(bitrate5)'''

		h1.append(hit1/(r_num+1))
		h2.append(hit2/(r_num+1))
		h3.append(hit3/(r_num+1))
		h4.append(hit4/(r_num+1))
		h5.append(hit5/(r_num+1))
		'''h1.append(bitrate1)
		h2.append(bitrate2)
		h3.append(bitrate3)
		h4.append(bitrate4)
		h5.append(bitrate5)'''
		cache_list.clear()
		cache_list2.clear()
		cache_list3.clear()

		#初始化
		for j in range(1900):
			users[j].iswatching=False
			users[j].wait_watch=set()
			users[j].watched=set()

		files.sort(key=lambda x: x.count, reverse=False)

		for e in files:
			if e.file_name in cache_list4:
				cache_list4.remove(e.file_name)
				occupation4-=100
				break
	
	capacity += 100
	
	n1.append(sum(h1)/interval)
	n2.append(sum(h2)/interval)
	n3.append(sum(h3)/interval)
	n4.append(sum(h4)/interval)
	n5.append(sum(h5)/interval)
	#time series
	#plt.plot(t,h1,"g")
	#plt.plot(t,h2,"b")
	#plt.plot(t,h3,"r")
	#plt.plot(t,h4,"y")
plt.plot(x,n1,"g")
plt.plot(x,n2,"b")
plt.plot(x,n3,"r")
plt.plot(x,n4,"y")
plt.plot(x,n5,"m")
plt.show()