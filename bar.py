import matplotlib.pyplot as plt
x=['Collaborative','Non-Collaborative','Non Caching']
a=[0.295,0.81,1.7]
b=[1.94,1.4,1.165]
plt.bar(x,a)
plt.ylabel("average backhaul traffic (MB/s)")
plt.savefig('Collaborative.png', dpi=1000,bbox_inches='tight')
plt.show()
plt.bar(x,b)
plt.ylabel("average fronthaul traffic (MB/s)")
plt.show()