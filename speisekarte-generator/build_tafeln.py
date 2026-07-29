# -*- coding: utf-8 -*-
"""Leuchtkasten-Tafeln innen – 5 Stück, je 200 x 60 cm (quer), hinterleuchtet.

Nutzt dieselbe menu_data.py wie die Speisekarte -> Inhalte können nicht auseinanderlaufen.
Hintergrund bewusst FLACH (kein Schiefer-Rauschen, keine Vignette), weil feine Strukturen
und Verläufe auf transluzenter Backlit-Folie fleckig wirken.

Schriftgröße über SCALE (Standard 1.12) - so kalibriert, dass die vollste Spalte
aller fünf Tafeln knapp unter 100 % Höhe bleibt.

    python3 build_tafeln.py              -> Vorschau/Freigabe, 200 x 60 cm ohne Beschnitt
    BLEED_MM=3 python3 build_tafeln.py   -> Druckdaten, 206 x 66 cm mit 3 mm Beschnitt

Die Speisekarten-PDFs werden davon nicht berührt.
"""
import os
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
from reportlab.lib.colors import HexColor, Color
from PIL import Image
from menu_data import RESTAURANT, SECTIONS

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "photos")
OUTDIR = os.path.join(HERE, "tafeln")
os.makedirs(OUTDIR, exist_ok=True)

BLEED_MM = float(os.environ.get("BLEED_MM", "0"))
BLEED = BLEED_MM * mm

# ---------- Format ----------
W, H = 2000*mm, 600*mm            # Endformat einer Tafel (Trimbox)
PAGE = (W + 2*BLEED, H + 2*BLEED)
ML = MR = 55*mm
MT = 45*mm
MB = 40*mm
GUTTER = 46*mm

# ---------- Farben ----------
# Dunkle Fassung – optisch identisch zur gedruckten Speisekarte.
# Bewusst kein reines Schwarz: auf transluzenter Backlit-Folie wird das nie deckend
# und kippt ins Graue. Vor der Serie Andruck prüfen, siehe TAFELN-INFO.md.
BG       = HexColor("#231B15")
TAN      = HexColor("#D2A168")   # Überschriften
TAN_LT   = HexColor("#E3B683")   # Gerichtnamen
CREAM    = HexColor("#EBE2D3")   # Beschreibungen
CREAM_BR = HexColor("#F7F1E4")   # Preise
NUMCOL   = HexColor("#B9976B")
DOTCOL   = Color(0.62, 0.53, 0.42, alpha=0.55)
ORN      = HexColor("#B08B55")
GREEN    = HexColor("#8CCB5A")
GREEN_D  = HexColor("#55993A")
RED      = HexColor("#D2452F")

# ---------- Fonts ----------
# Schriften liegen im Projektordner -> laeuft auf Mac, Windows und Linux gleich.
def _font(name):
    p = os.path.join(HERE, name)
    if os.path.exists(p):
        return p
    for d in ("/usr/share/fonts/truetype/dejavu",
              "/Library/Fonts", "C:/Windows/Fonts"):
        q = os.path.join(d, name)
        if os.path.exists(q):
            return q
    raise FileNotFoundError(
        f"Schrift {name} nicht gefunden. Sie muss neben den Skripten liegen.")

pdfmetrics.registerFont(TTFont("Serif",   _font("p052.ttf")))
pdfmetrics.registerFont(TTFont("Serif-B", _font("p052b.ttf")))
pdfmetrics.registerFont(TTFont("Serif-I", _font("p052i.ttf")))
pdfmetrics.registerFont(TTFont("Cond",    _font("DejaVuSansCondensed.ttf")))
pdfmetrics.registerFont(TTFont("Cond-B",  _font("DejaVuSansCondensed-Bold.ttf")))

# Größen 1:1 in pt (1 mm = 2.835 pt). SCALE skaliert die komplette Typografie;
# der Wert ist so gewählt, dass die vollste Spalte aller Tafeln knapp unter 100 % füllt.
SCALE = float(os.environ.get("SCALE", "1.12"))

S_HEAD  = 92.0 * SCALE      # Rubrik-Überschrift
S_NAME  = 56.0 * SCALE      # Gerichtname
S_PRICE = 56.0 * SCALE
S_NUM   = 44.0 * SCALE
S_DESC  = 34.0 * SCALE      # Beschreibung
S_ALG   = 22.0 * SCALE
S_NOTE  = 38.0 * SCALE

