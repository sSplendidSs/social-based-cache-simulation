import matplotlib.pyplot as plt
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
capacity=5000
occupation1=0
occupation2=0
occupation3=0
occupation4=0
#14
#16337
#4513
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
		edge[i][0]=int(float(edge[i][0])-1189809385)
		#edge[i][0]=int(float(edge[i][0])-1181102401)
		#edge[i][0]=int(float(edge[i][0])-1201639675)
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
		if users[i].active<50:
			continue
		for j in range(len(users)):
			if users[j].active<50:
				continue
			if i==j:
				continue
			a=len(users[i].history)
			b=len(users[j].history)
			similar=0
			for e in users[i].history:
				if e in users[j].history:
					similar+=1
			users[i].interest[j]=similar/a/b
		print(i)
	for i in range(len(users)):
		print(sum(users[i].interest))
	hour=1
	num=0
	hit=[0]*4
	for e in edge:
		if int(e[0]/3600)==hour:
			print(num)
			occupation1=0
			occupation2=0
			cache_list1=set()
			cache_list2=set()
			buf=sorted(files, key=lambda x: x.score, reverse=True)
			for e in buf:					
				if occupation1 <capacity:
					if e.file_name not in cache_list2:
						cache_list1.add(e.file_name)
						occupation1+=50
				else:
					break
			buf=sorted(files, key=lambda x: x.count, reverse=True)
			for e in buf:					
				if occupation2 <capacity:
					if e.file_name not in cache_list2:
						cache_list2.add(e.file_name)
						occupation2+=100
				else:
					break		
			print(cache_list1)
			print(cache_list2)	
			y1.append(hit[0]/num)
			y2.append(hit[1]/num)
			#y3.append(hit[2]/num)
			#y4.append(hit[3]/num)			
			hour+=1
			num=0
			for i in range(len(files)):
				files[i].score=0
			for i in range(len(hit)):
				hit[i]=0
		else:
			if users[userbook[edge[i][2]]].active>50:
				files[filebook[e[4]]].count+=1
				files[filebook[e[4]]].score+=sum(users[userbook[edge[i][2]]].interest)
				#print(sum(users[userbook[edge[i][2]]].interest))
				#print(filebook[e[4]])
				if filebook[e[4]] in cache_list1:				
					hit[0]+=1
				if filebook[e[4]] in cache_list2:
					hit[1]+=1		
				'''if e[4] in cache_list3:
					hit[2]+=1
				if e[4] in cache_list4:
					hit[3]+=1'''
				num+=1

plt.xlabel("hour")
plt.ylabel("number of requests")
plt.plot(y1,"g",)
plt.plot(y2,"b",)
plt.show()