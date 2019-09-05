import matplotlib.pyplot as plt
import random
x=list()
y1=list()
y2=list()
y3=list()
y4=list()
users=list()
files=list()
userbook=dict()
filebook=dict()
cache_list1=set()
cache_list2=set()
cache_list3=list()
cache_list4=list()
capacity=200000
occupation1=0
occupation2=0
occupation3=0
occupation4=0
x_num=30
class user:
	def __init__(self):
		self.active=0
		self.history=list()
		self.interest=[0]*5000
class file:
	def __init__(self, file_name):
		self.file_name = file_name
		self.count = 0
		self.score = 0
with open('youtube.parsed.012908.S1.dat') as f:
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
		if users[i].active<10:
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
	#for i in range(len(users)):
	#	print(sum(users[i].interest))
	hour=1
	num=1
	hit=[0]*4
	for e in edge:
		if int(float(e[0])/600)==hour:
			print(num)
			print(hour)
			y1.append(float(hit[0])/num)
			y2.append(float(hit[1])/num)
			y3.append(float(hit[2])/num)
			y4.append(float(hit[3])/num)	
			print(y1)		
			hour+=1
			num=1
			occupation1=0
			occupation2=0
			cache_list1=set()
			cache_list2=set()
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
			buf=sorted(files, key=lambda x: x.count, reverse=False)
			for t in range(30):
				for this in buf:					
					if this.file_name in cache_list3:
						cache_list3.remove(this.file_name)
						occupation3-=100					
						break

			for i in range(len(files)):
				files[i].count=0
				files[i].score=0
			for i in range(len(hit)):
				hit[i]=0
		else:
			if sum(users[userbook[e[2]]].interest)>0:
				files[filebook[e[4]]].count+=1
				files[filebook[e[4]]].score+=sum(users[userbook[e[2]]].interest)
				'''if filebook[e[4]] in cache_list1:				
					hit[0]+=15
				else:
					hit[0]+=45
				if filebook[e[4]] in cache_list2:
					hit[1]+=15
				else:
					hit[1]+=45		
				if filebook[e[4]] in cache_list3:
					hit[2]+=15
				else:
					hit[2]+=45	
				if filebook[e[4]] in cache_list4:
					hit[3]+=15
				else:
					hit[3]+=45'''	
				num+=1
				if filebook[e[4]] in cache_list1:				
					hit[0]+=1
				if filebook[e[4]] in cache_list2:				
					hit[1]+=1
				if filebook[e[4]] in cache_list3:				
					hit[2]+=1
				if filebook[e[4]] in cache_list4:				
					hit[3]+=1
			else:
				if occupation3<capacity:
					cache_list3.append(filebook[e[4]])
					occupation3+=100
				if occupation4<capacity:
					cache_list4.append(filebook[e[4]])
					occupation4+=100
print(sum(y1)/23/6)
print(sum(y2)/23/6)
print(sum(y3)/23/6)
print(sum(y4)/23/6)
plt.xlabel("hour")
plt.ylabel("hit rate")
plt.plot(y1,"g",label='proposed')
plt.plot(y2,"b",label='MP')
plt.plot(y3,"y",label='LFU')
plt.plot(y4,"r",label='Random')
plt.legend()
plt.show()