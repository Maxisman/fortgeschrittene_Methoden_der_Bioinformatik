# WP0 Graph Theory
## 01 Graphs
### Video Reducible — "Introduction to Graph Theory: A Computer Science Perspective"
https://www.youtube.com/watch?v=LFKZLXVO-Dg
#### Layman's Definition of a Graph
Network that helps define and visualize relationships (edges) between various components (vertices or nodes)
A graph $G=(V,E)$ is a set of vertices $V$ and edges $E$ where each edge $(u,v)$ is a connection between vertices $u,v\in V$.
Edges are usually referred to as a pair of vertices. Vertices and Edges are presented using set notations.
**Neighbors**: vertices $u$ and $v$ are neighbors if an edge $(u,v)$ connects them (returns a set)
**Degree**: degree$(v)$ is equal to the number of edges connected to $v$ (returns a number)
**Path**: sequence of (usually unique) vertices connected by edges, **path length**: number of edges in a path
**Cycle**: path that starts and ends at the same vertex
**Connectivity**: two vertices are *connected* if a path exists between them. A graph is called *connected* when all vertices are connected.
**Connected Component**: a subset of vertices $V_i\subseteq V$ that is connected

#### Types of Graphs
**Undirected graph**: Edge $(u,v)$ implies $(v,u)$
**Directed graph**: Edges are unidirectional
- Directed cyclic graph: with cycle
- Directed acyclic graph: no cycle
**Weighted graph**: Edges have weights
**Trees**:
1. Connected and acyclic
2. Removing edge disconnects graph
3. adding edge creates a cycle

#### Graph representations 
Adjacency matrix
$$A_{ij}=\begin{cases}1\text{ for ege }(i,j)\\ 0\text{ otherwiese} \end{cases}
$$
Edge set:
List of edges inside a set
Adjacency List: One list per vertex, the list contains all the vertices that have a direct edge to that vertex

### Exercise 01:
Ich musste zusätzlich noch das package: `PyQt6` installieren
Ergebnis:
![[Graph_WP0_01.png|350]]

Das hat für mich noch nicht funktioniert:
Use `G.degree()`, `nx.all_simple_paths()`, `nx.is_connected()`, and `G.subgraph()` to verify your paper answers.
Die Funktionen scheinen was zu machen, aber es wird nicht geprinted. Funktioniert vielleicht besser in Jupyter?

## 02 Directed Graphs
### Video Reducible — "Depth First Search (DFS) Explained: Algorithm, Examples, and Code"
https://www.youtube.com/watch?v=PMMc4VsIacU

**Graph Traversal**: algorithm to visit every vertex of a graph
**DFS algorithm**: Continue looking for new vertices until you hit a dead end, then retrace steps until you find a new vertex.

**Directed Graph**: Each vertex has an **in-degree** (arrows coming in) and an **out-degree** (arrows going out). 
**Out-neighborhood**: N⁺(x) is the set of vertices that x points to. 
**Sink**: vertex with out-degree zero (no arrows leaving).
**Source**: vertex with in-degree 0 (no arrows arriving).
**Weakly connected**: Only connected if you ignore arrow directions
**Strongly connected**: A directed path between every ordered pair of vertices exists.

### Exercise 02:
Output from Code:
```
In Degree of directed Graph:
 [('1', 0), ('2', 2), ('3', 2), ('4', 1)]
Out Degree of directed Graph:
 [('1', 2), ('2', 1), ('3', 1), ('4', 1)]
Out-neighborhood of directed Graph:
 [['2', '3'], ['3'], ['4'], ['2']]
The graph is weakly connected:  True
The graph is strongly connected:  False
```

## 03 Colored Digraphs
Vertices: represent genes
colors: represent species
**vertex coloring**: σ assigns each vertex a color from a set S
**colored digraph G, σ)**: only has edges between vertices (genes) of *different* colors (species) (no connection between two genes from the same species).

**Properties of Best Match Graphs**:
- Sink-free: Each vertex has at least one outgoing edge
- Color-sink-free: Each gene of a species is connected to at least one other gene of a different species. Formally: for every vertex $x$ and every color $s \ne \sigma(x)$, there exists at least one edge from $x$ to some vertex of color $s$.
  This can be even stronger: at least one edge to every other species

Every best match graph is color-sink-free by construction (every gene has a closest relative in every other species).