LEAD_NAME = 70.0 * SCALE
LEAD_DESC = 42.0 * SCALE
GAP_ITEM  = 26.0 * SCALE
GAP_HEAD  = 46.0 * SCALE    # unter der Überschrift
ICON_S    = 34.0 * SCALE
NUM_W     = 78.0 * SCALE    # Breite der Nummernspalte

# ---------- Aufteilung auf die 5 Tafeln ----------
# Spaltenzahl je Tafel so gewählt, dass der Inhalt die volle Tafelbreite nutzt.
# Spaltentypen:
#   {"sections": [ids]}            – Rubriken mit eigener Überschrift untereinander
#   {"items": (sid, von, bis)}     – Teilstück einer Rubrik (Überschrift steht oben quer)
#   {"photo": (key, hoehe_anteil)} – Foto, optional über mehrere Spalten ("span")
TAFELN = [
    {"file": "Tafel_1_Vorspeisen_Salate",
     "cols": [{"sections": ["suppen", "meze"], "w": 1.10},
              {"sections": ["salate"],         "w": 1.10},
              {"photo": ("salat", 0.80),       "w": 0.80}]},

    {"file": "Tafel_2_Grill",
     "banner": "grill",
     "cols": [{"items": ("grill", 0, 6),  "w": 1.10},
              {"items": ("grill", 6, 11), "w": 1.10},
              {"photo": ("grill", 0.66),  "w": 0.80}]},

    {"file": "Tafel_3_Pizza",
     "banner": "pizza",
     "cols": [{"items": ("pizza", 0, 6),   "w": 1.05},
              {"items": ("pizza", 6, 12),  "w": 1.05},
              {"items": ("pizza", 12, 17), "w": 1.05},
              {"photo": ("pizza", 0.55),   "w": 0.85}]},

    {"file": "Tafel_4_Doener_Duerum_Pide",
     "cols": [{"sections": ["doener"], "w": 1.12},
              {"sections": ["duerum"], "w": 1.12},
              {"sections": ["pide"],   "w": 0.98},
              {"photo": ("doener", 0.50), "w": 0.78}]},

    {"file": "Tafel_5_Vegetarisch_Desserts_Getraenke",
     "cols": [{"sections": ["veg"],           "w": 1.15},
              {"sections": ["desserts"],      "w": 0.90},
              {"sections": ["heiss", "kalt"], "w": 1.00},
              {"sections": ["kalt2"], "pad": True, "w": 0.95}]},
]

def col_geom(spec):
    """Liefert [(x, breite), ...] – Spalten dürfen unterschiedlich breit sein ("w" = Gewicht)."""
    ws = [cs.get("w", 1.0) for cs in spec["cols"]]
    n = len(ws)
    total = W - ML - MR - GUTTER*(n - 1)
    unit = total / sum(ws)
    out, x = [], ML
    for wgt in ws:
        cw = unit*wgt
        out.append((x, cw))
        x += cw + GUTTER
    return out

# Nur für die Tafeln: Überschrift/Unterzeile abweichend von der Speisekarte.
# (menu_data.py bleibt unangetastet – die Karte ändert sich dadurch nicht.)
TITLE_OVR = {
    "kalt":  ("", "Kalte Getränke  (0,33 L / 1 L)"),
    "kalt2": ("", "Weitere kalte Getränke"),
}

def sec(sid):
    return next(s for s in SECTIONS if s["id"] == sid)


# ---------- Zeichen-Helfer ----------
def spaced(c, txt, cx, y, font, size, charspace, color):
    tw = pdfmetrics.stringWidth(txt, font, size) + charspace*(len(txt)-1)
    c.saveState()
    t = c.beginText(cx - tw/2, y)
    t.setFont(font, size); t.setFillColor(color); t.setCharSpace(charspace)
    t.textOut(txt); c.drawText(t)
    c.restoreState()
    return tw

def ornament(c, cx, y, half):
    c.saveState()
    c.setStrokeColor(ORN); c.setLineWidth(2.6)
    c.line(cx - half, y, cx - 26, y)
    c.line(cx + 26, y, cx + half, y)
    c.setFillColor(ORN)
    p = c.beginPath()
    p.moveTo(cx, y + 10); p.lineTo(cx + 10, y); p.lineTo(cx, y - 10); p.lineTo(cx - 10, y); p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()

def leaf(c, x, y, s=ICON_S):
    c.saveState(); c.translate(x, y + s*0.12); c.rotate(-18)
    c.setFillColor(GREEN)
    p = c.beginPath(); p.moveTo(0, 0)
    p.curveTo(s*0.15, s*0.75, s*0.75, s*0.95, s, s*0.55)
    p.curveTo(s*0.8, s*0.15, s*0.35, -s*0.08, 0, 0); p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.setStrokeColor(GREEN_D); c.setLineWidth(s*0.08)
    c.line(s*0.08, s*0.06, s*0.82, s*0.55)
    c.restoreState()

