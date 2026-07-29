# -*- coding: utf-8 -*-
"""Diyarbakır Ocakbaşı – Speisekarte, A4 Druck-PDF. Alles programmatisch -> 100% konsistente Typografie."""
import os, math, random
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.lib.colors import HexColor, Color
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from menu_data import RESTAURANT, SECTIONS, ADDITIVES, DIYARBAKIR_TEXT

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "photos")

# Beschnittzugabe (Bleed) in mm – per Umgebungsvariable steuerbar.
#   python3 build_menu.py            -> normale A4-Version (unverändert)
#   BLEED_MM=3 python3 build_menu.py -> Druckversion 216 x 303 mm mit 3 mm Beschnitt
BLEED_MM = float(os.environ.get("BLEED_MM", "0"))

W, H = A4  # 595.27 x 841.89 pt – Endformat (Trimbox) bleibt immer A4
BLEED = BLEED_MM * mm
PAGE = (W + 2*BLEED, H + 2*BLEED)

OUT = os.path.join(HERE, "Speisekarte_Diyarbakir_Ocakbasi_DRUCK_3mm_Beschnitt.pdf"
                   if BLEED else "Speisekarte_Diyarbakir_Ocakbasi.pdf")
ML, MR, MT, MB = 18*mm, 18*mm, 16*mm, 14*mm
CW = W - ML - MR

# ---------- Farben ----------
TAN      = HexColor("#D2A168")   # Überschriften
TAN_LT   = HexColor("#DFAF7B")   # Gerichtnamen
CREAM    = HexColor("#EBE2D3")   # Beschreibung
CREAM_BR = HexColor("#F2EADB")   # Preise
NUMCOL   = HexColor("#C4A87F")   # Nummern
DOTCOL   = Color(0.62, 0.53, 0.42, alpha=0.65)
ORN      = HexColor("#A9834F")
GREEN    = HexColor("#7CB94E")
GREEN_D  = HexColor("#4C8A2E")
RED      = HexColor("#C63B28")

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

F_H1,   S_H1   = "Serif-B", 21.5
F_SUB,  S_SUB  = "Serif-B", 14.5
F_NOTE, S_NOTE = "Serif-I", 10.5
F_NAME, S_NAME = "Cond-B",  11.8
F_NNOTE,S_NNOTE= "Cond",    10.0
F_ALG,  S_ALG  = "Cond",    6.6
F_DESC, S_DESC = "Cond",    9.6
F_PRICE,S_PRICE= "Cond-B",  11.8
F_NUM,  S_NUM  = "Cond",    11.8

NUM_X   = ML + 9*mm          # rechte Kante der Nummernspalte
NAME_X  = ML + 12*mm         # Start Gerichtname
PRICE_R = W - MR             # rechte Kante Preis

LEAD_ITEM = 15.2             # Zeilenhöhe Namenszeile
LEAD_DESC = 11.6             # Zeilenhöhe Beschreibung
GAP_ITEM  = 6.2              # Abstand zwischen Gerichten
GAP_SEC   = 13               # Abstand vor neuer Sektion

