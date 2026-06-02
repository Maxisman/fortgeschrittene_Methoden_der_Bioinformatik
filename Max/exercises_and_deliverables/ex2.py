import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph([(1,2), (1,3), (2,3), (3,4), (4,2)])
for i in G:
    print(i)
    print(list(G.successors(i)))
    print(G.in_degree(i))
    print(str(G.out_degree(i)) + "\n")

nx.draw(G, with_labels=True)
plt.show()

print(nx.is_weakly_connected(G))
print(nx.is_strongly_connected(G))