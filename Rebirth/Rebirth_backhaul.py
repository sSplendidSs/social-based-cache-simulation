import matplotlib.pyplot as plt
import numpy as np
q=3
size=5
x_num=10
times=30
x=list()
perform=list()
for i in range(4):	perform.append([])
for i in range(x_num):
	buf=[0]*4
	for j in range(times):
		users=dict()
		video=dict()
		day=0
		total=0
		cache_0=list()
		cache_1=list()
		cache_2=list()
		cache_3=list()
		hit=[0]*4
		with open('CollegeMsg.txt','r') as f:
			edge=f.read().split()
			ii=0
			while ii+1<len(edge):
				time=int((int(edge[ii+2])-1082040961)/60/60/24)
				#update social graph
				if edge[ii] not in users:
					users[edge[ii]]=dict()
					users[edge[ii]]['friend']=dict()
					users[edge[ii]]['counter']=0
					users[edge[ii]]['seen']=set()
					users[edge[ii]]['wait_watch']=set()
					users[edge[ii]]['wait_buf']=set()
				if edge[ii+1] not in users:
					users[edge[ii+1]]=dict()
					users[edge[ii+1]]['friend']=dict()
					users[edge[ii+1]]['counter']=0
					users[edge[ii+1]]['seen']=set()
					users[edge[ii+1]]['wait_watch']=set()
					users[edge[ii+1]]['wait_buf']=set()

				if edge[ii+1] not in users[edge[ii]]['friend']:
					users[edge[ii]]['friend'][edge[ii+1]]=0

				if edge[ii] not in users[edge[ii+1]]['friend']:
					users[edge[ii]]['friend'][edge[ii+1]]=0
					
				users[edge[ii]]['friend'][edge[ii+1]]+=1
				users[edge[ii]]['counter']+=1
				ii+=3
				
				if time>day:
					day+=1
					requests=list()
					vr=set()
					#share
					for u in users:
						users[u]['wait_watch']|=users[u]['wait_buf']
						users[u]['wait_buf']=set()
					for u in users:
						for v in users[u]['wait_watch']:
							if v not in users[u]['seen']:
								video[v]['view']+=1
								video[v]['count']+=1
								video[v]['recent']=1
								requests.append(v)
								vr.add(v)
								for f in users[u]['friend']:
									if (users[u]['friend'][f])>1 and (users[f]['friend'][u])>1:
										users[f]['wait_buf'].add(v)
						users[u]['wait_watch']=set()

					#video request
					for u in users:
						if users[u]['counter']>0:
							if np.random.rand()<0.07:
								v_id=str(np.random.rand())
								requests.append(v_id)
								vr.add(v_id)
								video[v_id]=dict()
								video[v_id]['view']=0
								video[v_id]['count']=0
								video[v_id]['recent']=0
								users[u]['seen'].add(v_id)
								for f in users[u]['friend']:
									if (users[u]['friend'][f])>1 and (users[f]['friend'][u])>1:
										users[f]['wait_buf'].add(v_id)
					
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
					sortedLFU=sorted(video.items(), key=lambda kv: -kv[1]['count'])
					cache_0=list()
					for e in sortedLFU:
						cache_0.append(e[0])
						if len(cache_0)>1.5*size:
							break
					sortedLFU=sorted(video.items(), key=lambda kv: -kv[1]['view'])
					cache_1=list()
					for e in sortedLFU:
						cache_1.append(e[0])
						if len(cache_1)>size:
							break
					sortedLFU=sorted(video.items(), key=lambda kv: -kv[1]['recent'])
					cache_2=list()
					for e in sortedLFU:
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
					if day%q==0:
						for v in video:
							video[v]['count']=0
						for u in users:
							users[u]['counter']=0
							leave=list()
							for f in users[u]['friend']:
								leave.append(f)
							for e in leave:
								users[u]['friend'].pop(e)

					if day>47:
						for k in range(4):
							buf[k]+=hit[k]/total
						break
	for k in range(4):
		perform[k].append(buf[k]/times)
		print(buf[k]/times)
	x.append((i+1)*10)
	size+=4
plt.plot(x,perform[0],"g",label='CSQCA')
plt.plot(x,perform[1],"b",label='MP')
plt.plot(x,perform[2],"y",label='LRU')
plt.plot(x,perform[3],"r",label='Random')
plt.plot(x,perform[0],"go")
plt.plot(x,perform[1],"bo")
plt.plot(x,perform[2],"yo")
plt.plot(x,perform[3],"ro")
plt.xlabel("Cache size (GB)")
plt.ylabel("Hitrate")
plt.legend()
plt.savefig('size.jpg', dpi = 600)