git #%%
import networkx as nx
import matplotlib.pyplot as plt
#%%
#0.1

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
#0.2
V = [1,2,3,4]
E = [(1,2),(1,3),(2,3),(3,4),(4,2)]
G = nx.DiGraph()
G.add_nodes_from(V)
G.add_edges_from(E)
nx.draw(G,with_labels=True)

#%%
G.in_degree(1)
G.out_degree(1)
nx.is_weakly_connected(G)
#nx.is_strongly_connected(G)

#0.3
#%%
V = {"red":("a_1","a_2"),"blue":("b_1","b_2"),"green":("c_1",)}
E = (("a_1","b_1"),("b_1","a_1"),("a_1","c_1"),("c_1","a_2"),("a_2","c_1"),("a_2","b_2"),("b_2","a_2"),("c_1","b_2"))
G_colored = nx.DiGraph()
for key, value in V.items():
    G_colored.add_nodes_from(value, color=key)
G_colored.add_edges_from(E)
node_colors = [G_colored.nodes[v]["color"] for v in G_colored.nodes()]
nx.draw(G_colored,with_labels=True, node_color=node_colors)

#def is_color_sink_free(G):

all_colors = set(nx.get_node_attributes(G_colored, "color").values())

for node in G_colored.nodes():
    successor_colors = set()
    for vertex in G_colored.successors(node):
        successor_colors.add(G_colored.nodes[vertex]["color"])
    missing = all_colors - {G_colored.nodes[node]["color"]} - successor_colors
    if missing:
        print(f"{node} fails, missing edges to {missing}")
    else:
        print(f"{node} passes")
#%%
#0.4

Nodes = ["p","u","v","a_1","w","b_1","c_1","v","b_2","c_2"]
Edges = [("p","u"),("u","a_1"),("u","w"),("w","b_1"),("w","c_1"),("p","v"),("v","b_2"),("v","c_2")]
G = nx.DiGraph()
G.add_nodes_from(Nodes)
G.add_edges_from(Edges)
nx.draw(G)

def lca(T,root,x,y):
    path_x=nx.shortest_path(T,root,x)
    path_y=nx.shortest_path(T,root,y)

    for a,b, in zip(path_x,path_y):
        if a == b:
            ancestor = a
        else:
            break
    return ancestor
