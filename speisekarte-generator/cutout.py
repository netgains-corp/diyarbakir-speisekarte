# -*- coding: utf-8 -*-
"""Weißen Hintergrund freistellen (Flood-Fill von den Rändern, damit
weiße Flächen IM Objekt – Logos, Zuckerwürfel, Glanzlichter – erhalten bleiben)."""
import numpy as np
from PIL import Image, ImageFilter
from collections import deque

def remove_white_bg(src, dst, tol=28, feather=1.2):
    raw = Image.open(src)
    # Bereits transparente Bilder (PNG/TIFF mit Alpha): Alpha übernehmen
    if "transparency" in raw.info or (raw.mode in ("RGBA", "LA", "P") and raw.convert("RGBA").getchannel("A").getextrema()[0] < 200):
        out = raw.convert("RGBA")
        box = out.getbbox()
        if box:
            out = out.crop(box)
        return _bake_shadow(out, dst)
    im = raw.convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    # "weiß-ähnlich": alle Kanäle nah an 255
    near_white = (a.min(axis=2) >= 255 - tol*2) & (a.max(axis=2) - a.min(axis=2) <= tol)
    bg = np.zeros((h, w), dtype=bool)
    dq = deque()
    for x in range(w):
        for y in (0, h-1):
            if near_white[y, x] and not bg[y, x]:
                bg[y, x] = True; dq.append((y, x))
    for y in range(h):
        for x in (0, w-1):
            if near_white[y, x] and not bg[y, x]:
                bg[y, x] = True; dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for ny, nx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
            if 0 <= ny < h and 0 <= nx < w and near_white[ny, nx] and not bg[ny, nx]:
                bg[ny, nx] = True; dq.append((ny, nx))
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    am = Image.fromarray(alpha, "L").filter(ImageFilter.GaussianBlur(feather))
    # Halbtransparente Kante: leicht nach innen ziehen gegen weiße Säume
    am = am.point(lambda p: 0 if p < 90 else min(255, int((p-90)*255/165)))
    out = im.convert("RGBA")
    out.putalpha(am)
    # auf Inhalt beschneiden
    box = out.getbbox()
    if box:
        out = out.crop(box)
    return _bake_shadow(out, dst)

def _bake_shadow(out, dst):
    # weicher Schlagschatten, direkt eingebacken
    pad = 30
    cw, ch = out.width + 2*pad, out.height + 2*pad
    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    sh = Image.new("L", (cw, ch), 0)
    sh.paste(out.split()[3], (pad + 4, pad + 10))
    sh = sh.filter(ImageFilter.GaussianBlur(9)).point(lambda p: int(p*0.45))
    shadow = Image.new("RGBA", (cw, ch), (0, 0, 0, 255))
    shadow.putalpha(sh)
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(out, (pad, pad))
    canvas.save(dst, "PNG")
    return canvas.size

def circle_cut(src, dst, cx, cy, r, feather=2.0):
    """Runde Schale/Teller per Kreismaske freistellen (für Fotos ohne weißen Hintergrund)."""
    im = Image.open(src).convert("RGBA")
    mask = Image.new("L", im.size, 0)
    ImageDraw = __import__("PIL.ImageDraw", fromlist=["ImageDraw"])
    d = ImageDraw.Draw(mask)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather))
    im.putalpha(mask)
    im = im.crop(im.getbbox())
    return _bake_shadow(im, dst)

if __name__ == "__main__":
    import sys
    print(remove_white_bg(sys.argv[1], sys.argv[2]))
