import pytest
import networkx as nx
from bmg_Tony import bmg
import bmg_fun
import asymmetree.treeevolve as te

# medium tree with three colors that can be shared across functions
@pytest.fixture
def medium_three_color_tree():
    T = nx.DiGraph()
    T.add_nodes_from([("a1", {"color": "red"}), ("b1", {"color": "blue"}), ("c1", {"color": "green"}),
                      ("b2", {"color": "blue"}), ("c2", {"color": "green"})])
    T.add_edges_from([("p", "u"), ("u", "a1"), ("u", "w"), ("w", "b1"), ("w", "c1"), ("p", "v"), ("v", "b2"), ("v", "c2")])
    return T

# BMG of medium tree with three colors that can be shared across functions
@pytest.fixture
def medium_three_color_tree_expected_bmg():
    G = nx.DiGraph()
    G.add_nodes_from([("a1", {"color": "red"}), ("b1", {"color": "blue"}), ("c1", {"color": "green"}),
                      ("b2", {"color": "blue"}), ("c2", {"color": "green"})])
    G.add_edges_from([("a1", "c1"), ("c1", "a1"), ("b1", "a1"), ("a1", "b1"), ("c2", "a1"), ("b2", "a1"), ("b1", "c1"), ("c1", "b1"),
                      ("b2", "c2"), ("c2", "b2")])
    return G

# BIC cherry network with two colors that can be shared across functions, BMG of this nw differs between weak and strong
@pytest.fixture
def bic_cherry_nw(): # example from bmg_in_networks paper
    bic_cherry = nx.DiGraph()
    bic_cherry.add_nodes_from([("y", {"color": "red"}), ("x", {"color": "blue"}), ("z", {"color": "red"})])
    bic_cherry.add_edges_from([("p", "Pxy"), ("Pxy", "y"), ("Pxy", "x"), ("Pxy", "Qxz"), ("Qxz", "x"), ("Qxz", "z"),
                               ("p", "Pxz"), ("Pxz", "z"), ("Pxz", "x"), ("Pxz", "Qxy"), ("Qxy", "x"), ("Qxy", "y")])
    return bic_cherry

# medium network with two colors that can be shared across functions, BMG of this nw differs between weak and strong
@pytest.fixture
def medium_two_color_nw(): # example from Stadler in last lecture
    G = nx.DiGraph()
    G.add_nodes_from([("y", {"color": "red"}), ("y1", {"color":'red'}), ("y2", {"color":'red'}), ("x", {"color":'green'})])
    G.add_edges_from([("rho", "Pxy"), ("rho", "Pxy1"), ("rho", "Pxy2"), ("Pxy", "y"), ("Pxy", "x"), ("Pxy", "Qxy2"), ("Pxy1", "y1"),
                      ("Pxy1", "x"), ("Pxy1", "Qxy2"),  # remove this edge later
                      ("Pxy2", "y2"), ("Pxy2", "x"), ("Pxy2", "Qxy"), ("Qxy", "x"), ("Qxy", "y"), ("Qxy2", "x"), ("Qxy2", "y2")])
    return G

