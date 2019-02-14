import numpy as np
import math
'''quality = 
stalling = 
QoE = quality/stalling
'''
#initialize necessary variable
#parameter
capacity = 1024 #GB
w = 120 #Mbps
p = 600 #transcoding process
hit1 = 0
hit2 = 0
hit3 = 0
mid = 0

#file attribute class
class file:
	#initialize
	def __init__(self, file_name, file_size):
		self.file_name = file_name
		self.file_size = file_size
		self.count = 0
		self.score = 0
		self.PING = 0

#request attribute class
class request:
	#initialize
	def __init__(self, file_name, social_factor, network_condition):
		self.file_name = file_name
		self.social_factor = social_factor 
		self.PING = network_condition
		
def cal_social():
	interact_number = list()
	People_interact = list()
	time_interact = list()

	#initialize
	for i in range(1000):
	    People_interact.append([])

	for i in range(1000):
	    interact_number.append(int(np.random.chisquare(3)))

	for i in range(1000):
	    time_interact.append([])
	    intimate.append([])
	    for j in range(1000):
	        time_interact[i].append([])
	        intimate.append([])

	#everyone's people interact distribution
	for i in range(1000):
	    for j in range(interact_number[i]):
	        temp = np.random.randint(0,1000)
	        if (temp not in People_interact[i]) and (temp != i):
	            People_interact[i].append(temp)

	#address multi problem
	for i in range(1000):
	    for j in range(1000):
	        if (i in People_interact[j]) and (j not in People_interact[i]):
	            People_interact[i].append(j)
	            interact_number[i]+=1
	#sort
	for i in range(1000):
	    People_interact[i].sort()

	#message time record
	for i in range(1000):
	    for j in range(i+1,1000):
	        if j in People_interact[i]:
	            a = np.random.chisquare(abs(np.random.normal(3)),100)
	            for k in range(len(a)):
	                if a[k]>5.:
	                    time_interact[i][j].append(k)
	                    time_interact[j][i].append(k)
	for i in range(1000):
	    for j in range(1000):
	        if len(time_interact[i][j])>0:
	        	intimate[i].append(j)

	#count
	denominator = 0
	for i in range(1000):
	    count = 0
	    for j in range(1000):
	        if len(time_interact[i][j])>0:
	            for k in range(len(time_interact[i][j])):
	                count+=math.exp(-time_interact[i][j][k]/350)

	    #count=count**(1/1.5)
	    denominator += count*interact_number[i]
	    social_factor.append(int(count*interact_number[i]*10)/10)
	#for i in range(len(social_factor)):
	#	social_factor[i]=social_factor[i]/denominator*1000
	#print(social_factor)
	global mid
	mid = sorted(social_factor)[500]

def generate_data():
	global preference
	#video lenght (==size)
	for i in range(1000):
		#buf = np.random.normal(6,8)
		buf = np.random.chisquare(8)
		if buf >1 :
			viedo_lenght.append(int(buf*10)/10)
		else:
			while 1:
				#buf = np.random.normal(6,8)
				buf = np.random.chisquare(8)
				if buf <8 and buf >1:
					viedo_lenght.append(int(buf*10)/10)
					break

	#creat random normal network condition (network condition)
	for i in range(1000):	
		buf = np.random.normal(48,10)
		wu.append(buf)

	#user preference
	for i in range(1000):
		'''a = int(np.random.normal(500,200))
		while a<0 or a>999:
				a = int(np.random.normal(500,200))'''
		a = np.random.randint(1,1000)
		preference.append(a)

#creat files	
def creat_files():		
	for i in range(1000):
		name = str(i)
		#1080p
		size = viedo_lenght[i]*50
		new_file = file(name, size)
		files.append(new_file)

def init_requests():
	for i in range(1000):
		social = social_factor[i]
		#print(int(4*social/mid))
		for j in range(int(4*social/mid)):
			a = int(np.random.poisson(preference[i]))
			while a<0 or a>999:
				a = int(np.random.poisson(preference[i]))
			#a = np.random.randint(0,1000)
			name = str(a)
			ping = wu[i]
			new_request = request(name, social, ping)
			requests.append(new_request)

def creat_requests():
	for i in range(1000):
		social = social_factor[i]
		#print(int(4*social/mid))
		for j in range(int(4*social/mid)):
			a = int(np.random.poisson(preference[i]))
			while a<0 or a>999:
				a = int(np.random.poisson(preference[i]))
			#a = np.random.randint(0,1000)
			name = str(a)
			ping = wu[i]
			new_request = request(name, social, ping)
			requests.append(new_request)

			for e in intimate[i]:
				social = social_factor[e]
				name = str(a)
				ping = wu[e]
				new_request = request(name, social, ping)
				requests.append(new_request)

#parse the request
def collect():
	for e in requests:
		name = e.file_name
		s = e.social_factor
		ping = e.PING
		#request_file
		files[int(name)].count += 1
		files[int(name)].score += s
		files[int(name)].PING = (files[int(name)].PING *(files[int(name)].count-1) + ping)/files[int(name)].count

#def compare():
#	global hit1,hit2,hit3

for n in range(15):
	
	#initialize necessary variable

	#store one slot of request
	requests = list()
	viedo_lenght = list()
	#store requested file
	files = list()
	#store user network condition
	wu = list()
	#user's
	preference = list()
	#store every user's social factor
	social_factor = list()
	intimate = list()

	cal_social()
	generate_data()
	creat_files()
	#cache 1 ,parse one slot of request
	init_requests()
	collect()
	print(len(requests))
	#compare()
	#compare different algorithm
	occupation3 = 0
	cache_list3 = list()
	for e in files:
		if e.count>0:
			occupation3+=e.file_size
			if occupation3 <= capacity:
				cache_list3.append(e.file_name)
			else:
				print('full')
				break

	#sort
	files.sort(key=lambda x: x.score, reverse=True)

	occupation = 0
	cache_list = list()
	#our algorithm
	for e in files:
		#C3
		if e.count>0:
			n = (1/w+1/p)/(1/e.PING+2/p+1/w)
		#cache2
			#if e.count*(1-n)*0.833333*1.024>=w:
			#	print('crash')
			#print('name:')
			#print(e.file_name)
			#print("score:")
			#print(e.score)
			#print("count:")
			#print(e.count)
			#occupation += n*e.file_size
			occupation += 100
		#C1
			if occupation <=capacity:
				#bitrate+=5/6*1.024
				cache_list.append(e.file_name)
				#C2 ,降畫質
			else:
				print('full')
				break
	files.sort(key=lambda x: x.count, reverse=True)

	#popular algorithm
	occupation2=0
	cache_list2=list()
	for e in files:
		if e.count>0:
			n = (1/w+1/p)/(1/e.PING+2/p+1/w)
			#occupation2 += n*e.file_size
			occupation2 += 100
			if occupation2 <= capacity:
				cache_list2.append(e.file_name)
			else:
				print('full')
				break

	#首次cache結果
	#print(cache_list)
	#print(cache_list2)
	#print(cache_list3)

	for i in range(15):
		#第n次request
		requests = list()
		#creat_requests(450)
		creat_requests()

		for r in requests:
			#print(e.file_name)
			if r.file_name in cache_list:
				hit1+=1
			if r.file_name in cache_list2:
				hit2+=1
			if r.file_name in cache_list3:
				hit3+=1

print(hit1/225)
print(hit2/225)
print(hit3/225)