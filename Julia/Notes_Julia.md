# WP0 Graph Theory
## Video Reducible — "Introduction to Graph Theory: A Computer Science Perspective"
https://www.youtube.com/watch?v=LFKZLXVO-Dg
### Layman's Definition of a Graph
Network that helps define and visualize relationships (edges) between various components (vertices or nodes)
A graph $G=(V,E)$ is a set of vertices $V$ and edges $E$ where each edge $(u,v)$ is a connection between vertices $u,v\in V$.
Edges are usually referred to as a pair of vertices. Vertices and Edges are presented using set notations.
**Neighbors**: vertices $u$ and $v$ are neighbors if an edge $(u,v)$ connects them (returns a set)
**Degree**: degree$(v)$ is equal to the number of edges connected to $v$ (returns a number)
**Path**: sequence of (usually unique) vertices connected by edges, **path length**: number of edges in a path
**Cycle**: path that starts and ends at the same vertex
**Connectivity**: two vertices are *connected* if a path exists between them. A graph is called *connected* when all vertices are connected.
**Connected Component**: a subset of vertices $V_i\subseteq V$ that is connected

### Types of Graphs
**Undirected graph**: Edge $(u,v)$ implies $(v,u)$
**Directed graph**: Edges are unidirectional
- Directed cyclic graph: with cycle
- Directed acyclic graph: no cycle
**Weighted graph**: Edges have weights
**Trees**:
1. Connected and acyclic
2. Removing edge disconnects graph
3. adding edge creates a cycle

Exercise 01:
Ich musste zusätzlich noch das package: `PyQt6` installieren
Ergebnis:
![[Graph_WP0_01.png|350]]

Das hat für mich noch nicht funktioniert:
Use `G.degree()`, `nx.all_simple_paths()`, `nx.is_connected()`, and `G.subgraph()` to verify your paper answers.
Die Funktionen scheinen was zu machen, aber es wird nicht geprinted. Funktioniert vielleicht besser in Jupyter?