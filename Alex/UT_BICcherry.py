import pytest
import networkx as nx
from BICcherry import BICcherry
import random

#Ass-sertion tests

def test_rejects_non_digraph():
    with pytest.raises(AssertionError):
        BICcherry("I am *not* an nx.digraph :))")

def test_rejects_nocolornode():
    G = nx.DiGraph()

    for i in range(6):
        G.add_node(i, color=random.choice(["red", "yellow", "blue"]))

    del G.nodes[random.randint(0,5)]["color"]

    with pytest.raises(AssertionError):
        BICcherry(G)


def test_rejects_sicor_nohub():
    G = nx.DiGraph()
    G.add_node('a', color='red')
    G.add_node('b', color='red')
    G.add_node('c', color='blue')  # sicor — only blue

    G.add_edge('a', 'c')  # a points to c
    # b does NOT point to c — sicor not an in-hub
    G.add_edge('c', 'a')
    G.add_edge('c', 'b')

    with pytest.raises(AssertionError):
        BICcherry(G)

#con-struct-est

def test_root_exists():
    G = nx.DiGraph()
    G.add_node('x', color='red')
    G.add_node('y', color='blue')
    G.add_edge('x', 'y')
    G.add_edge('y', 'x')
    N = BICcherry(G)
    assert 'rho' in N.nodes()
    assert N.in_degree('rho') == 0

def test_output_is_dag():
    G = nx.DiGraph()
    G.add_node('x', color='blue')
    G.add_node('y', color='red')
    G.add_node('z', color='red')
    G.add_edge('y', 'x')
    G.add_edge('z', 'x')
    G.add_edge('x', 'z')
    N = BICcherry(G)
    assert nx.is_directed_acyclic_graph(N)

def test_no_extensions_complete_multipartite():
    G = nx.DiGraph()
    G.add_node('a', color='red')
    G.add_node('b', color='blue')
    G.add_node('c', color='green')
    G.add_edge('a', 'b'); G.add_edge('a', 'c')
    G.add_edge('b', 'a'); G.add_edge('b', 'c')
    G.add_edge('c', 'a'); G.add_edge('c', 'b')
    N = BICcherry(G)
    q_nodes = [n for n in N.nodes() if str(n).startswith('q_')]
    assert len(q_nodes) == 0

def test_q_count_five_leaves():
    G = nx.DiGraph()
    G.add_node('a', color='red')
    G.add_node('b', color='red')
    G.add_node('c', color='blue')
    G.add_node('d', color='blue')
    G.add_node('e', color='green')
    G.add_edge('a', 'c'); G.add_edge('a', 'd'); G.add_edge('a', 'e')
    G.add_edge('b', 'c'); G.add_edge('b', 'e')
    G.add_edge('c', 'a'); G.add_edge('c', 'b'); G.add_edge('c', 'e')
    G.add_edge('d', 'a'); G.add_edge('d', 'e')
    G.add_edge('e', 'a'); G.add_edge('e', 'c')
    N = BICcherry(G)
    q_nodes = [n for n in N.nodes() if str(n).startswith('q_')]
    assert len(q_nodes) == 4

def test_p_count_five_leaves():
    G = nx.DiGraph()
    G.add_node('a', color='red')
    G.add_node('b', color='red')
    G.add_node('c', color='blue')
    G.add_node('d', color='blue')
    G.add_node('e', color='green')
    G.add_edge('a', 'c'); G.add_edge('a', 'd'); G.add_edge('a', 'e')
    G.add_edge('b', 'c'); G.add_edge('b', 'e')
    G.add_edge('c', 'a'); G.add_edge('c', 'b'); G.add_edge('c', 'e')
    G.add_edge('d', 'a'); G.add_edge('d', 'e')
    G.add_edge('e', 'a'); G.add_edge('e', 'c')
    N = BICcherry(G)
    p_nodes = [n for n in N.nodes() if str(n).startswith('p_')]
    # 2 red × 2 blue + 2 red × 1 green + 2 blue × 1 green = 4 + 2 + 2 = 8
    assert len(p_nodes) == 8