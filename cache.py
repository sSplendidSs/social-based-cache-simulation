import numpy as np
import math
'''quality = 
stalling = 
QoE = quality/stalling
'''

#initialize necessary variable
requests = list()
viedo_lenght = list()
files = list()
PING = list()
social_factor = list()
cache_list = list()
capacity = 8*1024 #GB
occupation = 0
bitrate = 0
w = 100 #Mbps
R = 22 #Mbps
p = 300 #transcoding process


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
	def __init__(self, file_name, social_factor, PING):
		self.file_name = file_name
		self.social_factor = social_factor 
		self.PING = PING
		
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
	for i in range(1000):
	    count = 0
	    for j in range(1000):
	        if len(time_interact[i][j])>0:
	            for k in range(len(time_interact[i][j])):
	                count+=math.exp(-time_interact[i][j][k]/350)
	    count=math.sqrt(count+1)
	    social_factor.append(int(count*interact_number[i]*10)/10)

	print(social_factor)

def generate_data():
	#video lenght
	for i in range(100):
		buf = np.random.normal(6,8)
		if buf >1 :
			viedo_lenght.append(int(buf*10)/10)
		else:
			while 1:
				buf = np.random.normal(6,8)
				if buf <6 and buf >1:
					viedo_lenght.append(int(buf*10)/10)
					break

	#creat random normal ping
	seed = list()
	for i in range(1000):	
		buf = np.random.normal(55,50)
		if buf >5:
			seed.append(int(buf))
		else:
			while 1:
				buf = np.random.normal(55,50)
				if buf >5 and buf <60:
					seed.append(int(buf))
					break
	for i in range(1000):
		PING.append(seed[np.random.randint(0,100)])
	#print(PING)

#creat files	
def creat_files():		
	for i in range(100):
		name = str(i)
		#480p
		size = viedo_lenght[i]*50
		#print(size)
		new_file = file(name, size)
		files.append(new_file)

#creat requests
def creat_requests():
	for i in range(1000):
		name = int(np.random.chisquare(50))
		social = social_factor[i]
		ping = PING[i]
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
	social_factor = e.social_factor
	ping = e.PING
	#request_file
	files[int(name)].count += 1
	files[int(name)].score += social_factor
	files[int(name)].PING += ping

#sort
files.sort(key=lambda x: x.score, reverse=True)

for e in files:
	#C3
	if e.count>0:
		
		e.PING/=e.count
		n = (1/w)/(1/R*e.PING/55+1/w)
		#cache2
		if e.count*(1-n)*0.833333*1.024>=w:
			print('crash')
		#print(n)
		'''print("score:")
		print(e.score)
		print("count:")
		print(e.count)
		print("ping:")
		print(e.PING)'''
		occupation += n*e.file_size
		if occupation <=capacity:
			bitrate+=5/6*1.024
			cache_list.append(e.file_name)
		else:
			bitrate+=2.7/60*1.024
			print('full')
			break
print(cache_list)

cache_list.reverse()
print(bitrate)
#C2 ,降畫質
for e in cache_list:
	if bitrate>w:
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
		print('to 360')
