Wann immer eine Korrektur für x nötig ist, weil x -/> y für mindestens ein y einer Farbe, und der best match zwischen x und z (dabei z = bm(x)) asymmetrisch ist, kann der BCEA dies nicht abbilden


Sei `N(x) = {y : (x,y) ∈ E(BMG)}` die Menge der echten Best Matches von x, und `L_c = {v ∈ V : σ(v) = c}` die Menge aller Gene der Farbe c.

**x braucht eine Korrektur bezüglich Farbe c** genau dann, wenn `N(x) ∩ L_c ⊊ L_c` — d. h. **mindestens ein** y der Farbe c fehlt (nicht "alle"!). Wichtig: Ist x zu **allen** Genen der Farbe c bereits verbunden (`N(x) ∩ L_c = L_c`), dann wird für diese Farbe **nie** ein Q-Knoten für x eingefügt — selbst wenn einer dieser Matches asymmetrisch wäre, bleibt die ursprüngliche P-Cherry für dieses Paar unangetastet, also kann dort auch keine Kette entstehen. Die Unvollständigkeit ist also notwendig, nicht nur hinreichend.

**Das BMG ist NICHT durch den (einstufigen) BCEA darstellbar** genau dann, wenn:

```
∃ x, z ∈ V:  σ(x) ≠ σ(z)  ∧  (x,z) ∈ E  ∧  (z,x) ∉ E  ∧  ∃ y ∈ V: σ(y) = σ(z) ∧ (x,y) ∉ E
```

In Worten: _Es gibt ein x mit einem asymmetrischen Best Match z (x→z ja, z→x nein), und x deckt die Farbe von z nicht vollständig ab (es gibt mindestens ein weiteres Gen dieser Farbe, das x nicht als Match hat)._