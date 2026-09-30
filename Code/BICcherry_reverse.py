from collections import defaultdict
from collections import Counter

import networkx as nx


def BICcherry_reverse(BMG: nx.DiGraph, root: str = "rho", simplify: bool = False) -> nx.DiGraph:
    """Build a network from a best match graph (BMG).

    Works edge by edge. Every edge x -> y of the BMG gets a "connecting
    node" in the network (a p, q or r node that has y below it and
    makes y a match of x):

    Case 1: every reciprocal edge x <-> y becomes a cherry with parent
            p_x_y, attached to `root`. These root -> p edges are never
            removed.
    Case 2: edge x -> y where y has a reciprocal partner z of x's color:
            node q_x_y with `root` as parent and x plus the cherry
            p(y, z) as children. If y has several such partners, every
            one of them gets its own q-node (q_x_y, q_x_y_z2, ...).
    Case 3: every other edge x -> y. Starting from y, follow y's own BMG
            edges and find the nodes w of x's color that take the fewest
            edges to reach (ties: all of them). For each such w, the path
            y -> u -> ... -> w starts with the edge y -> u; its connecting
            node (the parent of y and u) gets a new node r_x_y_w above
            it: `root` -> r_x_y_w -> {x, connecting node of y -> u}.
            Only candidates whose cluster (all leaves below the connecting
            node) holds nothing but best matches of x (leaves of x's own
            color ignored) are used. If none exists at the nearest
            distance, the search continues one edge further, and so on;
            if no distance has one, the nearest candidates are used.
            Case-3 edges are processed repeatedly until nothing changes,
            because the connecting node of y -> u may itself be a
            case-3 node.

    p can end up with several parents (root plus q's and r's).

    Special case: a BMG consisting of exactly one reciprocal pair (two
    nodes) yields `root` directly as the parent of the two leaves.
    """
    # BMG
    bmg = BMG.copy()
    ## assert colored digraph
    assert isinstance(bmg, nx.DiGraph)
    assert all("color" in bmg.nodes[v] for v in bmg.nodes)

    ## assert properly colored (no edges between same color)
    colors = nx.get_node_attributes(bmg, "color")
    for u, v in bmg.edges():
        assert colors[u] != colors[v]

    ## assert sicor in hub
    ### find all sicors
    color_counts = Counter(colors.values())
    sicor = [v for v, c in colors.items() if color_counts[c] == 1]
    ### assert in-hub-ness
    for s in sicor:
        for u in bmg.nodes():
            if colors[u] != colors[s]:
                assert bmg.has_edge(u, s)

    # simplifying the BMG and resulting generated network if flagged
    net = nx.DiGraph()
    if simplify:
        need_to_break1 = False
        need_to_break2 = False
        curr_root_num = 0
        curr_root = "rho" + f"_{curr_root_num}"
        net.add_node(curr_root)

        # create a color to node dict
        color_to_leaves = {}
        for v in bmg.nodes:
            key = (
                bmg.nodes[v]["color"]
            )
            color_to_leaves.setdefault(key, []).append(v)

        # test if any node in the BMG exists that has every other node as a reciprocal best match
        # run through this multiple times to catch nodes in subtrees
        for i in range(len(bmg.nodes)):
            leaves = bmg.nodes()
            leaves_to_remove = []
            att_to_root = False
            for leaf in leaves:
                suc = frozenset(bmg.successors(leaf))
                cur_color = bmg.nodes[leaf]["color"]
                same_color = color_to_leaves[cur_color]
                prec = frozenset(bmg.predecessors(leaf))
                # reciprocal best matches and every node of different color is best match
                if ((suc == prec) and (suc == leaves - [leaf])):
                    #print(f"found {leaf}")
                    cur_color = bmg.nodes[leaf]["color"]
                    net.add_node(leaf, color=cur_color)
                    net.add_edge(curr_root, leaf)
                    leaves_to_remove.append(leaf)
                    att_to_root = True
            bmg.remove_nodes_from(leaves_to_remove)
            if att_to_root:
                curr_root_num += 1
                curr_root = "rho" + f"_{curr_root_num}"
            else:
                need_to_break1 = True


            # test if any node in BMG exists that has no incoming edges (pred) but has every other node (different color) as best match
            leaves = bmg.nodes()
            leaves_to_remove = []
            att_to_root = False
            for leaf in leaves:
                cur_color = bmg.nodes[leaf]["color"]
                same_color = color_to_leaves[cur_color]
                prec = frozenset(bmg.predecessors(leaf))
                suc = frozenset(bmg.successors(leaf))
                #print(f"{leaf} has no indegrees: {len(prec) == 0} and out to all but same color {suc == leaves - same_color}")
                if ((len(prec) == 0) and (suc == leaves - same_color)):
                    #print(f"found {leaf}")
                    net.add_node(leaf, color=cur_color)
                    net.add_edge(curr_root, leaf)
                    leaves_to_remove.append(leaf)
                    att_to_root = True
            bmg.remove_nodes_from(leaves_to_remove)
            if att_to_root:
                curr_root_num += 1
                curr_root = "rho" + f"_{curr_root_num}"
            else:
                need_to_break2 = True

            if (need_to_break1 and need_to_break2):
                # both steps did not find any improvements, break the loop
                break

        # reattach all roots
        for i in range(curr_root_num):
            net.add_edge("rho" + f"_{i}", "rho" + f"_{i + 1}")


        # No edges left in BMG, return N
        if len(bmg.edges()) == 0:
            # remove last unused root
            net.remove_node(curr_root)
            return net
        else:
            # set root as current root for downstream processes
            root = curr_root
    else:
        # add root and continue without simplification
        net.add_node(root)

    key = str

    def color(n):
        return bmg.nodes[n].get("color")

    edges = sorted(
        ((u, v) for u, v in bmg.edges() if u != v),
        key=lambda e: (key(e[0]), key(e[1])),
    )

    # --- reciprocal pairs ----------------------------------------------
    pairs = sorted(
        {tuple(sorted((u, v), key=key)) for u, v in edges
         if bmg.has_edge(v, u)},
        key=lambda p: (key(p[0]), key(p[1])),
    )


    for n in bmg.nodes:            # all leaves, with their color
        net.add_node(n, **bmg.nodes[n])

    # --- simple case: a single cherry only -----------------------------
    if len(bmg) == 2 and len(pairs) == 1:
        a, b = pairs[0]
        net.add_edges_from([(root, a), (root, b)])
        return net

    # connecting[(a, b)] = network node(s) that are "the parent of a and
    # b" for the BMG edge a -> b (p, q or r nodes)
    connecting = defaultdict(list)

    # --- case 1: one cherry per reciprocal edge ------------------------
    cherries_of = defaultdict(list)  # leaf -> names of cherry parents
    cherry_sibling = {}              # (p, leaf) -> the leaf's sibling in p
    for a, b in pairs:
        p = f"p_{a}_{b}"
        net.add_edges_from([(root, p), (p, a), (p, b)])
        cherries_of[a].append(p)
        cherries_of[b].append(p)
        cherry_sibling[(p, a)] = b
        cherry_sibling[(p, b)] = a
        connecting[(a, b)].append(p)
        connecting[(b, a)].append(p)

    # --- case 2: y has a reciprocal partner of x's color ---------------
    pending = []                     # edges left for case 3
    for x, y in edges:
        if bmg.has_edge(y, x):
            continue                 # reciprocal edge, handled by case 1
        # one q-node per cherry of y whose other child has x's color
        ps = [p for p in cherries_of[y]
              if color(cherry_sibling[(p, y)]) == color(x)]
        for i, p in enumerate(ps):
            q = f"q_{x}_{y}" + (f"_{cherry_sibling[(p, y)]}" if i else "")
            net.add_edges_from([(root, q), (q, x), (q, p)])
            connecting[(x, y)].append(q)
        if not ps:
            pending.append((x, y))

    # --- case 3: nodes of x's color, searched outward from y ----------
    def hits_by_distance(x, y):
        """Breadth-first search along BMG edges starting at y. Returns a
        list with one entry per distance (nearest first) that contains
        nodes of x's color: {w: set of first edges (y, u) of the
        shortest paths from y to w}. x itself is excluded."""
        first_hops = {y: set()}      # node -> first edges of shortest paths
        frontier = [y]
        layers = []
        while frontier:
            nxt = {}
            for v in frontier:
                for s in bmg.successors(v):
                    if s in first_hops:
                        continue     # already reached with fewer edges
                    hops = {(y, s)} if v == y else first_hops[v]
                    nxt.setdefault(s, set()).update(hops)
            first_hops.update(nxt)
            hits = {w: h for w, h in nxt.items()
                    if w != x and color(w) == color(x)}
            if hits:
                layers.append(hits)
            frontier = sorted(nxt, key=key)
        return layers

    def cluster(n):
        """All leaves below network node n."""
        return {d for d in nx.descendants(net, n) if d in bmg}

    def candidates_of(hits):
        """All (w, connecting node of the first edge) pairs, fixed order."""
        cands = []
        for w in sorted(hits, key=key):
            for e in sorted(hits[w], key=lambda e: key(e[1])):
                for t in connecting[e]:
                    if (w, t) not in cands:
                        cands.append((w, t))
        return cands

    def matches_only(x, t):
        """True if every leaf below t that does not have x's color is a
        best match of x."""
        return all(bmg.has_edge(x, l) for l in cluster(t)
                   if color(l) != color(x))

    def place(x, y, relaxed=False):
        """Try to place the case-3 edge x -> y. Goes outward distance by
        distance; a distance is only looked at once the connecting nodes
        of all its first edges exist (in `relaxed` mode, missing ones
        are simply skipped). Returns False if it has to wait."""
        layers = hits_by_distance(x, y)
        chosen = None
        nearest = None
        for hits in layers:
            needed = {e for h in hits.values() for e in h}
            if not relaxed and any(not connecting[e] for e in needed):
                return False                   # wait for a later round
            cands = candidates_of(hits)
            if nearest is None and cands:
                nearest = cands
            good = [(w, t) for w, t in cands if matches_only(x, t)]
            if good:
                chosen = good
                break
        if chosen is None:
            chosen = nearest                   # no clean candidate anywhere
        if not chosen:
            return False
        index = defaultdict(int)
        for w, t in chosen:
            index[w] += 1
            i = index[w]
            r = f"r_{x}_{y}_{w}" + (f"_{i}" if i > 1 else "")
            net.add_edges_from([(root, r), (r, x), (r, t)])
            connecting[(x, y)].append(r)
        return True

    while pending:
        still_pending = [e for e in pending if not place(*e)]
        if len(still_pending) == len(pending):
            # edges waiting on each other in a cycle: place the first one
            # that can be placed with the connecting nodes that exist
            for i, e in enumerate(still_pending):
                if place(*e, relaxed=True):
                    del still_pending[i]
                    break
            else:
                break                          # nothing can be placed
        pending = still_pending

    if pending:
        import warnings
        warnings.warn(f"BICcherry_reverse: could not place edges {pending}")

    # --- nodes that ended up without a parent go directly under root ---
    for n in bmg.nodes:
        if n != root and net.in_degree(n) == 0:
            net.add_edge(root, n)

    return net


