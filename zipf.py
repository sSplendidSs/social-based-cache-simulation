import numpy as np
import tensorflow as tf
import scipy.stats as stats
import matplotlib.pyplot as plt
interval=1000
file_num=10000
people=100
a=0.56
b=4
ThB=1.5
downloading=0
threshold=0.001
vq=0.2
Ei=0.8

x=np.arange(1, file_num+1)
weights=x**(-a)
weights/=weights.sum()
bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(x, weights))

users=list()
cache=list()
class user:
	def __init__(self):
		self.watching=False
		self.remain=300
		self.cached=0
		self.bwi=0
		self.bt_1=1
#init
for i in range(people):
	users.append(user())

for t in range(interval):

	for u in users:
		if not u.watching:
			#requests
			if np.random.rand()<=np.random.poisson(2)/10:
				request=bounded_zipf.rvs()
				if request in cache:
					u.cached=120
				downloading+=1
				u.watching=True
		else:
			u.bwi=stats.rice.rvs(b)

			#個人SP2
			bi = tf.Variable(float(u.bt_1))
			loss=vq*tf.math.log(bi)+Ei*tf.math.minimum((u.cached/u.remain)*(1+ThB/(bi-ThB)),1)#+tf.math.log(1+u.bwi-bi)
			train_op = tf.train.AdamOptimizer(0.01).minimize(-loss)
			with tf.Session() as sess:
				sess.run(tf.global_variables_initializer())
				L_1=99999
				for it in range(100):
					bis,loss_show = sess.run([bi,loss])
					print(loss_show,float(bis))
					if float(bis)>u.bwi:
						break
					#L_1=float(loss_show)
					sess.run(train_op)
			if (float(bis)-ThB)>u.cached:
				u.cached+=ThB
			
			else:
				u.remain-=ThB
				u.cached+=(ThB-float(bis))

			u.bt_1=float(bis)

			if u.remain<=0:
				u.watching=False
				u.remain=0
				u.cached=0

plt.show()