def chili(c, x, y, s=ICON_S):
    c.saveState(); c.translate(x, y)
    c.setFillColor(RED)
    p = c.beginPath(); p.moveTo(s*0.12, s*0.9)
    p.curveTo(s*0.55, s*0.95, s*0.95, s*0.55, s*0.9, 0)
    p.curveTo(s*0.86, s*0.3, s*0.5, s*0.55, s*0.12, s*0.62)
    p.curveTo(s*0.02, s*0.72, s*0.02, s*0.84, s*0.12, s*0.9); p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.setStrokeColor(GREEN_D); c.setLineWidth(s*0.11)
    c.line(s*0.10, s*0.88, -s*0.06, s*1.05)
    c.restoreState()

def draw_icons(c, icons, x, y):
    for ic in icons:
        (leaf if ic == "v" else chili)(c, x, y)
        x += ICON_S + 12
    return x

# ---------- Höhenberechnung ----------
def item_h(it, maxw):
    """maxw = Breite des Textbereichs (Spaltenbreite minus Nummernspalte)."""
    nr, name, note, alg, icons, price, desc = it
    h = LEAD_NAME
    nw = pdfmetrics.stringWidth(name, "Cond-B", S_NAME) + NUM_W
    if note:
        nw += 14 + pdfmetrics.stringWidth(note, "Cond", S_NAME*0.82)
    if alg:
        nw += 12 + pdfmetrics.stringWidth(alg, "Cond", S_ALG)
    if icons:
        nw += 16 + len(icons)*(ICON_S + 12)
    if nw + 40*SCALE + pdfmetrics.stringWidth(price, "Cond-B", S_PRICE) > maxw + NUM_W:
        h += S_PRICE * 1.18
    if desc:
        h += len(simpleSplit(desc, "Cond", S_DESC, maxw)) * LEAD_DESC + 6
    return h + GAP_ITEM

def col_h(cs, w):
    """Höhe eines Spalteninhalts – 0 für Fotospalten."""
    if "sections" in cs:
        return block_h(cs["sections"], w) + ((S_HEAD + GAP_HEAD + 26) if cs.get("pad") else 0)
    if "items" in cs:
        sid, a, b = cs["items"]
        return sum(item_h(it, w - NUM_W) for it in sec(sid)["items"][a:b])
    return 0

def block_h(sids, colw):
    """Höhe eines Spalteninhalts (mehrere Sektionen untereinander)."""
    maxw = colw - NUM_W
    h = 0
    for sid in sids:
        s = sec(sid)
        t = TITLE_OVR.get(sid, (None, None))[0]
        t = s.get("title") if t is None else t
        st = TITLE_OVR.get(sid, (None, None))[1]
        st = s.get("subtitle") if st is None else st
        if t:
            h += S_HEAD + GAP_HEAD + 26
        if st:
            h += S_NOTE + 26
        if s.get("note"):
            h += S_NOTE * 1.6 + 18
        for it in s["items"]:
            h += item_h(it, maxw)
        h += 40
    return h

