import networkx as nx
import random


def findCandidate(BMG: nx.DiGraph,x,y):
    # Suche nach einem besseren Match für x als y
    # zunächst wird geschaut, ob es einen Best Match für x gibt, der die egleiche Farbe wie y hat
    # wird davon keiner gefunden, wird Node z gewählt, mit gleicher Farbe wie y und dessen Best Match x ist
    # wenn davon keiner gefunden wird, wird irgendeine Node gewählt, die die gleiche Farbe wie y hat
    
    candidates = []
    candidates = [v for v in BMG.successors(x) if BMG.nodes[v]['color'] == BMG.nodes[y]['color'] and BMG.has_edge(v,x)]

    if not candidates:
        candidates = [v for v in BMG.successors(x) if BMG.nodes[v]['color'] == BMG.nodes[y]['color']]

    if not candidates:
        candidates = [v for v in BMG.predecessors(x) if BMG.nodes[v]['color'] == BMG.nodes[y]['color'] and v != y]

    if not candidates:
        candidates = [v for v in BMG.nodes if BMG.nodes[v]['color'] == BMG.nodes[y]['color'] and v != y]

    z = random.choice(candidates)

    # candidates = [
    #     z
    #     for z in BMG.successors(x)
    #     if BMG.nodes[z]["color"] == BMG.nodes[y]["color"]
    # ]
    # if not candidates:
    #     candidates = [
    #         z
    #         for z in BMG.predecessors(x)
    #         if BMG.nodes[z]["color"] == BMG.nodes[y]["color"] and z != y
    #     ]
    # if not candidates:
    #     candidates = [
    #         z
    #         for z in BMG.nodes()
    #         if BMG.nodes[z]["color"] == BMG.nodes[y]["color"] and z != y
    #     ]

    # z = random.choice(candidates)
    return z

def insertNode(BCN: nx.DiGraph,layer: int, namePrev, x, z):

    # hier muss noch ein umwandeln von layer(int) ind layer(str) stattfunden. 
    nameNew = f"{layer}_{x}_{z}"
    BCN.add_edge(namePrev, nameNew)
    BCN.add_edge(nameNew, x)
    BCN.add_edge(nameNew, z)
    if BCN.has_edge(namePrev,x):
        BCN.remove_edge(namePrev,x)

    return nameNew



def MultiLayerdBICCherry(BMG: nx.DiGraph, maxLayers: int = 20):
    BCN = nx.DiGraph()
    BCN.add_node("rho")

    cherryPs = {}
    currentDict = {}
    nextDict = {}
    for leaf in BMG.nodes():
        BCN.add_node(leaf, color= BMG.nodes[leaf]["color"], label=leaf)
    
    if len(BMG.nodes()) == 2:
        for leaf in BMG.nodes():
            BCN.add_edge("rho", leaf)
        return BCN

    # P-Layer
    for x, y in itertools.combinations(BMG.nodes(), 2):
        if BMG.nodes[x]["color"] != BMG.nodes[y]["color"]:
            p_name = f"p_{x}_{y}"
            BCN.add_edge("rho", p_name)
            BCN.add_edge(p_name, x)
            BCN.add_edge(p_name, y)
            cherryPs[(x, y)] = p_name

    # Q-Extensions
    for (x, y), p_name in cherryPs.items():

        if not BMG.has_edge(x,y):
            z = findCandidate(BMG, x, y)
            nodeName = insertNode(BCN, 1, p_name, x, z)
            currentDict[(x,z)] = nodeName

        if not BMG.has_edge(y,x):
            z = findCandidate(BMG, y, x)
            nodeName = insertNode(BCN, 1, p_name, y, z)
            currentDict[(y,z)] = nodeName

    # lower leayers
    # Es werden die gerade eingefügten Kanten (x->y) untersucht, ob diese einen Best-Match (y->x) generiert haben, der gar nicht da sein sollte.
    # Ist dies der Fall, wird für y->x eine neue Ebene eingefügt um diese zu trennen

    # Problem: neue Kanten nicht eindeutig benannt. Wenn x,y1 und x,y2 fälschlicherweise noch vorhanden sind, und beide durch x,z gelöst werden,
    # so sollte es zwei neue Knoten geben, allerdings entsteht hier nur ein neuer: layer_x_z

    # (BMG.edges() - bmg(BCN).edges())
    for layer in range(2,maxLayers):
        currentBMG = bmg(BCN)
        if nx.utils.graphs_equal(BMG, currentBMG):
            break

        
        for (x,y), prevName in currentDict.items():
            if not BMG.has_edge(y,x):
                z = findCandidate(BMG, y, x)
                nodeName = insertNode(BCN, layer, prevName, y, z)
                nextDict[(y,z)] = nodeName

        currentDict = nextDict
        nextDict = {}

    return BCN
