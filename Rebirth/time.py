import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
alpha=0.5
bound=np.arange(1, 10000)
weights=bound**(-alpha)
weights/=weights.sum()
bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(bound, weights))
q=2
r=4
size=25
x_num=1
times=1
x=range(61)
result=list()
perform=list()
for i in range(2):	perform.append([])
for i in range(x_num):
	buf=[0]*4
	users=dict()
	video=dict()
	vr=set()
	day=0
	total=0
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
				total+=len(requests)
				print('day:',day,len(requests))
				perform[0].append(len(requests))

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
	total=0
	cache_0=list()
	cache_1=list()
	cache_2=list()
	cache_3=list()
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
			time=int((int(edge[ii+2]))/60/60/24/2)
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
				total+=len(requests)
				print('day:',day,len(requests))
				perform[1].append(len(requests))
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
plt.plot(x,perform[0],"b:", label='Dataset 1')
plt.plot(x,perform[1],"g-", label='Dataset 2')
plt.xlabel("Time slots (day)")
plt.ylabel("Number of requests")
plt.legend()
plt.savefig('realtime5.jpg', dpi = 600)