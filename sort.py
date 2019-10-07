a=open('test.txt','r')
edge1=a.read().split()
b=open('email-Eu-core-temporal.txt','r')
edge2=b.read().split()
i1=0
i2=0
f=open('allinone.txt','w')
for t in range(16736181):
	while t==int(edge1[i1+2]):	 	
		f.write(edge1[i1])
		f.write(' ')
		f.write(edge1[i1+1])
		f.write(' ')
		f.write(str(t))
		f.write('\n')
		i1+=3
	while t==int(edge2[i2+2]):
		f.write(str(int(edge2[i2])+1900))
		f.write(' ')
		f.write(str(int(edge2[i2+1])+1900))
		f.write(' ')
		f.write(str(t))
		f.write('\n')
		i2+=3
"""f=open('CollegeMsg.txt')
edge=f.read().split()
i=0
while i+1<len(edge):
	edge[i+2]=str(int(edge[i+2])-1082040961)
	i+=3
#print(edge)
f.close()
f=open('test.txt','w')
i=0
for e in edge:
	f.write(e)
	i+=1
	if i%3==0:
		f.write('\n')
	else:
		f.write(' ')"""