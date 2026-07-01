import pytest
import networkx as nx
from insert_hybrid import insertHybrid

@pytest.fixture
def clean_tree():
    G = nx.DiGraph()
    # Ein perfekter Baum: Jeder Knoten hat maximal 1 Parent
    G.add_nodes_from([
        (1, {"label": 1, "tstamp": 0.5, "dist": 0.0, "reconc": "A"}),
        (2, {"label": 2, "tstamp": 0.2, "dist": 0.3, "reconc": "A"}),
        (3, {"label": 3, "tstamp": 0.2, "dist": 0.3, "reconc": "A"}),
        (4, {"label": 4, "tstamp": 0.0, "dist": 0.2, "reconc": "A"}),
    ])
    G.add_edges_from([(1, 2), (1, 3), (2, 4)])
    return G


# 2. Der neue Test: Wird aus dem Baum ein Netzwerk?
def test_tree_becomes_network(clean_tree):
    """
    Prüft, ob der Ausgangsgraph ein reiner Baum ist (max 1 Parent pro Node)
    und nach der Hybridisierung zu einem Netzwerk wird (mind. 1 Node mit >1 Parents).
    """
    # Vorher-Check: Es darf keine Node mit mehr als 1 Parent geben (Baum-Eigenschaft)
    for node in clean_tree.nodes:
        # in_degree gibt die Anzahl der eingehenden Kanten (Parents) an
        assert clean_tree.in_degree(node) <= 1, f"Ausgangsgraph ist kein sauberer Baum bei Node {node}!"

    # Hybridisierung durchführen (1 Event)
    result_G = insertHybrid(clean_tree, i=1)

    # Nachher-Check: Es MUSS jetzt mindestens eine Hybrid-Node mit genau 2 Parents geben
    # Da label -> randomNode geht, hat randomNode nun 2 Parents.
    nodes_with_multiple_parents = [node for node in result_G.nodes if result_G.in_degree(node) > 1]
    
    assert len(nodes_with_multiple_parents) >= 1, "Das Netzwerk enthält keine Retikulation (keine Node mit >1 Parent)!"
    
    # Optionaler Zusatz-Check: Der eigentliche Hybrid-Knoten (event='H') wurde korrekt verdrahtet
    hybrid_nodes = [n for n, attr in result_G.nodes(data=True) if attr.get("event") == "H"]
    assert len(hybrid_nodes) == 1, "Die Hybrid-Node mit event='H' wurde nicht gefunden."


# 3. Die bisherigen Tests, angepasst an die .py-Struktur
def test_no_hybrid_events(clean_tree):
    result_G = insertHybrid(clean_tree, i=0)
    assert result_G.number_of_nodes() == clean_tree.number_of_nodes()
    assert result_G.number_of_edges() == clean_tree.number_of_edges()

def test_single_hybrid_event(clean_tree):
    result_G = insertHybrid(clean_tree, i=1)
    assert result_G.number_of_nodes() == clean_tree.number_of_nodes() + 1
    assert result_G.number_of_edges() == clean_tree.number_of_edges() + 2

def test_result_is_always_dag(clean_tree):
    result_G = insertHybrid(clean_tree, i=400)
    assert nx.is_directed_acyclic_graph(result_G)

# Test, dass keine unnötige Hybridisierung bei einem minimalen Baum eingefügt wird

def test_minimal_tree_cannot_hybridize():
    """
    Prüft, ob bei einem minimalen Baum (Root + 2 Blätter) kein Paar gefunden wird
    und die Funktion den Graphen unverändert zurückgibt, ohne abzustürzen.
    """
    # 1. Minimalen Baum aufbauen (Root -> 2 Blätter)
    minimal_tree = nx.DiGraph()
    minimal_tree.add_nodes_from([
        (1, {"label": 1, "tstamp": 0.5, "dist": 0.0, "reconc": "A"}), # Root
        (2, {"label": 2, "tstamp": 0.0, "dist": 0.5, "reconc": "A"}), # Leaf 1
        (3, {"label": 3, "tstamp": 0.0, "dist": 0.5, "reconc": "A"}), # Leaf 2
    ])
    minimal_tree.add_edges_from([(1, 2), (1, 3)])

    # 2. Funktion aufrufen (wir fordern 1 Event)
    result_G = insertHybrid(minimal_tree, i=1)

    assert nx.utils.graphs_equal(result_G, minimal_tree), "Der Graph wurde fälschlicherweise modifiziert!"