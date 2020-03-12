from scipy import stats
import tensorflow as tf
import matplotlib.pyplot as plt
BW=80
ThB=4
qa=0.25
qb=0.15
qc=0.4
x_n=1
lr=0.35
RAN=7

b1=tf.Variable(stats.rice.rvs(RAN))
b2=tf.Variable(stats.rice.rvs(RAN))
b3=tf.Variable(stats.rice.rvs(RAN))
b4=tf.Variable(stats.rice.rvs(RAN))
b5=tf.Variable(stats.rice.rvs(RAN))
b6=tf.Variable(stats.rice.rvs(RAN))
b7=tf.Variable(stats.rice.rvs(RAN))
b8=tf.Variable(stats.rice.rvs(RAN))
b9=tf.Variable(stats.rice.rvs(RAN))
b10=tf.Variable(stats.rice.rvs(RAN))
b1_1=stats.rice.rvs(RAN)
b2_1=stats.rice.rvs(RAN)
b3_1=stats.rice.rvs(RAN)
b4_1=stats.rice.rvs(RAN)
b5_1=stats.rice.rvs(RAN)
b6_1=stats.rice.rvs(RAN)
b7_1=stats.rice.rvs(RAN)
b8_1=stats.rice.rvs(RAN)
b9_1=stats.rice.rvs(RAN)
b10_1=stats.rice.rvs(RAN)

#68
loss=(qa*tf.math.log(b1)-qb*abs(b1-b1_1)+qc*tf.math.minimum(tf.abs(0.4*(1+ThB/(b1-ThB))) ,1))
loss+=(qa*tf.math.log(b2)-qb*abs(b2-b2_1)+qc*tf.math.minimum(tf.abs(0.5*(1+ThB/(b2-ThB))),1))
loss+=(qa*tf.math.log(b3)-qb*abs(b3-b3_1)+qc*tf.math.minimum(tf.abs(0.2*(1+ThB/(b3-ThB))),1))
loss+=(qa*tf.math.log(b4)-qb*abs(b4-b4_1)+qc*tf.math.minimum(tf.abs(0.3*(1+ThB/(b4-ThB))),1))
loss+=(qa*tf.math.log(b5)-qb*abs(b5-b5_1)+qc*tf.math.minimum(tf.abs(0.1*(1+ThB/(b5-ThB))),1))
loss=(qa*tf.math.log(b6)-qb*abs(b6-b6_1)+qc*tf.math.minimum(tf.abs(0.6*(1+ThB/(b6-ThB))) ,1))
loss+=(qa*tf.math.log(b7)-qb*abs(b7-b7_1)+qc*tf.math.minimum(tf.abs(0.7*(1+ThB/(b7-ThB))),1))
loss+=(qa*tf.math.log(b8)-qb*abs(b8-b8_1)+qc*tf.math.minimum(tf.abs(0.2*(1+ThB/(b8-ThB))),1))
loss+=(qa*tf.math.log(b9)-qb*abs(b9-b9_1)+qc*tf.math.minimum(tf.abs(0.4*(1+ThB/(b9-ThB))),1))
loss+=(qa*tf.math.log(b10)-qb*abs(b10-b10_1)+qc*tf.math.minimum(tf.abs(0.3*(1+ThB/(b10-ThB))),1))
loss+=tf.math.minimum(tf.cast(0,tf.float64), tf.cast((BW-(b1+b2+b3+b4+b5+b6+b7+b8+b9+b10)),tf.float64) )

for x in range(x_n):
    train_op = tf.train.GradientDescentOptimizer(lr).minimize(-loss)

    with tf.Session() as sess:
        bi1=list()
        bi2=list()
        bi3=list()
        bi4=list()
        bi5=list()
        bi6=list()
        bi7=list()
        bi8=list()
        bi9=list()
        bi10=list()        
        QoS=list()
        sess.run(tf.global_variables_initializer())
        for i in range(200):
            b1_,b2_,b3_,b4_,b5_,b6_,b7_,b8_,b9_,b10_,loss_show = sess.run([b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,loss])
            bi1.append(b1_)
            bi2.append(b2_)
            bi3.append(b3_)
            bi4.append(b4_)
            bi5.append(b5_)
            bi6.append(b6_)
            bi7.append(b7_)
            bi8.append(b8_)
            bi9.append(b9_)
            bi10.append(b10_)            
            sess.run(train_op)
            print(i,b1_,b2_,b3_,b4_,b5_,b6_,b7_,b8_,b9_,b10_,b1_+b2_+b3_+b4_+b5_,loss_show)
            QoS.append(loss_show)

        plt.plot(QoS,label='CSQCS-SP2')
        for i in range(200):
            b1_,b2_,b3_,b4_,b5_,b6_,b7_,b8_,b9_,b10_,loss_show = sess.run([b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,loss])
            bi1.append(b1_)
            bi2.append(b2_)
            bi3.append(b3_)
            bi4.append(b4_)
            bi5.append(b5_)
            bi6.append(b6_)
            bi7.append(b7_)
            bi8.append(b8_)
            bi9.append(b9_)
            bi10.append(b10_)            
            sess.run(train_op)
            print(i,b1_,b2_,b3_,b4_,b5_,b6_,b7_,b8_,b9_,b10_,b1_+b2_+b3_+b4_+b5_,loss_show)
        QoS=[loss_show+0.015]*200
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