## 04 Rooted trees as graphs
- **Paralogs:** Related genes separated by gene duplication within the **same** organism.
- **Orthologs:** Related genes separated by a speciation event; they exist in **different** organisms but perform similar roles.
- **Homologs:** The overarching, general term for any two genes derived from a common ancestral gene (this covers both paralogs and orthologs). 

## 05 Partial Orders and DAGs 
### Video Reducible — "Breadth First Search (BFS): Visualized and Explained"
https://www.youtube.com/watch?v=xlVX7dXLS64
First visit the vertices with distance 1 of a chosen vertex. Continue with visiting all vertices with distance two, and so on.

### Partial order
A partial order is
- reflexive: $x\le x$
- antisymmetric: $x\le y$ and $y\le x \Rightarrow x=y$ 
- transitive: $x\le y\le z \Rightarrow x\le z$
**Directed acyclic graph** (DAG): digraph with no directed cycles. Every DAG defines a partial order via reachability ($x\le y$ if there is a directed path from $x$ to $y$ or $x=y$). Phylogenetic trees are DAGs.

# WP 1 Best Match Graphs


Figure from [Geiß et al 2019](https://link.springer.com/article/10.1007/s00285-019-01332-9#Fig1)
![[Pasted image 20260526111110.png]]
An evolutionary scenario (left) consists of a gene tree whose inner vertices are marked by the event type ( for speciations, for gene duplications, and for gene loss) together with its embedding into a species tree (drawn as tube-like outline). All events are placed on a time axis. The middle panel shows the observable part of the gene tree ; it is obtained from the gene tree in the full evolutionary scenario by removing all leaves marked as loss events and suppression of all resulting degree two vertices. The r.h.s. panel shows the colored best match graph that is explained by . Directed arcs indicate the best match relation . Bi-directional best matches ( and ) are drawn as solid lines without arrow heads instead of pairs of arrows. Dotted circles collect sets of leaves that have the same in- and out-neighborhood. The corresponding arcs are shown only once.


# Function compute_bmg
Seems to be facing some weird difficulties with the color scheme of Asymetree:
![[Pasted image 20260615214625.png]]
For example, node 45 is a best match of node 42, although both have the same color, while 43 is no best match of 42. Need to fix code to run with Asymetree color scheme...
Seems that I've mostly fixed it, except that here for whatever reason:
![[Pasted image 20260615215628.png]]
40 did not pair with 39 as a best match. However, all other best matches are correct.

There seems to be a greater issue with the BMG function:
![[Pasted image 20260629141743.png]]
15 should only have 32 and 33 as purple and yellow best-matches, but has other nodes of that color as well. And 29 (in the middle) points to its own color...

Solved the problem!!!
The issue was how colors were represented using matplotlib (the colors in the graphs were just printed wrongly).
It's important to use this when printing the graphs: `node_color=[color] * len(node_list)`
![[BMG_finalized.png]]

# ToDos
- mathematical equation for difference between best match graph definitions (formal)
- translate lrt from asymetree to network x
-  create function to reduce bmg based on thinness classes (same edges in both directions)

# Vereinfachungen vor Ansetzen des Bic Cherry Algorithmus
Einführung von zwei neuen Regeln:
1. Gibt es eine node, die im BMG best match zu und von allen ist, häng sie direkt an die Wurzel des Bic Cherry und betrachte sie nicht weiter
2. Gibt es eine node, die keine eingehenden Kanten im BMG ist (von keinem best match ist) und mindestens eine andere node derselben Farbe, dann hänge sie direkt an die Wurzel des (Sub)Baumes

Demonstration alt gegen neu:
![[Screenshot From 2026-09-25 20-54-13.png]]

Neue Variante kann direkt den lrt raus geben
![[Screenshot From 2026-09-25 21-30-36.png]]

Neue Idee für zusätzliche Erweiterung:
Nachdem die erste Runde abgeschlossen ist, überprüfe ob sich die BMGs in zwei Gruppen aufteilen lassen (e.g. ist der Graph connected). Falls nicht, (wie es in diesem Fall der Fall wäre, nachdem die 3 entfernt wurde), dann teile an der Wurzel in die beiden Komponenten, und betrachte die Komponenten einzeln weiter.
![[Pasted image 20260925214128.png]]

Tatsächlich kann man das für einen ähnlichen Graph auch schon mit einem mehrfach loop lösen:
![[Screenshot From 2026-09-25 21-50-00.png]]