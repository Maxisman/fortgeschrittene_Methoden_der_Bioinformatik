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

"""Paper exercise 0.2:** Draw a digraph on 4 vertices {1, 2, 3, 4} with arcs {1→2, 1→3, 2→3, 3→4, 4→2}.

(a) For each vertex, list in-degree, out-degree, and out-neighborhood.
(b) Is vertex 1 a source? Is any vertex a sink?
(c) Is the digraph weakly connected? Strongly connected? (Hint: can you get from 3 back to 1?)
Build this digraph using `nx.DiGraph()`. Use `D.in_degree()`, `D.out_degree()`, `D.successors()`, 
`nx.is_weakly_connected()`, and `nx.is_strongly_connected()` to verify your answers.
"""
diG=nx.DiGraph()
diG.add_edge("1","2")
diG.add_edge("1","3")
diG.add_edge("2","3")
diG.add_edge("3","4")
diG.add_edge("4","2")
pos = nx.circular_layout(diG)
nx.draw(diG, pos, with_labels=True)

print("In Degree of directed Graph:\n", diG.in_degree())
print("Out Degree of directed Graph:\n", diG.out_degree())
print("Out-neighborhood of directed Graph:\n", [list(diG.successors(n)) for n in list(diG)])
print("The graph is weakly connected: ", nx.is_weakly_connected(diG))
print("The graph is strongly connected: ",nx.is_strongly_connected(diG))

plt.show()

"""
**✏️ Paper exercise 0.3:** Consider 6 vertices with colors: a₁, a₂ (red), b₁, b₂ (blue), c₁ (green).

(a) Draw a digraph where every vertex has arcs to at least one vertex of every other color. Verify it's color-sink-free.
(b) Now remove the arc from c₁ to any blue vertex. Is it still sink-free? Still color-sink-free?

**💻 NetworkX exercise 0.3:** Build a colored digraph in NetworkX. Store colors as node attributes using
 `G.add_node(name, color='red')`. Write a function `is_color_sink_free(G)` that checks the property: 
 for every vertex x and every color s ≠ σ(x), there's at least one arc from x to a vertex of color s.

*Hint:* Use `G.nodes[v]['color']` to read attributes. `G.successors(v)` gives out-neighbors.
"""
colors = ['red', 'blue', 'green']
diG_color = nx.DiGraph()
diG_color.add_node("a1", color=colors[0])
diG_color.add_node("a2", color=colors[0])
diG_color.add_node("b1", color=colors[1])
diG_color.add_node("b2", color=colors[1])
diG_color.add_node("c1", color=colors[2])
diG_color.add_edge("a1", "b1")
diG_color.add_edge("b1", "c1")
diG_color.add_edge("b2", "c1")
diG_color.add_edge("c1", "b1")
diG_color.add_edge("b1", "a1")
diG_color.add_edge("b2", "a2")
diG_color.add_edge("a2", "b2")
diG_color.add_edge("a1", "b2")
diG_color.add_edge("c1", "a1")
diG_color.add_edge("a1", "c1")
diG_color.add_edge("a2", "c1")


pos = nx.circular_layout(diG_color)
#nx.draw_networkx_nodes(diG_color, pos, nodelist=["a1", "a2"], node_color="tab:red")
#nx.draw_networkx_nodes(diG_color, pos, nodelist=["b1", "b2"], node_color="tab:blue")
#nx.draw_networkx_nodes(diG_color, pos, nodelist=["c1"], node_color="tab:green")
nx.draw(diG_color, pos, nodelist=["a1", "a2"], node_color="tab:red", with_labels=True)
nx.draw(diG_color, pos, nodelist=["b1", "b2"], node_color="tab:blue", with_labels=True)
nx.draw(diG_color, pos, nodelist=["c1"], node_color="tab:green", with_labels=True)

# Function to test if graph is color-sink-free:
def is_color_sink_free(G, colours):
    # initiate output:
    is_cs_free = []
    # iterate through nodes in G:
    for v in list(G):
        # access the color of v:
        color_v = G.nodes[v]['color']
        # remove node color from the list of colors to find
        find_color = colours.copy()
        find_color.remove(color_v)
        # access out-neighborhood of v
        for n in list(G.successors(v)):
            color_n = G.nodes[n]['color']
            try:
                find_color.remove(color_n)
            except ValueError:
                continue

        # check if find_color is an empty list
        if not find_color:
            is_cs_free.append(True)
        else:
            is_cs_free.append(False)

    # Check if there are only True entries in is_cs_free
    if False in is_cs_free:
        return False
    else:
        return True


print("Is the graph color-sink-free? ", is_color_sink_free(diG_color, colors))

plt.show()

# remove edges from c1 to all blue vertices
diG_color.remove_edge("c1", "b1")

nx.draw(diG_color, pos, nodelist=["a1", "a2"], node_color="tab:red", with_labels=True)
nx.draw(diG_color, pos, nodelist=["b1", "b2"], node_color="tab:blue", with_labels=True)
nx.draw(diG_color, pos, nodelist=["c1"], node_color="tab:green", with_labels=True)

print("Is the graph still color-sink-free? ", is_color_sink_free(diG_color, colors))
plt.show()

# Excercise 4
"""
 Paper exercise 0.4:** Consider this gene tree with species map:


         ρ
        / \
       u    v
      / \   |\ 
     a₁  w  b₂ c₂
        / \
       b₁  c₁

σ: a₁ = red, b₁ = blue, b₂ = blue, c₁ = green, c₂ = green. 
"""
diG_root = nx.DiGraph()
diG_root.add_node("a1", color='red')
diG_root.add_node("b1", color='blue')
diG_root.add_node("b2", color='blue')
diG_root.add_node("c1", color='green')
diG_root.add_node("c2", color='green')
nx.add_path(diG_root, ["p","u","w"])
nx.add_path(diG_root, ["p","v"])
diG_root.add_edge("u", "a1")
diG_root.add_edge("w", "b1")
diG_root.add_edge("w", "c1")
diG_root.add_edge("v", "b2")
diG_root.add_edge("v", "c2")
#nx.add_path(diG, ["p","u","a1"])
#nx.add_path(diG, ["p","u","w","b1"])
#nx.add_path(diG, ["p","u","w","c1"])
#nx.add_path(diG, ["p","v","b2"])
#nx.add_path(diG, ["p","v","c2"])

pos = nx.spring_layout(diG_root)
nx.draw(diG_root, pos, nodelist=["a1"], node_color="tab:red", with_labels=True)
nx.draw(diG_root, pos, nodelist=["b1", "b2"], node_color="tab:blue", with_labels=True)
nx.draw(diG_root, pos, nodelist=["c1", "c2"], node_color="tab:green", with_labels=True)
print("The lowest common ancestor of a1 and b1 is: ", nx.lowest_common_ancestor(diG_root, "a1", "b1"))
print("The lowest common ancestor of a1 and b2 is: ", nx.lowest_common_ancestor(diG_root, "a1", "b2"))

plt.show()

# Exercise 5

G_05 = nx.DiGraph([("p", "u"), ("p", "v"),("u", "x"), ("u", "y"), ("v", "x")])
pos = nx.spring_layout(G_05)
nx.draw(G_05, pos, with_labels=True)
print("Is the graph a DAG? ", nx.is_directed_acyclic_graph(G_05))
print("Topological ordering: ", list(nx.topological_sort(G_05)))
print("Parents of x: ", list(G_05.predecessors("x")))

plt.show()