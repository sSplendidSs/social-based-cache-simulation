import networkx as nx
import matplotlib.pyplot as plt
people=146
G = nx.Graph()
#G.add_nodes_from(H)
for i in range(people):
	G.add_node(i)

with open('CollegeMsg.txt','r') as f:
	edge=f.read().split()
	i=0
	while i+1<len(edge):
		G.add_edge(int(edge[i]),int(edge[i+1]))
		i+=3 
print(nx.average_clustering(G))