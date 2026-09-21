import numpy as np
import networkx as nx
import asymmetree.treeevolve as te
import asymmetree.analysis.best_matches as bm
from BICcherry import BICcherry as BC
from BICcherryRestrict import BICcherryRestrict as BCR
import tralda
import random
from collections import defaultdict

random.seed(42)

# species tree
ST=te.species_tree_n(3)
# gene tree
GT=te.dated_gene_tree(ST, dupl_rate=.2,)

## optimize leaf count
while True:
    GT = te.prune_losses(te.dated_gene_tree(ST, dupl_rate=.2))
    if 4 <= len(list(GT.leaves())) <= 6: break

#BMG
BMG = bm.bmg_from_tree(GT)

#LRT from gene tree
LRT = bm.lrt_from_tree(GT)

#LRT from BMG
BMG_LRT = bm.lrt_from_colored_graph(BMG)

## test isomorphism
print(LRT.equal_topology(BMG_LRT))

#Build Network N via BC from BMG
N = BC(BMG)

# toy: two triangles joined by a bridge
U = nx.Graph([('a','b'),('b','c'),('a','c'),
              ('c','d'),                     # the bridge
              ('d','e'),('e','f'),('d','f')])

nx.draw(U)
nodes = list(U.nodes)
L = nx.laplacian_matrix(U, nodelist=nodes).toarray()
w, V = np.linalg.eigh(L)

print('     ' + '  '.join(f'{n:>6}' for n in nodes))
for k in range(len(nodes)):
    print(f'{w[k]:5.2f} ' + '  '.join(f'{V[i,k]:6.2f}' for i in range(len(nodes))))