if __name__ == "__main__":
    # x1 <-> y1, x2 <-> y2 <- x3, colored (x* red, y* blue)
    g = nx.DiGraph()
    g.add_nodes_from([
        ("x1", {"color": "red"}), ("x2", {"color": "red"}),
        ("x3", {"color": "red"}),
        ("y1", {"color": "blue"}), ("y2", {"color": "blue"}),
    ])
    g.add_edges_from([
        ("x1", "y1"), ("y1", "x1"),
        ("x2", "y2"), ("y2", "x2"),
        ("x3", "y2"),
    ])
    net = bmg_to_network(g)
    expected = {
        ("rho", "q_x3_y2"), ("rho", "p_x1_y1"), ("rho", "p_x2_y2"),
        ("p_x1_y1", "x1"), ("p_x1_y1", "y1"),
        ("q_x3_y2", "x3"), ("q_x3_y2", "p_x2_y2"),
        ("p_x2_y2", "x2"), ("p_x2_y2", "y2"),
    }
    print(sorted(net.edges()))
    assert set(net.edges()) == expected, "does not match the example"

    # colors carried over for leaves, internal nodes have none
    for n in ("x1", "x2", "x3"):
        assert net.nodes[n]["color"] == "red", n
    for n in ("y1", "y2"):
        assert net.nodes[n]["color"] == "blue", n
    for n in ("rho", "p_x1_y1", "p_x2_y2", "q_x3_y2"):
        assert "color" not in net.nodes[n], n

    # second example: x1 -> y1, x2 <-> y1, y2 -> x2
    g3 = nx.DiGraph()
    g3.add_nodes_from([
        ("x1", {"color": "red"}), ("x2", {"color": "red"}),
        ("y1", {"color": "blue"}), ("y2", {"color": "blue"}),
    ])
    g3.add_edges_from([
        ("x1", "y1"), ("x2", "y1"), ("y1", "x2"), ("y2", "x2"),
    ])
    net3 = bmg_to_network(g3)
    expected3 = {
        ("rho", "p_x2_y1"), ("rho", "q_x1_y1"), ("rho", "q_y2_x2"),
        ("p_x2_y1", "x2"), ("p_x2_y1", "y1"),
        ("q_x1_y1", "x1"), ("q_x1_y1", "p_x2_y1"),
        ("q_y2_x2", "y2"), ("q_y2_x2", "p_x2_y1"),
    }
    print(sorted(net3.edges()))
    assert set(net3.edges()) == expected3, "does not match the second example"

    # color-restricted q: x1<->y1<->z1, x2->y1 (x2 same color as x1,
    # not as z1) -> only q_x2_y1 -> p_x1_y1 should be created
    g4 = nx.DiGraph()
    g4.add_nodes_from([
        ("x1", {"color": "red"}), ("x2", {"color": "red"}),
        ("y1", {"color": "blue"}),
        ("z1", {"color": "green"}),
    ])
    g4.add_edges_from([
        ("x1", "y1"), ("y1", "x1"),
        ("y1", "z1"), ("z1", "y1"),
        ("x2", "y1"),
    ])
    net4 = bmg_to_network(g4)
    expected4 = {
        ("rho", "p_x1_y1"), ("rho", "p_y1_z1"), ("rho", "q_x2_y1"),
        ("p_x1_y1", "x1"), ("p_x1_y1", "y1"),
        ("p_y1_z1", "y1"), ("p_y1_z1", "z1"),
        ("q_x2_y1", "x2"), ("q_x2_y1", "p_x1_y1"),
    }
    print(sorted(net4.edges()))
    assert set(net4.edges()) == expected4, "color restriction not respected"

    # third class: 4<->5, 6->5, 6->7, 7->4 (7 is class 2, 6 is class 3)
    g5 = nx.DiGraph()
    g5.add_nodes_from([
        ("4", {"color": 2}), ("5", {"color": 3}),
        ("6", {"color": 2}), ("7", {"color": 3}),
    ])
    g5.add_edges_from([
        ("4", "5"), ("5", "4"),
        ("6", "5"), ("6", "7"), ("7", "4"),
    ])
    net5 = bmg_to_network(g5)
    expected5 = {
        ("rho", "p_4_5"), ("rho", "q_7_4"),
        ("rho", "q_6_5"), ("rho", "r_6_7_4"),
        ("p_4_5", "4"), ("p_4_5", "5"),
        ("q_7_4", "7"), ("q_7_4", "p_4_5"),
        ("q_6_5", "6"), ("q_6_5", "p_4_5"),
        ("r_6_7_4", "6"), ("r_6_7_4", "q_7_4"),
    }
    print(sorted(net5.edges()))
    assert set(net5.edges()) == expected5, "third-class handling is wrong"

    # cherry member with an extra edge: 4<->7, 5<->6, 5->4, 6->7
    g6 = nx.DiGraph()
    colors6 = [("4", 2), ("5", 3), ("6", 2), ("7", 3)]
    g6.add_nodes_from((n, {"color": c}) for n, c in colors6)
    g6.add_edges_from([
        ("4", "7"), ("5", "4"), ("5", "6"),
        ("6", "5"), ("6", "7"), ("7", "4"),
    ])
    net6 = bmg_to_network(g6)
    expected6 = {
        ("rho", "p_4_7"), ("rho", "p_5_6"),
        ("rho", "q_5_4"), ("rho", "q_6_7"),
        ("p_4_7", "4"), ("p_4_7", "7"),
        ("p_5_6", "5"), ("p_5_6", "6"),
        ("q_5_4", "5"), ("q_5_4", "p_4_7"),
        ("q_6_7", "6"), ("q_6_7", "p_4_7"),
    }
    print(sorted(net6.edges()))
    assert set(net6.edges()) == expected6, "cherry-member edges not handled"

    # manual example: 15, 20, 21 -> 23, where 23's only cherry partner
    # (18) has the wrong color -> case 3 via 23's nearest matches
    N7 = [('14',5),('15',5),('23',6),('24',6),('18',7),('19',5),
          ('20',3),('21',3),('22',3),('17',3)]
    E7 = [('14','20'),('14','22'),('14','24'),('14','18'),('15','20'),
          ('15','22'),('15','23'),('15','24'),('15','18'),('23','22'),
          ('23','14'),('23','19'),('23','18'),('24','20'),('24','22'),
          ('24','14'),('24','19'),('24','18'),('18','20'),('18','22'),
          ('18','14'),('18','15'),('18','23'),('18','24'),('19','20'),
          ('19','22'),('19','24'),('19','18'),('20','14'),('20','23'),
          ('20','24'),('20','18'),('21','14'),('21','15'),('21','19'),
          ('21','23'),('21','24'),('21','18'),('22','14'),('22','15'),
          ('22','19'),('22','24'),('22','18'),('17','14'),('17','15'),
          ('17','19'),('17','24'),('17','18')]
    g7 = nx.DiGraph()
    g7.add_nodes_from((n, {"color": c}) for n, c in N7)
    g7.add_edges_from(E7)
    net7 = bmg_to_network(g7)
    r_nodes = {n: sorted(net7.successors(n)) for n in net7 if str(n).startswith("r_")}
    print(r_nodes)
    assert r_nodes == {
        "r_15_23_14": ["15", "q_23_14"],
        "r_15_23_19": ["15", "q_23_19"],
        "r_20_23_22": ["20", "q_23_22"],
        "r_21_23_22": ["21", "q_23_22"],
    }, r_nodes

    # single cherry, colored
    g2 = nx.DiGraph()
    g2.add_nodes_from([("a", {"color": "red"}), ("b", {"color": "blue"})])
    g2.add_edges_from([("a", "b"), ("b", "a")])
    net2 = bmg_to_network(g2)
    print(sorted(net2.edges()))
    assert net2.nodes["a"]["color"] == "red"
    assert net2.nodes["b"]["color"] == "blue"
    assert "color" not in net2.nodes["rho"]

    print("OK")