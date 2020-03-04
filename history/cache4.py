import numpy as np
graph=dict()
interaction=list()
table=list()
requests=list()
preference=list()
social_factor=list()

class request:
	def __init__(self,name,source):
		self.name=name
		self.source=source

class file:
	def __init__(self, file_name):
		self.file_name = file_name
		self.count = 0
		self.score = 0


for i in range(1900):
	interaction.append([])
	table.append([])
	for j in range(1900):
		interaction[i].append(0)
		table.append(0)

with open('CollegeMsg.txt','r') as f:
	edge=f.read().split()
	i=0

	while i+1<len(edge):
		interaction [int(edge[i])] [int(edge[i+1])] += 1
		interaction [int(edge[i+1])] [int(edge[i])] += 1
		#print(int(edge[i]),int(edge[i+1]))
		#print(i)
		i+=3
	for i in range(1900):
		m=float(max(interaction[i]))
		if m==0:
			continue
		for j in range(1900):
			interaction[i][j]/=m

	for i in range(1900):
		for j in range(1900):
			if i == j:
				interaction[i][j]=1
				continue
			'''interaction[i][j]*=1.5
			if interaction[i][j]>1:
				interaction[i][j]=1'''
			if interaction[i][j]>=0.05:
				interaction[i][j]=1

	'''for i in range(1900):
		buf=dict()
		for j in range(1900):
			if interaction[i][j]!=0:
				buf[j]=interaction[i][j]
		graph[i]=buf'''
	#print(graph)
	for i in range(1900):
		social_factor.append(sum(interaction[i]))
	#print(interaction)
	print(social_factor)

capacity=1024*14
occupation=0
occupation2=0
cache_list=list()
cache_list2=list()
files=list()

for i in range(900):
	new_file=file(i)
	files.append(new_file)

#creat request
for i in range(1900):
	name=int(np.random.uniform(0,900))
	preference.append(name)
	#requests.append(request(name,i))
	files[name].count+=1
	files[name].score+=social_factor[i]

files.sort(key=lambda x: x.score, reverse=True)

for e in files:
	if occupation <=capacity:
		if e.file_name not in cache_list:
			cache_list.append(e.file_name)
			occupation += 100
	else:
		break

files.sort(key=lambda x: x.count, reverse=True)

for e in files:
	if occupation2 <=capacity:
		if e.file_name not in cache_list2:
			cache_list2.append(e.file_name)
			occupation2 += 100
	else:
		break
print(cache_list)
print(cache_list2)

wait_watch=list()

for i in range(900):
	wait_watch.append([])
#evaluate
for i in range(1900):
	for j in range(1900):
		if interaction[i][j] >0:
			#if np.random.uniform(0,100)/100.0>=interaction[i][j]:
			requests.append(preference[i])
			wait_watch[preference[i]].append(i)

for i in range(900):
	for j in range(2*len(wait_watch[i])):
		requests.append(i)
hit1=0
hit2=0
for e in requests:
	if e in cache_list:
		hit1+=1
	if e in cache_list2:
		hit2+=1

print(len(requests))
print(float(hit1)/hit2)
print(hit1/float(len(requests)))
print(hit2/float(len(requests)))

#for e 

'''

score=list()

#calculate table
for i in range(1900):
	for j in range(1900):
		interaction[i][j]*=1.5
		if interaction[i][j]>1:
			interaction[i][j]=1
		interaction[i][j]=1-interaction[i][j]



#parse request
for e in files:
	for i in e:
'''
