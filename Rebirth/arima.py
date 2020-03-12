from statsmodels.tsa.arima_model import ARIMA
from pandas import read_csv
import matplotlib.pyplot as plt
import numpy as np
#1,320
#2,172
#3,90
#4,146
#all,1005
users=1005
interaction=list()
#continuous=list()	
for a in range(users):
	interaction.append([])
	#continuous.append([])
	for b in range(users):	
		interaction[a].append(0)
		#continuous[a].append(0)

for k in range(1):
	y=list()
	day=0
	with open('email-Eu-core-temporal.txt','r') as f:
		edge=f.read().split()
		i=0
		buf=0
		m=1
		while i+1<len(edge):
			time=int((int(edge[i+2]))/60/60/24)
			interaction[int(edge[i])][int(edge[i+1])]=1
			'''if int(edge[i])==168:
				#m+=1
				if int(edge[i+1])==912:
					buf+=1'''
			i+=3
			if time>day:
				day+=1
				'''y.append(buf/m)
				m=1
				week+=1
				print(week)
				for a in range(1005):
					for b in range(1005):
						if interaction[a][b]==1:
							continuous[a][b]+=1
							interaction[a][b]=0'''
			if day>47:
				break
	inter_n=[0]*users
	for i in range(users):
		count=0
		for j in range(users):
			if interaction[i][j]==1:
				count+=1
		inter_n[i]=count
	print(inter_n)
	print(sum(inter_n)/users)
	'''m=0
	index=0
	for a in range(1005):
		for b in range(1005):
			if continuous[a][b]>m:
				m=continuous[a][b]
				index=(a,b)
	print(m)
	print(index)'''
	#predictions = list()
	'''model = ARIMA(y, order=(5,0,0))
	model_fit = model.fit(disp=0,trend='nc')
	predictions = list()
	for i in range(len(y)):
		output=model_fit.predict(start=i, end=i)[0]
		predictions.append(output)
	plt.plot(y,'g',label='Ii,j,t')
	plt.plot(predictions,label='P*i,j,t')
	plt.plot(y,'g*')
	plt.plot(predictions,'b*')
	plt.xlabel("time(days)")
	plt.ylabel("value")
	plt.legend()
	plt.show()'''
	'''
	for i in range(len(t)):
		t[i]=int(t[i])

	y=list()
	buf=list()
	index=0
	for i in range(int(12613/4)):
		if i in t:
			buf.append(1)

		if index==24:
			y.append(sum(buf))
			index=0
			buf.clear()
		index+=1
	m=max(y)
	for k in range(len(y)):
		y[k]/=m
	print(t)
	print(len(t))
	print(len(y))

	model.fit().forecast()[0]'''