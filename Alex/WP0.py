#%%
import networkx as nx
import matplotlib.pyplot as plt

verteces = ["a","b","c","d","e"]
edges = [("a","b"),("b","c"),("c","d"),("d","e"),("a","e"),("b","d")]

G = nx.Graph()
G.add_nodes_from(verteces)
G.add_edges_from(edges)

nx.draw(G,with_labels=True)
#%%
G.degree()
paths = nx.all_simple_paths(G,"a","e")
print(paths)


#%%