# ---------- Gericht ----------
def draw_item(c, it, x, y, colw):
    nr, name, note, alg, icons, price, desc = it
    num_w = NUM_W
    name_x = x + num_w
    right = x + colw
    base = y - S_NAME
    maxw = colw - NUM_W

    c.setFont("Cond", S_NUM); c.setFillColor(NUMCOL)
    c.drawRightString(x + num_w - 22*SCALE, base, str(nr))

    c.setFont("Cond-B", S_NAME); c.setFillColor(TAN_LT)
    c.drawString(name_x, base, name)
    cx = name_x + pdfmetrics.stringWidth(name, "Cond-B", S_NAME)
    if note:
        cx += 14
        c.setFont("Cond", S_NAME*0.82); c.setFillColor(CREAM)
        c.drawString(cx, base, note)
        cx += pdfmetrics.stringWidth(note, "Cond", S_NAME*0.82)
    if alg:
        cx += 12
        c.setFont("Cond", S_ALG); c.setFillColor(CREAM)
        c.drawString(cx, base + S_NAME*0.42, alg)
        cx += pdfmetrics.stringWidth(alg, "Cond", S_ALG)
    if icons:
        cx = draw_icons(c, icons, cx + 16, base)

    # Preis: passt er nicht neben den Namen (z. B. Mehrpersonen-Preise),
    # kommt er rechtsbündig in eine eigene Zeile darunter.
    ps = S_PRICE
    pw = pdfmetrics.stringWidth(price, "Cond-B", ps)
    own_line = (cx + 40 + pw) > right
    c.setFont("Cond-B", ps); c.setFillColor(CREAM_BR)
    if own_line:
        y -= LEAD_NAME
        c.drawRightString(right, y - ps + 8, price)
        y -= ps * 1.18
    else:
        c.drawRightString(right, base, price)
        x0, x1 = cx + 20, right - pw - 20
        if x1 - x0 > 50:
            c.saveState()
            c.setStrokeColor(DOTCOL); c.setLineWidth(4)
            c.setLineCap(1); c.setDash(0.1, 15)
            c.line(x0, base + 8, x1, base + 8)
            c.restoreState()
        y -= LEAD_NAME
    if desc:
        c.setFont("Cond", S_DESC); c.setFillColor(CREAM)
        for ln in simpleSplit(desc, "Cond", S_DESC, maxw):
            c.drawString(name_x, y - S_DESC + 6, ln)
            y -= LEAD_DESC
        y -= 6
    return y - GAP_ITEM

def fit_head(title, colw):
    """Überschriftgröße so wählen, dass sie in die Spalte passt."""
    avail = colw - 30
    size, cs = S_HEAD, 8
    tw = pdfmetrics.stringWidth(title, "Serif-B", size) + cs*(len(title)-1)
    if tw > avail:
        f = avail / tw
        size, cs = size*f, cs*f
    return size, cs

def draw_column(c, sids, x, y, colw):
    for sid in sids:
        s = sec(sid)
        title = TITLE_OVR.get(sid, (None, None))[0]
        title = s.get("title") if title is None else title
        subtitle = TITLE_OVR.get(sid, (None, None))[1]
        subtitle = s.get("subtitle") if subtitle is None else subtitle
        if title:
            hs, hcs = fit_head(title, colw)
            tw = spaced(c, title, x + colw/2, y - hs, "Serif-B", hs, hcs, TAN)
            y -= S_HEAD + 26
            ornament(c, x + colw/2, y, half=min(colw/2 - 20, tw/2 + 50))
            y -= GAP_HEAD
        if subtitle:
            c.setFont("Serif-B", S_NOTE); c.setFillColor(TAN)
            c.drawCentredString(x + colw/2, y - S_NOTE, subtitle)
            y -= S_NOTE + 26
        if s.get("note"):
            c.setFont("Serif-I", S_NOTE); c.setFillColor(CREAM)
            for ln in simpleSplit(s["note"], "Serif-I", S_NOTE, colw - 20):
                c.drawCentredString(x + colw/2, y - S_NOTE, ln)
                y -= S_NOTE * 1.35
            y -= 18
        for it in s["items"]:
            y = draw_item(c, it, x, y, colw)
        y -= 40
    return y

# ---------- Foto ----------
# Diese Motive sind keine Freisteller (Holzbrett, Grillrost im Hintergrund)
# -> wie in der Speisekarte rund beschneiden statt als Rechteck stehen lassen.
CIRCLE_KEYS = {"grill", "pizza", "diyarbakir"}

def _find(key):
    for ext in (".png", ".jpg.png", ".jpg.tiff", ".tiff", ".jpg", ".jpeg"):
        p = os.path.join(PHOTOS, key + ext)
        if os.path.exists(p):
            return p
    return None

def photo(c, key, cx, cy, target_h, max_w=None):
    src = _find(key)
    if not src:
        return

    if key in CIRCLE_KEYS:
        r = target_h / 2
        img = Image.open(src).convert("RGB")
        side = min(img.size)
        l, t = (img.width - side)//2, (img.height - side)//2
        img = img.crop((l, t, l + side, t + side))
        tmp = os.path.join(HERE, f"_tafel_crop_{key}.jpg")
        img.save(tmp, "JPEG", quality=92)
        c.saveState()
        p = c.beginPath(); p.circle(cx, cy, r)
        c.clipPath(p, stroke=0)
        c.drawImage(tmp, cx - r, cy - r, 2*r, 2*r)
        c.restoreState()
        c.saveState()
        c.setStrokeColor(ORN); c.setLineWidth(5)
        c.circle(cx, cy, r + 4, stroke=1, fill=0)
        c.restoreState()
        return side / (2*r / 72)

    dst = os.path.join(HERE, f"_cut_{key}.png")
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        from cutout import remove_white_bg
        remove_white_bg(src, dst)
    img = Image.open(dst)
    w = target_h * img.width / img.height
    if max_w and w > max_w:                      # nicht über den Spaltenbereich hinauslaufen
        target_h *= max_w / w
        w = max_w
    c.drawImage(dst, cx - w/2, cy - target_h/2, w, target_h, mask='auto')
    return img.width / (w / 72)

