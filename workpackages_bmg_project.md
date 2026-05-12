# Workpackages: Best Match Graphs & Phylogenetic Networks

**Project basis:** Geiß et al., "Best Match Graphs" (J Math Biol, 2019) + Corrigendum by Schaller et al.; project brief `bmg1.1.1`; the [AsymmeTree](https://github.com/david-schaller/AsymmeTree) Python library by David Schaller.

**Total study time:** ~3 hours per person (WP0 shared by all ~1.5 h, then one specialist WP each ~1.5 h).

**How to use this:** Everyone works through WP0 first. Then each person takes exactly one of WP1–WP4. After individual study, a short sync session lets each person teach the others. The result: the full team can read both documents, use AsymmeTree, and start implementing the tasks in `bmg1.1.1`.

**Important:** The exercises ask you to write code yourself. Descriptions, hints, and function signatures are provided — but not the implementations. Try hard before looking at the solutions appendix at the very end of this document.

---

## WP0 — Graph Theory & Tree Foundations (everyone, ~1.5 h)

This package gives you the vocabulary you need for everything else. It's structured as a mini-curriculum: watch a video, read a short explanation, do a paper exercise, then do a coding exercise in NetworkX.

### Setup: Install NetworkX

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

**✏️ Paper exercise 0.1:** Draw a graph on 5 vertices {a, b, c, d, e} with edges {ab, bc, cd, de, ae, bd}.

(a) List the degree of each vertex.
(b) Find all paths from a to d.
(c) Is the graph connected?
(d) Find a subgraph that is a cycle.
(e) Find the induced subgraph on {a, b, d, e} — list its edges.

**💻 NetworkX exercise 0.1:** Build this graph in NetworkX. Use `G.degree()`, `nx.all_simple_paths()`, `nx.is_connected()`, and `G.subgraph()` to verify your paper answers.

*Hint:* `nx.Graph()` creates an undirected graph. `add_edges_from()` takes a list of tuples. `nx.draw(G, with_labels=True)` visualizes it.

---

### 0.2 — Directed Graphs (Digraphs) (~10 min)

**📺 Watch:** "NetworkX Crash Course — Graph Theory in Python" by NeuralNine (first 15 min, covers both undirected and directed graphs in NetworkX with live coding):
https://www.youtube.com/watch?v=VetBkjcm9Go

**The idea.** In a **directed graph** (digraph), every edge has a direction — it's an arrow from a start vertex to an end vertex. We write (x, y) or x → y for an arc from x to y. Each vertex now has an **in-degree** (arrows coming in) and an **out-degree** (arrows going out). The **out-neighborhood** N⁺(x) is the set of vertices that x points to. A vertex with out-degree 0 is a **sink** (no arrows leaving); one with in-degree 0 is a **source** (no arrows arriving).

A digraph is **weakly connected** if it's connected when you ignore arrow directions. It's **strongly connected** if there's a directed path between every ordered pair of vertices.

**✏️ Paper exercise 0.2:** Draw a digraph on 4 vertices {1, 2, 3, 4} with arcs {1→2, 1→3, 2→3, 3→4, 4→2}.

(a) For each vertex, list in-degree, out-degree, and out-neighborhood.
(b) Is vertex 1 a source? Is any vertex a sink?
(c) Is the digraph weakly connected? Strongly connected? (Hint: can you get from 3 back to 1?)

**💻 NetworkX exercise 0.2:** Build this digraph using `nx.DiGraph()`. Use `D.in_degree()`, `D.out_degree()`, `D.successors()`, `nx.is_weakly_connected()`, and `nx.is_strongly_connected()` to verify your answers.

---

### 0.3 — Vertex-Colored Digraphs & Sink-Freeness (~10 min)

**No video — this is specific to our project.** Read this section carefully.

In this project, vertices represent **genes** and colors represent **species**. A **vertex coloring** σ assigns each vertex a color from a set S. A colored digraph (G, σ) only has arcs between vertices of *different* colors — you never point from a gene to another gene in the same species.

Key properties for BMGs:

- **Sink-free:** Every vertex has at least one outgoing arc.
- **Color-sink-free:** For every vertex x and every color s ≠ σ(x), there exists at least one arc from x to some vertex of color s. This is stronger — not just "at least one arrow out," but "at least one arrow to every other species."

Every best match graph is color-sink-free by construction (every gene has a closest relative in every other species).

**✏️ Paper exercise 0.3:** Consider 6 vertices with colors: a₁, a₂ (red), b₁, b₂ (blue), c₁ (green).

(a) Draw a digraph where every vertex has arcs to at least one vertex of every other color. Verify it's color-sink-free.
(b) Now remove the arc from c₁ to any blue vertex. Is it still sink-free? Still color-sink-free?

**💻 NetworkX exercise 0.3:** Build a colored digraph in NetworkX. Store colors as node attributes using `G.add_node(name, color='red')`. Write a function `is_color_sink_free(G)` that checks the property: for every vertex x and every color s ≠ σ(x), there's at least one arc from x to a vertex of color s.

*Hint:* Use `G.nodes[v]['color']` to read attributes. `G.successors(v)` gives out-neighbors.

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

**💻 NetworkX exercise 0.4:** Build this tree as a `DiGraph` (edges from parent to child). Then write a function `lca(T, root, x, y)` that finds the last common ancestor of two leaves.

*Strategy:* Compute the path from root to x and the path from root to y (use `nx.shortest_path()`). Walk both paths in parallel from the root — the last vertex they share is the lca.

Skeleton:

```python
def lca(T, root, x, y):
    path_x = nx.shortest_path(T, root, x)
    path_y = nx.shortest_path(T, root, y)
    # Walk both paths from the root.
    # As long as they agree, track the current vertex.
    # The last vertex where they agree is the lca.
    # YOUR CODE HERE
    pass
```

Test it on the three pairs from the paper exercise.

---

### 0.5 — Partial Orders and DAGs (~10 min)

**📺 Watch:** "Directed Acyclic Graphs (1) — Introduction to DAGs" by Nick Huntington-Klein (~10 min, clear visual introduction to DAG structure, paths, and terminology):
https://www.youtube.com/watch?v=PiekvYYHeVQ

**The idea.** A **partial order** ⪯ on a set is reflexive (x ⪯ x), antisymmetric (x ⪯ y and y ⪯ x ⟹ x = y), and transitive (x ⪯ y ⪯ z ⟹ x ⪯ z). The ancestor order on a tree is a partial order. A **directed acyclic graph (DAG)** is a digraph with no directed cycles. Every DAG defines a partial order via reachability (x ⪯ y iff there's a directed path from x to y, or x = y).

The key connection to our project: **phylogenetic networks are DAGs**. Unlike trees, a vertex in a DAG can have multiple parents. This means two leaves can have *multiple* least common ancestors (a set, not a unique vertex). This is exactly what makes BMGs on networks harder than BMGs on trees.

A **topological ordering** of a DAG is a linear arrangement of vertices where every arrow goes "downhill." Every DAG has at least one.

**✏️ Paper exercise 0.5:** Draw a DAG on 5 vertices {ρ, u, v, x, y} with edges ρ→u, ρ→v, u→x, v→x, u→y.

(a) Does x have a unique parent?
(b) List all common ancestors of x and y.
(c) Which common ancestor is the "lowest" (closest to the leaves)? Is it unique?
(d) Give a topological ordering.

**💻 NetworkX exercise 0.5:** Build this DAG in NetworkX. Use `nx.is_directed_acyclic_graph()`, `nx.topological_sort()`, `nx.ancestors()`, and `N.predecessors()` to verify your paper answers. Confirm that x has two parents.

---

### 0.6 — Rooted Triples and the Aho Algorithm (~15 min)

**📖 Reference reading:** The PeerJ paper "Speeding up iterative applications of the Build supertree algorithm" has a clean description of the Aho/BUILD algorithm (Section "The Build Algorithm"):
https://peerj.com/articles/16624/ — read just that section.

**The idea.** A **rooted triple** ab|c (read: "a and b together, separate from c") is the simplest possible statement about tree structure. It says lca(a, b) is strictly below lca(a, c) = lca(b, c). In picture form: ((a, b), c) — a tiny tree where a and b share a more recent ancestor than either shares with c.

Triples are the atoms of tree structure. From a best match graph, you extract:

- **Informative triples** R: if gene a sees b but not b' (same species as b), then ab|b' — a and b must be closer in any explaining tree.
- **Forbidden triples** F: triples that must *not* appear in the explaining tree.

A set of triples R is **consistent** if some tree displays all of them. The **Aho algorithm** (BUILD) checks this. Here's how it works:

1. Build a "cluster graph": an *undirected* graph on the leaf set. For each triple ab|c, add an edge between a and b (the "close pair").
2. Find connected components of this cluster graph.
3. If there's only one component (everything is connected), the triples are **inconsistent** — stop.
4. If there are multiple components, each becomes a child subtree of the current root. **Recurse** on each component with only the triples relevant to that component's leaves.
5. Base case: ≤ 2 leaves → return them as a leaf or cherry.

The result is the unique **least resolved tree** — the tree with as few internal vertices as possible that displays all the triples.

**✏️ Paper exercise 0.6:** Given leaves {a, b, c, d} and triples R = {ab|c, ab|d}:

(a) Draw the cluster graph.
(b) Find its connected components.
(c) What tree does the Aho algorithm produce? Draw it.
(d) Now add cd|a to R. Redraw the cluster graph. What happens? Is R still consistent?

**💻 NetworkX exercise 0.6:** Implement the Aho algorithm. Here's the skeleton:

```python
def aho_build(leaves, triples):
    """
    leaves:  a set of leaf labels
    triples: a list of tuples (a, b, c) meaning "ab|c"
    Returns: a nested tuple representing the tree, or None if inconsistent.
    """
    if len(leaves) <= 2:
        return tuple(sorted(leaves))
    
    # Step 1: Build the cluster graph (undirected) on these leaves.
    # For each triple (a,b,c) where all three are in `leaves`,
    # add an undirected edge between a and b.
    # YOUR CODE HERE
    
    # Step 2: Find connected components.
    # If only one component → inconsistent, return None.
    # YOUR CODE HERE
    
    # Step 3: Recurse on each component.
    # Only pass triples whose three leaves all belong to that component.
    # Collect the results as children of the current node.
    # YOUR CODE HERE
    
    pass
```

Test cases:
- `aho_build({'a','b','c','d'}, [('a','b','c'), ('a','b','d')])` should give a tree with {a,b} grouped.
- `aho_build({'a','b','c','d'}, [('a','b','c'), ('a','b','d'), ('c','d','a')])` should give a fully resolved tree.
- `aho_build({'a','b','c'}, [('a','b','c'), ('b','c','a'), ('c','a','b')])` should return `None` (inconsistent).

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

**(a) On paper:** For each leaf x and each color s ≠ σ(x), find the best match(es). The rule: y is a best match of x in species s if lca(x, y) ⪯ lca(x, y') for all y' with σ(y') = s. In other words, there's no gene in the same species that has a *deeper* (closer to leaves) lca with x.

Work through it systematically:

- a₁ in blue: compare lca(a₁, b₁) vs lca(a₁, b₂). Which is deeper?
- a₁ in green: compare lca(a₁, c₁) vs lca(a₁, c₂).
- b₁ in red: only one red vertex, so a₁ is automatically a best match.
- b₁ in green: compare lca(b₁, c₁) vs lca(b₁, c₂).
- Continue for b₂, c₁, c₂...

Draw the resulting digraph (G, σ). Verify it is color-sink-free.

**(b) In NetworkX:** Write a function that takes a tree (T, σ) and computes its BMG. Here's the skeleton:

```python
def compute_bmg(T, root, sigma):
    """
    T:     a nx.DiGraph representing a rooted tree (edges parent→child)
    root:  the root vertex
    sigma: dict mapping each leaf to its color
    
    Returns: a nx.DiGraph representing the BMG
    """
    leaves = list(sigma.keys())
    all_colors = set(sigma.values())
    BMG = nx.DiGraph()
    for node, color in sigma.items():
        BMG.add_node(node, color=color)
    
    # For each leaf x, for each color s ≠ σ(x):
    #   1. Find all leaves y with σ(y) = s (the "candidates").
    #   2. Compute lca_depth(x, y) for each candidate.
    #      (lca_depth = distance from root to lca(x,y) — deeper = closer relative)
    #   3. Find the maximum depth among candidates.
    #   4. Add arc x→y for every candidate achieving that maximum.
    # YOUR CODE HERE (use your lca function from 0.4)
    
    return BMG
```

Verify your code produces the same arcs as your paper answer.

**(c) Extract informative triples:** Write code to extract the informative triples R from the BMG. Recall: R = {ab|b' : σ(a) ≠ σ(b) = σ(b'), (a,b) ∈ E(G), (a,b') ∉ E(G)}.

In words: if a has an arc to b but *not* to b' (where b and b' are the same color, different from a), then the triple ab|b' is informative.

```python
def extract_informative_triples(BMG, sigma):
    """
    Returns a list of tuples (a, b, b_prime) meaning "ab|b'"
    """
    # YOUR CODE HERE
    pass
```

---

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

---
---

## APPENDIX — Solutions

**Try the exercises yourself first!** These solutions are for checking your work, not for skipping ahead.

---

### Solution 0.1 — Graphs

```python
G = nx.Graph()
G.add_edges_from([('a','b'), ('b','c'), ('c','d'), ('d','e'), ('a','e'), ('b','d')])

# (a) Degrees
for v in sorted(G.nodes()):
    print(f"deg({v}) = {G.degree(v)}")
# a:2, b:3, c:2, d:3, e:2

# (b) All paths from a to d
for path in nx.all_simple_paths(G, 'a', 'd'):
    print("Path a→d:", path)
# a-b-c-d, a-b-d, a-e-d

# (c) Connected
print("Connected?", nx.is_connected(G))  # True

# (d) One cycle: a-b-d-e-a

# (e) Induced subgraph on {a,b,d,e}
H = G.subgraph(['a', 'b', 'd', 'e'])
print("Induced subgraph edges:", sorted(H.edges()))
# Edges: (a,b), (a,e), (b,d), (d,e)

nx.draw(G, with_labels=True, node_color='lightblue', node_size=500)
plt.show()
```

---

### Solution 0.2 — Digraphs

```python
D = nx.DiGraph()
D.add_edges_from([(1,2), (1,3), (2,3), (3,4), (4,2)])

# (a)
for v in sorted(D.nodes()):
    print(f"Vertex {v}: in-deg={D.in_degree(v)}, out-deg={D.out_degree(v)}, "
          f"out-neighbors={sorted(D.successors(v))}")
# 1: in=0, out=2, out-nbrs=[2,3]
# 2: in=2, out=1, out-nbrs=[3]
# 3: in=2, out=1, out-nbrs=[4]
# 4: in=1, out=1, out-nbrs=[2]

# (b) Vertex 1 is a source (in-degree 0). No sinks.
print("Sources:", [v for v in D.nodes() if D.in_degree(v) == 0])  # [1]
print("Sinks:", [v for v in D.nodes() if D.out_degree(v) == 0])    # []

# (c) Weakly connected: yes. Strongly connected: no (can't reach 1 from anywhere).
print("Weakly connected?", nx.is_weakly_connected(D))    # True
print("Strongly connected?", nx.is_strongly_connected(D)) # False

pos = nx.spring_layout(D, seed=42)
nx.draw(D, pos, with_labels=True, node_color='lightcoral',
        node_size=500, arrows=True, arrowsize=20)
plt.show()
```

---

### Solution 0.3 — Colored digraphs

```python
G = nx.DiGraph()
colors = {'a1': 'red', 'a2': 'red', 'b1': 'blue', 'b2': 'blue', 'c1': 'green'}
for node, color in colors.items():
    G.add_node(node, color=color)

G.add_edges_from([
    ('a1','b1'), ('a1','c1'), ('a2','b2'), ('a2','c1'),
    ('b1','a1'), ('b1','c1'), ('b2','a2'), ('b2','c1'),
    ('c1','a1'), ('c1','b1')
])

def is_color_sink_free(G):
    all_colors = set(nx.get_node_attributes(G, 'color').values())
    for v in G.nodes():
        v_color = G.nodes[v]['color']
        reachable_colors = {G.nodes[u]['color'] for u in G.successors(v)}
        missing = all_colors - {v_color} - reachable_colors
        if missing:
            print(f"  FAIL: {v} (color={v_color}) missing arcs to {missing}")
            return False
        else:
            print(f"  OK:   {v} (color={v_color}) → all other colors")
    return True

print("Color-sink-free?", is_color_sink_free(G))

node_colors_list = [colors[v] for v in G.nodes()]
pos = nx.spring_layout(G, seed=7)
nx.draw(G, pos, with_labels=True, node_color=node_colors_list,
        node_size=600, arrows=True, arrowsize=15, font_weight='bold')
plt.show()
```

---

### Solution 0.4 — Rooted trees and lca

```python
T = nx.DiGraph()
T.add_edges_from([
    ('rho', 'u'), ('rho', 'v'),
    ('u', 'a1'), ('u', 'w'),
    ('w', 'b1'), ('w', 'c1'),
    ('v', 'b2'), ('v', 'c2')
])

# Parent/children listing
for v in T.nodes():
    parents = list(T.predecessors(v))
    children = list(T.successors(v))
    print(f"{v}: parent={parents if parents else 'none (root)'}, "
          f"children={children if children else '(leaf)'}")

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

# (b) lca computations
print("\nlca(a1, b1) =", lca(T, 'rho', 'a1', 'b1'))  # u
print("lca(b1, c2) =", lca(T, 'rho', 'b1', 'c2'))    # rho
print("lca(a1, c1) =", lca(T, 'rho', 'a1', 'c1'))    # u

# (d) Closest relatives of a1
leaves = ['a1', 'b1', 'b2', 'c1', 'c2']
for leaf in leaves:
    if leaf != 'a1':
        a = lca(T, 'rho', 'a1', leaf)
        depth = nx.shortest_path_length(T, 'rho', a)
        print(f"lca(a1, {leaf}) = {a} at depth {depth}")
# b1 and c1 are closest (lca=u at depth 1); b2 and c2 are farther (lca=rho at depth 0)
```

---

### Solution 0.5 — DAGs

```python
N = nx.DiGraph()
N.add_edges_from([('rho','u'), ('rho','v'), ('u','x'), ('v','x'), ('u','y')])

print("Is DAG?", nx.is_directed_acyclic_graph(N))  # True
print("Topological order:", list(nx.topological_sort(N)))

# (a) x has two parents
print("Parents of x:", list(N.predecessors('x')))  # [u, v]

# (b) Common ancestors of x and y
ancestors_x = nx.ancestors(N, 'x')  # {rho, u, v}
ancestors_y = nx.ancestors(N, 'y')  # {rho, u}
common = ancestors_x & ancestors_y
print("Common ancestors of x and y:", common)  # {rho, u}

# (c) u is the lowest common ancestor (closer to leaves than rho)

pos = {'rho': (1, 3), 'u': (0.5, 2), 'v': (1.5, 2), 'x': (1, 1), 'y': (0, 1)}
nx.draw(N, pos, with_labels=True, node_color='lightyellow',
        node_size=600, arrows=True, arrowsize=20)
plt.show()
```

---

### Solution 0.6 — Aho algorithm

```python
def aho_build(leaves, triples):
    """
    leaves:  a set of leaf labels
    triples: a list of tuples (a, b, c) meaning "ab|c"
    Returns: a nested tuple representing the tree, or None if inconsistent.
    """
    if len(leaves) <= 2:
        return tuple(sorted(leaves))

    # Build cluster graph
    cluster = nx.Graph()
    cluster.add_nodes_from(leaves)
    relevant = [(a, b, c) for (a, b, c) in triples
                if a in leaves and b in leaves and c in leaves]
    for (a, b, c) in relevant:
        cluster.add_edge(a, b)

    components = list(nx.connected_components(cluster))

    if len(components) == 1:
        return None  # inconsistent

    children = []
    for comp in components:
        subtree = aho_build(comp, triples)
        if subtree is None:
            return None
        children.append(subtree)
    return tuple(children)

# Test 1: R = {ab|c, ab|d}
print("Test 1:", aho_build({'a','b','c','d'}, [('a','b','c'), ('a','b','d')]))
# Expected: (('a', 'b'), ('c', 'd'))  — {a,b} grouped, {c,d} are separate leaves
# (c and d end up in one component because they have no edges in the cluster graph,
#  but since they're singletons they get grouped by default)

# Test 2: add cd|a
print("Test 2:", aho_build({'a','b','c','d'},
                           [('a','b','c'), ('a','b','d'), ('c','d','a')]))
# Expected: (('a', 'b'), ('c', 'd'))  — now c-d are explicitly grouped too

# Test 3: inconsistent
print("Test 3:", aho_build({'a','b','c'},
                           [('a','b','c'), ('b','c','a'), ('c','a','b')]))
# Expected: None
```

---

### Solution 0.8 — BMG construction

**Paper answers:**

| x | color s | candidates | lca depths | best match(es) |
|---|---------|-----------|-----------|----------------|
| a₁ | blue | b₁ (lca=u, depth 1), b₂ (lca=ρ, depth 0) | b₁ deeper | a₁→b₁ |
| a₁ | green | c₁ (lca=u, depth 1), c₂ (lca=ρ, depth 0) | c₁ deeper | a₁→c₁ |
| b₁ | red | a₁ (lca=u, depth 1) | only one | b₁→a₁ |
| b₁ | green | c₁ (lca=w, depth 2), c₂ (lca=ρ, depth 0) | c₁ deeper | b₁→c₁ |
| b₂ | red | a₁ (lca=ρ, depth 0) | only one | b₂→a₁ |
| b₂ | green | c₁ (lca=ρ, depth 0), c₂ (lca=v, depth 1) | c₂ deeper | b₂→c₂ |
| c₁ | red | a₁ (lca=u, depth 1) | only one | c₁→a₁ |
| c₁ | blue | b₁ (lca=w, depth 2), b₂ (lca=ρ, depth 0) | b₁ deeper | c₁→b₁ |
| c₂ | red | a₁ (lca=ρ, depth 0) | only one | c₂→a₁ |
| c₂ | blue | b₁ (lca=ρ, depth 0), b₂ (lca=v, depth 1) | b₂ deeper | c₂→b₂ |

**Code:**

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

def compute_bmg(T, root, sigma):
    leaves = list(sigma.keys())
    all_colors = set(sigma.values())
    BMG = nx.DiGraph()
    for node, color in sigma.items():
        BMG.add_node(node, color=color)

    for x in leaves:
        for s in all_colors:
            if s == sigma[x]:
                continue
            candidates = [y for y in leaves if sigma[y] == s]
            best_depth = max(lca_depth(T, root, x, y) for y in candidates)
            for y in candidates:
                if lca_depth(T, root, x, y) == best_depth:
                    BMG.add_edge(x, y)
    return BMG

BMG = compute_bmg(T, root, sigma)

print("BMG arcs:")
for (u, v) in sorted(BMG.edges()):
    print(f"  {u} ({sigma[u]}) → {v} ({sigma[v]})")

# Verify color-sink-free
all_colors = set(sigma.values())
for x in leaves:
    out_colors = {sigma[y] for y in BMG.successors(x)}
    expected = all_colors - {sigma[x]}
    assert out_colors == expected, f"{x} missing arcs to {expected - out_colors}"
print("\n✓ BMG is color-sink-free")

# Extract informative triples
def extract_informative_triples(BMG, sigma):
    leaves = list(sigma.keys())
    all_colors = set(sigma.values())
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
    return R

R = extract_informative_triples(BMG, sigma)
print("\nInformative triples:")
for (a, b, bp) in R:
    print(f"  {a}{b}|{bp}")
```
