# Workpackages: Best Match Graphs & Phylogenetic Networks

**Project basis:** Geiß et al., "Best Match Graphs" (J Math Biol, 2019) + Corrigendum by Schaller et al.; project brief `bmg1.1.1`; the [AsymmeTree](https://github.com/david-schaller/AsymmeTree) Python library by David Schaller.

**Total study time:** ~3 hours per person (WP0 shared by all ~1.5 h, then one specialist WP each ~1.5 h).

**How to use this:** Everyone works through WP0 first. Then each person takes exactly one of WP1–WP4. After individual study, a short sync session lets each person teach the others. The result: the full team can read both documents, use AsymmeTree, and start implementing the tasks in `bmg1.1.1`.

---

## WP0 — Graph Theory & Tree Foundations (everyone, ~1.5 h)

This package gives you the vocabulary you need for everything else. It's structured as a mini-curriculum: watch a video, read a short explanation, do a paper exercise, then do a coding exercise in NetworkX. By the end you should be able to draw and manipulate the kinds of graphs and trees that appear in both project documents without hesitation.

### Setup: Install NetworkX

Before you start, get your Python environment ready. You'll use it throughout.

```bash
pip install networkx matplotlib
```

```python
import networkx as nx
import matplotlib.pyplot as plt
```

---

### 0.1 — Graphs: Vertices, Edges, Neighborhoods (~15 min)

**📺 Watch:** "Graph Theory: An Introduction to Key Concepts" by Sarada Herke — first 10 minutes cover vertices, edges, degree, adjacency.
https://www.youtube.com/watch?v=HmQR8Xy9DeM

**The idea in a nutshell.** A **graph** G = (V, E) is a set V of **vertices** (dots) and a set E of **edges** (lines between pairs of dots). Two vertices connected by an edge are **adjacent** or **neighbors**. The **degree** of a vertex is how many edges touch it. A **path** is a sequence of distinct vertices where consecutive ones are connected by edges. A graph is **connected** if every pair of vertices is linked by some path. A maximal connected piece is a **connected component**.

A **subgraph** picks some vertices and some edges between them. An **induced subgraph** on a vertex set S keeps *all* edges of the original graph whose both endpoints are in S — you pick the vertices and the edges come for free.

A **bipartite graph** splits its vertices into two groups with every edge going between groups, never within. A **complete bipartite graph** K_{m,n} has *every* possible edge between the two groups.

**✏️ Paper exercise 0.1:** Draw a graph on 5 vertices {a, b, c, d, e} with edges {ab, bc, cd, de, ae, bd}. List the degree of each vertex. Find all paths from a to d. Is the graph connected? Find a subgraph that is a cycle. Find the induced subgraph on {a, b, d, e}.

**💻 NetworkX exercise 0.1:**

```python
# Build the graph from the paper exercise
G = nx.Graph()
G.add_edges_from([('a','b'), ('b','c'), ('c','d'), ('d','e'), ('a','e'), ('b','d')])

# Print the degree of each vertex
for v in G.nodes():
    print(f"deg({v}) = {G.degree(v)}")

# Find all simple paths from a to d
for path in nx.all_simple_paths(G, 'a', 'd'):
    print("Path a→d:", path)

# Check if connected
print("Connected?", nx.is_connected(G))

# Draw it
nx.draw(G, with_labels=True, node_color='lightblue', node_size=500)
plt.show()

# Extract the induced subgraph on {a, b, d, e}
H = G.subgraph(['a', 'b', 'd', 'e'])
print("Induced subgraph edges:", list(H.edges()))
nx.draw(H, with_labels=True, node_color='lightyellow', node_size=500)
plt.show()
```

---

### 0.2 — Directed Graphs (Digraphs) (~10 min)

**📺 Watch:** "NetworkX Crash Course — Graph Theory in Python" by NeuralNine (first 15 min, covers both undirected and directed graphs in NetworkX with live coding):
https://www.youtube.com/watch?v=VetBkjcm9Go

**The idea.** In a **directed graph** (digraph), every edge has a direction — it's an arrow from a start vertex to an end vertex. We write (x, y) or x → y for an arc from x to y. Each vertex now has an **in-degree** (arrows coming in) and an **out-degree** (arrows going out). The **out-neighborhood** N⁺(x) is the set of vertices that x points to. A vertex with out-degree 0 is a **sink** (no arrows leaving); one with in-degree 0 is a **source** (no arrows arriving).

A digraph is **weakly connected** if it's connected when you ignore arrow directions. It's **strongly connected** if there's a directed path between every ordered pair of vertices.

**✏️ Paper exercise 0.2:** Draw a digraph on 4 vertices {1, 2, 3, 4} with arcs {1→2, 1→3, 2→3, 3→4, 4→2}. For each vertex, list in-degree, out-degree, and out-neighborhood. Is vertex 1 a source? Is any vertex a sink? Is the digraph weakly connected? Strongly connected? (Hint: can you get from 3 back to 1?)

**💻 NetworkX exercise 0.2:**

```python
D = nx.DiGraph()
D.add_edges_from([(1,2), (1,3), (2,3), (3,4), (4,2)])

for v in D.nodes():
    print(f"Vertex {v}: in-deg={D.in_degree(v)}, out-deg={D.out_degree(v)}, "
          f"out-neighbors={list(D.successors(v))}")

print("Sources (in-degree 0):", [v for v in D.nodes() if D.in_degree(v) == 0])
print("Sinks (out-degree 0):", [v for v in D.nodes() if D.out_degree(v) == 0])
print("Weakly connected?", nx.is_weakly_connected(D))
print("Strongly connected?", nx.is_strongly_connected(D))

# Visualize with arrows
pos = nx.spring_layout(D, seed=42)
nx.draw(D, pos, with_labels=True, node_color='lightcoral', 
        node_size=500, arrows=True, arrowsize=20)
plt.show()
```

---

### 0.3 — Vertex-Colored Digraphs & Sink-Freeness (~10 min)

**No video — this is specific to our project.** Read this section carefully.

In this project, vertices represent **genes** and colors represent **species**. A **vertex coloring** σ assigns each vertex a color from a set S. A colored digraph (G, σ) only has arcs between vertices of *different* colors — you never point from a gene to another gene in the same species.

Key properties for BMGs:

- **Sink-free:** Every vertex has at least one outgoing arc.
- **Color-sink-free:** For every vertex x and every color s ≠ σ(x), there exists at least one arc from x to some vertex of color s. This is stronger — not just "at least one arrow out," but "at least one arrow to every other species."

Every best match graph is color-sink-free by construction (every gene has a closest relative in every other species).

**✏️ Paper exercise 0.3:** Consider 6 vertices with colors: a₁, a₂ (red), b₁, b₂ (blue), c₁ (green). Draw a digraph where every vertex has arcs to at least one vertex of every other color. Is your graph color-sink-free? Now remove the arc from c₁ to any blue vertex — is it still sink-free? Still color-sink-free?

**💻 NetworkX exercise 0.3:**

```python
# Build a colored digraph
G = nx.DiGraph()
# Add nodes with color attributes
colors = {'a1': 'red', 'a2': 'red', 'b1': 'blue', 'b2': 'blue', 'c1': 'green'}
for node, color in colors.items():
    G.add_node(node, color=color)

# Add arcs (only between different colors)
G.add_edges_from([
    ('a1','b1'), ('a1','c1'), ('a2','b2'), ('a2','c1'),
    ('b1','a1'), ('b1','c1'), ('b2','a2'), ('b2','c1'),
    ('c1','a1'), ('c1','b1')
])

# Check color-sink-free property
all_colors = set(colors.values())
for v in G.nodes():
    v_color = G.nodes[v]['color']
    reachable_colors = {G.nodes[u]['color'] for u in G.successors(v)}
    missing = all_colors - {v_color} - reachable_colors
    if missing:
        print(f"  {v} (color={v_color}) is MISSING arcs to colors: {missing}")
    else:
        print(f"  {v} (color={v_color}) ✓ has arcs to all other colors")

# Visualize with node colors
node_colors_list = [colors[v] for v in G.nodes()]
pos = nx.spring_layout(G, seed=7)
nx.draw(G, pos, with_labels=True, node_color=node_colors_list, 
        node_size=600, arrows=True, arrowsize=15, font_weight='bold')
plt.show()
```

---

### 0.4 — Rooted Trees, Children, Ancestors, lca (~20 min)

**📺 Watch:** Khan Academy — "Understanding and building phylogenetic trees" (~6 min, excellent biological motivation for rooted trees, ancestor relationships, and reading tree diagrams):
https://www.khanacademy.org/science/hs-biology/x4c673362230887ef:evolution-and-natural-selection/x4c673362230887ef:evidence-of-common-ancestry/v/understanding-and-building-phylogenetic-trees-or-cladograms

**📖 Then read:** This Nature Scitable primer (~10 min) — defines root, branch, node, clade, and last common ancestor with clear figures:
https://www.nature.com/scitable/topicpage/reading-a-phylogenetic-tree-the-meaning-of-41956/

**The idea.** A **tree** is a connected graph with no cycles. A **rooted tree** picks one vertex as the **root** (drawn at top). Every other vertex has a unique **parent** (next vertex toward root) and zero or more **children** (one step away from root). Vertices with no children are **leaves**; all others are **internal**.

The **ancestor order** ⪯: x ⪯ y means "y is on the path from x up to the root" (y is an ancestor of x). Leaves are minimal; the root is the unique maximum.

The **last common ancestor** lca(x, y) is the deepest vertex that is an ancestor of both x and y. In a tree, this is always unique.

A **phylogenetic tree** requires that every internal vertex has ≥ 2 children (no "pass-through" nodes with one child).

A **leaf-colored tree** (T, σ) assigns each leaf a color (= species). Multiple leaves can share a color — that represents gene duplication.

**✏️ Paper exercise 0.4:** Draw this tree:

```
         ρ
        / \
       u    v
      / \   |\ 
     a₁  w  b₂ c₂
        / \
       b₁  c₁
```

Colors: a₁ = red, b₁ = blue, b₂ = blue, c₁ = green, c₂ = green.

(a) List the parent and children of every vertex.
(b) Compute lca(a₁, b₁), lca(b₁, c₂), lca(a₁, c₁).
(c) Is it a phylogenetic tree? (Does every internal vertex have ≥ 2 children?)
(d) Which leaves are "closest relatives" of a₁ in terms of lca depth?

**💻 NetworkX exercise 0.4:**

```python
# Build a rooted tree as a DiGraph (edges point from parent to child)
T = nx.DiGraph()
T.add_edges_from([
    ('rho', 'u'), ('rho', 'v'),
    ('u', 'a1'), ('u', 'w'),
    ('w', 'b1'), ('w', 'c1'),
    ('v', 'b2'), ('v', 'c2')
])
leaves = ['a1', 'b1', 'b2', 'c1', 'c2']
sigma = {'a1': 'red', 'b1': 'blue', 'b2': 'blue', 'c1': 'green', 'c2': 'green'}

# Find parent and children of each vertex
for v in T.nodes():
    parents = list(T.predecessors(v))
    children = list(T.successors(v))
    print(f"{v}: parent={parents if parents else 'none (root)'}, children={children if children else '(leaf)'}")

# Compute lca by finding paths from root to each leaf
def lca(T, root, x, y):
    """Find last common ancestor by comparing root-to-leaf paths."""
    path_x = nx.shortest_path(T, root, x)
    path_y = nx.shortest_path(T, root, y)
    ancestor = root
    for a, b in zip(path_x, path_y):
        if a == b:
            ancestor = a
        else:
            break
    return ancestor

print("\nlca(a1, b1) =", lca(T, 'rho', 'a1', 'b1'))
print("lca(b1, c2) =", lca(T, 'rho', 'b1', 'c2'))
print("lca(a1, c1) =", lca(T, 'rho', 'a1', 'c1'))

# For each leaf, find its lca with a1 — lower = closer relative
for leaf in leaves:
    if leaf != 'a1':
        a = lca(T, 'rho', 'a1', leaf)
        depth = nx.shortest_path_length(T, 'rho', a)
        print(f"lca(a1, {leaf}) = {a} at depth {depth}")
```

---

### 0.5 — Partial Orders and DAGs (~10 min)

**📺 Watch:** "Directed Acyclic Graphs (1) — Introduction to DAGs" by Nick Huntington-Klein (~10 min, clear visual introduction to DAG structure, paths, and terminology):
https://www.youtube.com/watch?v=PiekvYYHeVQ

**The idea.** A **partial order** ⪯ on a set is reflexive (x ⪯ x), antisymmetric (x ⪯ y and y ⪯ x ⟹ x = y), and transitive (x ⪯ y ⪯ z ⟹ x ⪯ z). The ancestor order on a tree is a partial order. A **directed acyclic graph (DAG)** is a digraph with no directed cycles. Every DAG defines a partial order via reachability (x ⪯ y iff there's a directed path from x to y, or x = y).

The key connection to our project: **phylogenetic networks are DAGs**. Unlike trees, a vertex in a DAG can have multiple parents. This means two leaves can have *multiple* least common ancestors (a set, not a unique vertex). This is exactly what makes BMGs on networks harder than BMGs on trees.

A **topological ordering** of a DAG is a linear arrangement of vertices where every arrow goes "downhill." Every DAG has at least one.

**✏️ Paper exercise 0.5:** Draw a DAG on 5 vertices {ρ, u, v, x, y} with edges ρ→u, ρ→v, u→x, v→x, u→y. What is the partial order? (List all pairs a ⪯ b.) Does x have a unique parent? What are all common ancestors of x and y? Which is the "lowest"? (This previews LCA sets in networks.)

**💻 NetworkX exercise 0.5:**

```python
# Build a DAG (a simple network, not a tree — x has two parents)
N = nx.DiGraph()
N.add_edges_from([('rho','u'), ('rho','v'), ('u','x'), ('v','x'), ('u','y')])

# Check it's a DAG
print("Is DAG?", nx.is_directed_acyclic_graph(N))

# Topological order
print("Topological order:", list(nx.topological_sort(N)))

# Find all ancestors of x
ancestors_x = nx.ancestors(N, 'x')
print("Ancestors of x:", ancestors_x)

# Find all ancestors of y
ancestors_y = nx.ancestors(N, 'y')
print("Ancestors of y:", ancestors_y)

# Common ancestors of x and y
common = ancestors_x & ancestors_y
print("Common ancestors of x and y:", common)

# Parents of x (direct predecessors)
print("Parents of x:", list(N.predecessors('x')))  # should be [u, v] — two parents!

# Visualize
pos = {'rho': (1, 3), 'u': (0.5, 2), 'v': (1.5, 2), 'x': (1, 1), 'y': (0, 1)}
nx.draw(N, pos, with_labels=True, node_color='lightyellow', 
        node_size=600, arrows=True, arrowsize=20)
plt.show()
```

---

### 0.6 — Rooted Triples and the Aho Algorithm (~15 min)

**📖 Reference reading:** The PeerJ paper "Speeding up iterative applications of the Build supertree algorithm" has a clean description of how the Aho/BUILD algorithm works (Section "The Build Algorithm"):
https://peerj.com/articles/16624/ — read just the "Build Algorithm" section for a self-contained explanation with the cluster graph construction.

**The idea.** A **rooted triple** ab|c (read: "a and b together, separate from c") is the simplest possible statement about tree structure. It says lca(a, b) is strictly below lca(a, c) = lca(b, c). In picture form: ((a, b), c) — a tiny tree where a and b share a more recent ancestor than either shares with c.

Triples are the atoms of tree structure. From a best match graph, you extract:

- **Informative triples** R: if gene a sees b but not b' (same species as b), then ab|b' — a and b must be closer in any explaining tree.
- **Forbidden triples** F: triples that must *not* appear in the explaining tree.

A set of triples R is **consistent** if some tree displays all of them. The **Aho algorithm** (BUILD) checks this: construct a "cluster graph" where for each triple ab|c you add an undirected edge between a and b. If this graph is connected (one component), the triples are inconsistent. If it has multiple components, each component becomes a subtree, and you recurse. The result is the unique **least resolved tree**.

**✏️ Paper exercise 0.6:** Given leaves {a, b, c, d} and triples R = {ab|c, ab|d}:

(a) Draw the cluster graph (undirected, edge between the "close pair" of each triple).
(b) Find its connected components.
(c) What tree does the Aho algorithm produce? Draw it.
(d) Now add cd|a to R. Redraw the cluster graph. What happens? Is R still consistent?

**💻 NetworkX exercise 0.6:**

```python
# Implement a toy version of the Aho algorithm
def aho_build(leaves, triples):
    """
    Given a set of leaves and a list of triples (a, b, c) meaning ab|c,
    build the least resolved tree or return None if inconsistent.
    """
    if len(leaves) <= 2:
        return tuple(sorted(leaves))
    
    # Build cluster graph: undirected edge between a and b for each ab|c
    cluster = nx.Graph()
    cluster.add_nodes_from(leaves)
    relevant = [(a, b, c) for (a, b, c) in triples 
                if a in leaves and b in leaves and c in leaves]
    for (a, b, c) in relevant:
        cluster.add_edge(a, b)
    
    components = list(nx.connected_components(cluster))
    
    if len(components) == 1:
        print(f"  INCONSISTENT at leaves {sorted(leaves)}")
        return None  # all in one component → inconsistent
    
    print(f"  Leaves {sorted(leaves)} split into {[sorted(c) for c in components]}")
    
    # Recurse on each component
    children = []
    for comp in components:
        subtree = aho_build(comp, triples)
        if subtree is None:
            return None
        children.append(subtree)
    
    return tuple(children)

# Test 1: R = {ab|c, ab|d}
print("=== Test 1: R = {ab|c, ab|d} ===")
result = aho_build({'a','b','c','d'}, [('a','b','c'), ('a','b','d')])
print("Tree:", result, "\n")

# Test 2: add cd|a → R = {ab|c, ab|d, cd|a}
print("=== Test 2: R = {ab|c, ab|d, cd|a} ===")
result = aho_build({'a','b','c','d'}, [('a','b','c'), ('a','b','d'), ('c','d','a')])
print("Tree:", result, "\n")

# Test 3: inconsistent set
print("=== Test 3 (inconsistent): R = {ab|c, bc|a, ca|b} ===")
result = aho_build({'a','b','c'}, [('a','b','c'), ('b','c','a'), ('c','a','b')])
print("Tree:", result)
```

---

### 0.7 — Hierarchies (Nested Set Systems) (~5 min)

**Quick read, no video needed.** A **hierarchy** on a set L is a collection H of subsets of L where: (i) L ∈ H, (ii) {x} ∈ H for every x, and (iii) any two sets in H are either disjoint or one contains the other (no partial overlaps). Every rooted tree defines a hierarchy: each internal vertex v corresponds to the set of all leaves below v. Conversely, every hierarchy can be drawn as a rooted tree.

This matters because the BMG characterization uses hierarchies built from "reachable sets" in the graph — the hierarchy *is* the tree.

**✏️ Paper exercise 0.7:** For the tree in exercise 0.4, list the hierarchy H (the set of leaf-sets below each vertex). Verify the no-partial-overlap property.

---

### 0.8 — Capstone: Build a BMG by Hand (~15 min)

This ties everything together by walking through the central construction of the project: going from a leaf-colored tree to its best match graph.

**✏️ + 💻 Combined exercise 0.8:** Use the tree from exercise 0.4:

```
         ρ
        / \
       u    v
      / \   |\ 
     a₁  w  b₂ c₂
        / \
       b₁  c₁
```

σ: a₁=red, b₁=blue, b₂=blue, c₁=green, c₂=green.

**(a) On paper:** For each leaf x and each color s ≠ σ(x), find the best match(es). The rule: y is a best match of x in species s if lca(x, y) ⪯ lca(x, y') for all y' with σ(y') = s. Work it out systematically — start with a₁'s best matches in blue (compare lca(a₁, b₁) vs lca(a₁, b₂)), then a₁ in green, then b₁ in red, b₁ in green, etc. Draw the resulting digraph.

**(b) In NetworkX:** Implement the computation and verify:

```python
T = nx.DiGraph()
T.add_edges_from([
    ('rho', 'u'), ('rho', 'v'),
    ('u', 'a1'), ('u', 'w'),
    ('w', 'b1'), ('w', 'c1'),
    ('v', 'b2'), ('v', 'c2')
])
sigma = {'a1': 'red', 'b1': 'blue', 'b2': 'blue', 'c1': 'green', 'c2': 'green'}
leaves = list(sigma.keys())
root = 'rho'

def lca(T, root, x, y):
    path_x = nx.shortest_path(T, root, x)
    path_y = nx.shortest_path(T, root, y)
    ancestor = root
    for a, b in zip(path_x, path_y):
        if a == b:
            ancestor = a
        else:
            break
    return ancestor

def lca_depth(T, root, x, y):
    return nx.shortest_path_length(T, root, lca(T, root, x, y))

# Build the BMG
BMG = nx.DiGraph()
for node, color in sigma.items():
    BMG.add_node(node, color=color)

all_colors = set(sigma.values())
for x in leaves:
    for s in all_colors:
        if s == sigma[x]:
            continue
        candidates = [y for y in leaves if sigma[y] == s]
        best_depth = max(lca_depth(T, root, x, y) for y in candidates)
        for y in candidates:
            if lca_depth(T, root, x, y) == best_depth:
                BMG.add_edge(x, y)

print("BMG arcs:")
for (u, v) in BMG.edges():
    print(f"  {u} ({sigma[u]}) → {v} ({sigma[v]})")

# Verify color-sink-free
for x in leaves:
    out_colors = {sigma[y] for y in BMG.successors(x)}
    expected = all_colors - {sigma[x]}
    assert out_colors == expected, f"{x} missing arcs to {expected - out_colors}"
print("\n✓ BMG is color-sink-free")
```

**(c) Extract informative triples** and compare with your paper work:

```python
R = []
for a in leaves:
    for s in all_colors:
        if s == sigma[a]:
            continue
        same_color = [y for y in leaves if sigma[y] == s]
        if len(same_color) < 2:
            continue
        for b in same_color:
            for b_prime in same_color:
                if b == b_prime:
                    continue
                if BMG.has_edge(a, b) and not BMG.has_edge(a, b_prime):
                    R.append((a, b, b_prime))
                    print(f"  Informative triple: {a}{b}|{b_prime}")
```

If you got through all of WP0 — you have all the vocabulary. Now pick your specialist workpackage.

---

## WP1 — Best Match Graphs: Theory & Characterization (Person 1, ~1.5 h)

**Goal:** Understand the mathematical characterization of BMGs and the recognition algorithm. After this WP you can explain the main theorem of the Geiß et al. paper and walk through Algorithm 1.

### 1.1 Definition of best matches (20 min)

Read Section 1 and Definitions 1–2 of the Geiß et al. paper. You already built a BMG by hand in WP0 exercise 0.8 — now read the formal definition and verify your hand computation matches. Key subtlety: if two genes y and y' in the same species are equidistant from x (same lca depth), *both* are best matches — the relation is not unique per species.

### 1.2 The 2-colored case (25 min)

Read Section 3, focusing on Theorem 6 (three conditions characterizing 2-cBMGs).

The paper introduces ∼• ("thinness classes") — vertices are equivalent if they have identical out-neighborhoods and the same color. The characterization uses these collapsed classes. The 2-color case is the building block for everything else.

The key outputs from a 2-cBMG are **informative triples** R and **forbidden triples** F. You already extracted R in exercise 0.8(c). Read how F is defined and why both sets matter.

### 1.3 General n-colored characterization (20 min)

Read Section 4, Theorem 14, and Corollary 5. The punchline: a connected colored digraph (G, σ) is an n-cBMG iff every 2-color induced subgraph is a 2-cBMG *and* the union of all informative triples is consistent. The Aho tree of that union is the unique least resolved tree. This reduces the multi-color problem to pairwise checks plus one global consistency check.

### 1.4 The recognition algorithm (15 min)

Read Section 5 and Algorithms 1–3. Algorithm 1 implements the characterization: decompose into connected components → 2-color subgraphs → check each → build supertree. Complexity: O(|L|³) time, O(|L|²) space. Two sub-algorithms compute the least resolved tree for 2-cBMGs: Algorithm 2 (hierarchy from reachable sets) and Algorithm 3 (Aho tree from triples).

### 1.5 The Corrigendum + Reciprocal BMGs (10 min)

Read the Corrigendum by Schaller et al.: the sink-free assumption must be stated explicitly; Theorem 9 needs an extra condition. Then skim Section 6 on reciprocal BMGs: every 2-cRBMG is a disjoint union of complete bipartite graphs, but the 3-color case is already harder (Figure 13).

### Deliverable

Prepare a 10-minute explanation: definition of BMG, the triple-based characterization, how Algorithm 1 works, and your worked example from WP0 exercise 0.8 as illustration.

---

## WP2 — The AsymmeTree Library: Generating & Using Trees (Person 2, ~1.5 h)

**Goal:** Install AsymmeTree, generate trees, extract BMGs, and understand the data structures well enough to modify trees programmatically. You are the team's tool expert.

### 2.1 Installation and first steps (15 min)

```bash
pip install asymmetree
```

Browse the [documentation](https://david-schaller.github.io/AsymmeTree/) and the `examples/` folder on GitHub. Run an example script to verify installation.

### 2.2 Core simulation pipeline (25 min)

AsymmeTree simulates evolution in stages: species tree (birth-death process) → gene tree evolution (duplications, losses, optional HGT) → observable gene tree (pruning lost genes yields (T, σ)).

Study the `asymmetree.treeevolve` module. Map out: how species trees are generated, how gene family evolution is parameterized (duplication/loss rates), and how the observable tree is extracted.

### 2.3 Extracting best match graphs (20 min)

From (T, σ), learn how the library computes the BMG (lca-based forward direction). Also find how to extract: orthologous pairs, informative/forbidden triples, and the least resolved tree. These are the inputs WP3's algorithm will need.

### 2.4 Data structures and Task (0) (20 min)

Understand how trees are stored internally (node/edge attributes, root, σ-map, parent/child access). Then read Task (0) from the project brief — generating networks by inserting hybridization vertices into trees. Sketch pseudocode: pick two random edges, subdivide each (insert new internal vertex), connect them with a directed edge. Think about maintaining the DAG property.

### 2.5 Visualization (10 min)

Learn AsymmeTree's matplotlib-based tree plots: species trees, gene trees, embedded trees.

### Deliverable

A runnable Jupyter notebook or script: generate a species tree, evolve a gene family, extract the observable tree and its BMG, print the triples, show the visualization. The others should be able to run this.

---

## WP3 — The BIC-Cherry + Expansion Algorithm (Person 3, ~1.5 h)

**Goal:** Understand the construction that turns any colored digraph with the sicor-in-hub property into an explaining network. You will implement this.

### 3.1 When trees aren't enough (10 min)

Re-read the "Phylogenetic Networks" section of `bmg1.1.1`. (G, σ) is a **network-BMG** iff it has the **sicor-in-hub property**: every single-color-representative is an in-hub. This is much weaker than being a tree-BMG.

### 3.2 Best matches in networks: two definitions (25 min)

Read the "Two definitions" section carefully. In a network, LCA(x, y) is a *set*.

- **Strict:** y is best match of x if no alternative y' has a strictly closer ancestor in *every* sense.
- **Weak:** y is best match of x if at least one of their common ancestors is among the globally lowest.

For trees they coincide. For networks they can differ. Tasks 1(d) and Objective 1(a) investigate this.

### 3.3 The BIC-cherry + expansion construction (30 min)

**Phase 1 — BIC-cherry network:** Root ρ, all leaves L, and for every differently-colored pair x, y an intermediate vertex p_{xy} (child of ρ, parent of both x and y).

**Phase 2 — Expansion:** For each missing edge (x, y) ∉ E(G), perform [xy : xy'] — insert vertex q_{xz} as child of p_{xy} and parent of both x and z (where z has σ(z) = σ(y), z ≠ y).

Work a concrete example: 3 vertices, 2 colors, one arc missing. Build the BIC-cherry network, perform the expansion, verify the result's BMG matches the input.

### 3.4 Variant + Testing strategy (25 min)

Task 1(b): restrict expansions to arcs in (G, σ). Task 1(c,d): testing — unit tests on small examples, round-trip tests (generate network → compute weak BMG → run algorithm → check), minimal counterexample search.

### Deliverable

Explain the algorithm with a worked 3-color, 5-vertex example. Draw the BIC-cherry network, show one expansion, verify. Clarify strict vs. weak best matches with an example.

---

## WP4 — Network Simplification & Editing (Person 4, ~1.5 h)

**Goal:** Understand editing operations for simplifying networks and design heuristics for good edit sequences.

### 4.1 The simplification problem (15 min)

Read Tasks 2(a)–(f). The BIC-cherry output is correct but complex — often far from a tree even for tree-BMGs. Goal: stepwise editing to become more tree-like while preserving the (weak) BMG.

### 4.2 Network editing operations (30 min)

Three basic moves (from `bmg1.1.1` Task 2c):

- **Pull up:** vertex v with parent u, u with parent w → make v a direct child of w. Flattens the network.
- **Pull down:** reverse — move a child to a lower level.
- **Remove redundant vertices:** merge vertices with identical parent/child sets; suppress single-child internal vertices.

Each move requires recomputing the BMG to check preservation.

### 4.3 DAG operations you need (15 min)

Brush up on topological ordering, reachability, transitive reduction. Editing changes ⪯, which changes lca sets, which changes best matches non-obviously.

### 4.4 Heuristic design (30 min)

Strategies for Tasks 2(d)–(f):

- **Greedy:** try every single move, keep the one reducing reticulation vertices most while preserving the BMG.
- **Beam search:** keep top-k candidates per round.
- **Target-guided:** when T* is known, measure distance (reticulation count, edge symmetric difference) and move toward it.
- **Failure analysis (Task 2f, 3):** find minimal stuck cases, determine *why* — are moves too local? Need to temporarily worsen the metric?

### Deliverable

Present the three editing operations with a small network (before/after drawings). One case where 2–3 edits reach a tree, one where a single edit breaks the BMG. Propose your heuristic and distance metric.

---

## How the WPs fit together

```
WP0 (everyone, 1.5 h)
 │  graphs → digraphs → colored digraphs → trees → lca → DAGs → triples → BMG by hand
 │
 ├── WP1 (1.5 h): Theory     → knows WHAT a BMG is and how to recognize one
 ├── WP2 (1.5 h): Tooling    → knows HOW to generate data and use AsymmeTree
 ├── WP3 (1.5 h): Algorithm  → knows HOW to build explaining networks
 └── WP4 (1.5 h): Editing    → knows HOW to simplify networks toward trees
```

Overlaps are intentional: WP1 ∩ WP3 share the BMG definition (trees vs. networks). WP2 ∩ WP4 share data structure manipulation. WP2 ∩ WP3 share the testing pipeline. Every pair has common ground.

### Sync session after individual study

Each person gives a ~10-minute presentation of their deliverable. Total: ~40 min plus discussion. After this, everyone can read both papers and tackle the full task list.
