# Best matches in Netzwerken

>[!note] Definition best match — strikt
>Gilt für ein Netzwerk $N$: $(N,\sigma), \, x,y\in L(N), \, \sigma (y) \ne \sigma(x)$, dann ist $y$ ein best match von $x$ wenn gilt: $\forall \, y': \sigma(y') = \sigma(y)$ existiert kein $u \in lca(x,y')$ sodass $u \prec v$ für ein $v \in lca(x,y)$.
>Formale Definition: $y$ ist BM für $x$ wenn $\forall y': \sigma(y) = \sigma(y'), \forall u \in lca(x,y'), v\in lca (x,y), u \nprec v$.

>[!warning] Definition best match — weak
>Hierfür müssen wir ein neues Set definieren. Für alle $x \in L(N)$ und $\tau \in \sigma(L(N)\backslash x)$ definieren wir:
>$$Q(x,\tau) \coloneqq \min_{\preceq} \{v\in lca(x,y):\sigma(y) = \tau\}$$
>$Q(x,\tau)$ ist also die Menge aller lcas zwischen $x$ und einem Blatt mit der Farbe $\tau$.
>Damit gilt für *weak best matches*: Gilt für ein Netzwerk $N$: $x,y\in L(N), \, \sigma (y) \ne \sigma(x)$, dann ist $y$ ein *weak* best match von $x$ wenn gilt: $lca(x,y) \cap Q(x,\sigma(y)) \ne \varnothing$.
>Das bedeutet, $y$ ist ein weak best match wenn es von $x$ aus über irgendeinen der lowest common ancestors zwischen $x$ und einem Blatt derselben Farbe wie $y$ erreichbar ist.

# Objectives
Compare the definition of best matches and weak best matches:
Check whether every best match in $(N, \sigma)$ is also a weak best match. Test this computationally, but also try to give a formal argument.

Computational tests sind z.B. in den unit tests für BMGs, aber dass die beiden auf Netzwerken nicht gleich sind ist klar. Wir haben allerdings keine tests dafür gemacht, ob jeder strikte best match auch immer ein weak best match ist. Allerdings sollte das immer der Fall sein, und warum das so ist zeigen wir jetzt formal.

## Formal argument for BM definitions
Wie bereits oben beschrieben, erstellen wir ein neues Set, welches die Menge aller last common ancestors zwischen einem bestimmten Blatt und einer anderen Farbe darstellt.
Für alle $x \in L(N)$ und $\tau \in \sigma(L(N)\backslash x)$ definieren wir:
$$Q(x,\tau) \coloneqq \min_{\preceq} \{v\in lca(x,y):\sigma(y) = \tau\}$$
Für die *weak* best matches haben wir dabei bereits definiert, dass: Gilt für ein Netzwerk $N$: $x,y\in L(N), \, \sigma (y) \ne \sigma(x)$, dann ist $y$ ein *weak* best match von $x$ wenn gilt: $lca(x,y) \cap Q(x,\sigma(y)) \ne \varnothing$.
Die Anforderung ist also, dass die Menge der last common ancestors von x und y eine Schnittmenge bildet mit der Menge Q.
Für die *strong* best matches definieren wir: Gilt für ein Netzwerk $N$: $x,y\in L(N), \, \sigma (y) \ne \sigma(x)$, dann ist $y$ ein *strong* best match von $x$ wenn gilt: $lca(x,y) \cap Q(x,\sigma(y)) \ne \varnothing$ und $u \nprec v \, \forall u \in Q(x,\sigma(y)), v\in lca (x,y)$. Sprich, es gilt die Bedingung für weak best matches, und die Zusatzbedingung dass die Menge der last common ancestors keine Node enthalten dürfen, die über irgendeiner node in Q liegt.
Die formale Definition zeigt direkt, dass alle strong best matches auch weak best matches sind, aber dass das nicht zwingend umgekehrt gelten muss. 


Beispiel zur Erklärung, warum der Unterschied in Netzwerken wichtig ist:
![[Screenshot From 2026-08-12 16-44-27.png|450]]
Nach der strengen (standard) Definition hat $x$ hier keinen best match der Farbe $\sigma(y)$, da $lca(x,y) = \{P_{xy}, Q_{xy}\}, \, lca(x,y') = \{P_{xy'}\}, \, lca(x,y'') = \{Q_{xy''}, P_{xy''} \}$, aber $Q_{xy} \prec P_{xy''}$ und $Q_{xy''}\prec P_{xy}$ und $Q_{xy''}\prec P_{xy'}$. In jeder Menge an lca gibt es also einen Knoten, der höher liegt als ein anderer lca.
Weak best match: $Q(x,\sigma(y)) = \min_{\preceq}\{P_{xy}, Q_{xy}, P_{xy'}, Q_{xy''}, P_{xy''}\} = \{Q_{xy}, Q_{xy''}\}$, demnach sind $y, y''$ *weak* best match von $x$.
Entfernt man die orange Edge $(P_{xy'}, Q_{xy''})$ dann ist nach der strengen Definition $y'$ best match von $x$ da nun $Q_{xy''}\nprec P_{xy'}$. Nach der schwachen Definition sind $y, y', y''$ alle *weak* best match von $x$, da $Q(x,\sigma(y)) = \{Q_{xy}, P_{xy'}, Q_{xy''}\}$


# Umsetzung in Python

```python
import networkx as nx
from bmg_Tony import bmg
```


```python
G = nx.DiGraph()
G.add_node("y", reconc='red')
G.add_node("y1", reconc='red')
G.add_node("y2", reconc='red')
G.add_node("x", reconc='green')
G.add_edge("rho", "Pxy")
G.add_edge("rho", "Pxy1")
G.add_edge("rho", "Pxy2")
G.add_edge("Pxy", "y")
G.add_edge("Pxy", "x")
G.add_edge("Pxy", "Qxy2")
G.add_edge("Pxy1", "y1")
G.add_edge("Pxy1", "x")
G.add_edge("Pxy1", "Qxy2") #remove this edge later
G.add_edge("Pxy2", "y2")
G.add_edge("Pxy2", "x")
G.add_edge("Pxy2", "Qxy")
G.add_edge("Qxy", "x")
G.add_edge("Qxy", "y")
G.add_edge("Qxy2", "x")
G.add_edge("Qxy2", "y2")
```


```python
pos = nx.kamada_kawai_layout(G)
nx.draw(G, pos, with_labels=True)
nx.draw(G, pos, nodelist=["y", "y1", "y2"], node_color="tab:red", with_labels=True)
nx.draw(G, pos, nodelist=["x"], node_color="tab:green", with_labels=True)
```


    
![png](output_2_0.png)
    



```python
BMG_network_tony_weak = bmg(G, mode= 'weak')
BMG_network_tony_strong = bmg(G, mode= 'strong')
```


```python
# weak definition
pos = nx.circular_layout(BMG_network_tony_weak)
nx.draw(BMG_network_tony_weak, pos, nodelist=["y", "y1", "y2"], node_color="tab:red", with_labels=True)
nx.draw(BMG_network_tony_weak, pos, nodelist=["x"], node_color="tab:green", with_labels=True)

```


    
![png](output_4_0.png)
    



```python
# strong definition
pos = nx.circular_layout(BMG_network_tony_strong)
nx.draw(BMG_network_tony_strong, pos, nodelist=["y", "y1", "y2"], node_color="tab:red", with_labels=True)
nx.draw(BMG_network_tony_strong, pos, nodelist=["x"], node_color="tab:green", with_labels=True)
```


    
![png](output_5_0.png)
    



```python
# Results with edge removed
G.remove_edge("Pxy1", "Qxy2") #remove this edge later
BMG_network_tony_weak = bmg(G, mode= 'weak')
pos = nx.circular_layout(BMG_network_tony_weak)
nx.draw(BMG_network_tony_weak, pos, nodelist=["y", "y1", "y2"], node_color="tab:red", with_labels=True)
nx.draw(BMG_network_tony_weak, pos, nodelist=["x"], node_color="tab:green", with_labels=True)

```


    
![png](output_6_0.png)
    



```python
BMG_network_tony_strong = bmg(G, mode= 'strong')
pos = nx.circular_layout(BMG_network_tony_strong)
nx.draw(BMG_network_tony_strong, pos, nodelist=["y", "y1", "y2"], node_color="tab:red", with_labels=True)
nx.draw(BMG_network_tony_strong, pos, nodelist=["x"], node_color="tab:green", with_labels=True)
```


    
![png](output_7_0.png)
    