# ---------- Schiefer-Hintergrund (einmal generieren) ----------
def make_slate(path, w=1240, h=1754, seed=7):
    if os.path.exists(path):
        return
    random.seed(seed)
    img = Image.new("L", (w//6, h//6))
    img.putdata([random.randint(0, 255) for _ in range((w//6)*(h//6))])
    big = img.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(2))
    fine = Image.new("L", (w, h))
    fine.putdata([random.randint(0, 255) for _ in range(w*h)])
    fine = fine.filter(ImageFilter.GaussianBlur(0.6))
    base = Image.new("RGB", (w, h), (23, 19, 16))
    # Mottling
    m = big.point(lambda p: int(p*0.14))
    warm = Image.new("RGB", (w, h), (48, 38, 28))
    base = Image.composite(warm, base, m)
    # feine Körnung
    g = fine.point(lambda p: int(p*0.10))
    grain = Image.new("RGB", (w, h), (62, 52, 42))
    base = Image.composite(grain, base, g)
    # Kratzer (diagonale helle Linien, sehr subtil)
    d = ImageDraw.Draw(base, "RGBA")
    for _ in range(26):
        x0, y0 = random.randint(-100, w), random.randint(-100, h)
        ln = random.randint(120, 500); ang = random.uniform(-0.9, 0.9)
        x1, y1 = x0 + ln*math.cos(ang), y0 + ln*math.sin(ang)
        d.line([x0, y0, x1, y1], fill=(120, 100, 80, 10), width=1)
    # Vignette
    vig = Image.new("L", (w, h), 0)
    dv = ImageDraw.Draw(vig)
    dv.ellipse([-w*0.35, -h*0.25, w*1.35, h*1.25], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGB", (w, h), (8, 6, 5))
    base = Image.composite(base, dark, vig)
    base = ImageEnhance.Contrast(base).enhance(1.04)
    base.save(path, "JPEG", quality=88)

SLATE = os.path.join(HERE, "slate_bg.jpg")
make_slate(SLATE)
SLATE_IR = ImageReader(SLATE)

def draw_bg(c):
    # Hintergrund läuft bis in die Beschnittzugabe hinein
    c.drawImage(SLATE_IR, -BLEED, -BLEED, W + 2*BLEED, H + 2*BLEED)

# ---------- Deko ----------
def ornament(c, cx, y, half=52):
    """Linie – Raute – Linie unter Überschriften."""
    c.saveState()
    c.setStrokeColor(ORN); c.setLineWidth(0.7)
    c.line(cx - half, y, cx - 9, y)
    c.line(cx + 9, y, cx + half, y)
    c.setFillColor(ORN)
    p = c.beginPath()
    p.moveTo(cx, y + 3.4); p.lineTo(cx + 3.4, y); p.lineTo(cx, y - 3.4); p.lineTo(cx - 3.4, y); p.close()
    c.drawPath(p, stroke=0, fill=1)
    for dx in (-half - 8, half + 8):
        c.circle(cx + dx, y, 1.1, stroke=0, fill=1)
    c.restoreState()

def sparkle(c, x, y, r=5, alpha=0.5):
    c.saveState()
    c.setFillColor(Color(0.93, 0.90, 0.85, alpha=alpha))
    p = c.beginPath()
    p.moveTo(x, y + r)
    p.curveTo(x + r*0.18, y + r*0.18, x + r*0.18, y + r*0.18, x + r, y)
    p.curveTo(x + r*0.18, y - r*0.18, x + r*0.18, y - r*0.18, x, y - r)
    p.curveTo(x - r*0.18, y - r*0.18, x - r*0.18, y - r*0.18, x - r, y)
    p.curveTo(x - r*0.18, y + r*0.18, x - r*0.18, y + r*0.18, x, y + r)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()

def leaf_icon(c, x, y, s=7.2):
    """Vegetarisch-Blatt; (x,y) = Grundlinie links."""
    c.saveState()
    c.translate(x, y + s*0.12); c.rotate(-18)
    c.setFillColor(GREEN)
    p = c.beginPath()
    p.moveTo(0, 0)
    p.curveTo(s*0.15, s*0.75, s*0.75, s*0.95, s, s*0.55)
    p.curveTo(s*0.8, s*0.15, s*0.35, -s*0.08, 0, 0)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.setStrokeColor(GREEN_D); c.setLineWidth(0.55)
    c.line(s*0.08, s*0.06, s*0.82, s*0.55)
    c.restoreState()

def chili_icon(c, x, y, s=7.2):
    c.saveState()
    c.translate(x, y)
    c.setFillColor(RED)
    p = c.beginPath()
    p.moveTo(s*0.12, s*0.9)
    p.curveTo(s*0.55, s*0.95, s*0.95, s*0.55, s*0.9, 0)
    p.curveTo(s*0.86, s*0.3, s*0.5, s*0.55, s*0.12, s*0.62)
    p.curveTo(s*0.02, s*0.72, s*0.02, s*0.84, s*0.12, s*0.9)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.setStrokeColor(GREEN_D); c.setLineWidth(0.8)
    c.line(s*0.10, s*0.88, -s*0.06, s*1.05)
    c.restoreState()

def crescent_icon(c, cx, cy, r, color):
    """Halbmond + Stern (Halal), gezeichnet statt Font-Glyph."""
    c.saveState()
    c.setFillColor(color)
    c.circle(cx, cy, r, stroke=0, fill=1)
    c.setFillColor(HexColor("#1A1512"))
    c.circle(cx + r*0.42, cy + r*0.12, r*0.82, stroke=0, fill=1)
    # kleiner Stern
    c.setFillColor(color)
    sx, sy, sr = cx + r*0.55, cy + r*0.1, r*0.32
    p = c.beginPath()
    for i in range(10):
        ang = math.pi/2 + i*math.pi/5
        rr = sr if i % 2 == 0 else sr*0.4
        x, y2 = sx + rr*math.cos(ang), sy + rr*math.sin(ang)
        (p.moveTo if i == 0 else p.lineTo)(x, y2)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()

def icons_width(icons, s=7.2):
    return len(icons) * (s + 3)

def draw_icons(c, icons, x, y):
    for ic in icons:
        (leaf_icon if ic == "v" else chili_icon)(c, x, y, 7.2)
        x += 10.2

# ---------- Header ----------
def spaced_text(c, txt, cx, y, font, size, charspace, color):
    """Zentrierter Text mit Buchstabenabstand; Tc sauber gekapselt (q/Q)."""
    tw = pdfmetrics.stringWidth(txt, font, size) + charspace*(len(txt)-1)
    c.saveState()
    t = c.beginText(cx - tw/2, y)
    t.setFont(font, size); t.setFillColor(color); t.setCharSpace(charspace)
    t.textOut(txt)
    c.drawText(t)
    c.restoreState()
    return tw

def section_header(c, title, y, size=S_H1, pad_top=0):
    y -= pad_top
    tw = spaced_text(c, title, W/2, y - size, F_H1, size, 2.6, TAN)
    y -= size + 9
    ornament(c, W/2, y, half=min(150, tw/2 + 18))
    return y - 14

def sub_header(c, title, y):
    spaced_text(c, title, W/2, y - S_SUB, F_SUB, S_SUB, 1.4, TAN)
    return y - S_SUB - 12

# ---------- Gericht ----------
def item_height(it, maxw):
    nr, name, note, alg, icons, price, desc = it
    h = LEAD_ITEM
    if desc:
        lines = simpleSplit(desc, F_DESC, S_DESC, maxw)
        h += len(lines) * LEAD_DESC + 1.5
    return h + GAP_ITEM

def draw_item(c, it, y, desc_maxw):
    nr, name, note, alg, icons, price, desc = it
    base = y - S_NAME
    # Nummer
    c.setFont(F_NUM, S_NUM); c.setFillColor(NUMCOL)
    c.drawRightString(NUM_X, base, str(nr))
    # Name
    x = NAME_X
    c.setFont(F_NAME, S_NAME); c.setFillColor(TAN_LT)
    c.drawString(x, base, name)
    x += pdfmetrics.stringWidth(name, F_NAME, S_NAME)
    # Zusatz (kursiv-artig, regular cream)
    if note:
        x += 4
        c.setFont(F_NNOTE, S_NNOTE); c.setFillColor(CREAM)
        c.drawString(x, base, note)
        x += pdfmetrics.stringWidth(note, F_NNOTE, S_NNOTE)
    # Allergene hochgestellt
    if alg:
        x += 3.5
        c.setFont(F_ALG, S_ALG); c.setFillColor(CREAM)
        c.drawString(x, base + 3.6, alg)
        x += pdfmetrics.stringWidth(alg, F_ALG, S_ALG)
    # Icons
    if icons:
        x += 4
        draw_icons(c, icons, x, base)
        x += icons_width(icons)
    # Preis
    c.setFont(F_PRICE, S_PRICE); c.setFillColor(CREAM_BR)
    pw = pdfmetrics.stringWidth(price, F_PRICE, S_PRICE)
    c.drawRightString(PRICE_R, base, price)
    # Punktlinie
    x0, x1 = x + 6, PRICE_R - pw - 6
    if x1 - x0 > 14:
        c.saveState()
        c.setStrokeColor(DOTCOL); c.setLineWidth(0.9)
        c.setLineCap(1); c.setDash(0.1, 3.1)
        c.line(x0, base + 1.4, x1, base + 1.4)
        c.restoreState()
    y = y - LEAD_ITEM
    # Beschreibung
    if desc:
        c.setFont(F_DESC, S_DESC); c.setFillColor(CREAM)
        for ln in simpleSplit(desc, F_DESC, S_DESC, desc_maxw):
            c.drawString(NAME_X, y - S_DESC + 1.5, ln)
            y -= LEAD_DESC
        y -= 1.5
    return y - GAP_ITEM

def section_note(c, text, y):
    c.setFont(F_NOTE, S_NOTE); c.setFillColor(CREAM)
    c.drawCentredString(W/2, y - S_NOTE, text)
    return y - S_NOTE - 10

# ---------- Freisteller ----------
# Fotos ohne weißen Hintergrund: runde Schale per Kreismaske freistellen (cx, cy, r im Quellbild)
CIRCLE_CUTS = {}

def cutout_slot(c, key, cx, cy, target_h):
    """Foto freistellen (weißer Hintergrund, Transparenz oder Kreismaske) und rahmenlos einsetzen."""
    src = None
    for ext in (".jpg.png", ".jpg.tiff", ".tiff", ".tif", ".png", ".jpg", ".jpeg"):
        p = os.path.join(PHOTOS, key + ext)
        if os.path.exists(p):
            src = p; break
    if not src:
        return
    dst = os.path.join(HERE, f"_cut_{key}.png")
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        raw = Image.open(src)
        has_alpha = "transparency" in raw.info or (
            raw.mode in ("RGBA", "LA", "P") and raw.convert("RGBA").getchannel("A").getextrema()[0] < 200)
        if key in CIRCLE_CUTS and not has_alpha:
            from cutout import circle_cut
            circle_cut(src, dst, *CIRCLE_CUTS[key])
        else:
            from cutout import remove_white_bg
            remove_white_bg(src, dst)
    img = Image.open(dst)
    w = target_h * img.width / img.height
    c.drawImage(dst, cx - w/2, cy - target_h/2, w, target_h, mask='auto')

def rect_photo(c, key, x, y, w, h, radius=10):
    """Foto in abgerundetem Rechteck (Cover-Zuschnitt)."""
    src = None
    for ext in (".jpg", ".jpeg", ".png"):
        p = os.path.join(PHOTOS, key + ext)
        if os.path.exists(p):
            src = p; break
    if not src:
        return
    img = Image.open(src).convert("RGB")
    ratio = w / h
    iw, ih = img.size
    if iw/ih > ratio:  # zu breit -> seitlich beschneiden
        nw = int(ih * ratio)
        l = (iw - nw)//2
        img = img.crop((l, 0, l + nw, ih))
    else:
        nh = int(iw / ratio)
        t = (ih - nh)//2
        img = img.crop((0, t, iw, t + nh))
    tmp = os.path.join(HERE, f"_rect_{key}.jpg")
    img.save(tmp, "JPEG", quality=90)
    c.saveState()
    p = c.beginPath()
    p.roundRect(x, y, w, h, radius)
    c.clipPath(p, stroke=0)
    c.drawImage(tmp, x, y, w, h)
    c.restoreState()
    c.saveState()
    c.setStrokeColor(Color(0, 0, 0, alpha=0.5)); c.setLineWidth(5)
    c.roundRect(x - 2, y - 2, w + 4, h + 4, radius + 2, stroke=1, fill=0)
    c.setStrokeColor(ORN); c.setLineWidth(1.1)
    c.roundRect(x, y, w, h, radius, stroke=1, fill=0)
    c.restoreState()

# ---------- Foto-Slot ----------
def photo_slot(c, key, label, cx, cy, r):
    path = None
    for ext in (".jpg", ".jpeg", ".png"):
        p = os.path.join(PHOTOS, key + ext)
        if os.path.exists(p):
            path = p; break
    c.saveState()
    if path:
        img = Image.open(path).convert("RGB")
        side = min(img.size)
        l = (img.width - side)//2; t = (img.height - side)//2
        img = img.crop((l, t, l + side, t + side))
        tmp = os.path.join(HERE, f"_crop_{key}.jpg")
        img.save(tmp, "JPEG", quality=90)
        p = c.beginPath(); p.circle(cx, cy, r)
        c.clipPath(p, stroke=0)
        c.drawImage(tmp, cx - r, cy - r, 2*r, 2*r)
        c.restoreState(); c.saveState()
        c.setStrokeColor(Color(0, 0, 0, alpha=0.55)); c.setLineWidth(6)
        c.circle(cx, cy, r + 3, stroke=1, fill=0)
        c.setStrokeColor(ORN); c.setLineWidth(1.1)
        c.circle(cx, cy, r + 1, stroke=1, fill=0)
    else:
        c.setFillColor(Color(1, 1, 1, alpha=0.04))
        c.circle(cx, cy, r, stroke=0, fill=1)
        c.setStrokeColor(Color(0.66, 0.51, 0.31, alpha=0.8)); c.setLineWidth(1)
        c.setDash(4, 4)
        c.circle(cx, cy, r, stroke=1, fill=0)
        c.setDash()
        c.setFillColor(Color(0.85, 0.78, 0.66, alpha=0.75))
        c.setFont("Serif-I", 10)
        c.drawCentredString(cx, cy + 3, "Foto")
        c.setFont("Cond", 8.2)
        c.drawCentredString(cx, cy - 9, label)
    c.restoreState()

# ---------- Seiten ----------
def start_page(c, spark=False):
    # Nullpunkt auf die A4-Ecke schieben -> alle Layout-Koordinaten bleiben identisch
    if BLEED:
        c.translate(BLEED, BLEED)
    draw_bg(c)

def sec_by_id(sid):
    return next(s for s in SECTIONS if s["id"] == sid)

def render_sections(c, y, ids, desc_indent=0):
    maxw = CW - (NAME_X - ML) - 30*mm
    for sid in ids:
        s = sec_by_id(sid)
        if s.get("title"):
            y = section_header(c, s["title"], y)
        if s.get("subtitle"):
            y = sub_header(c, s["subtitle"], y)
        if s.get("note"):
            y = section_note(c, s["note"], y)
        for it in s["items"]:
            y = draw_item(c, it, y, maxw)
        if s.get("extras"):
            y -= 2
            c.setFont("Cond-B", 10.2); c.setFillColor(CREAM)
            c.drawCentredString(W/2, y - 10, s["extras"])
            y -= 24
        y -= GAP_SEC
    return y

LOGO = os.path.join(HERE, "logo.jpg")

def draw_logo(c, cx, cy, r):
    img = Image.open(LOGO).convert("RGB")
    side = min(img.size)
    l = (img.width - side)//2; t = (img.height - side)//2
    img = img.crop((l, t, l + side, t + side))
    tmp = os.path.join(HERE, "_logo_sq.jpg")
    if not os.path.exists(tmp):
        img.save(tmp, "JPEG", quality=92)
    c.saveState()
    p = c.beginPath(); p.circle(cx, cy, r)
    c.clipPath(p, stroke=0)
    c.drawImage(tmp, cx - r, cy - r, 2*r, 2*r)
    c.restoreState()
    c.saveState()
    c.setStrokeColor(Color(0.72, 0.55, 0.32, alpha=0.9)); c.setLineWidth(1.2)
    c.circle(cx, cy, r + 2, stroke=1, fill=0)
    c.restoreState()

def page_cover(c):
    start_page(c)
    R = RESTAURANT
    # Name
    y = H - 34*mm
    for line in R["name"].split(" ", 1):
        spaced_text(c, line, W/2, y, F_H1, 30, 4.5, TAN)
        y -= 38
    y += 8
    ornament(c, W/2, y, half=120)
    if R.get("subtitle"):
        y -= 26
        c.setFont("Serif-I", 16); c.setFillColor(CREAM_BR)
        c.drawCentredString(W/2, y, R["subtitle"])
    # Logo
    draw_logo(c, W/2, H*0.565, 34*mm)
    # Adresse / Telefon
    y = H*0.565 - 34*mm - 14*mm
    spaced_text(c, "ADRESSE", W/2, y, F_SUB, 12.5, 2, TAN)
    y -= 15
    c.setFont("Cond", 11.5); c.setFillColor(CREAM_BR)
    for ln in R["address"]:
        c.drawCentredString(W/2, y, ln); y -= 14
    y -= 6
    spaced_text(c, "TELEFON", W/2, y, F_SUB, 12.5, 2, TAN)
    y -= 15
    c.setFont("Cond", 11.5); c.setFillColor(CREAM_BR)
    for ln in R["phone"]:
        c.drawCentredString(W/2, y, ln); y -= 14
    # Tagline
    y -= 10
    c.setFont("Serif-I", 14.5); c.setFillColor(TAN_LT)
    for ln in R["tagline"].split("\n"):
        c.drawCentredString(W/2, y, ln); y -= 18
    y -= 4
    c.setFont("Cond", 9.4); c.setFillColor(CREAM)
    for ln in simpleSplit(R["welcome"], "Cond", 9.4, CW - 30*mm):
        c.drawCentredString(W/2, y, ln); y -= 12
    c.showPage()

def page_items(c, ids, *photos):
    """photos: ("circle", key, label, cx, cy, r) | ("cutout", key, cx, cy, h)"""
    start_page(c)
    y = H - MT
    y = render_sections(c, y, ids)
    for ph in photos:
        if ph[0] == "circle":
            _, key, label, cx, cy, r = ph
            photo_slot(c, key, label, cx, cy, r)
        elif ph[0] == "cutout":
            _, key, cx, cy, hh = ph
            cutout_slot(c, key, cx, cy, hh)
    c.showPage()
    return y

def page_legend(c):
    start_page(c)
    y = section_header(c, "LEGENDE & ZUSATZSTOFFE", H - MT, size=19)
    y -= 4
    # Symbole
    c.setFont(F_SUB, 13); c.setFillColor(TAN)
    c.drawCentredString(W/2, y - 13, "Symbole auf der Speisekarte")
    y -= 34
    cx = W/2
    c.setFont("Cond", 10.5); c.setFillColor(CREAM_BR)
    leaf_icon(c, cx - 108, y, 8)
    c.drawString(cx - 95, y, "Vegetarisch")
    chili_icon(c, cx - 18, y, 8)
    c.drawString(cx - 5, y, "Pikant / Scharf")
    crescent_icon(c, cx + 88, y + 3.5, 5.2, TAN)
    c.setFont("Cond", 10.5); c.setFillColor(CREAM_BR)
    c.drawString(cx + 98, y, "Halal")
    y -= 30
    c.setFont(F_SUB, 13); c.setFillColor(TAN)
    c.drawCentredString(W/2, y - 13, "Zusatzstoffe & Allergene (1–12)")
    y -= 40
    x_nr, x_name, x_det = ML + 6*mm, ML + 16*mm, ML + 72*mm
    for nr, name, det in ADDITIVES:
        c.setFont("Cond-B", 10.5); c.setFillColor(TAN_LT)
        c.drawRightString(x_nr + 8, y, nr)
        c.drawString(x_name, y, name)
        c.setFont("Cond", 10); c.setFillColor(CREAM)
        for i, ln in enumerate(simpleSplit(det, "Cond", 10, W - MR - x_det)):
            c.drawString(x_det, y - i*12, ln)
            if i: y -= 12
        y -= 21
    c.showPage()

def page_city(c):
    start_page(c)
    y = section_header(c, "ENTDECKE DIYARBAKIR", H - MT)
    y -= 6
    c.setFont("Cond", 10.6); c.setFillColor(CREAM_BR)
    for para in DIYARBAKIR_TEXT:
        for ln in simpleSplit(para, "Cond", 10.6, CW - 14*mm):
            c.drawCentredString(W/2, y - 10, ln)
            y -= 14.6
        y -= 12
    ph_h = y - MB - 10*mm
    rect_photo(c, "diyarbakir", ML + 4*mm, MB + 4*mm, CW - 8*mm, ph_h, radius=12)
    c.showPage()

def page_back(c):
    start_page(c)
    R = RESTAURANT
    y = H - 30*mm
    for ln in ("HOLZKOHLEGRILL", "& HOLZOFEN SPEZIALITÄTEN"):
        spaced_text(c, ln, W/2, y, F_H1, 19, 2.4, TAN)
        y -= 26
    draw_logo(c, W/2, y - 36*mm, 32*mm)
    y = y - 72*mm - 12*mm
    c.setFont(F_SUB, 15); c.setFillColor(CREAM_BR)
    c.drawCentredString(W/2, y, "Wiesbaden")
    y -= 34
    c.setFont(F_SUB, 14.5); c.setFillColor(TAN)
    c.drawCentredString(W/2, y, "Qualitätsversprechen")
    y -= 18
    c.setFont("Cond-B", 12); c.setFillColor(CREAM_BR)
    qw = pdfmetrics.stringWidth(R["quality"], "Cond-B", 12)
    group_w = qw + 16 + 26          # Text + Abstand + Badge-Durchmesser
    tx = W/2 - group_w/2            # linke Kante des Textes
    c.drawString(tx, y, R["quality"])
    # Halal-Badge
    bx = tx + qw + 16 + 13
    c.setStrokeColor(CREAM_BR); c.setLineWidth(1)
    c.circle(bx, y + 4, 13, stroke=1, fill=0)
    crescent_icon(c, bx, y + 7.5, 5.4, CREAM_BR)
    c.setFont("Cond", 5.6); c.setFillColor(CREAM_BR)
    c.drawCentredString(bx, y - 4.5, "HALAL")
    y -= 26
    ornament(c, W/2, y, half=90)
    y -= 30
    c.setFont(F_SUB, 14.5); c.setFillColor(TAN)
    c.drawCentredString(W/2, y, "Öffnungszeiten")
    y -= 18
    c.setFont("Cond", 12); c.setFillColor(CREAM_BR)
    c.drawCentredString(W/2, y, R["hours"])
    free_cy = (y - 14*mm - MB)/2 + MB
    cutout_slot(c, "back", W/2, free_cy, min(105*mm, y - 22*mm - MB))
    c.showPage()

# ---------- Build ----------
def main():
    c = canvas.Canvas(OUT, pagesize=PAGE)
    c.setTitle("Speisekarte – Diyarbakir Restaurant Wiesbaden")
    if BLEED:
        # Endformat A4 mitteilen, damit die Druckerei weiß, wo geschnitten wird
        trim = (BLEED, BLEED, BLEED + W, BLEED + H)
        for setter in ("setTrimBox", "setArtBox"):
            if hasattr(c, setter):
                getattr(c, setter)(trim)
        if hasattr(c, "setBleedBox"):
            c.setBleedBox((0, 0, PAGE[0], PAGE[1]))
    page_cover(c)                                                        # 1
    page_items(c, ["suppen", "meze"], ("cutout", "suppe", W - 30*mm, 84*mm, 66*mm))               # 2
    page_items(c, ["salate"],        ("cutout", "salat", W/2, 112*mm, 88*mm))                     # 3
    page_items(c, ["grill"],         ("circle", "grill", "Grillplatte", W - 42*mm, 40*mm, 26*mm)) # 4
    page_items(c, ["pizza"],         ("circle", "pizza", "Holzofen-Pizza", W - 40*mm, 34*mm, 22*mm))   # 5
    page_items(c, ["doener", "duerum"], ("cutout", "doener", W - 44*mm, 38*mm, 46*mm))            # 6
    page_items(c, ["pide", "veg"],   ("cutout", "pide", W - 52*mm, 44*mm, 52*mm))                 # 7
    page_items(c, ["desserts"],
               ("cutout", "baklava", W/2 - 42*mm, 98*mm, 82*mm),
               ("cutout", "kuenefe", W - 26*mm, 95*mm, 62*mm))                                    # 8
    page_items(c, ["heiss", "kalt", "kalt2"],
               ("cutout", "softgetraenke", W/2 - 38*mm, 42*mm, 52*mm),
               ("cutout", "tee", W/2 + 42*mm, 44*mm, 58*mm))                                      # 9
    page_legend(c)                                                                                # 10
    page_city(c)                                                                                  # 11
    page_back(c)                                                                                  # 12
    c.save()
    print("OK ->", OUT)

if __name__ == "__main__":
    main()
