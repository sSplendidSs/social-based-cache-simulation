import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
alpha=0.7
bound=np.arange(1, 5000)
weights=bound**(-alpha)
weights/=weights.sum()
bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(bound, weights))
q=2
r=4
size=25
x_num=1
times=1
x=range(60)
result=list()
for i in range(x_num):
	buf=[0]*4
	users=dict()
	video=dict()
	vr=set()
	day=0
	cache_0=list()
	cache_1=list()
	perform1=list()
	for i in range(4):	perform1.append([])
	with open('CollegeMsg.txt','r') as f:
		edge=f.read().split()
		ii=0
		for u in range(1900):
			users[str(u)]=dict()
			users[str(u)]['friend']=dict()
			users[str(u)]['seen']=set()
			users[str(u)]['wait_watch']=set()
			users[str(u)]['wait_buf']=set()
			users[str(u)]['counter']=0

		while ii+1<len(edge):
			time=int((int(edge[ii+2])-1082040961)/60/60/24)
			#update social graph
			if edge[ii] not in users[edge[ii+1]]['friend']:
				users[edge[ii+1]]['friend'][edge[ii]]=0
			users[edge[ii]]['friend'][edge[ii+1]]=1
			users[edge[ii]]['counter']=1							
			ii+=3
				
			if time>day:
				day+=1
				requests=list()
				#share
				for u in users:
					users[u]['wait_watch']|=users[u]['wait_buf']
					users[u]['wait_buf']=set()
				for u in users:
					for v in users[u]['wait_watch']:
						if v not in users[u]['seen']:
							users[u]['seen'].add(v)
							video[v]['view']+=1
							video[v]['count']+=1
							video[v]['recent']=1
							requests.append(v)
							vr.add(v)
							for f in users[u]['friend']:
								if users[u]['friend'][f] and users[f]['friend'][u]:
									users[f]['wait_buf'].add(v)
					users[u]['wait_watch']=set()
				#video request
				for u in users:
					if users[u]['counter']:
						if np.random.rand()<0.05:
							#v=str(np.random.poisson(1000))
							#v=str(np.random.rand())
							v=str(bounded_zipf.rvs())
							requests.append(v)
							vr.add(v)
							if v not in video:
								video[v]=dict()
								video[v]['view']=0
								video[v]['count']=0
								video[v]['recent']=0
							users[u]['seen'].add(v)
							for f in users[u]['friend']:
								if users[u]['friend'][f] and users[f]['friend'][u]:
									users[f]['wait_buf'].add(v)					
				bt_nc=0
				bt_c=0
				bt_cc=0
				for e in requests:
					bt_nc+=stats.rice.rvs(4)
					if e not in cache_0:
						bt_cc+=stats.rice.rvs(4)
					if e not in cache_1:
						bt_c+=stats.rice.rvs(4)
				requests.append(0)
				perform1[0].append(bt_nc/3600*8/4)
				perform1[1].append(bt_c/3600*8/4)
				perform1[2].append(bt_cc/3600*8/4)
				print('day:',day,len(requests))
				sortedv=sorted(video.items(), key=lambda kv: -kv[1]['count'])
				cache_0=list()
				for e in sortedv:
					cache_0.append(e[0])
					if len(cache_0)>2*size:
						break
				sortedv=sorted(video.items(), key=lambda kv: -kv[1]['count'])
				cache_1=list()
				for e in sortedv:
					cache_1.append(e[0])
					if len(cache_1)>size:
						break
				for v in video:
					video[v]['recent']=0
				for u in users:
					users[u]['counter']=0
				if day%r==0:
					vr=set()
					for u in users:
						users[u]['seen']=set()
				if day%q==0:						
					for v in video:
						video[v]['count']=0
					for u in users:
						for f in users[u]['friend']:
							users[u]['friend'][f]=0
				if day>60:
					break

	buf=[0]*4
	users=dict()
	video=dict()
	vr=set()
	day=0
	cache_0=list()
	cache_1=list()
	perform2=list()
	for i in range(4):	perform2.append([])
	with open('email-Eu-core-temporal.txt','r') as f:
		edge=f.read().split()
		ii=0
		for u in range(1005):
			users[str(u)]=dict()
			users[str(u)]['friend']=dict()
			users[str(u)]['seen']=set()
			users[str(u)]['wait_watch']=set()
			users[str(u)]['wait_buf']=set()
			users[str(u)]['counter']=0

		while ii+1<len(edge):
			time=int(int(edge[ii+2])/60/60/24/2)
			#update social graph
			if edge[ii] not in users[edge[ii+1]]['friend']:
				users[edge[ii+1]]['friend'][edge[ii]]=0
			users[edge[ii]]['friend'][edge[ii+1]]=1
			users[edge[ii]]['counter']=1							
			ii+=3
				
			if time>day:
				day+=1
				requests=list()
				#share
				for u in users:
					users[u]['wait_watch']|=users[u]['wait_buf']
					users[u]['wait_buf']=set()
				for u in users:
					for v in users[u]['wait_watch']:
						if v not in users[u]['seen']:
							users[u]['seen'].add(v)
							video[v]['view']+=1
							video[v]['count']+=1
							video[v]['recent']=1
							requests.append(v)
							vr.add(v)
							for f in users[u]['friend']:
								if users[u]['friend'][f] and users[f]['friend'][u]:
									users[f]['wait_buf'].add(v)
					users[u]['wait_watch']=set()
				#video request
				for u in users:
					if users[u]['counter']:
						if np.random.rand()<0.1:
							#v=str(np.random.poisson(1000))
							#v=str(np.random.rand())
							v=str(bounded_zipf.rvs())
							requests.append(v)
							vr.add(v)
							if v not in video:
								video[v]=dict()
								video[v]['view']=0
								video[v]['count']=0
								video[v]['recent']=0
							users[u]['seen'].add(v)
							for f in users[u]['friend']:
								if users[u]['friend'][f] and users[f]['friend'][u]:
									users[f]['wait_buf'].add(v)					
				bt_nc=0
				bt_c=0
				bt_cc=0
				for e in requests:
					bt_nc+=stats.rice.rvs(4)
					if e not in cache_0:
						bt_cc+=stats.rice.rvs(4)
					if e not in cache_1:
						bt_c+=stats.rice.rvs(4)
				requests.append(0)
				perform2[0].append(bt_nc/3600*8/4)
				perform2[1].append(bt_c/3600*8/4)
				perform2[2].append(bt_cc/3600*8/4)
				print('day:',day,len(requests))
				sortedv=sorted(video.items(), key=lambda kv: -kv[1]['count'])
				cache_0=list()
				for e in sortedv:
					cache_0.append(e[0])
					if len(cache_0)>2*size:
						break
				sortedv=sorted(video.items(), key=lambda kv: -kv[1]['count'])
				cache_1=list()
				for e in sortedv:
					cache_1.append(e[0])
					if len(cache_1)>size:
						break
				for v in video:
					video[v]['recent']=0
				for u in users:
					users[u]['counter']=0
				if day%r==0:
					vr=set()
					for u in users:
						users[u]['seen']=set()
				if day%q==0:						
					for v in video:
						video[v]['count']=0
					for u in users:
						for f in users[u]['friend']:
							users[u]['friend'][f]=0
				if day>60:
					break
for i in range(4):	result.append([])
print(perform2)
print(perform1)
for i in range(60):
	for j in range(3):
		result[j].append(perform1[j][i]+perform2[j][i])
print(result)
plt.plot(x,result[0],"k",label='Non cache')
plt.plot(x,result[1],"b",label='Non-Collaborative cache')
plt.plot(x,result[2],"g",label='Collaborative cache')
plt.xlabel("Time slots (day)")
plt.ylabel("Average Backhaul Traffic (MB/s)")
plt.legend()
plt.savefig('traffic.jpg', dpi = 600)