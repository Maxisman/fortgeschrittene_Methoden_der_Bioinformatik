Ablauf: Die ersten paar Stunden Theorie, dann Projektarbeit in Gruppen von max 4 Leuten
Prüfung: Mündlich, pro Gruppe. Jeder bekommt 1-2 theoretische Fragen zu Beginn, dann max 25 Minuten Projektvorstellung: zeigen, dass die software funktioniert, Probleme besprechen und Lösungen zeigen.
Hauptthema der Projektarbeiten: Best match graphs in phylogenetic networks (erlaubt Hybride)

# Definitionen Bäume
## Gewurzelte Bäume
Gewurzelte Bäume werden mit $T$ bezeichnet, die Wurzel (root) mit $\varrho$.
![[Screenshot From 2026-08-08 16-02-18.png|700]]

Nomenklatur:
L(T): Menge der Blätter
E(T): Menge der Kanten
V(T): Menge der Knoten
V°(T): V(T)\L(T)

Halbordnung auf der Knotenmenge V(T):
$u\le v \Leftrightarrow$ v liegt auf dem (eindeutigen) **Pfad** von $\varrho$ nach u
$\varrho \ge x$ für alle $x \in V(T)$
$u<v \Leftrightarrow u\le v \text{ mit } u \ne v$

Die drei Regeln der Halbordnung:
i) $u \le u \, \forall u \in V(T)$
ii) $u\le v \land v\le u \Rightarrow u=v$
iii) $u\le v, v\le w \Rightarrow u\le w$

>[!note] Definition **Least common ancestor**
>Least common ancestor ist der minimale Knoten $Z$, so dass $Z\ge x$ für alle $x \in A$, geschrieben als $lca(A)\in V(T)$.
>Der LCA kann für Paare und Mengen von Knoten definiert werden.
>Der LCA ist immer eine Menge, aber wir schreiben: $lca(\{x,y\}) \eqqcolon lca (x,y)$
>![[Screenshot From 2026-08-08 16-21-26.png|500]]

**Kinder**
Kinder sind eine Menge von Knoten $ch(x) = \{ y\in V \backslash y<x, xy\in E(T)\}$. Die Kinder sind also alle Knoten, die eine Kante zu x haben, aber in der Hierarchie tiefer stehen.
**Teilbaum**
Beschrieben als T(x) für den Teilbaum von T der gewurzelt ist in $x \in V\degree (T)$ (die Wurzel eines Teilbaumes kann also kein Blatt von T sein). Wir sagen: "T(L) is displayed in T".

## Phylogenetische Bäume

>[!note] Definition phylogenetischer Baum
>Ein gewurzelter Baum T ist phylogenetisch wenn es keinen inneren Knoten $u\in V\degree(T)$ mit nur einem Nachfolger/ Kinder gibt.
>Beispiel: Wenn $x \in V\degree(T)$, dann gibt es mindestens zwei Kinder von $z$: $x_1, x_2 \in ch(z)$, sodass $lca(L(T(z)))=z$ (sprich, der LCA aller Blätter des Teilbaumes mit der Wurzel $z$ ist die Wurzel $z$ selbst).

$$\begin{align}
&\exists u_1, u_2 \in L(T) \text{ s.d. } lca(\{u_1,u_2\}) = v\\
&u_1 \in L(T(x_1))\\
&u_2 \in L(T(x_2))
\end{align}$$
![[Screenshot From 2026-08-08 16-36-18.png|500]]

