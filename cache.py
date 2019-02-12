import numpy as np
import math
'''quality = 
stalling = 
QoE = quality/stalling
'''

#initialize necessary variable

#store one slot of request
requests = list()
viedo_lenght = list()
#store requested file
files = list()
#store user network condition
wu = list()
#store every user's social factor
social_factor = list()
#store cached file name
cache_list = list()

#parameter
capacity = 4*1024 #GB
occupation = 0
w = 120 #Mbps
p = 600 #transcoding process


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
	#print(Peoinact)
	for i in range(1000):
	    interact_number.append(int(np.random.chisquare(2)))

	for i in range(1000):
	    time_interact.append([])
	    for j in range(1000):
	        time_interact[i].append([])

	#everyone's people interact distribution
	for i in range(1000):
	    for j in range(interact_number[i]):
	        temp = np.random.randint(0,1000)
	        if (temp not in People_interact[i]) and (temp != i):
	            People_interact[i].append(temp)
	#print(Peoinact)

	#address multi problem
	for i in range(1000):
	    for j in range(1000):
	        if (i in People_interact[j]) and (j not in People_interact[i]):
	            People_interact[i].append(j)
	            interact_number[i]+=1
	print(interact_number)
	#sort
	for i in range(1000):
	    People_interact[i].sort()
	print(People_interact)

	#message time record
	for i in range(1000):
	    for j in range(i+1,1000):
	        if j in People_interact[i]:
	            a = np.random.chisquare(abs(np.random.normal(2)),100)
	            for k in range(len(a)):
	                if a[k]>5.:
	                    time_interact[i][j].append(k)
	                    time_interact[j][i].append(k)
	#show
	'''for i in range(1000):
	    for j in range(1000):
	        print('user '+str(i)+' user '+str(j))
	        print(tinact[i][j])'''

	#count
	denominator = 0
	for i in range(1000):
	    count = 0
	    for j in range(1000):
	        if len(time_interact[i][j])>0:
	            for k in range(len(time_interact[i][j])):
	                count+=math.exp(-time_interact[i][j][k]/350)
	    count=math.sqrt(count)
	    denominator += count*interact_number[i]
	    social_factor.append(count*interact_number[i])
	for i in range(len(social_factor)):
		social_factor[i]=int(social_factor[i]/denominator*10000)


	print(social_factor)

def generate_data():
	#video lenght (==size)
	for i in range(1000):
		buf = np.random.normal(6,8)
		if buf >1 :
			viedo_lenght.append(int(buf*10)/10)
		else:
			while 1:
				buf = np.random.normal(6,8)
				if buf <6 and buf >1:
					viedo_lenght.append(int(buf*10)/10)
					break

	#creat random normal network condition (network condition)
	for i in range(1000):	
		buf = np.random.normal(48,10)
		wu.append(buf)

#creat files	
def creat_files():		
	for i in range(1000):
		name = str(i)
		#480p
		size = viedo_lenght[i]*50
		#print(size)
		new_file = file(name, size)
		files.append(new_file)

#creat requests
def creat_requests():
	for i in range(1000):
		name = int(np.random.normal(500,100))
		social = social_factor[i]
		ping = wu[i]
		new_request = request(name, social, ping)
		requests.append(new_request)
'''
def degrade():
	bitrate-=5/6*1.024
	bitrate'''

#cache 1 ,parse one slot of request
cal_social()
generate_data()
creat_files()
creat_requests()

for e in requests:
	name = e.file_name
	s = e.social_factor
	ping = e.PING
	#request_file
	files[int(name)].count += 1
	files[int(name)].score += s
	files[int(name)].PING += ping

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
#our algorithm
for e in files:
	#C3
	if e.count>0:
		
		#e.PING/=e.count
		n = (1/w+1/p)/(1/e.PING+2/p+1/w)
		#print(n)
	#cache2
		if e.count*(1-n)*0.833333*1.024>=w:
			print('crash')
		'''print('name:')
		print(e.file_name)
		print('size')
		print(e.file_size)
		print('n:')
		print(n)
		print("score:")
		print(e.score)
		print("count:")
		print(e.count)
		print("ping:")
		print(e.PING)'''
		occupation += n*e.file_size
	#C1
		if occupation <=capacity:
			#bitrate+=5/6*1.024
			cache_list.append(e.file_name)
			#C2 ,降畫質
			'''if bitrate>w:
				bitrate-=5/6*1.024
				bitrate+=25/60*1.024
				print('to 720')
			if bitrate>w:
				bitrate-=25/60*1.024
				bitrate+=8.3/60*1.024
				print('to 480')
			if bitrate>w:
				bitrate-=8.3/60*1.024
				bitrate+=5/60*1.024
				print('to 360')'''
		else:
			print('full')
			break
files.sort(key=lambda x: x.count, reverse=True)

#popular algorithm
occupation2=0
cache_list2=list()
for e in files:
	if e.count>0:
		e.PING/=e.count
		n = (1/w+1/p)/(1/e.PING+2/p+1/w)
		occupation2 += n*e.file_size
		if occupation2 <= capacity:
			cache_list2.append(e.file_name)
		else:
			print('full')
			break
			
#首次cache結果
print(cache_list)
print(cache_list2)
print(cache_list3)
#第2次request
requests = list()
#creat_requests(450)
for i in range(1000):
	name = int(np.random.normal(450,100))
	social = social_factor[i]
	ping = wu[i]
	new_request = request(name, social, ping)
	requests.append(new_request)

hit1 = 0
hit2 = 0
hit3 = 0
for e in requests:
	#print(e.file_name)
	if str(e.file_name) in cache_list:
		#print(e.file_name)
		hit1+=1
	if str(e.file_name) in cache_list2:
		hit2+=1
	if str(e.file_name) in cache_list3:
		hit3+=1
print(hit1)
print(hit2)
print(hit3)