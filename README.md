# Diyarbakir Restaurant – Speisekarte & Leuchttafeln

Alle Drucksachen des Restaurants entstehen aus **einer** Datenquelle über Python-Skripte.
Kein Canva, kein Word, keine Bildgenerierung – dadurch sind Typografie und Preise
über Karte, Tafeln und Website hinweg zwangsläufig identisch.

---

## In 5 Minuten startklar

Voraussetzung: **Python 3.10 oder neuer**. Prüfen mit `python3 --version`
(Windows: `py --version`).

```bash
cd speisekarte-generator
python3 -m venv .venv

# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt
python3 build_all.py
```

Das war's. Nach etwa einer Minute liegen alle PDFs bereit:

- Speisekarte → direkt in `speisekarte-generator/`
- Leuchttafeln → in `speisekarte-generator/tafeln/`

Beim ersten Lauf werden Hintergrundtexturen und freigestellte Fotos erzeugt und
zwischengespeichert. Jeder weitere Lauf ist deutlich schneller.

---

## Wie das Projekt aufgebaut ist

```
speisekarte-generator/
  menu_data.py       ← ALLE Inhalte: Gerichte, Preise, Texte, Adresse
  build_menu.py      ← Layout Speisekarte, A4, 12 Seiten
  build_tafeln.py    ← Layout Leuchttafeln, 5 × 200 × 60 cm
  build_all.py       ← baut alles auf einmal
  cutout.py          ← stellt Fotos frei (Hintergrund entfernen)
  photos/            ← Bildmaterial
  *.ttf              ← Schriften (liegen im Projekt, nichts installieren)
  tafeln/            ← fertige Tafel-PDFs (entstehen beim Bauen)
```

**Die wichtigste Regel:** Inhalte stehen ausschließlich in `menu_data.py`.
Die Layout-Skripte importieren sie beide. Wer einen Preis in `menu_data.py` ändert
und neu baut, hat ihn automatisch auf Karte *und* Tafeln korrekt.

---

## Typische Aufgaben

### Preis oder Beschreibung ändern

In `menu_data.py` die Zeile suchen und ändern. Der Aufbau je Gericht:

```python
# (nr, name, zusatz, allergene, icons, preis, beschreibung)
(42, "Döner Kebab", "", "2, 3, 6, 8", "", "7,00 €", "Dönerfleisch, grüner Salat, …"),
```

`icons`: `"v"` = vegetarisch (Blatt), `"s"` = scharf (Chili), `"sv"` = beides, `""` = keins.

Danach `python3 build_all.py`.

### Gericht hinzufügen

Neue Zeile in die passende Rubrik einfügen. **Die Nummern laufen durchgehend
über alle Rubriken** – wird mitten in der Karte etwas eingefügt, verschieben sich
alle folgenden Nummern. Am einfachsten hinten in der Rubrik anhängen.

Beim Bauen meldet `build_tafeln.py` in Prozent, wie voll jede Spalte ist. Steht
dort `⚠ ZU HOCH`, passt der Inhalt nicht mehr auf die Tafel. Dann entweder in
`build_tafeln.py` die Spaltenaufteilung anpassen (`TAFELN`) oder `SCALE`
etwas verringern.

### Foto austauschen

Neues Bild nach `photos/` legen, gleicher Dateiname wie bisher. Beim nächsten Lauf
wird es automatisch neu freigestellt – der Zwischenspeicher erkennt das am Datum.

Fotos mit weißem Hintergrund werden freigestellt, Fotos mit echtem Hintergrund
(Grill, Pizza) rund beschnitten. Welches Bild wie behandelt wird, steht in
`CIRCLE_KEYS` in `build_tafeln.py`.

**Wichtig:** keine Vorschaubilder von Stockportalen verwenden. Die tragen Wasserzeichen
und sind rechtlich nicht nutzbar, auch nicht retuschiert.

### Druckdaten mit Beschnitt erzeugen

```bash
BLEED_MM=3 python3 build_menu.py         # Speisekarte 216 × 303 mm
BLEED_MM=3 python3 build_tafeln.py       # Tafeln 206 × 66 cm
```