# ---------- Bau ----------
def build_tafel(spec, idx):
    name = spec["file"] + ("_DRUCK_3mm_Beschnitt" if BLEED else "")
    out = os.path.join(OUTDIR, name + ".pdf")
    c = canvas.Canvas(out, pagesize=PAGE)
    c.setTitle(f"Diyarbakir Restaurant – Leuchttafel {idx} (200 x 60 cm)")
    if BLEED:
        trim = (BLEED, BLEED, BLEED + W, BLEED + H)
        for s in ("setTrimBox", "setArtBox"):
            if hasattr(c, s):
                getattr(c, s)(trim)
        if hasattr(c, "setBleedBox"):
            c.setBleedBox((0, 0, PAGE[0], PAGE[1]))
        c.translate(BLEED, BLEED)

    # Hintergrund bis in den Beschnitt
    c.setFillColor(BG)
    c.rect(-BLEED, -BLEED, W + 2*BLEED, H + 2*BLEED, stroke=0, fill=1)

    geom = col_geom(spec)
    top = H - MT
    dpis = []

    # Rubrik-Überschrift quer über die ganze Tafel (bei Tafeln mit nur einer Rubrik)
    if spec.get("banner"):
        s = sec(spec["banner"])
        tw = spaced(c, s["title"], W/2, top - S_HEAD, "Serif-B", S_HEAD, 10, TAN)
        top = top - S_HEAD - 26
        ornament(c, W/2, top, half=tw/2 + 110)
        top -= GAP_HEAD
        for key, font in (("note", "Serif-I"), ("extras", "Cond-B")):
            if s.get(key):
                c.setFont(font, S_NOTE); c.setFillColor(CREAM)
                c.drawCentredString(W/2, top - S_NOTE, s[key])
                top -= S_NOTE + 26

    # Inhaltsblock vertikal in der Restfläche zentrieren
    avail = top - MB
    maxh = max([col_h(cs, w) for cs, (x, w) in zip(spec["cols"], geom)] + [0])
    top -= max(0, (avail - maxh) / 2)

    for colspec, (x, w) in zip(spec["cols"], geom):
        if "sections" in colspec:
            y0 = top - (S_HEAD + GAP_HEAD + 26 if colspec.get("pad") else 0)
            draw_column(c, colspec["sections"], x, y0, w)
        elif "items" in colspec:
            sid, a, b = colspec["items"]
            y = top
            for it in sec(sid)["items"][a:b]:
                y = draw_item(c, it, x, y, w)
        elif "photo" in colspec:
            key, fh = colspec["photo"]
            d = photo(c, key, x + w/2, MB + (H - MT - MB)*0.47, H*fh, max_w=w + GUTTER)
            if d:
                dpis.append((key, d))

    c.showPage(); c.save()
    return out, geom, dpis

def main():
    print(f"Format: {W/mm:.0f} x {H/mm:.0f} mm" + (f"  + {BLEED_MM:.0f} mm Beschnitt" if BLEED else "  (ohne Beschnitt)"))
    print(f"Typo-Skalierung: {SCALE:.2f}\n")
    for i, spec in enumerate(TAFELN, 1):
        out, geom, dpis = build_tafel(spec, i)
        warn = []
        avail = H - MT - MB - (S_HEAD + GAP_HEAD + 26 if spec.get("banner") else 0)
        for cs, (x, w) in zip(spec["cols"], geom):
            h = col_h(cs, w)
            if not h:
                continue
            lbl = "+".join(cs["sections"]) if "sections" in cs else f"{cs['items'][0]}"
            warn.append(f"{lbl}: {h/avail*100:.0f}%" + ("  ⚠ ZU HOCH" if h > avail else ""))
        d = "  ".join(f"Foto {k} {v:.0f} dpi" for k, v in dpis)
        cols = " · ".join(f"{w/mm:.0f} mm" for _, w in geom)
        print(f"Tafel {i}: {os.path.basename(out)}")
        print(f"          Spalten {cols}   {d}")
        print(f"          Füllung " + " · ".join(warn))

if __name__ == "__main__":
    main()
