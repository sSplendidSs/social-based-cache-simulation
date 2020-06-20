import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
alpha=0.7
bound=np.arange(1, 10000)
q=2
r=4
size=10
x_num=12
times=18
x=list()
perform=list()
for i in range(6):	perform.append([])
for i in range(x_num):
	buf=[0]*6
	weights=bound**(-alpha)
	weights/=weights.sum()
	bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(bound, weights))	
	for j in range(times):
		users=dict()
		video=dict()
		vr=set()		
		day=0
		total=0
		cache=list()
		for alg in range(6):	cache.append([])
		hit=[0]*6
		for u in range(1900):
			users[str(u)]=dict()
			users[str(u)]['friend']=dict()
			users[str(u)]['seen']=set()
			users[str(u)]['wait_watch']=set()
			users[str(u)]['wait_buf']=set()
			users[str(u)]['counter']=0		
		with open('CollegeMsg.txt','r') as f:
			edge=f.read().split()
			ii=0
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
								video[v]['count']+=1
								video[v]['recent']=(10-day%q)
								video[v]['ARC']+=1
								requests.append(v)
								vr.add(v)
								for f in users[u]['friend']:
									if users[u]['friend'][f] and users[f]['friend'][u]:
										users[f]['wait_buf'].add(v)
										video[v]['EN']+=1
						users[u]['wait_watch']=set()
					#video request
					for u in users:
						if users[u]['counter']:
							if np.random.rand()<0.07:
								#v=str(np.random.rand())
								#v=str(np.random.poisson(2000))
								v=str(bounded_zipf.rvs())
								users[u]['seen'].add(v)
								requests.append(v)
								vr.add(v)
								if v not in video:
									video[v]=dict()
									video[v]['EN']=1
									video[v]['count']=0
									video[v]['recent']=0
									video[v]['ARC']=0

								for f in users[u]['friend']:
									if users[u]['friend'][f] and users[f]['friend'][u]:
										users[f]['wait_buf'].add(v)
										video[v]['EN']+=1
					for e in requests:
						for alg in range(len(cache)):
							if e in cache[alg]:
								hit[alg]+=1						
					total+=len(requests)
					#print('day:',day,len(requests))
					sortedv=sorted(video.items(), key=lambda kv: -kv[1]['EN'])
					cache[0]=list()
					for e in sortedv:
						cache[0].append(e[0])
						if len(cache[0])>size/0.45:	break
					sortedv=sorted(video.items(), key=lambda kv: -kv[1]['EN'])
					cache[1]=list()
					for e in sortedv:
						cache[1].append(e[0])
						if len(cache[1])>1.15*size:	break
					sortedv=sorted(video.items(), key=lambda kv: -kv[1]['ARC'])
					cache[2]=list()
					for e in sortedv:
						cache[2].append(e[0])
						if len(cache[2])>size:	break
					sortedv=sorted(video.items(), key=lambda kv: -kv[1]['count'])
					cache[3]=list()
					for e in sortedv:
						cache[3].append(e[0])
						if len(cache[3])>size:	break
					sortedv=sorted(video.items(), key=lambda kv: -kv[1]['recent'])
					cache[4]=list()
					for e in sortedv:
						cache[4].append(e[0])
						if len(cache[4])>size:	break
					cache[5]=list()
					for e in vr:
						if e not in cache[5]:
							cache[5].append(e)
						if len(cache[5])>size/1.15:	break

					for u in users:
						users[u]['counter']=0
					if day%r==0:
						vr=set()
						for u in users:							
							users[u]['seen']=set()
						for v in video:
							video[v]['count']=0							
							video[v]['recent']=0		
					if day%q==0:
						for v in video:
							video[v]['EN']=0
							video[v]['ARC']=0
						for u in users:	
							for f in users[u]['friend']:
								users[u]['friend'][f]=0
					if day>47:	break
		users=dict()
		video=dict()
		vr=set()		
		day=0
		cache=list()
		for alg in range(6):	cache.append([])
		for u in range(1005):
			users[str(u)]=dict()
			users[str(u)]['friend']=dict()
			users[str(u)]['seen']=set()
			users[str(u)]['wait_watch']=set()
			users[str(u)]['wait_buf']=set()
			users[str(u)]['counter']=0		
		with open('email-Eu-core-temporal.txt','r') as f:
			edge=f.read().split()
			ii=0
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
								video[v]['count']+=1
								video[v]['recent']=(10-day%q)
								video[v]['ARC']+=1
								requests.append(v)
								vr.add(v)
								for f in users[u]['friend']:
									if users[u]['friend'][f] and users[f]['friend'][u]:
										users[f]['wait_buf'].add(v)
										video[v]['EN']+=1
						users[u]['wait_watch']=set()
					#video request
					for u in users:
						if users[u]['counter']:
							if np.random.rand()<0.14:
								v=str(bounded_zipf.rvs())
								users[u]['seen'].add(v)
								requests.append(v)
								vr.add(v)
								if v not in video:
									video[v]=dict()
									video[v]['EN']=1
									video[v]['count']=0
									video[v]['recent']=0
									video[v]['ARC']=0

								for f in users[u]['friend']:
									if users[u]['friend'][f] and users[f]['friend'][u]:
										users[f]['wait_buf'].add(v)
										video[v]['EN']+=1
					for e in requests:
						for alg in range(len(cache)):
							if e in cache[alg]:
								hit[alg]+=1						
					total+=len(requests)
					#print('day:',day,len(requests))

					sortedv=sorted(video.items(), key=lambda kv: -kv[1]['EN'])
					cache[0]=list()
					for e in sortedv:
						cache[0].append(e[0])
						if len(cache[0])>size/0.45:	break
					sortedv=sorted(video.items(), key=lambda kv: -kv[1]['EN'])
					cache[1]=list()
					for e in sortedv:
						cache[1].append(e[0])
						if len(cache[1])>1.15*size:	break
					sortedv=sorted(video.items(), key=lambda kv: -kv[1]['ARC'])
					cache[2]=list()
					for e in sortedv:
						cache[2].append(e[0])
						if len(cache[2])>size:	break
					sortedv=sorted(video.items(), key=lambda kv: -kv[1]['count'])
					cache[3]=list()
					for e in sortedv:
						cache[3].append(e[0])
						if len(cache[3])>size:	break
					sortedv=sorted(video.items(), key=lambda kv: -kv[1]['recent'])
					cache[4]=list()
					for e in sortedv:
						cache[4].append(e[0])
						if len(cache[4])>size:	break
					cache[5]=list()
					for e in vr:
						if e not in cache[5]:
							cache[5].append(e)
						if len(cache[5])>size/1.15:	break
					for u in users:
						users[u]['counter']=0
					if day%r==0:
						vr=set()
						for u in users:							
							users[u]['seen']=set()
						for v in video:
							video[v]['count']=0							
							video[v]['recent']=0		
					if day%q==0:
						for v in video:
							video[v]['EN']=0
							video[v]['ARC']=0
						for u in users:	
							for f in users[u]['friend']:
								users[u]['friend'][f]=0
					if day>47:
						for k in range(6):
							buf[k]+=hit[k]/total
						break
	for k in range(6):
		perform[k].append(buf[k]/times)
		print(buf[k]/times)
	x.append(alpha)
	alpha+=0.1
plt.plot(x,perform[0],"go-",label='CSQCA')
plt.plot(x,perform[1],"k*-",label='CSQCA-F')
plt.plot(x,perform[2],"mH-",label='ARC')
plt.plot(x,perform[3],"bs-",label='MP')
plt.plot(x,perform[4],"yp-",label='LRU')
plt.plot(x,perform[5],"rD-",label='RA')
plt.xlabel("ν")
plt.ylabel("Hitrate")
plt.legend()
plt.savefig('zipf.png', dpi = 600)