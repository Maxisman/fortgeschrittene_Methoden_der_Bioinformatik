import networkx as nx
import matplotlib.pyplot as plt

"""
# Informationen von Prof Wieseke:
G=nx.Graph() # Konstruktor fuer leeren Graphen
G.add_node("A") # Funktion um Knoten hinzuzufuegen
nx.draw(G) # In jupter funtioniert das automatisch, dass der Graph gezeigt wird. In einem python Skript muss man die grafische Darstellung
# mit plt.show() noch extra aufrufen
G.add_edge("A","B") # Knoten werden mein Kanten legen mit hinzugefuegt.
G.add_edge("A","C")
nx.draw(G, with_labels=True) # Gibt nicht immer zwangsweise dasselbe Bild, die Position der Knoten ist variable
nx.draw(G, with_labels=True)
G.remove_edge("A", "C")
nx.draw(G,pos,with_labels=True)
G.remove_node("C")
nx.draw(G,pos,with_labels=True)
"""
# Exercise 0.1
"""
Draw a graph on 5 vertices {a, b, c, d, e} with edges {ab, bc, cd, de, ae, bd}.
a) List the degree of each vertex.
(b) Find all paths from a to d.
(c) Is the graph connected?
(d) Find a subgraph that is a cycle.
(e) Find the induced subgraph on {a, b, d, e} — list its edges.

**💻 NetworkX exercise 0.1:** Build this graph in NetworkX. Use `G.degree()`, 
`nx.all_simple_paths()`, `nx.is_connected()`, and `G.subgraph()` to verify your paper answers."""
# create a graph
G=nx.Graph()
G.add_edge("a","b")
G.add_edge("b","c")
G.add_edge("c","d")
G.add_edge("d","e")
G.add_edge("a","e")
G.add_edge("b","d")
pos = nx.circular_layout(G)
nx.draw(G,pos,with_labels=True)

print(G.degree())
print(list(nx.all_simple_paths(G, source="a", target="d")))
print(nx.is_connected(G))
print(list(nx.cycle_basis(G)))
print(list(G.subgraph(["a","b","d","e"])))
plt.show()