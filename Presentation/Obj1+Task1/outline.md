# Task 1 — Explaining Networks for Best Match Graphs

## 0. Setting, Definitions, Objective 1a  (direction N → G)

### 0.1 Notation
- Leaf-coloured network $(N,\sigma)$, leaf set $L$, colouring $\sigma: L \to S$
- Ancestor order $\preceq$; $\mathrm{LCA}(x,y)$ as a set (non-empty antichain)
- $Q(x,\tau) := \min_{\preceq} \bigcup_{\sigma(y)=\tau} \mathrm{LCA}(x,y)$

### 0.2 Definitions
- Def 1 (strict best match)
- Def 2 (weak best match)
- Remark: both reduce to Geiß et al. Def 1 on trees

### 0.3 Formal argument
- Lemma: strict $\iff \mathrm{LCA}(x,y) \subseteq Q(x,\sigma(y))$
- Corollary (Objective 1a): strict $\Rightarrow$ weak
- Counterexample: weak $\not\Rightarrow$ strict

### 0.4 Implementation `bmg(N, mode)`
- Ancestor sets, minimal elements as induced-subgraph sinks
- $M(x,B) = Q(x,B)$ via union of ancestor sets
- Equivalence with AsymmeTree `bmg_from_tree` on trees

### 0.5 Computational check of 0.3
- strict BMG ⊆ weak BMG on all Task-0 networks; frequency of strict inclusion

### 0.6 Consequences used later
- Weak BMGs are colour-sink-free
- Colour-sink-free $\Rightarrow$ sicor-in-hub

---

## 1. Explaining Networks, Tasks 1a–1c  (direction G → N)

### 1.0 Direction switch
- Input $(G,\sigma)$, output $(N,\sigma)$; "explains" means $\mathrm{BMG}_{\text{mode}}(N) = G$

### 1.1 Characterization
- sicor-in-hub; necessity

### 1.2 Task 1a — BIC-cherry + expansion (report version)
- Pseudocode `BCEA(G, σ, mode, choose_witness)`, rule (i): arbitrary $y'$
- Cherry network explains the complete multipartite graph (strict and weak)
- Effect of one expansion on $\mathrm{LCA}$ and $Q$
- Shortcut-edge deletion is reachability-invariant

### 1.3 Task 1b — restricted witness
- Rule (ii): $y' \in N^+_G(x)$
- Remark: relabel $q \to p$

### 1.4 Task 1c — tests
- Cherry network complete
- Shortcut deletion leaves BMG unchanged
- Tree-BMGs explained strictly under every rule
- `bmg` vs AsymmeTree

---

## 2. Task 1d / Objective 1b — Weak BMGs

### 2.1 Experiment: rule (ii) on weak network-BMGs
- Failures; signature: spurious reverse arcs only

### 2.2 Lemma: q-vertices are symmetric
- A $q$-vertex is a minimal common ancestor of both children ⇒ weak arc in both directions
- Rule (ii) is not sufficient

### 2.3 Rule (iii): reciprocal witness
- `find_candidate`, weak mode
- Remaining failures: leaves without reciprocal partner in some colour

### 2.4 Minimal example
- $((a_1,(b_1,a_2)),b_2)$ — a tree-BMG not weakly explainable by two layers

### 2.5 MLBCEA — multilayer expansion
- Spurious arc treated as a fresh correction problem one layer down
- `insertNode`, `pending`, one-step lookahead `_has_reciprocal_option` (heuristic, not correctness)
- Why extra layers do not help strict
- Termination via `maxLayers`; residual failure class: blame-passing cycles

### 2.6 Strict side: double expansion
- Double expansion at one cherry kills the arc between the two witnesses
- Rule (iv): safe pair, `find_joint_candidates`
- When no safe pair exists

### 2.7 Answer to Objective 1b (boxed)

---

## 3. Empirical Validation

### 3.1 Design
- Fixed seeds, identical instances across rules
- Input classes: tree-BMGs, strict network-BMGs, weak network-BMGs
- Parameters: $n$, $|S|$, number of hybridizations

### 3.2 Success rate per rule × input class

### 3.3 Failure anatomy
- Spurious vs missing arcs, direction
- Predicted vs observed signature

### 3.4 Predictors
- Fraction of $(x,\tau)$ without reciprocal partner vs failure rate
- MLBCEA: layers needed

### 3.5 Network size
- Vertices, edges, leaf in-degree — hand-off to Task 2

---

## 4. Minimal Failing Examples and Summary

### 4.1 Exhaustive search over small $n$
- Smallest failure per rule

### 4.2 Table of witness rules
| rule | witness | guarantee | fails when | minimal example |
|------|---------|-----------|------------|-----------------|

### 4.3 Outlook
- Implications for Task 2 and for the multilayer idea
- 