Ohne die Variable entsteht jeweils das Endformat für Freigabe und Website.
`build_all.py` macht beides in einem Rutsch.

Windows-PowerShell setzt Variablen anders:

```powershell
$env:BLEED_MM="3"; python build_tafeln.py
```

### Farben ändern

Alle Farben stehen oben in `build_tafeln.py` bzw. `build_menu.py` als benannte
Konstanten (`BG`, `TAN`, `CREAM` …). Die Tafeln sind bewusst auf **eine** dunkle
Fassung festgelegt – frühere Varianten in Braun, Holz und Hell wurden entfernt,
damit es beim Weitergeben an die Druckerei keine Verwechslung gibt.

### Schriftgröße der Tafeln

`SCALE` in `build_tafeln.py` (Standard 1.12). Der Wert ist so kalibriert, dass die
vollste Spalte aller fünf Tafeln knapp unter 100 % Höhe bleibt – also die größte
Schrift, die noch passt. Nach Inhaltsänderungen neu kalibrieren: `SCALE` schrittweise
erhöhen, bis beim Bauen die erste Überlaufwarnung erscheint, dann eine Stufe zurück.

---

## Druckdaten

| Produkt | Endformat | Datei |
|---|---|---|
| Speisekarte, Freigabe | A4 | `Speisekarte_Diyarbakir_Ocakbasi.pdf` |
| Speisekarte, Druckerei | 216 × 303 mm | `…_DRUCK_3mm_Beschnitt.pdf` |
| Leuchttafeln, Freigabe | 200 × 60 cm | `tafeln/Tafel_…pdf` |
| Alle 5 Tafeln am Stück | 200 × 60 cm | `tafeln/Alle_5_Tafeln_Vorschau.pdf` |
| Leuchttafeln, Druckerei | 206 × 66 cm | `tafeln/Tafel_…_DRUCK_3mm_Beschnitt.pdf` |

Die Druckversionen tragen eine TrimBox auf dem Endformat – die Druckerei sieht
dadurch automatisch, wo geschnitten wird. Der Hintergrund läuft in die Zugabe hinein,
sodass ein leicht schiefer Schnitt keine weißen Ränder erzeugt.

**Für Auflicht, Website und Eigendruck immer die Version ohne Beschnitt nehmen.**

---

## Was noch offen ist

Details dazu in `TAFELN-INFO.md`, der vollständige Übergabestand in
`BRIEFING-FUER-CLAUDE.md`:

- Andruck der Leuchttafeln vor der Serie (hinterleuchtete dunkle Flächen sind heikel)
- Fotoauflösung für Großformat – die konkret benötigten Pixelmaße stehen dort
- Banner für außen, noch nicht begonnen
- Pos. 2 des Druckangebots (60 × 1 m) noch keinem Inhalt zugeordnet

`AENDERUNGEN-WEBSITE.md` enthält alle Textänderungen der letzten Runde zum
Übertragen auf die Website, inklusive einer Suchliste zum Gegenprüfen.

---

## Fehlersuche

**`ModuleNotFoundError: No module named 'reportlab'`**
Die virtuelle Umgebung ist nicht aktiv. `source .venv/bin/activate` bzw.
`.venv\Scripts\activate`, dann erneut versuchen.

**`Schrift … nicht gefunden`**
Eine `.ttf`-Datei fehlt im Ordner `speisekarte-generator/`. Alle fünf müssen dort liegen:
`p052.ttf`, `p052b.ttf`, `p052i.ttf`, `DejaVuSansCondensed.ttf`,
`DejaVuSansCondensed-Bold.ttf`.

**Änderung wirkt nicht**
Fotos und Texturen werden zwischengespeichert. Betroffene Dateien löschen und neu bauen:

```bash
rm _cut_*.png _tafel_*.jpg slate_bg.jpg
python3 build_all.py
```

**Ergebnis kontrollieren**
PDFs immer ansehen, nicht nur bauen. Als Bild exportieren geht mit Poppler:

```bash
pdftoppm -r 60 -png Speisekarte_Diyarbakir_Ocakbasi.pdf seite
```