# Start of unit tests, separated by classes depending on topic
# class tests for self designed examples of trees and networks
class TestBMGKnownExamples:
    def test_small_two_color_tree(self):
        # create small tree wot two colors
        T = nx.DiGraph()
        T.add_nodes_from([("x", {"color": "red"}), ("y", {"color": "blue"})])
        T.add_edges_from([("p", "x"), ("p", "y")])
        # create corresponding bmg
        G = nx.DiGraph()
        G.add_nodes_from([("x", {"color": "red"}), ("y", {"color": "blue"})])
        G.add_edges_from([("x", "y"), ("y", "x")])
        # get result from bmg function
        result = bmg(T, mode="strong")
        assert nx.utils.graphs_equal(result, G)

    def test_small_three_color_tree(self):
        # create small tree with three colors
        T = nx.DiGraph()
        T.add_nodes_from([("x", {"color": "red"}), ("y", {"color": "blue"}), ("z", {"color": "green"})])
        T.add_edges_from([("p", "u"), ("p", "z"), ("u", "x"), ("u", "y")])
        # create corresponding bmg
        G = nx.DiGraph()
        G.add_nodes_from([("x", {"color": "red"}), ("y", {"color": "blue"}), ("z", {"color": "green"})])
        G.add_edges_from([("x", "y"), ("y", "x"), ("x", "z"), ("y", "z"), ("z", "y"), ("z", "x")])
        # get result from bmg function
        result = bmg(T, mode="strong")
        assert nx.utils.graphs_equal(result, G)

    # testing medium tree
    def test_medium_three_color_tree(self, medium_three_color_tree, medium_three_color_tree_expected_bmg):
        T = medium_three_color_tree
        result = bmg(T, mode="strong")
        #print(result.edges(data=True))
        #print(medium_three_color_tree_expected_bmg.edges(data=True))
        assert nx.utils.graphs_equal(result, medium_three_color_tree_expected_bmg)

    # testing medium tree changed into network
    def test_medium_three_color_nw(self, medium_three_color_tree, medium_three_color_tree_expected_bmg):
        T = medium_three_color_tree
        T.remove_edge("w", "c1")
        T.add_edges_from([("w", "q"), ("q", "c1"), ("q", "b2")])
        result = bmg(T, mode="strong")
        G = medium_three_color_tree_expected_bmg
        G.remove_edge("c1", "b1")
        G.add_edges_from([("c1", "b2"), ("b2", "c1"), ("a1", "b2")])
        #print(result.edges(data=True))
        #print(G.edges(data=True))
        assert nx.utils.graphs_equal(result, G)

    ### -- Test showing that same BIC cherry network results in different BMGs depending on definition --

    def test_bic_cherry_strong(self, bic_cherry_nw):
        result = bmg(bic_cherry_nw, mode="strong")
        G = nx.DiGraph()
        G.add_nodes_from([("y", {"color": "red"}), ("x", {"color": "blue"}), ("z", {"color": "red"})])
        G.add_edges_from([("y", "x"), ("z", "x")])
        #print(result.edges(data=True))
        #print(G.edges(data=True))
        assert nx.utils.graphs_equal(result, G)

    def test_bic_cherry_weak(self, bic_cherry_nw):
        result = bmg(bic_cherry_nw, mode="weak")
        G = nx.DiGraph()
        G.add_nodes_from([("y", {"color": "red"}), ("x", {"color": "blue"}), ("z", {"color": "red"})])
        G.add_edges_from([("y", "x"), ("z", "x"), ("x", "y"), ("x", "z")])
        #print(result.edges(data=True))
        #print(G.edges(data=True))
        assert nx.utils.graphs_equal(result, G)

    ### -- Test showing that same medium network results in different BMGs depending on definition --

    def test_medium_nw_strong(self, medium_two_color_nw):
        result = bmg(medium_two_color_nw, mode="strong")
        G = nx.DiGraph()
        G.add_nodes_from([("y", {"color": "red"}), ("y1", {"color":'red'}),
                          ("y2", {"color":'red'}), ("x", {"color":'green'})])
        G.add_edges_from([("y", "x"), ("y1", "x"), ("y2", "x")])
        # print(result.edges(data=True))
        # print(G.edges(data=True))
        assert nx.utils.graphs_equal(result, G)

    def test_medium_nw_weak(self, medium_two_color_nw):
        result = bmg(medium_two_color_nw, mode="weak")
        G = nx.DiGraph()
        G.add_nodes_from([("y", {"color": "red"}), ("y1", {"color": 'red'}),
                          ("y2", {"color": 'red'}), ("x", {"color": 'green'})])
        G.add_edges_from([("y", "x"), ("y1", "x"), ("y2", "x"), ("x", "y"), ("x", "y2")])
        # print(result.edges(data=True))
        # print(G.edges(data=True))
        assert nx.utils.graphs_equal(result, G)

# class tests that weak and strong definition give the same results for trees
class TestBMGInvariants:
    def test_weak_equals_strong_on_tree(self, medium_three_color_tree):
        T = medium_three_color_tree
        assert nx.utils.graphs_equal(bmg(T, mode="strong"), bmg(T, mode="weak"))

    # Test equality between weak and strong on random asymmetree
    def test_weak_equals_strong_on_asymmetree(self):
        # species tree
        S = te.species_tree_n_age(
            4, 1.0, contraction_probability=0.0, contraction_proportion=0.2, contraction_bias="exponential"
        )
        # gene tree
        T = te.dated_gene_tree(
            S, dupl_rate=1.0, loss_rate=0, hgt_rate=0.2, gc_rate=0.2, prohibit_extinction="per_species",
            dupl_polytomy=0.5
        )
        # prune all loss branches and the planted root
        observable_gene_tree = te.prune_losses(T)
        tree_to_nx = bmg_fun.convert_to_nx(observable_gene_tree)
        assert nx.utils.graphs_equal(bmg(tree_to_nx, mode="strong"), bmg(tree_to_nx, mode="weak"))


# Input tests (wrong network, wrong mode)
class TestInputVariants:
    # Test invalid mode
    def test_invalid_mode_raises(self, medium_three_color_tree):
        with pytest.raises(ValueError):
            bmg(medium_three_color_tree, mode="banana")
    # Test that undirected networkx graph is rejected
    def test_undirected_graph_raises(self):
        G = nx.Graph()  # undirected
        with pytest.raises(TypeError):
            bmg(G, {}, mode="strong")
    # Test that asymmetree is rejected
    def test_asymmetree_raises(self):
        # species tree
        S = te.species_tree_n_age(
            4, 1.0, contraction_probability=0.0, contraction_proportion=0.2, contraction_bias="exponential"
        )
        # gene tree
        T = te.dated_gene_tree(
            S, dupl_rate=1.0, loss_rate=0, hgt_rate=0.2, gc_rate=0.2, prohibit_extinction="per_species",
            dupl_polytomy=0.5
        )
        # prune all loss branches and the planted root
        observable_gene_tree = te.prune_losses(T)
        with pytest.raises(TypeError):
            bmg(observable_gene_tree, {}, mode="strong")