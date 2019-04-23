import numpy as np
import math

interact_number = list()
People_interact = list()
time_interact = list()
social_factor = list()
cache_list=list()
cache_list2=list()
wait_watch = list()
intimate = list()
requests=list()
files = list()
capacity = 1024 #MB


for i in range(100):
	wait_watch.append([])

class request:
	def __init__(self, file_name, social_factor):
		self.file_name = file_name
		self.social_factor = social_factor 

class file:
	#initialize
	def __init__(self, file_name):
		self.file_name = file_name
		self.count = 0
		self.score = 0

#creat
def creat_file():
	files.clear()
	for i in range(100):
		new_file=file(i)
		files.append(new_file)

def cal_social():
	#initialize
	for i in range(100):
		People_interact.append([])

	for i in range(100):
		interact_number.append(int(np.random.poisson(7)))

	for i in range(100):
		time_interact.append([])
		for j in range(100):
		    time_interact[i].append([])

	for i in range(100):
		intimate.append([])

	#everyone's people interact distribution
	for i in range(100):
		for j in range(interact_number[i]):
		    temp = np.random.poisson(40)
		    if (temp not in People_interact[i]) and (temp != i):
		        People_interact[i].append(temp)

	#address multi problem
	for i in range(100):
		for j in range(100):
		    if (i in People_interact[j]) and (j not in People_interact[i]):
		        People_interact[i].append(j)
		        interact_number[i]+=1
	#sort
	for i in range(100):
		People_interact[i].sort()

	#message time record
	for i in range(100):
		for j in range(i+1,100):
		    if j in People_interact[i]:
		        #a = np.random.chisquare(abs(np.random.normal(3)),100)
		        a = np.random.poisson(3,100)
		        for k in range(len(a)):
		            if a[k]>5:
		            	b=np.random.poisson(2)
		            	for l in range(b):
		                	time_interact[i][j].append(k)
		                	time_interact[j][i].append(k)

	#cal intimate
	for i in range(100):
		for j in range(100):
		    if len(time_interact[i][j])>0:
		    	intimate[i].append(j)

	#count social factor
	denominator = 0
	for i in range(100):
		count = 0
		for j in range(100):
		    if len(time_interact[i][j])>0:
		        for k in range(len(time_interact[i][j])):
		            count+=math.exp(-time_interact[i][j][k]/350)

		#count=math.log(count+1)
		denominator += count*interact_number[i]
		social_factor.append(int(interact_number[i]*20)/10)

def creat_request():
	requests.clear()
	wait_watch.clear()
	for i in range(100):
		wait_watch.append([])

	for i in range(100):
		name=np.random.randint(0,100)
		new_request=request(name,social_factor[i])
		requests.append(new_request)
		for j in People_interact[i]:
			if name not in wait_watch[j]:
				wait_watch[j].append(name)

def parse_request():

	occupation = 0
	occupation2 = 0
	cache_list.clear()
	cache_list2.clear()
	for e in requests:
		name = e.file_name
		s = e.social_factor
		files[int(name)].count += 1
		files[int(name)].score += s

	files.sort(key=lambda x: x.score, reverse=True)

	for e in files:
		if occupation <=capacity:
			if e.file_name not in cache_list:
				cache_list.append(e.file_name)
				occupation += 40
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

def evaluate():
	global hit1
	global hit2
	requests.clear()

	for i in range(100):
		for j in wait_watch[i]:
			new_request=request(j,social_factor[i])
			requests.append(new_request)

	#print(cache_list)
	#print(cache_list2)

	for r in requests:
		#print(r.social_factor)
		if r.file_name in cache_list:
			hit1+=1
		if r.file_name in cache_list2:
			hit2+=1



cal_social()
for i in range(15):
	capacity=256*(i+1)		
	hit1=0
	hit2=0
	for j in range(5):

		creat_file()
		creat_request()
		parse_request()
		evaluate()
	print(i)
	print(hit1/5200)
	print(hit2/5200)
	#print(wait_watch)
'''
print(People_interact)
print(social_factor)
print(wait_watch)
print(len(requests))'''