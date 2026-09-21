- [x] Eine Datei für alle Funktionen
- [x] Neue Funktion für BMG über die Menge der LCAs
- [ ] Definitionen konkretisieren
- [ ] BIC Cherry verbessern
	- [ ] Kann man bei BIC-Cherry gewisse Kanten rauslöschen, ohne dass etwas kaputt geht
	- [ ] kann man nach jeder hinzugefügten Kante schauen, ob der BMG bereits der Richtige ist (selektiv Kanten hinzufügen) (erst die BM fixen, die in keine Richtung verbunden sind, vielleicht mit nur einer Kante, dann wenn der BMG noch nicht stimmt, weiter machen)
	- [x] Bei der Wahl von Z: Wenn es mehrere best matches zu x gibt, dann den wählen, bei dem auch gilt z->x
	- [ ] Kandidatenwahl als Hilfsfunktion? -> bessere Lesbarkeit
- [ ] Funktion für Vereinfachung der Genbäume (alle Gene einer Spezies die aus der selben Speziation entstanden sind zu einem Gen zusammenfassen)?
- [x] Kann man im BIC Cherry nur die p-Knoten einfügen, für die es im BMG eine Verbindung gibt? Und dann mit den Q-Knoten erweitern?
	- [x] Nein!
- [x] Kann es sein, dass die BMGs immer dann kaputte gehen, wenn ein Hybrid zu einem Blatt einer anderen Farbe gebildet wird?
- [ ] Neue Darstellung für BICCherry Netzwerke
- [x] Vergleich ```asymmetree.analysis.bmg``` mit unserer BMG Funktion
	- [x] assymetree funktioniert nur bei Bäumen!




In unserem letzten Chat haben wir einen Code gebaut, mit dem wir untersuchen konnten, warum der BCEA nicht mehr funktioniert um einen bestimmten BMG darzustellen.

Ich möchte nun einen Code schreiben, der mir graphisch darstellt, wie viele Hybride man im Schnitt einfügen kann, bevor der BCEA den BMG nicht mehr abbilden kann, in Abhängigkeit der Anzahl der Spezies im Genbaum und in Abhängigkeit der Anzahl an Blättern.

Zunächst auch wieder für die weak-Definition der best matches.

Dabei sollen zum einen mehrere Bäume Bäume pro Anzahl an Spezies gebaut werden, die Anzahl der Blätter sollte dabei limitiert sein, da zu große Bäume zu rechenintensiv währen.

Zum generieren der Genbäume verwenden wir asymmetree.

Über jeden Generierten Baum sollen dann n_runs laufen, die wieder so lange hybriden einfügen (insert_hybrid - schon geschrieben) bis die BMGs nicht mehr übereinstimmen.

Dann hätte ich gerne einen Graphischen output, der mir zeigt wie viele Hybride im Schnitt eingefügt werden konnten.