Sei ein Baum T gegeben mit $L(T)$ und $L' \subseteq L(T)$.
![[Screenshot From 2026-08-08 16-40-20.png|500]]
$T^*(L')$ ist als Teilbaum von T definiert durch die Pfade von $\varrho$ zu $x \in L'$. Aber: dieser Teilbaum ist kein phylogenetischer Baum, da manche innere Knoten nur ein Kind haben. Lösung: wandle solche inneren Knoten in Kanten um, bzw entferne diese Knoten.
**Hinweis**: Es gilt stets zu überprüfen dass die Bedingung für phylogenetische Bäume erfüllt bleibt, sprich dass alle inneren Knoten immer zwei Kinder haben.

**Hierarchien**
Wir nutzen $\preceq$ um die partielle Ordnung auf $V(T)$ zu definieren. Sie ist definiert durch $x\preceq y$ wenn $y$ auf dem einzigartigen Weg von der Wurzel zu $x$ liegt. Die Blätter sind die minimalen Elemente, die Wurzel ist das einzige maximale Element und $lca(x,y)$ ist der $\preceq$-minimale Vertex in $V(T)$, der sowohl $x\preceq lca(x,y)$ wie auch $y\preceq lca(x,y)$ einhält. Beispiel: $L(T(u)) \subseteq L(T(v)) \Rightarrow u\preceq v$.
Hierarchien von $L$ ist ein Mengensystem $\mathcal{H}\subseteq 2^L$, welches durch ein Hasse-Diagramm (die Knoten sind die Mengen) entspricht. Beispiel $\mathcal{H}=\{\{a\},\{b\},\{c\},\{a,b\},\{a,b,c\}\}$.


>[!note] Definition **Triples**
>$xy|z$ ist ein Triple in T wenn der Pfad von $x$ nach $y$ in T den Pfad von $varrho$ nach $z$ *nicht* schneidet.
>$$xy|z \text{ ist ein Triple in T } \Leftrightarrow lca(x,y) {\color{orange}<} lca (x,z), lca(y,z)$$
>![[Screenshot From 2026-08-08 16-48-10.png|500]]
>Da nur Blätter label tragen, ist $((x,y),z)$ in $T$ gleichbedeutend mit $xy|z \in T$. Außerdem gilt $xy|z = yx|z$.
>R(T) ist die Menge aller Triple in T. Über diese Menge können Bäume häufig zusammengesetzt werden.

**Kompatibilität von Triples**
Gegeben ist eine Menge R von Triples über L. R ist kompatibel $\Leftrightarrow \exists$ Baum T sodass T alle Triple in R enthält. Kompatibilität zu überprüfen ist einfach, alle nicht kompatiblen Tripel aus der Menge zu entfernen ist schwierig.
Beispiel:
![[Screenshot From 2026-08-08 17-00-59.png]]

>[!note] BUILD(R,L) Algorithmus zum Bauen eines trees aus triples
>R steht hier wieder für die Menge der triples, L für die Menge der Blätter (leafs)
>Zusammenhangskomponente $Z_i$ von Hilfsgraph H $\Leftrightarrow L(T(x_i)), x_i \in ch(\varrho)$.
>for each $Z_i$: BUILD$(R_{Z_i}, L(Z_i))$
>Kompatibilitätsfrage $\sigma (|L|\cdot |R|) \rightarrow \text{ (Anzahl triple)}$
>Hilfsgraph: Es darf keine Kanten zwischen den Teilkanten geben.
>Die Zerlegung in die Zusammenhangskomponenten erzeugt einen sogennanten Aho(R,L) Baum, was auch bedeutet, dass es einen durch R eindeutig definierten Baum gibt. Ansonsten ist das Ergebnis *incompatible* (nicht kompatibel).

**Supertree**
$$\begin{align}
&\{(T_i, i=1\ldots k)\}\\
&L(T_i) = L_i\\
&R\coloneqq \bigcup_{i=1}^k R(T_i), L_i = \bigcup_{i=1}^k L_i\\
&BUILD(R,L) = \begin{cases} notcompat. \\ Aho(R) \end{cases}
\end{align}$$
Wird zusammengesetzt aus einer Menge von Teilbäumen, die durch Mengen von Triples und Blättern definiert sind.

# Eigenschaften Graphen
## Best matches von Bäumen
Werden genutzt für evolutionäre Szenarien wie "gene family histories". Man unterscheidet zwischen species Baum $S$ und Gen Baum $T$.
Beispielabbildung, der Artenbaum ist die "Röhre", der Genbaum die Kanten und Knoten darin.
![[Screenshot From 2026-08-08 17-21-33.png]]

Ist $x\in V(T)$, dann ist $\sigma (x) \in S$ die Spezies, in der das Gen $x$ gefunden wurde. Die Sigma-Funktion gibt also die Spezies eines Knotens an.

>[!note] Definition **Best match**
>$y$ ist ein best match von $x$ wenn $\sigma(y)\ne \sigma(x)$ und $\forall y$ mit $\sigma(y) = \sigma(y')$ gilt $lca(x,y')\ge lca(x,y)$. Sprich, hat Knoten $x$ eine andere Spezies als $y$, und LCA aller anderen Knoten dergleichen Farbe wie $y$ und $x$ sind in der Hierarchie gleich oder über dem $lca(x,y)$, dann ist $y$ ein best match von $x$.

**Best Match Graph**
$BMG(T,\sigma)$ ist der Graph mit Knotenmenge $L(T)$ und gerichteten Kanten $(x,y) \Leftrightarrow y$  ist best match für $x$.
Beispielabbildung:
![[Screenshot From 2026-08-08 17-30-28.png|250]]

Problem: In Netzwerken sind LCA nicht klar definiert, deshalb gestaltet sich das hier schwieriger. Wir wollen: Modifikationen der Netzwerke, sodass eine Erklärung als Baum gefunden wird (wenn sie denn existiert).

>[!example] Eigenschaften von BMGs
>1. Best match Graphen $(G,\sigma)$ sind color-sink-free, für jedes $x$ gibt es eine Kante $(x,y)$ für jede Farbe $\sigma(y) \ne \sigma(x)$.


>[!danger] BMGs sind sicht erblich (hereditary)!
>![[Screenshot From 2026-08-10 13-26-17.png|400]]


>[!abstract] Summary Best Match Graphen
>A best match relation can be represented as a vertex colored graph $G(T, \sigma)$ with vertex set $V (G) = L$, vertex colors $\sigma(x)$ for all $x \in L$, and directed edges $(x, y) \in E(G)$ if and only if $y$ is a best match $x$.
>Note that by definition every gene $x$ with color $\sigma(x)$ has a best match in every other species, i.e., for all colors/species $\sigma '$ , there is a best match $y$ of $x$ with $\sigma(y) = \sigma'$ . A graph with this propery is called *color sink-free*.
>A vertex-colored graph $(G, \sigma)$ is called a best match graph (BMG) if there is leaf-colored tree $(T, \sigma)$ such that $(G, \sigma)$ corresponds to the best match relation derived from $(T, \sigma)$.

## Nachbarschaften
Ausgehende Nachbarn (out-neighbours)
$N(x) = \{y|(x,y) \in E (\xi) \}$
Eingehende Nachbarn (in-neighbours)
$N^-(x) = \{y|(y,x) \in E (\xi) \}$
![[Screenshot From 2026-08-10 14-06-16.png|300]]

**Dünnheit**
Eine reine Äquivalenz-Relation. Die Knoten haben dieselben eingehenden und ausgehenden Kanten, und können formal nicht unterschieden werden.
$x \mathrel{\dot\sim} y \Leftrightarrow N(x) = N(y) \land N^{-} (x) = N^{-} (y)$
Ist $\alpha$ eine Dünnheitsklasse ($\mathrel{\dot\sim}$ KLasse), dann gilt $N(\alpha) = N(x) \, \forall x\in\alpha$.
Äquivalenz-Relation: gilt $x_1 \mathrel{\dot\sim} x_2, y_1 \mathrel{\dot\sim} y_2$, dann ist $y_1$ best match von $x_1\Leftrightarrow y_2$ ist best match von $x_2$
![[Screenshot From 2026-08-10 14-07-16.png|150]]

Sei $G$ der BMG $(T,\gamma)$, dann gilt 
$$\varrho_\alpha\coloneqq \max_{\substack{x\in\alpha\\ y\in N(\alpha)}} lca(x,y)$$
Daraus folgt $N(\alpha) \preceq \varrho_{\alpha}$. Ist $\beta \subseteq N(\alpha) \Rightarrow \varrho_\beta \preceq \varrho_\alpha$. 
Gilt $\alpha \subseteq N(\beta) \land \beta \subseteq N(\alpha) \Rightarrow \varrho_\alpha = \varrho_\beta$. Anderersets gilt $\alpha \subseteq N(\beta) \land \beta \cap N(\alpha)=\varnothing \Rightarrow \varrho_\alpha \prec \varrho_\beta$. Gilt allerdings $\alpha \cap N(\beta) = \beta \cap N(\alpha)=\varnothing$, dann ist $\varrho_\beta$ mit $\varrho_\alpha$ in $T$ unvergleichbar.
## 2-BMGs
2-BMGs (2-fach best match graphs): Einschränkung eines best match Graphen auf zwei Farben (bipartite). Der induzierte Teilgraph $G(x\in V| \sigma(x) \in \{\alpha,\beta\})$ ist also wieder ein BMG. Sie sind ebenfalls color-sink-free $N(x) \ne \varnothing$.

>[!example] Eigenschaften von 2-BMGs
>(N0) $N(x) \ne \varnothing$ — nicht erblich!
>(N1) $\alpha \cap N(\beta) = \beta \cap N(\alpha) = \varnothing \Rightarrow N(\alpha) \cap N(N(\beta)) = N(\beta) \cap N(N(\alpha))=\varnothing$
>(N2) $N(N(N(\alpha))) \subseteq N(\alpha)$
>(N3) $\alpha \cap N(N(\beta)) = \beta \cap N(N(\alpha)) = \varnothing$ und $N(\alpha) \cap N(\beta) \ne \varnothing \Rightarrow N^{-}(\alpha) = N^{-}(\beta)$ und $N(\alpha) \subseteq N(\beta)$ oder $N(\beta) \subseteq N(\alpha)$ Wenn die best matches von zwei Klassen überlappen, dann enthält eine die andere oder beide sind gleich.
>(N3') $N(\alpha) \cap N(\beta) \ne \varnothing \Rightarrow N(\alpha) \subseteq N(\beta) \text{ oder } N(\beta) \subseteq N(\alpha)$

$2BMG \Leftrightarrow (N0), (N1), (N2), (N3')$
$2QBMG \Leftrightarrow (N1), (N2), (N3')$: quasi best match graph, erblich!

**Redundanz von Kanten**
Sei $e=uv$ eune unnere Kante in $T$. $e$ ist redundant, wenn der Baum $T_e$, der aus $T$ durch Kontraktion von $e$ ensteht, wieder ein Baum für den gleichen BMG ist $BMG(T_e,\sigma) = BMG(T,\sigma)$. Sind $e,f$ redundant in $T$ gilt $BMG(T_e,\sigma) = BMG(T_f,\sigma) = BMG(T,\sigma) \Rightarrow BMG(T_{\{e,f\}}, \sigma)= BMG(T,\sigma)$.

**Least-resolved tree**
Wenn $(G,\sigma)=BMG(T,\sigma)$ dann existiert ein eindeutiger least-resolved tree $T^{*}$ mit $(G,\sigma) = BMG(T^{*},\sigma)$. Alle Bäume, die den BMG erklären, kann man aus dem least-resolved tree bekommen, indem redundante Kanten eingefügt werden. Enthält $T^{*}$ Knoten mit mehr als zwei Kindern, ist kein aufgelöster Binärbaum möglich.

**Erreichbare Menge (reachable sets)**
Reachable sets ist die Menge, die von einem bestimmten Knoten oder von einer Dünnheitsklasse aus erreichbar ist $R(\alpha) = \alpha \cup N(\alpha) \cup N(N(\alpha)) \cup \ldots$. Aufgrund von der Eigenschaft (N2), reicht in unseren Fällen folgende Definition für die reachable sets aus: $R(\alpha)= \alpha \cup N(\alpha) \cup N(N(\alpha))$.
Die reachable sets sollten bereits sehr nahe an der Hierarchie sein, die den endgültigen Baum ergibt. Allerdings gibt es da noch ein paar Probleme.
>[!danger] Das reachable set R und die Menge aller triples R benutzen dieselben Buchstaben!

Ein Problem ist beispielsweise, wenn Knoten existieren, die nur durch sich selbst erreicht werden können, sprich $W=\{\alpha| N^{-}(\alpha) = \varnothing\}$. Beispiel mit Baum oben und BMG unten:
![[Screenshot From 2026-08-10 18-31-02.png|200]]
Problem formal beschrieben: Sei $(G,\sigma)$ ein 2-farbiger Graph, der (N0), (N1), (N2) & (N3) erfüllt, dann ist $\{R(\alpha)\}$ eine Hierarchie von $L \backslash (\bigcup_{\alpha \in W}\alpha)$, für $W=\{\alpha| N^{-}(\alpha) = \varnothing\}$.

$$\begin{align}
Q(\alpha) \coloneqq & \{ x\in L | \exists \beta: x\in \beta, N^{-} (\beta) = N^{-}(\alpha), N(\beta) \subseteq N(\alpha)\}\\
\Rightarrow & \alpha \subseteq Q(\alpha)\\
\Rightarrow & \beta \subseteq Q(\alpha) \Rightarrow \sigma(\alpha) = \sigma(\beta) \land Q(\beta) \subseteq Q(\alpha) \land R(\alpha) \subseteq R(\beta)\\
& \alpha \cap N(\beta) = \varnothing \Rightarrow Q(\alpha) \cap N(\beta) = \varnothing\\
& \alpha \cap N(N(\beta)) = \varnothing \Rightarrow Q(\alpha) \cap N(N(\beta)) = \varnothing
\end{align}$$
Erklärung zur Definition:
$Q(\alpha)$ ist die Vereinigung aller Blätter aus Klassen $\beta$ **gleicher Farbe** wie $\alpha$, die **exakt dieselbe In-Nachbarschaft** haben wie $\alpha$, und deren Out-Nachbarschaft eine **Teilmenge** der von $\alpha$ ist.
Problem, das damit angegangen wird: Wenn zwei verschiedene $\mathrel{\dot\sim}$-Klassen $\beta, \gamma$  **dieselbe In-Nachbarschaft** haben $N^-(\beta) = N^-(\gamma)$, dann landen sie im $R(\alpha)$-Hierarchie-Baum $T(\mathcal{H})$ am **selben Knoten** — sie sind dort ununterscheidbar, obwohl sie im tatsächlich erklärenden Baum $T$ an unterschiedlichen Stellen (unterschiedlich tief geschachtelt) sitzen müssen, wenn ihre Out-Nachbarschaften unterschiedlich groß/verschachtelt sind (eine ist Teilmenge der anderen).
$Q(\alpha)$ fängt genau diese Fälle ein: Für jede Klasse $\beta$ mit gleicher In-Nachbarschaft wie $\alpha$, aber "schmalerer" (Teilmengen-)Out-Nachbarschaft, wird $\beta$ **unter** $\alpha$ eingeordnet — $\beta$ ist die "spezifischere" Klasse und muss im Baum tiefer/innerhalb von $\alpha$ liegen. So bekommt man die zusätzliche Auflösung, die $R(\alpha)$ allein nicht liefert.

Daraus ergibt sich folgendes:
Def: $R'(\alpha) \coloneqq R(\alpha) \cup Q(\alpha)$
Thm: $\mathcal{H}' \coloneqq \{R'(\alpha) \}$ ist eine Hierarchie von $L$. Durch Hasse $(\mathcal{H}')=T^{*}$. Sprich, wenn das eine HIerarchie ist, bekomme ich einen Baum. Im schlimmsten Fall erklärt der meinen Graphen nicht.

Grober Ablauf des Algorithmus:
1. Bestimmen der Dünnheitsklassen $\mathrel{\dot\sim}$
2. Bestimmung der erreichbaren Mengen $R$
3. Bestimmung von $Q$ (kann in $O(n^3)$ ermittelt werden)
4. Berechnen von $R'$ (Hierarchie, die wir haben wollen)
5. Hasse Diagramm
6. Prüfen, ob $BMG(T^*, \sigma) = (G,\sigma)$ tatsächlich gilt — nur dann war $(G,\sigma)$ wirklich ein 2-cBMG, und $T^*$ ist sein eindeutiger least-resolved tree

### Informative und verbotene Triples
Die Triples können mithilfe des BMGs bestimmt werden.
Beispiel für vier informative triples, die alle denselben (Teil-)Baum ergeben:
![[Screenshot From 2026-08-10 19-22-34.png]]

>[!note] $R(G,\sigma)$ ist die Menge aller informativen Triples
>$$R(G,\sigma)\coloneqq \{ab|b':\sigma(a) \ne \sigma(b) = \sigma (b'), (a,b) \in E(G), (a,b') \notin E(G)\}$$
>Beispiel:
>![[Screenshot From 2026-08-11 12-08-06.png|150]] $R=\{12|3, 12|4, 12|5, 45|1, 45|2, 45|3, 34|1\}$ 

Die Konsistenz von Triples ist ebenfalls erblich.

Der Aho ist der least-resolved tree von $(G,\sigma) \Leftrightarrow BMG(Aho(R(G,\sigma)), \sigma) = (G,\sigma)$. Diese Aussage stimmt für alle Paare von Farben. Setzt man die 2-cBMGs zusammen, erweitert man so auf mehr als zwei Farben.

>[!note] $F(G,\sigma)$ ist die Menge aller verbotenen Triples
>$$F(G,\sigma)\coloneqq \{ab|b':\sigma(a) \ne \sigma(b) = \sigma (b'), b\ne b', (a,b) , (a,b') \in E(G)\}$$
>$F$ enthält also $xy|z \notin T$.

$(R,F)$ sind zulässig genau dann wenn ein Baum $T$ existiert. $ab|b' \in R$ ist in $T$ enthalten, $ab|b' \in F$ ist kein Triple in $T$.
$(G,\sigma)$ ist ein QBMG $\Leftrightarrow (R(G,\sigma),F(G,\sigma))$ ist zulässig (admissible).
$(G,\sigma)$ ist ein BMG $\Leftrightarrow (R(G,\sigma),F(G,\sigma))$ ist zulässig und $(G,\sigma)$ ist color sink-free.

>[!abstract] Short summary
>A graph $(G, \sigma)$ is a BMG if and only if $(G, \sigma)$ is color-sink-free and $(R, F)$ is consistent. In this case, the so-called Aho-tree $T_R(R,F)$ is the unique least resolved tree explaining $(G, \sigma)$.


# Phylogenetische Netzwerke
Entstehen durch zusätzliche events wie introgression oder hybrid-events. Werden oft als gewurzelte, gerichtete azyklische Graphen (rooted directed acyclic graph (DAG)) dargestellt.
![[Screenshot From 2026-08-11 12-42-02.png|150]] 
In Bäumen wie Netzwerken gilt: $u\preceq v \Leftrightarrow \exists$ Pfad von $\varrho$ nach $u$ auf dem $v$ liegt. In Bäumen gilt zusätzlich $u \preceq v \land u \preceq w \Rightarrow v\preceq w \lor w\preceq v$. Diesen Rückschluss kann man in Netzwerken *nicht* mehr machen. Wir können damit nur abschätzen ob $v$ und $w$ vergleichbar sind oder nicht.

>[!note] Blätter in gewurzelten DAGs
>$$L(N) = \{x| \nexists y: y\preceq x, y \ne x\}$$
>Sprich $x\in L(N)$ wenn $x$ keine ausgehende Kante hat.

Definition von phylogenetischen Netzwerken nach [Gambette, Huber & Kelk (2027)](https://link.springer.com/article/10.1007/s00285-016-1068-3)
A _phylogenetic network_ _N_ _on_ _X_ is a rooted DAG whose set of leaves is _X_, and every interior vertex _v_ of _N_ except the root $\varrho_N$ is either (i) a _split vertex_ of _N_, that is, $indeg(v)=1$ and $outdeg(v)\ge 2$ or (ii) a _hybrid vertex_ of _N_, that is, $indeg(v) \ge 2$ and $outdeg(v)\ge 1$. 


>[!warning] Least common ancestors in gewurzelten DAGs
>$$lca(x,y) = \min_\preceq\{z|x\preceq z, y \preceq z\}$$
>Wir suchen also die Menge aller kleinsten (in der Hierarchie) gemeinsamen Vorfahren von $x$ und $y$. In dem Beispielbild wären alle gemeinsamen Vorfahren von $(a,b)$ $\{x,y,\varrho\}$, aber nur $x,y$ wären die minimalen (und damit die lca).
>![[Screenshot From 2026-08-11 12-59-36.png|150]]
>Es gilt: sind $u,v \in lca(x,y)$ und $u \ne v$, dann sind $u,v$ unvergleichbar.

## Best matches in Netzwerken

>[!note] Definition best match — strikt
>Gilt für ein Netzwerk $N$: $(N,\sigma), \, x,y\in L(N), \, \sigma (y) \ne \sigma(x)$, dann ist $y$ ein best match von $x$ wenn gilt: $\forall \, y': \sigma(y') = \sigma(y)$ existiert kein $u \in lca(x,y')$ sodass $u \prec v$ für ein $v \in lca(x,y)$.
>Formale Definition: $y$ ist BM für $x$ wenn $\forall y': \sigma(y) = \sigma(y'), \forall u \in lca(x,y'), v\in lca (x,y), u \nprec v$.

>[!warning] Definition best match — weak
>Hierfür müssen wir ein neues Set definieren. Für alle $x \in L(N)$ und $\tau \in \sigma(L(N)\backslash x)$ definieren wir:
>$$Q(x,\tau) \coloneqq \min_{\preceq} \{v\in lca(x,y):\sigma(y) = \tau\}$$
>$Q(x,\tau)$ ist also die Menge aller lcas zwischen $x$ und einem Blatt mit der Farbe $\tau$.
>Damit gilt für *weak best matches*: Gilt für ein Netzwerk $N$: $x,y\in L(N), \, \sigma (y) \ne \sigma(x)$, dann ist $y$ ein *weak* best match von $x$ wenn gilt: $lca(x,y) \cap Q(x,\sigma(y)) \ne \varnothing$.
>Das bedeutet, $y$ ist ein weak best match wenn es von $x$ aus über irgendeinen der lowest common ancestors zwischen $x$ und einem Blatt derselben Farbe wie $y$ erreichbar ist.

Beispiel zur Erklärung, warum der Unterschied in Netzwerken wichtig ist:
![[Screenshot From 2026-08-12 16-44-27.png|450]]
Nach der strengen (standard) Definition hat $x$ hier keinen best match der Farbe $\sigma(y)$, da $lca(x,y) = \{P_{xy}, Q_{xy}\}, \, lca(x,y') = \{P_{xy'}\}, \, lca(x,y'') = \{Q_{xy''}, P_{xy''} \}$, aber $Q_{xy} \prec P_{xy''}$ und $Q_{xy''}\prec P_{xy}$ und $Q_{xy''}\prec P_{xy'}$. In jeder Menge an lca gibt es also einen Knoten, der höher liegt als ein anderer lca.
Weak best match: $Q(x,\sigma(y)) = \min_{\preceq}\{P_{xy}, Q_{xy}, P_{xy'}, Q_{xy''}, P_{xy''}\} = \{Q_{xy}, Q_{xy''}\}$, demnach sind $y, y''$ *weak* best match von $x$.
Entfernt man die orange Edge $(P_{xy'}, Q_{xy''})$ dann ist nach der strengen Definition $y'$ best match von $x$ da nun $Q_{xy''}\nprec P_{xy'}$. Nach der schwachen Definition sind $y, y', y''$ alle *weak* best match von $x$, da $Q(x,\sigma(y)) = \{Q_{xy}, P_{xy'}, Q_{xy''}\}$
Siehe [[BMG_Definitions|Python Umsetzung]] hier.

In Bäumen ergeben best matches und weak best matches dieselben Ergebnisse, beide gleichen der Definition von best matches in Bäumen. Analog zu Bäumen stellt sich nun die Frage, wann wir einen Graphen $(G,\sigma)$ als BMG eines Netzwerkes $(N,\sigma)$ erhalten können. In der Regel gibt es viel mehr Graphen, die sich durch Netzwerke als durch Bäume erklären lassen.

>[!note] Definition BMG in Netzwerken
>$(G,\sigma)$ ist ein Netzwerk-BMG wenn ein phylogenetisches Netzwerk $(N,\sigma)$ existiert, sodass $(G,\sigma)$ die best machtes in $(G,\sigma)$ repräsentiert. 
>$$NBMG(T,\sigma) = TBMG(T,\sigma)$$
>Startpunkt für das Projekt ist also ein Netzwerk, dass einem Baum so nahe wie möglich ist.

**sicor**
Ein vertex-gefärbter Graph $(N,\sigma)$ ist color sink-free wenn für alle $x\in L(N), \forall \sigma \ne \sigma(x) \text{ mit } \sigma(y) = \sigma: (x,y) \in E(G)$.
Ist ein vertex $v \in V$ der einzige Vertex mit der Farbe $\sigma(v)$, nennen wir ihn *single color representative (sicor)*. Ein vertex $v \in V$ ist ein *in-hub* wenn alle vertices $u$ mit anderen Farben $\sigma(u) \ne \sigma(v)$ mit $v$ durch eine edge $(u,v) \in E(G)$ verbunden sind. Ist jeder sicor vertex in $(G,\sigma)$ ein in-hub, dann hat $(G,\sigma)$ die *sicor-in-hub* Eigenschaft. Color-sink-free impliziert sicor-in-hub.

>[!note] Ein Graph $(G,\sigma)$ ist ein Netzwerk-BMG genau dann wenn $(G,\sigma)$ ein *sicor-in-hub* ist und *properly colored*.

## BIC Cherry
Eine cherry $(x,y)$ ist ein Paar von Blättern mit gemeinsamen eindeutigen Vater.
Für eine *bicolored cherry (BIC)* $\{x,y\}$ gilt zusätzlich $\sigma(x)\ne\sigma(y)$.

Als ersten Schritt erstellen wir ein BIC-cherry Netzwerk für $L$. 
>[!note] BIC-cherry Netzwerk
>Ein BIC-cherry Netzwerk besteht aus einer Wurzel $\varrho$, den Blättern $L$ und einer Menge an dazwischenliegenden Vertizes $p_{xy}$ für $x,y \in L$ mit $\sigma(x)\ne \sigma(y)$. Dieser Vertex hat $x$ und $y$ als Kinder und ist deren einzigartiger Vorfahre. Ist $|L| = 2$, dann nimmt $p_{xy}$ die Rolle der Wurzel $\varrho$ ein (siehe Abbildung).
>![[Screenshot From 2026-08-11 14-11-51.png|400]]
>Somit erhalten wir einen vollständigen, symmetrischen, multipartiten Graph.


Nächster Schritt ist die Erweiterung des Netzwerks.
>[!note] Erweiterung des BIC-cherry Netzwerks
>Wir definieren die Erweiterung $[xy:xz]$ einer cherry $(x,y)$ mit parent $p_{xy}$ und einem dritten Vertex $z \in L(N)$ als die Insertion eines neuen Vertex $q_{xz}$ und der anschließenden insertion der gerichteten Kanten $(p_{xy},q_{xz}), (q_{xz},x),(q_{xz},y)$.
>![[Screenshot From 2026-08-11 14-21-04.png]]
>$y$ ist nun kein best match von $x$ mehr! Hier muss deshalb zusätzlich noch eine color sink-free Bedingung beachtet werden!

Damit ist $(N', \sigma)$ ein Netzwerk, das aus $(N,\sigma)$ durch eine endliche Zahl an Erweiterungen erzeugt wird.

???
(i) $x,y \in L$ und $x\ne y$ sodass $x,y$ wie in einer Erweiterung vorkommen. $lca_{N'}(x,y) = p_{xy}$
(ii) wenn $[xy:xz]$ benutzt wurde $p_{xy}\in lca_{N'}(x,y)$ und $q_{xy} \in lca_{N'}(x,z)$.
(iii) für $x,y,z \in L$  falls ein $u$ existiert mit $x \preceq u, z\preceq_{N'} u$ dann $\exists v, x\preceq_{N'} v\prec \varrho, y\preceq v\prec \varrho$. $u\preceq_{N'} v \Rightarrow$ die Extension $[xy:xz]$ wurde verwendet.

Gegen sein ein Graph $(G,\sigma)$ mit der sicor-in-hub Eigenschaft. Dann kann folgende Prozedur genutzt werden:
1. Konstruiere das BIC-Network $(N,\sigma)$ mit Blättern $L(N)=V(G)$ und Wurzel $\varrho$.
2. Für alle $x,y\in L$ mit $(x,y) \notin E(G)$ und $\sigma(x)\ne \sigma(y)$, erweitere $(N,\sigma)$ um $[xy:xy']$ für zufällig gewählte $y' \in L\backslash \{y\}$ mit $\sigma(y) \ne \sigma(y')$.
Das aus dieser Prozedur resultierende finale Netzwerk $(N,\sigma)$ erklärt den input graph. Allerdings ist $(N,\sigma)$ fast nie ein tree-BMG. Deshalb stellt sich die Frage ob wir $(N,\sigma)$ schrittweise modifizieren können, sodass es immer nich $(G,\sigma)$ erklärt, aber "Baum-ähnlicher" wird.

## Typen von phylogenetischen Netzwerken

**Cluster in phylogenetischen Netzwerken:**
$\forall u \in V(N)$ ist ein Cluster von $u$ definiert als
$$C(u) \coloneqq \{x \in L(N) | x \preceq u\}$$
was der Menge aller Blätter, die Nachfahren von $u$ sind, entspricht.
Entsprechend definieren wir $\mathfrak{C}_N \coloneqq \{C(u) | u \in V(N)\}$ als das Mengensystem, welches alle Cluster in $N$ erfasst.
Wenn $A,B\in \mathfrak{C}_N$ gilt $A\cap B \in \{A,B,\varnothing\}$.
Für die Hierarchie gilt: $\{x\} \in \mathfrak{C}_N$ für $x \in L(N)$,  $L(N) \in \mathfrak{C}_N$.
Entsprechend ist das Cluster der Wurzel die Menge aller Blätter $C(\varrho) = L(N)$, und das Cluster von $x$ ist $x$ selbst, wenn es ein Blatt ist: $C(x) = \{x\}$ wenn $x \in L(N)$.
Ist $N$ ein phylogenetischer Baum, dann ist $lca(C(u)) = u$, da das Cluster nur den einen gemeinsamen Vorfahren haben kann.
Allgemeiner gilt: $\forall A \subseteq L(N) \exists x,y \in A: lca(A) = lca(x,y)$.
Für alle Netzwerke gilt:
$u \preceq v \Rightarrow C(u) \subseteq C(v)$ 
$C(u) \subseteq C(v) \Rightarrow$ jedenfalls $u$ und $v$ $\preceq_N$-vergleichbar und daraus folgt, dass $u \preceq v$ oder $v\prec u$ und $C(u) = C(v)$ ???

Ein Netzwerk ist *regulär* wenn:
1. $u \ne v \Rightarrow C(u) \ne C(v)$
2. $u \preceq_N v \Leftrightarrow C(u) \subseteq C(v)$
3. $N$ hat keine schortcuts, welche definiert sind als: es existiert eine Kante $(u,v)$ mit $v\preceq u$ und $\exists x: v\prec x \prec u$ (sprich, es gibt mindestens zwei Pfade um von u nach v zu kommen, wobei der eine Pfad eine direkte Kante ist, der andere Pfad über mindestens einen anderen Knoten läuft)

>[!warning] **The network cluster section applies tree properties to networks.**
>It states A∩B ∈ {A, B, ∅} and that lca(A) = lca(x,y) for some pair x, y in A. Both hold for trees (hierarchies) but not in general for networks. There, clusters can overlap, which is precisely why networks form clustering systems rather than hierarchies.

**Knoten-und Netzwerktypen**:
Baumartige Knoten: haben *einen* direkten Vorfahren (grün in Abbildung)
phylogenetisch: jeder baumartige Knoten hat entweder keine oder mindestens zwei Nachfahren
Hybride Knoten: haben *mehr als einen* direkten Vorfahren (orange in Abbildung)
Stack-free: Kein Kind eines Hybrid-Knoten ist wieder ein Hybrid-Knoten.
Kaktus-Netzwerke: jeder Block ist ein einfacher Kreis (siehe Abbildung)
![[Screenshot From 2026-08-12 14-04-34.png|200]]
Level-1-Netzwerk: jeder Block hat einen Hybrid-Vertex
Tree-child-Netzwerke: $N$ ist tree-child Netzwerk wenn jeder Knoten ein Blatt ist oder wenigstens einen Baum-Knoten als Kind hat. Ein phylogenetisches Level-1-Netzwerk ergibt ein tree-child Netzwerk.
Tree-sibling-Netzwerke: Jeder (Hybrid-)Knoten hat einen sibling, der baumartig ist. Jeder Satz aus Kindern enhält also mindestens einen baumartigen Knoten. Da ein baumartiger Knoten nur einen direkten Vorfahren hat, können in einem tree-sibling Netzwerk keine zwei Kindermengen existieren, die dieselben Eltern haben.

Beispiel-Abbildung, zeigt ein Netzwerk, das kein tree-child Netzwerk ist (alle Kinder von $v$ sind Hybride), aber ein tree-sibling Netzwerk ist, da die Vertizes $A$ und $B$ entsprechend die Knoten 1 bzw 4 als Geschwister haben.
![[Pasted image 20260812142649.png|350]]
Abbildung aus [Cardona et. al, (2008)](https://academic.oup.com/bioinformatics/article/24/13/1481/238641?login=false)

## Bearbeitung von Netzwerken
>[!note] Definition Vorfahre und Nachfahre
>Vorfahre: $prec(x) =\{y|(y,x)\in E(N)\}$
>Nachfahre: $succ(x) = \{y| (x,y) \in E(N)\}$

**Mögliche Bearbeitungen, die auf Netzwerken durchgeführt werden können**
(i) Blattmenge bleibt unverändert, Wurzel bleibt Wurzel
(ii) Wenn $prec(x) = prec(y)$ und $succ(x)=succ(y)$ dann kann $x$ oder $y$ entfernt werden (denn jeder andere Knoten liegt dann entweder über oder unter $x$ und $y$).

**Editoperationen, die nur die Knotenmenge verändern ohne den BMG zu verliegen**
1. Insertion *oder* Deletion einer Kante
   ![[Screenshot From 2026-08-12 15-10-06.png|400]]
2. Kontraktion einer Kante *oder* vertex splitting
   ![[Screenshot From 2026-08-12 15-11-35.png|300]]
3. Insertion *oder* Deletion von unverbundenen Knoten ![[Screenshot From 2026-08-12 15-12-31.png|450]]

Als *minor operations* bezeichnet man eine Folge von Kanten- und Knotendeletionen. Eine geeignete Kombination ist notwendig, um alle Graph-Eigenschaften zu erhalten.
Beispielsweise könnte man einen Teilbaum auswählen, und durch hoch- und runterschieben innerhalb des Netzwerkes so das Netzwerk verändern. Zusätzlich könnte man die Bedingung aufstellen, dass die Graph-Eigenschaften in allen Zwischenschritten erhalten bleiben müssen, ebenso wie die BMG-Eigenschaften.
Eine andere Möglichkeit wäre zu erlauben, dass Zwischenschritte bestimmte Graph- oder BMG-Eigenschaften zerstören, und sie im Anschluss wieder herstellen.

Definition *ergodisch*: Eigenschaft, bei der man von jedem Obekt in einer Menge zu einem anderen Objekt über Editoperationen gelangen kann.
Eine Menge von Editoperationen ist ergodisch wenn für je zwei Objekte $N,N'$ (phylogenetische Netzwerke mit gegebenen $L(N)=L(N')$) eine Folge von Operationen existiert, die $N$ in $N'$ umwandelt.

Definition *Distanz*
- Die Distanz ist definiert als minimale Anzahl von Editieroperationen, die benötigt wird um $N$ in $N'$ zu überführen.
- Die Anzahl der Überführungsschritte ist immer endlich.
- Die Distanz ist symmetrisch, da Operationen invertierbar sind.
- Die Distanz von einem Netzwerk zu sich selbst ist immer 0.


