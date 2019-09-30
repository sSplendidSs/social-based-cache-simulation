import matplotlib.pyplot as plt
import networkx as nx
#H = nx.path_graph(1005)
G = nx.Graph()
#G.add_nodes_from(H)
for i in range(1005):
	G.add_node(i)
interaction=list()
for i in range(1005):
	interaction.append([])
	interaction[i]=[0]*1005
with open('email-Eu-core-temporal.txt','r') as f:
	edge=f.read().split()
	i=0
	while i+1<len(edge):
		interaction[int(edge[i])][int(edge[i+1])]+=1
		interaction[int(edge[i+1])][int(edge[i])]+=1
		i+=3 
for i in range(len(interaction)):
	m=max(interaction[i])
	if m>100:
		for j in range(len(interaction)):
			interaction[i][j]/=m
	else:
		for j in range(len(interaction)):
			interaction[i][j]=0

with open('email-Eu-core-temporal.txt','r') as f:
	edge=f.read().split()
	i=0
	while i+1<len(edge):
		if interaction[int(edge[i])][int(edge[i+1])]>0:
			#print(interaction[int(edge[i])][int(edge[i+1])])
			G.add_edge(int(edge[i]),int(edge[i+1]),weight=interaction[int(edge[i])][int(edge[i+1])])
		i+=3 

nx.draw(G, with_labels=0, edge_color='b', node_color='g', node_size=10)

plt.show()