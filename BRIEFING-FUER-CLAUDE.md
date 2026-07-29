# Projekt-Briefing

**An den KI-Assistenten, der hier weiterarbeitet.** Diese Datei ersetzt die
Vorgeschichte. Bitte vor dem ersten Eingriff vollständig lesen.

---

## Worum es geht

Drucksachen für ein Restaurant in Wiesbaden: eine A4-Speisekarte und fünf
hinterleuchtete Leuchttafeln à 60 × 200 (Cansin hatte es fälschlicherweise andersherum erstellt) cm für die Wand hinter der Theke.
Alles entsteht programmatisch über Python mit reportlab.

Bewusste Entscheidung: **kein Canva, kein Word, keine Bildgenerierung.**
Frühere Versuche mit generierten Bildern scheiterten an uneinheitlichen Ziffern
und springenden Zeilenabständen. Ein Generator löst das strukturell – jede Zeile
entsteht aus derselben Funktion, also ist die Typografie zwangsläufig konsistent.
Diesen Ansatz bitte nicht durch Bildgenerierung oder Layoutprogramme ersetzen.

---

## Technischer Stand

Läuft, ist fertig, wurde vom Kunden inhaltlich abgenommen.

| | |
|---|---|
| Sprache | Python 3.10+ |
| Bibliotheken | reportlab, pillow, numpy (siehe `requirements.txt`) |
| Schriften | liegen als `.ttf` im Projektordner, nichts installieren |
| Externe Tools | keine zwingend; Poppler (`pdftoppm`, `pdfinfo`) nur zum Kontrollieren |
| Betriebssystem | egal, Systempfade wurden entfernt |
| Bauzeit | rund 10 Sekunden für alles |

Einrichtung und Bedienung stehen in `README.md`. Ein Befehl baut alles:
`python3 build_all.py`.

---

## Architektur – die eine Regel

```
menu_data.py     ← ALLE Inhalte. Einzige Quelle der Wahrheit.
build_menu.py    ← Layout Speisekarte A4, 12 Seiten
build_tafeln.py  ← Layout Leuchttafeln, 5 × 200 × 60 cm
cutout.py        ← stellt Fotos frei
build_all.py     ← baut alles
```

Beide Layout-Skripte importieren `menu_data.py`. **Inhalte gehören ausschließlich
dorthin.** Wer einen Preis in ein Layout-Skript schreibt, zerstört die Garantie,
dass Karte und Tafeln übereinstimmen – das ist der teuerste Fehler, den man hier
machen kann.

Ausnahme, sauber gelöst: Wenn eine Rubrik auf der Tafel anders heißen muss als in
der Karte, steht das in `TITLE_OVR` in `build_tafeln.py`. Nicht die gemeinsame
Datendatei ändern.

Datensatz je Gericht:

```python
# (nr, name, zusatz, allergene, icons, preis, beschreibung)
(42, "Döner Kebab", "", "2, 3, 6, 8", "", "7,00 €", "Dönerfleisch, grüner Salat, …"),
```

`icons`: `"v"` vegetarisch, `"s"` scharf, `"sv"` beides, `""` keins.
Die Nummern laufen durchgehend über alle Rubriken – Einfügen in der Mitte
verschiebt alle folgenden. Gäste nennen diese Nummer auf Karte, Tafel und Website.

---

## Wie hier gearbeitet wird

**Immer rendern und ansehen.** Ein PDF, das gebaut wurde, ist nicht geprüft.

```bash
pdftoppm -r 80 -png -f 1 -l 12 Speisekarte_Diyarbakir_Ocakbasi.pdf /tmp/seite
pdftoppm -r 14 -png tafeln/Tafel_2_Grill.pdf /tmp/tafel     # 14 dpi reicht bei 2 m Breite
```

Bei den Tafeln lohnt es, alle fünf untereinander zu einem Bild zu montieren –
so sieht man sofort, ob die Wand als Einheit wirkt.

**Textänderungen am fertigen PDF gegenprüfen, nicht am Quelltext.** Nur so sind
Metadaten und Layoutfehler mit erfasst:

```bash
pdftotext -layout datei.pdf - | grep -i "suchbegriff"
```

**Freigegebene Dateien nicht anfassen.** Neue Varianten kommen über
Umgebungsvariablen, nicht durch Überschreiben bestehender Stände.

**Bei mehrdeutigen Wünschen nachfragen, bevor gebaut wird.** In diesem Projekt
waren das reale Fälle: Gilt „X aus allen Beschreibungen entfernen" wirklich überall?
Sollen fremdsprachige Zweitnamen auch raus? Was ersetzt einen gestrichenen Claim?
Raten kostet hier mehr als fragen.

---

## Steuerung über Umgebungsvariablen

```bash
BLEED_MM=3    # Druckdaten mit 3 mm Beschnitt statt Endformat
SCALE=…       # nur Tafeln: Typografie-Skalierung, Standard 1.12
```

Windows-PowerShell: `$env:BLEED_MM="3"; python build_tafeln.py`

Der Beschnitt ist so gelöst, dass die Layout-Koordinaten identisch bleiben:
Seite um 2 × Beschnitt vergrößern, Nullpunkt verschieben, Hintergrund in die
Zugabe ziehen, TrimBox aufs Endformat setzen. Ein Aufruf ohne Variable erzeugt
weiterhin exakt die Freigabeversion.

