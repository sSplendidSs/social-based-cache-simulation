import numpy as np
#import tensorflow as tf
import scipy.stats as stats
import matplotlib.pyplot as plt
x=np.arange(1, file_num+1)
weights=x**(-a)
weights/=weights.sum()
bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(x, weights))

#init
def init():
	for i in range(people):
		users.append(user())
		table.append([])
		for j in range(people):
			users[i].Iij.append([])
			table[i].append([])
		for j in range(day):
			users[i].interaction.append([])

	with open('email-Eu-core-temporal.txt','r') as f:
		edge=f.read().split()
		i=0
		while i+1<len(edge):
			timestamp=int((int(edge[i+2]))/60/60/24)
			users[int(edge[i])].interaction[timestamp].append(int(edge[i+1]))
			users[int(edge[i])].connect[int(edge[i+1])]+=1	
			users[int(edge[i])].online.add(timestamp)
			users[int(edge[i])].count+=1
			i+=3