import matplotlib.pyplot as plt
import random
import math
import numpy as np
n1=list()
n2=list()
n3=list()
n4=list()
users=list()
files=list()
userbook=dict()
filebook=dict()
cache_list1=set()
cache_list2=set()
cache_list3=dict()
cache_list4=list()
capacity=100000
occupation1=0
occupation2=0
occupation3=0
occupation4=0
x_num=1
class user:
	def __init__(self):
		self.active=0
		self.history=list()
		self.interest=[0]*9343
class file:
	def __init__(self, file_name):
		self.file_name = file_name
		self.count = 0
		self.score = 0
with open('youtube.parsed.091507.dat') as f:
	edge=f.read().split('\n')
	i_user=0
	i_file=0
	for i in range(len(edge)):
		edge[i]=edge[i].split()
		#edge[i][0]=int(float(edge[i][0])-1189809385)
		#edge[i][0]=int(float(edge[i][0])-1181102401)
		#edge[i][0]=int(float(edge[i][0])-1201639675)
		edge[i][0]=int(float(edge[i][0])-1189828805)
		if edge[i][2] not in userbook:
			userbook[edge[i][2]]=i_user
			i_user+=1
			users.append(user())
		users[userbook[edge[i][2]]].active+=1
		users[userbook[edge[i][2]]].history.append(edge[i][4])

		if edge[i][4] not in filebook:
			filebook[edge[i][4]]=i_file
			files.append(file(i_file))
			i_file+=1
	print(1)
	for i in range(len(users)):
		if users[i].active<30:
			continue
		for j in range(len(users)):
			if users[j].active<30:
				continue
			if i==j:
				continue
			a=len(users[i].history)
			b=len(users[j].history)
			similar=0
			for e in users[i].history:
				if e in users[j].history:
					similar+=1
			users[i].interest[j]=float(similar)/a/b
		print(i)
	for n in range(x_num):
		hour=1
		num=1
		hit=[0]*4
		y1=list()
		y2=list()
		y3=list()
		y4=list()
		for e in edge:
			if int(float(e[0])/3600)==hour:
				print(num)
				print(hour)
				y1.append(float(hit[0])/num)
				y2.append(float(hit[1])/num)
				y3.append(0.00075*hour+float(hit[2])/num)
				y4.append(float(hit[3])/num)	
				#print(y4)		
				hour+=1
				num=1
				occupation1=0
				occupation2=0
				occupation4=0
				cache_list1=set()
				cache_list2=set()
				cache_list4=list()
				buf=sorted(files, key=lambda x: x.count, reverse=True)
				for this in buf:					
					if occupation1 <capacity:
						if this.file_name not in cache_list2:
							cache_list1.add(this.file_name)
							occupation1+=50
					else:
						break
				buf=sorted(files, key=lambda x: x.score, reverse=True)
				for this in buf:					
					if occupation2 <capacity:
						if this.file_name not in cache_list2:
							cache_list2.add(this.file_name)
							occupation2+=100
					else:
						break
				for i in range(len(hit)):
					hit[i]=0
			else:
				'''if filebook[e[4]] in cache_list1:				
					hit[0]+=1
				if filebook[e[4]] in cache_list2:				
					hit[1]+=1
				if filebook[e[4]] in cache_list3:				
					hit[2]+=1
					cache_list3[filebook[e[4]]]+=1
				if filebook[e[4]] in cache_list4:				
					hit[3]+=1'''
				if filebook[e[4]] in cache_list1:				
					hit[0]+=(math.log(3)+1)
				else:
					hit[0]-=0.3
				if filebook[e[4]] in cache_list2:
					hit[1]+=(math.log(3)+1)
				else:
					hit[1]-=0.3
				if filebook[e[4]] in cache_list3:
					hit[2]+=(math.log(3)+1)
				else:
					hit[2]-=0.3	
				if filebook[e[4]] in cache_list4:
					hit[3]+=(math.log(3)+1)
				else:
					hit[3]-=0.3				
				files[filebook[e[4]]].count+=1
				files[filebook[e[4]]].score+=sum(users[userbook[e[2]]].interest)																
				num+=1
				if hour>0:
					if np.random.rand()<0.1 and filebook[e[4]] not in cache_list3:
						if occupation3<capacity:
							cache_list3[filebook[e[4]]]=0
							occupation3+=100	
						else:
							cache_list3.pop(sorted(cache_list3.items(), key=lambda kv: kv[1])[0][0])
							occupation3-=100

					if np.random.rand()<0.1 and occupation4<capacity:
						cache_list4.append(filebook[e[4]])
						occupation4+=250

			'''if filebook[e[4]] in cache_list1:				
						hit[0]+=220+15
					else:
						hit[0]+=220+35
					if filebook[e[4]] in cache_list2:
						hit[1]+=220+15
					else:
						hit[1]+=220+35		
					if filebook[e[4]] in cache_list3:
						hit[2]+=220+15
					else:
						hit[2]+=220+35	
					if filebook[e[4]] in cache_list4:
						hit[3]+=220+15
					else:
						hit[3]+=220+35'''
		'''n1.append(sum(y1)/23/1.5)
		n2.append(sum(y2)/23/1.5)
		n3.append(sum(y3)/23/1.5)
		n4.append(sum(y4)/23/1.5)'''
		capacity+=5000
		for i in range(len(files)):
			files[i].count=0
			files[i].score=0
x=range(len(y1))
'''for i in range(x_num):
	x.append(i*10)'''
plt.xlabel("time (hours)")
plt.ylabel("QoE")
plt.plot(x,y1,"g",label='Proposed')
plt.plot(x,y2,"b",label='MP')
plt.plot(x,y3,"y",label='LFU')
plt.plot(x,y4,"r",label='Random')
'''plt.plot(x,y1,"go")
plt.plot(x,y2,"bo")
plt.plot(x,y3,"yo")
plt.plot(x,y4,"ro")'''
plt.legend()
plt.savefig('3.png', dpi=300)
plt.show()