`SCALE` ist kalibriert, nicht geraten: 1.12 ist der größte Wert, bei dem die
vollste Spalte aller fünf Tafeln unter 100 % Höhe bleibt – also die größte
lesbare Schrift, die noch passt. Nach Inhaltsänderungen neu kalibrieren.
`build_tafeln.py` gibt beim Bauen je Spalte die Füllung in Prozent aus und
markiert Überläufe mit `⚠ ZU HOCH`.

---

## Druckspezifikation

| Produkt | Endformat | mit Beschnitt |
|---|---|---|
| Speisekarte | A4 | 216 × 303 mm |
| Leuchttafel | 2000 × 600 mm | 2006 × 606 mm |

TrimBox liegt jeweils auf dem Endformat. Schnittmarken sind bei 3 mm nicht
unterzubringen; Druckereien reicht die TrimBox. Werden Marken verlangt, Zugabe
auf 5 mm erhöhen.

Für Website, Auflicht und Eigendruck immer die Version **ohne** Beschnitt.

---

## Fallstricke, die schon aufgetreten sind

**Hinterleuchtung.** Die Druckerei warnt im Angebot ausdrücklich: tiefe
Schwarztöne und dunkle Vollflächen sind auf transluzenter Folie nicht in voller
Intensität sicherzustellen. Der Kunde hat sich trotzdem bewusst für die dunkle
Fassung entschieden – frühere Alternativen in Braun, Holz und Hell wurden auf
seinen Wunsch entfernt. Diese Entscheidung bitte nicht eigenmächtig revidieren.
Was bleibt: vor der Serie Andruck anfordern. Hintergrund in `TAFELN-INFO.md`.

**Fotorechte.** Es lagen bereits Wasserzeichen-Vorschaubilder von Stockportalen
im Projekt. Die sind rechtlich nicht nutzbar, auch nicht retuschiert. Bei jedem
neuen Bild prüfen: sichtbares Wasserzeichen, auffällig kleine Auflösung,
Dateiname mit Stock-ID. Im Zweifel Herkunft erfragen und nicht einbauen.

**Fotoauflösung im Großformat.** Die vorhandenen Bilder liegen bei 40–63 dpi im
Endformat der Tafeln. Für 2–4 m Betrachtungsabstand vertretbar, aus einem Meter
sichtbar weich. Nicht hochskalieren – das erzeugt keine Schärfe, verdeckt aber
das Problem bis zum Druck. Stattdessen die konkret fehlende Pixelzahl nennen;
die Tabelle steht in `TAFELN-INFO.md`.

**Freistellen.** `cutout.py` arbeitet mit Flood-Fill von den Bildrändern über
weiß-ähnliche Pixel, nicht mit globaler Weiß-Entfernung. Sonst verschwinden weiße
Flächen im Motiv – Teller, Glanzlichter. Bilder mit echtem Hintergrund
(Grill, Pizza) lassen sich nicht freistellen und werden rund beschnitten; sie
stehen in `CIRCLE_KEYS` in `build_tafeln.py`.

**Zwischenspeicher.** Freigestellte Fotos und Texturen werden als `_cut_*.png`
bzw. `_tafel_*.jpg` abgelegt und über das Änderungsdatum der Quelldatei
invalidiert. Wirkt eine Änderung nicht, diese Dateien löschen und neu bauen.
Alle Texturen sind über einen festen Seed reproduzierbar.

**Sprachliche Vorgabe des Kunden.** Auf allen Drucksachen darf nichts stehen, was
das Restaurant explizit als türkisch bezeichnet – Wunsch des Inhabers, um
Rückfragen von Gästen zu vermeiden. Gerichtnamen wie Adana Kebab oder Haydari
bleiben, aber keine Zweitnamen in türkischer Sprache, kein „türkische
Spezialitäten", kein Herkunftshinweis beim Fleisch. `AENDERUNGEN-WEBSITE.md`
enthält am Ende eine Suchliste mit Begriffen, die nirgends mehr vorkommen dürfen.

---

## Was offen ist

1. **Andruck der Leuchttafeln** vor der Serie – siehe oben.
2. **Bessere Fotos** für das Großformat, Zielwerte in `TAFELN-INFO.md`.
3. **Banner für außen** – noch nicht begonnen. Sollen laut Kunde Bildmotive
   werden, Format war zum Zeitpunkt der Übergabe noch nicht festgelegt. Ein
   eigenes Skript nach dem Muster von `build_tafeln.py` ist der naheliegende Weg –
   ebenfalls gespeist aus `menu_data.py`.
4. **Pos. 2 des Druckangebots** (60 × 1 m, 5 Stück) ist noch keinem Inhalt
   zugeordnet. Das Angebot liegt unter `unterlagen/`.
5. **Website** – die Textänderungen der letzten Runde sind noch zu übertragen.
   `AENDERUNGEN-WEBSITE.md` enthält alles zum Kopieren plus Kontrollliste.
6. **Domain** enthält noch den alten Restaurantnamen. Entscheidung offen.

---

## Weitere Dateien

| Datei | Inhalt |
|---|---|
| `README.md` | Einrichtung und typische Aufgaben |
| `TAFELN-INFO.md` | Leuchttafeln im Detail: Aufteilung, Backlit, Fotoauflösung |
| `AENDERUNGEN-WEBSITE.md` | Textänderungen für die Website, mit Kontrollliste |
| `unterlagen/` | Angebot der Druckerei |
| `aktuelle-pdfs/` | fertige Druckdaten zum Ansehen ohne Installation |
