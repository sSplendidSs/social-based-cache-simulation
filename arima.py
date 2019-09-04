from statsmodels.tsa.arima_model import ARIMA
from pandas import read_csv
import matplotlib.pyplot as plt

interaction=list()
#1,320
#2,172
#3,90
#4,146
#all,1005
for a in range(1005):
	interaction.append([])
	for b in range(1005):
		interaction[a].append(0)

for k in range(1):
	t=list()

	with open('email-Eu-core-temporal-Dept4.txt','r') as f:
		edge=f.read().split()
		i=0
		while i+1<len(edge):
			interaction[int(edge[i])][int(edge[i+1])]+=1
			#if int(edge[i])==774 and int(edge[i+1])==947:
			#t.append(float(int(edge[i+2])/60/60))
			i+=3
	m=0
	index=0
	for a in range(146):
		for b in range(146):
			if interaction[a][b]>m:
				m=interaction[a][b]
				index=(a,b)
	print(m)
	print(index)

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

	model = ARIMA(y, order=(10,0,0))
	model_fit = model.fit(disp=0)
	predictions = list()
	for i in range(1,len(y)):
		output = model_fit.predict(start=i, end=i)[0]
		if output<0:
			output=0
		predictions.append(output)

	plt.plot(y,'g',label='Ii,j,t')
	plt.plot(predictions,label='P*i,j,t')
	plt.plot(y,'g*')
	plt.plot(predictions,'b*')
	plt.xlabel("time(days)")
	plt.ylabel("value")
	plt.legend()
	plt.show()

	model.fit().forecast()[0]