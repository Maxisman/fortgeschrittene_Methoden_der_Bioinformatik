import pytest
import networkx as nx
from bmg_Tony import bmg

# medium tree with three colors that can be shared across functions
@pytest.fixture
def medium_three_color_tree():
    """Hand-built tree: ((a,b),c) with sigma = {a:1, b:1, c:2}."""
    T = nx.DiGraph()
    T.add_nodes_from([("a1", {"reconc": "red"}), ("b1", {"reconc": "blue"}), ("c1", {"reconc": "green"}),
                      ("b2", {"reconc": "blue"}), ("c2", {"reconc": "green"})])
    T.add_edges_from([("p", "u"), ("u", "a1"), ("u", "w"), ("w", "b1"), ("w", "c1"), ("p", "v"), ("v", "b2"), ("v", "c2")])
    return T

# BMG of medium tree with three colors that can be shared across functions
@pytest.fixture
def medium_three_color_tree_expected_bmg():
    """Expected best-match graph for small_two_color_tree."""
    G = nx.DiGraph()
    G.add_nodes_from([("a1", {"reconc": "red", 'label': 'a1'}), ("b1", {"reconc": "blue", 'label': 'b1'}), ("c1", {"reconc": "green", 'label': 'c1'}),
                      ("b2", {"reconc": "blue", 'label': 'b2'}), ("c2", {"reconc": "green", 'label': 'c2'})])
    G.add_edges_from([("a1", "c1"), ("c1", "a1"), ("b1", "a1"), ("a1", "b1"), ("c2", "a1"), ("b2", "a1"), ("b1", "c1"), ("c1", "b1"),
                      ("b2", "c2"), ("c2", "b2")])
    return G

# BIC cherry network with two colors that can be shared across functions
@pytest.fixture
def bic_cherry_nw(): # example from bmg_in_networks paper
    """Hand-built tree: ((a,b),c) with sigma = {a:1, b:1, c:2}."""
    bic_cherry = nx.DiGraph()
    bic_cherry.add_nodes_from([("y", {"reconc": "red"}), ("x", {"reconc": "blue"}), ("z", {"reconc": "red"})])
    bic_cherry.add_edges_from([("p", "Pxy"), ("Pxy", "y"), ("Pxy", "x"), ("Pxy", "Qxz"), ("Qxz", "x"), ("Qxz", "z"),
                               ("p", "Pxz"), ("Pxz", "z"), ("Pxz", "x"), ("Pxz", "Qxy"), ("Qxy", "x"), ("Qxy", "y")])
    return bic_cherry

# Start of unit tests, separated by classes depending on topic
# class tests for self designed examples of trees and networks
class TestBMGKnownExamples:
    def test_small_two_color_tree(self):
        # create small tree wot two colors
        T = nx.DiGraph()
        T.add_nodes_from([("x", {"reconc": "red"}), ("y", {"reconc": "blue"})])
        T.add_edges_from([("p", "x"), ("p", "y")])
        # create corresponding bmg
        G = nx.DiGraph()
        G.add_nodes_from([("x", {"reconc": "red", 'label': 'x'}), ("y", {"reconc": "blue", 'label': 'y'})])
        G.add_edges_from([("x", "y"), ("y", "x")])
        # get result from bmg function
        result = bmg(T, mode="strong")
        assert nx.utils.graphs_equal(result, G)

    def test_small_three_color_tree(self):
        # create small tree with three colors
        T = nx.DiGraph()
        T.add_nodes_from([("x", {"reconc": "red"}), ("y", {"reconc": "blue"}), ("z", {"reconc": "green"})])
        T.add_edges_from([("p", "u"), ("p", "z"), ("u", "x"), ("u", "y")])
        # create corresponding bmg
        G = nx.DiGraph()
        G.add_nodes_from([("x", {"reconc": "red", 'label': 'x'}), ("y", {"reconc": "blue", 'label': 'y'}), ("z", {"reconc": "green", 'label': 'z'})])
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
        G.add_nodes_from([("y", {"reconc": "red", 'label': 'y'}), ("x", {"reconc": "blue", 'label': 'x'}), ("z", {"reconc": "red", 'label': 'z'})])
        G.add_edges_from([("y", "x"), ("z", "x")])
        #print(result.edges(data=True))
        #print(G.edges(data=True))
        assert nx.utils.graphs_equal(result, G)

    def test_bic_cherry_weak(self, bic_cherry_nw):
        result = bmg(bic_cherry_nw, mode="weak")
        G = nx.DiGraph()
        G.add_nodes_from([("y", {"reconc": "red", 'label': 'y'}), ("x", {"reconc": "blue", 'label': 'x'}), ("z", {"reconc": "red", 'label': 'z'})])
        G.add_edges_from([("y", "x"), ("z", "x"), ("x", "y"), ("x", "z")])
        #print(result.edges(data=True))
        #print(G.edges(data=True))
        assert nx.utils.graphs_equal(result, G)

# class tests that weak and strong definition give the same results for trees
class TestBMGInvariants:
    def test_weak_equals_strong_on_tree(self, medium_three_color_tree):
        T = medium_three_color_tree
        assert nx.utils.graphs_equal(bmg(T, mode="strong"), bmg(T, mode="weak"))
    #TODO: Add a random tree from Assymetree here as well

#TODO: Add input tests (wrong network, wrong mode) for example like:
    # def test_invalid_mode_raises(self, small_tree):
    # T, sigma = small_tree
        # with pytest.raises(ValueError):
# bmg(T, sigma, mode="banana")
    # def test_undirected_graph_raises(self):
    # G = nx.Graph()  # undirected
        # with pytest.raises(TypeError):
# bmg(G, {}, mode="strong")