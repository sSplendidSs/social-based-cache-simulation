import tensorflow as tf
import matplotlib.pyplot as plt
ThB=1.25
quality=0.2
stall=0.8
b1 = tf.Variable(1.0)
b2 = tf.Variable(tf.random_normal(shape=[1],mean=2,stddev=0))
b3 = tf.Variable(tf.random_normal(shape=[1],mean=2,stddev=0))
b4 = tf.Variable(tf.random_normal(shape=[1],mean=2,stddev=0))
b5 = tf.Variable(tf.random_normal(shape=[1],mean=2,stddev=0))
#loss = 35*(math.log()+0.9*(1+ThB/(b1-ThB)))+17*(0.75*(1+ThB/(b2-ThB)))+9*(0.8*(1+ThB/(b3-ThB)))+5*(0.2*(1+ThB/(b4-ThB)))+2*(0.1*(1+ThB/(b5-ThB)))
loss = 35*(quality*tf.math.log(b1)+stall*tf.math.minimum(0.4*(1+ThB/(b1-ThB)),1))+17*(quality*tf.math.log(b2)+stall*tf.math.minimum(0.5*(1+ThB/(b2-ThB)),1))+9*(quality*tf.math.log(b3)+stall*tf.math.minimum(0.2*(1+ThB/(b3-ThB)),1))+5*(quality*tf.math.log(b4)+stall*tf.math.minimum(0.3*(1+ThB/(b4-ThB)),1))+2*(quality*tf.math.log(b5)+stall*tf.math.minimum(0.1*(1+ThB/(b5-ThB)),1))


train_op = tf.train.AdamOptimizer(1e-3).minimize(-loss)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    ite=list()
    bi1=list()
    bi2=list()
    bi3=list()
    bi4=list()
    bi5=list()
    for i in range(500):
        #b1,b2,b3,b4,b5,loss_show = sess.run([b1,b2,b3,b4,b5,loss])
        b1s,loss_show = sess.run([b1,loss])
        bi1.append(b1s)
        b2s,loss_show = sess.run([b2,loss])
        bi2.append(b2s)
        b3s,loss_show = sess.run([b3,loss])
        bi3.append(b3s)
        b4s,loss_show = sess.run([b4,loss])
        bi4.append(b4s)
        b5s,loss_show = sess.run([b5,loss])
        bi5.append(b5s)
        ite.append(i)
        if b1s>0 and b2s>0 and b3s>0 and b4s>0 and b5s>0 and b1s<3 and b2s<3 and b3s<3 and b4s<3 and b5s<3:
        	sess.run(train_op)
        else:
        	break
        print((i,loss_show,float(b1s),b2s,b3s,b4s,b5s))
plt.plot(ite,bi1,"g",)
plt.plot(ite,bi2,"b",)
plt.plot(ite,bi3,"y",)
plt.plot(ite,bi4,"m",)
plt.plot(ite,bi5,"k",)
plt.xlabel("iteration")
plt.ylabel("bitrate")
plt.legend()
plt.show()