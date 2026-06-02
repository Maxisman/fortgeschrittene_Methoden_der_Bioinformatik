import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_node(1,color="b")
G.add_node(2,color="b")
G.add_node(3,color="r")
G.add_node(4,color="r")
G.add_node(5,color="g")
G.add_edges_from([(1,3),(1,4),(1,5),(2,3),(2,5), (3,1),(3,5),(4,1),(4,5),(5,2), (5,4)])

def is_color_sink_free(graph):
    colors = {}
    for node in graph:
        colors.update({graph.nodes[node]["color"]:False})

    for node in graph:
        for color in colors:
            colors[color] = False
        neighbors = graph.successors(node)
        
        for neighbor in neighbors:
            colors.update({G.nodes[neighbor]["color"]: True})
        
        for (color, value) in colors.items():
            if color != G.nodes[node]["color"] and value == False:
                return False
    return True

#G.remove_edge(5,4)
print(is_color_sink_free(G))

nx.draw(G, with_labels=True, node_color=["blue", "blue", "red", "red", "green"])
plt.show()