
```python
# NetworkX
#NetworkX Docs: https://networkx.org/documentation/stable/reference/index.html

#Erzeugen und Zeichens eines einfachen Graphen

G=nx.Graph() # Konstruktor fuer leeren Graphen
G.add_node("A") # Funktion um Knoten hinzuzufuegen
nx.draw(G) # In jupter funtioniert das automatisch, dass der Graph gezeigt wird. In einem python Skript muss man die grafische Darstellung
# mit plt.show() noch extra aufrufen

#Hinzufuegen von Kanten:
#Beim Hinzufuegen von Kanten werden die jeweiligen Knoten mit erzeugt.
G = nx.Graph()
G.add_edge("A","B") # Knoten werden mein Kanten legen mit hinzugefuegt.
G.add_edge("A","C")
nx.draw(G, with_labels=True) # Gibt nicht immer zwangsweise dasselbe Bild, die Position der Knoten ist variable

#Festlegen der Position von Knoten

pos = {"A":(1,1), "B":(0,0), "C":(2,0)} # dict gibt Knoten als key und Position als value
nx.draw(G,pos,with_labels=True) # Funktion bekommt Graph, dict und labels-Bool uebergeben

#Knoten-Attribute: Die Positionen (und auch andere Informationen �ber die Knoten) koennen als Attribute im Grapgen selbst gespeichert und wieder ausgelesen werden.

pos = {"B":(1,1), "C":(0,0), "A":(2,0)}
nx.set_node_attributes(G, pos, "pos") # beliebe Attribute, hier position, koennen auch direkt mit den Knoten im Graph verknuepft werden
print(G.nodes(data=True))

pos = nx.get_node_attributes(G, 'pos') # Attribute koennen ueber ihren Namen (hier pos) wieder herausgezogen werden
nx.draw(G,pos,with_labels=True) # herausgezogenes dict hier verwendet zum Zeichnen

# Kanten-Attribute: Wie Knoten koennen auch Kanten Attribute besitzen (z.B. Kantengewichte). Diese koennen auch gleich beim Hinzufoegen mit angegeben werden.

G=nx.Graph()
G.add_node("A", pos=(0,0)) # Attribute koennen auch direkt beim erstellen der nodes mit angegeben werden
G.add_node("B", pos=(2,0))
G.add_node("C", pos=(1,1))

G.add_edge("A","B",weight=1) # weights koennen als Attribute an Kanten gespeichert werden
G.add_edge("A","C",weight=2)

print(G.nodes(data=True))
print(G.edges(data=True))

# Aendern von Attributen

G.nodes["C"]["pos"] = (2,1) # indexieren von nodes mit eckigen Klammern
G.edges[("A", "B")]["weight"] = 10 # indizieren von edges mit tuple der verknuepften Knoten
print(G.nodes(data=True))
print(G.edges(data=True))

# Anzeigen von Kantenattributen im Layout: Dafuer benoetigen wir ein Dictionary mit den Kanten (Tuple der Knotennamen) als keys und den anzugeigenden Werten als values 

pos = nx.get_node_attributes(G, 'pos')
# das Prinzip von List Comprehension funktioniert auch fuer Dictionaries!!! 
edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)} # key soll das tuple aus u,v sein, value soll value
# des Attribute Dict sein
print(edge_labels)
nx.draw(G,pos,with_labels=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) #Funktion fuer die Kantenbeschriftung, nachdem der Graph gezeichnet wurde

#Knoten und Kanten loeschen

G.remove_edge("A", "C")
nx.draw(G,pos,with_labels=True)

G.remove_node("C")
nx.draw(G,pos,with_labels=True)

# Layout-Algorithmen

G=nx.Graph()
G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(3,4)
G.add_edge(4,5)
G.add_edge(1,4)
G.add_edge(1,3)
G.add_edge(2,5)

pos = nx.spring_layout(G)
#This algorithm uses a force-directed approach to layout the nodes. Nodes that are connected by edges are attracted to each other, while nodes that are not connected are repelled. The algorithm tries to minimize the energy of the system by adjusting the position of the nodes.

pos = nx.circular_layout(G)
#This algorithm positions the nodes evenly around a circle.

pos = nx.spectral_layout(G)
#This algorithm uses the eigenvectors of the graph's adjacency matrix to position the nodes. The eigenvectors are used to project the nodes into a lower-dimensional space, and the positions of the nodes are then determined by optimizing a cost function.

pos = nx.random_layout(G)
#This algorithm positions the nodes randomly in a given bounding box.

pos = nx.shell_layout(G)
#This algorithm positions the nodes in concentric circles or shells, with nodes in the same shell having the same distance to the center.

pos = nx.kamada_kawai_layout(G)
#This algorithm uses an iterative optimization approach to layout the nodes. The algorithm tries to minimize the stress of the system by adjusting the position of the nodes.

pos = nx.fruchterman_reingold_layout(G)
#This algorithm is a variation of the nx.spring_layout() algorithm, and also uses a force-directed approach to layout the nodes.

nx.draw(G,pos,with_labels=True)


# Gerichtete Graphen (DiGraphs)

diG=nx.DiGraph()
diG.add_node("A", pos=(1,1))
diG.add_node("B", pos=(0,0))
diG.add_node("C", pos=(2,0))

diG.add_edge("A","B")
diG.add_edge("B","A") # muss explizit hinzugefuegt werden, dass diese Kante in beide Richtungen geht.
diG.add_edge("A","C")

pos = nx.get_node_attributes(diG, 'pos')
nx.draw(diG,pos,with_labels=True)

# Import Graph from egde list

file = open("edgelist.txt", "w") #schreibt das als neue text Datei
edge_list="""
A B
A C
B D
C D
D E
"""
file.write(edge_list)
file.close()

G = nx.read_edgelist('edgelist.txt') # liest die gerade geschriebene text Datei
nx.draw(G,with_labels=True)

# Import graph from adjacency matrix

import numpy as np
import networkx as nx
G_mat = np.array([[0, 2, 1, 10, 0, 3, 0, 0, 0, 0],
                  [1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
                  [0, 0, 0, 5, 0, 0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 3, 0]])
G_mat

G = nx.DiGraph(G_mat)
print(G.edges(data=True))
pos = nx.circular_layout(G)
nx.draw_networkx(G,pos)
edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) # Kann Kantengewichte bei gerichteten Graphen nicht darstellen (erster 
# Eintrag wird ueberschrieben)
```
