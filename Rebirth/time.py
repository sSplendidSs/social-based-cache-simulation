import matplotlib.pyplot as plt
import numpy as np
q=5
r=15
size=25
x_num=1
times=1
x=list()
perform=list()
result=list()
for i in range(4):	perform.append([])
for i in range(x_num):
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
			time=int((int(edge[ii+2]))/60/60/24)
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
							v=str(np.random.rand())
							#requests.append(v)
							vr.add(v)
							video[v]=dict()
							video[v]['view']=0
							video[v]['count']=0
							video[v]['recent']=0
							users[u]['seen'].add(v)
							for f in users[u]['friend']:
								if users[u]['friend'][f] and users[f]['friend'][u]:
									users[f]['wait_buf'].add(v)					
				hit=[0]*4
				for e in requests:
					if e in cache_0:
						hit[0]+=1
					if e in cache_1:
						hit[1]+=1
					if e in cache_2:
						hit[2]+=1
					if e in cache_3:
						hit[3]+=1
				total+=len(requests)
				#print('day:',day,len(requests))
				result.append(len(requests))
				sortedv=sorted(video.items(), key=lambda kv: -kv[1]['count'])
				cache_0=list()
				for e in sortedv:
					cache_0.append(e[0])
					if len(cache_0)>1.4*size:
						break
				sortedv=sorted(video.items(), key=lambda kv: -kv[1]['count'])
				cache_1=list()
				for e in sortedv:
					cache_1.append(e[0])
					if len(cache_1)>size:
						break
				sortedv=sorted(video.items(), key=lambda kv: -kv[1]['recent'])
				cache_2=list()
				for e in sortedv:
					cache_2.append(e[0])
					if len(cache_2)>size:
						break
				cache_3=list()
				for e in vr:
					if e not in cache_3:
						cache_3.append(e)
					if len(cache_3)>size:
						break
				for v in video:
					video[v]['recent']=0
				for u in users:
					users[u]['counter']=0
				if day%r==0:
					vr=set()
				if day%q==0:						
					for v in video:
						video[v]['count']=0
					for u in users:
						for f in users[u]['friend']:
							users[u]['friend'][f]=0

				for k in range(4):
					perform[k].append(hit[k])
					print(hit[k])
				x.append(day)
				if day>390:
					break
plt.plot(x,perform[0],"g",label='Hit-CSQCA')
plt.plot(x,perform[1],"b",label='Hit-MP')
plt.plot(x,perform[2],"y",label='Hit-LRU')
plt.plot(x,perform[3],"r",label='Hit-Random')
plt.plot(x,result,"k", )
plt.xlabel("time slot (hour)")
plt.ylabel("Number of requests")
plt.legend()
plt.savefig('realtime.jpg', dpi = 600)