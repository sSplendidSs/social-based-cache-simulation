from statsmodels.tsa.arima_model import ARIMA
from pandas import read_csv
import matplotlib.pyplot as plt

for k in range(100):
	t=list()

	with open('CollegeMsg.txt','r') as f:
		edge=f.read().split()
		i=0
		print(k	)
		while i+1<len(edge):
			#if edge[i]=='1168' or edge[i]=='1624':
			#if edge[i]=='1168' or edge[i+1]=='1168':
			#if (edge[i]=='1624' and edge[i+1]=='1168') or (edge[i]=='1168' and edge[i+1]=='1624'):
			if int(edge[i])==99 :
				t.append(float(int(edge[i+2])-1082040961)/60/60)
			i+=3

	for i in range(len(t)):
		t[i]=int(t[i])

	y=list()
	buf=list()
	index=0
	for i in range(4517):
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
	print(y)

	model = ARIMA(y, order=(7,0,0))
	model_fit = model.fit(disp=0)
	predictions = list()
	for i in range(len(y)):
		output = model_fit.predict(start=i, end=i)[0]
		if output<0:
			output=0
		predictions.append(output)

	plt.plot(y,'g',label='Ci,j,t')
	plt.plot(predictions,label='P*i,j,t')
	plt.plot(y,'g*')
	plt.plot(predictions,'b*')
	plt.xlabel("time(days)")
	plt.ylabel("value")
	plt.legend()
	plt.show()