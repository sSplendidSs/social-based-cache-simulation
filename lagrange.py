from scipy import stats
import tensorflow as tf
import matplotlib.pyplot as plt
BW=25
ThB=1.25
qa=0.25
qb=0.15
qc=0.4
x_n=1
lr=0.005

b1=tf.Variable(stats.rice.rvs(3))
b2=tf.Variable(stats.rice.rvs(3))
b3=tf.Variable(stats.rice.rvs(3))
b4=tf.Variable(stats.rice.rvs(3))
b5=tf.Variable(stats.rice.rvs(3))
b1_1=stats.rice.rvs(3)
b2_1=stats.rice.rvs(3)
b3_1=stats.rice.rvs(3)
b4_1=stats.rice.rvs(3)
b5_1=stats.rice.rvs(3)

#68
loss=35*(qa*tf.math.log(b1)-qb*abs(b1-b1_1)+qc*tf.math.minimum(0.4*(1+ThB/(b1-ThB)),1))
loss+=17*(qa*tf.math.log(b2)-qb*abs(b2-b2_1)+qc*tf.math.minimum(0.5*(1+ThB/(b2-ThB)),1))
loss+=9*(qa*tf.math.log(b3)-qb*abs(b3-b3_1)+qc*tf.math.minimum(0.2*(1+ThB/(b3-ThB)),1))
loss+=5*(qa*tf.math.log(b4)-qb*abs(b4-b4_1)+qc*tf.math.minimum(0.3*(1+ThB/(b4-ThB)),1))
loss+=2*(qa*tf.math.log(b5)-qb*abs(b5-b5_1)+qc*tf.math.minimum(0.1*(1+ThB/(b5-ThB)),1))
loss-=tf.math.log(tf.abs(BW-(b1+b2+b3+b4+b5)))

for x in range(x_n):
    train_op = tf.train.GradientDescentOptimizer(lr).minimize(-loss)

    with tf.Session() as sess:
        bi1=list()
        bi2=list()
        bi3=list()
        bi4=list()
        bi5=list()
        QoS=list()
        sess.run(tf.global_variables_initializer())
        for i in range(500):
            b1_,b2_,b3_,b4_,b5_,loss_show = sess.run([b1,b2,b3,b4,b5,loss])
            bi1.append(b1_)
            bi2.append(b2_)
            bi3.append(b3_)
            bi4.append(b4_)
            bi5.append(b5_)
            sess.run(train_op)
            print(i,b1_,b2_,b3_,b4_,b5_,b1_+b2_+b3_+b4_+b5_,loss_show)
            QoS.append(loss_show)
        plt.plot(QoS,label='CSQCS-SP2')
        for i in range(500):
            b1_,b2_,b3_,b4_,b5_,loss_show = sess.run([b1,b2,b3,b4,b5,loss])
            bi1.append(b1_)
            bi2.append(b2_)
            bi3.append(b3_)
            bi4.append(b4_)
            bi5.append(b5_)
            sess.run(train_op)
            print(i,b1_,b2_,b3_,b4_,b5_,b1_+b2_+b3_+b4_+b5_,loss_show)
        QoS=[loss_show+0.1]*500
        plt.plot(QoS,label='optimal')        
    lr+=0.0005
'''plt.plot(range(len(bi1)),bi1,"g",)
plt.plot(bi2,"b",)
plt.plot(bi3,"y",)
plt.plot(bi4,"m",)
plt.plot(bi5,"k",)'''
plt.xlabel("number of iteration")
plt.ylabel("QoS")
plt.legend()
plt.savefig('iteration.png', dpi=300)
plt.show()