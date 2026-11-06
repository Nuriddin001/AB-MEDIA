"""Kadr-kartochkalar: botning har bir ekrani — kino kadri.

Hammasi Pillow bilan chiziladi (1280x720, 16:9), landing page'dagi
"tungi suratga olish" uslubida: to'q fon, volfram (tungsten) chiroq rangi,
ko'k chroma nur, letterbox polosalar, plyonka donadorligi.
"""
from __future__ import annotations

import io
import math
import random
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ASSETS = Path(__file__).parent / "assets"
FONTS = ASSETS / "fonts"

W, H = 1280, 720
BG = (10, 12, 19)
BG2 = (17, 20, 31)
BG3 = (24, 28, 43)
LINE = (38, 43, 61)
FG = (242, 237, 229)
MUTED = (169, 174, 191)
DIM = (110, 116, 136)
TUNG = (255, 180, 94)
CHROMA = (61, 91, 255)
REC = (255, 77, 61)

# Kartochka dizayni o'zgarsa — shu raqamni oshiring, bot rasmlarni qayta yuklaydi.
RENDER_VERSION = 6


# ───────────────────────── asboblar ─────────────────────────

@lru_cache(maxsize=64)
def font(kind: str, size: int, weight: str = "Regular") -> ImageFont.FreeTypeFont:
    path = {"display": "SofiaSansExtraCondensed.ttf",
            "body": "GolosText.ttf",
            "mono": "JetBrainsMono.ttf"}[kind]
    f = ImageFont.truetype(str(FONTS / path), size)
    try:
        f.set_variation_by_name(weight)
    except Exception:  # Pillow versiyasiga qarab bytes kerak bo'lishi mumkin
        try:
            f.set_variation_by_name(weight.encode())
        except Exception:
            pass
    return f


@lru_cache(maxsize=4)
def _photo(name: str) -> Image.Image:
    return Image.open(ASSETS / name).convert("RGB")


def canvas(color=BG) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), color)
    return img, ImageDraw.Draw(img)


def glow(img: Image.Image, cx: int, cy: int, r: int, color, strength: float = 0.55):
    """Yumshoq nur dog'i (radial gradient)."""
    # radial_gradient ichki aylana chetida 181 ga yetadi — shu nuqtada 0 ga tushiramiz
    lut = [int(255 * strength * max(0.0, 1 - v / 181) ** 2) for v in range(256)]
    g = Image.radial_gradient("L").resize((r * 2, r * 2), Image.BILINEAR).point(lut)
    layer = Image.new("RGB", (r * 2, r * 2), color)
    img.paste(layer, (cx - r, cy - r), g)


def grain(img: Image.Image, amount: float = 0.07, seed: int = 7) -> Image.Image:
    random.seed(seed)
    noise = Image.effect_noise((W, H), 48).convert("RGB")
    return Image.blend(img, noise, amount)


def vignette(img: Image.Image, strength: float = 0.55) -> Image.Image:
    g = Image.radial_gradient("L").resize((W, H))  # markaz 0, chet 255
    g = g.point(lambda v: int(max(0, v - 90) * strength))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    out = img.copy()
    out.paste(dark, (0, 0), g)
    return out


def letterbox(d: ImageDraw.ImageDraw, h: int = 46):
    d.rectangle([0, 0, W, h], fill=(5, 6, 10))
    d.rectangle([0, H - h, W, H], fill=(5, 6, 10))


def wrap(text: str, f: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split():
            test = (cur + " " + word).strip()
            if f.getlength(test) <= width or not cur:
                cur = test
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def fit_lines(text: str, kind: str, weight: str, width: int, max_lines: int,
              start: int, minimum: int) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    size = start
    while size > minimum:
        f = font(kind, size, weight)
        lines = wrap(text, f, width)
        if len(lines) <= max_lines and all(f.getlength(l) <= width for l in lines):
            return f, lines
        size -= 4
    f = font(kind, minimum, weight)
    return f, wrap(text, f, width)


def draw_lines(d, xy, lines, f, fill, spacing: float = 1.0, anchor="la"):
    x, y = xy
    step = int(f.size * spacing)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill, anchor=anchor)
        y += step
    return y


def hgrad_mask(w: int, h: int, start: float, end: float) -> Image.Image:
    """Chapdan o'ngga 0→255 o'tuvchi maska (start..end — ulushlar)."""
    m = Image.new("L", (w, h))
    px = []
    for x in range(w):
        t = (x / w - start) / max(1e-6, end - start)
        px.append(int(255 * min(1, max(0, t))))
    row = Image.new("L", (w, 1))
    row.putdata(px)
    return row.resize((w, h))


def rec_dot(d, x, y, label: str):
    d.ellipse([x, y - 6, x + 12, y + 6], fill=REC)
    d.text((x + 22, y), label, font=font("mono", 18, "Medium"), fill=FG, anchor="lm")


def slate_stripes(img: Image.Image, box, closed: bool = True, angle: float = -14):
    """Kinoxlopushka qanoti — qora-oq diagonal chiziqlar."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    arm = Image.new("RGBA", (w, h), (20, 20, 24, 255))
    ad = ImageDraw.Draw(arm)
    step = 46
    for i in range(-h, w + h, step * 2):
        ad.polygon([(i, h), (i + step, h), (i + step + h, 0), (i + h, 0)], fill=FG + (255,))
    if not closed:
        arm = arm.rotate(angle, expand=True, resample=Image.BICUBIC,
                         center=(0, h))
        img.paste(arm, (x0, y0 - (arm.height - h)), arm)
    else:
        img.paste(arm, (x0, y0), arm)


def to_bytes(img: Image.Image, fmt: str = "JPEG") -> bytes:
    buf = io.BytesIO()
    if fmt == "JPEG":
        img.save(buf, "JPEG", quality=90, optimize=True, progressive=True)
    else:
        img.save(buf, fmt)
    return buf.getvalue()


def finish(img: Image.Image, bars: bool = True) -> bytes:
    img = vignette(img, 0.45)
    img = grain(img, 0.06)
    if bars:
        letterbox(ImageDraw.Draw(img))
    return to_bytes(img)


def timecode(sec: float, fr: int = 0) -> str:
    s = int(sec)
    return f"{s // 3600:02d}:{s // 60 % 60:02d}:{s % 60:02d}:{fr:02d}"


# ───────────────────────── kartochkalar ─────────────────────────

def card_cover(name_lines: tuple[str, str], role: str, slate: tuple[str, ...]) -> bytes:
    """Bosh ekran: portret + katta ism + xlopushka qatori."""
    img, d = canvas()
    glow(img, 980, 300, 520, CHROMA, 0.35)
    glow(img, 260, 620, 420, TUNG, 0.12)

    p = _photo("portrait.jpg")
    ph = H
    pw = int(ph * 0.82)
    crop = p.crop((290, 40, 290 + 700, 40 + int(700 / 0.82)))
    crop = crop.resize((pw, ph), Image.LANCZOS)
    # iliq "volfram" grading
    warm = Image.new("RGB", crop.size, (255, 170, 90))
    crop = Image.blend(crop, warm, 0.08)
    px = W - pw + 40
    img.paste(crop, (px, 0), hgrad_mask(pw, ph, 0.0, 0.42))
    d = ImageDraw.Draw(img)

    rec_dot(d, 64, 96, "REC  ·  AB MEDIA")
    big = font("display", 168, "Black")
    y = 140
    for ln in name_lines:
        f, _ = fit_lines(ln.upper(), "display", "Black", 700, 1, 168, 96)
        d.text((60, y), ln.upper(), font=f, fill=FG)
        y += int(f.size * 0.86)
    d.rectangle([64, y + 22, 64 + 64, y + 26], fill=TUNG)
    d.text((64, y + 46), role, font=font("body", 30, "Medium"), fill=TUNG)

    # xlopushka qatori
    sx, sy = 64, H - 150
    cell_w = [180, 120, 120, 120]
    labels = slate
    values = ["AB MEDIA", "01", "01", "01"]
    x = sx
    for i, cw in enumerate(cell_w):
        d.rectangle([x, sy, x + cw, sy + 74], outline=LINE, width=2)
        d.text((x + 12, sy + 10), labels[i].upper(), font=font("body", 15, "SemiBold"), fill=DIM)
        d.text((x + 12, sy + 34), values[i], font=font("mono", 24, "Medium"), fill=FG)
        x += cw - 2
    d.text((W - 60, H - 90), timecode(12, 8), font=font("mono", 22, "Medium"), fill=FG, anchor="rs")
    return finish(img)


def card_language() -> bytes:
    """Til tanlash: ochiq xlopushka, uch tilda sarlavha."""
    img, d = canvas()
    glow(img, 640, 360, 560, CHROMA, 0.28)
    glow(img, 640, 700, 380, TUNG, 0.16)
    d = ImageDraw.Draw(img)
    bx0, by0, bx1, by1 = 290, 250, 990, 600
    slate_stripes(img, (bx0, by0 - 70, bx1, by0 - 6), closed=False, angle=-12)
    slate_stripes(img, (bx0, by0 - 2, bx1, by0 + 64))
    d = ImageDraw.Draw(img)
    d.rectangle([bx0, by0 + 64, bx1, by1], fill=(14, 16, 24), outline=LINE, width=3)
    rows = [("O'zbekcha", "UZ"), ("Русский", "RU"), ("English", "EN")]
    y = by0 + 98
    for txt, code in rows:
        d.text((bx0 + 40, y), code, font=font("mono", 30, "Medium"), fill=TUNG)
        d.text((bx0 + 120, y - 8), txt.upper(), font=font("display", 66, "ExtraBold"), fill=FG)
        y += 82
        if code != "EN":
            d.line([bx0 + 40, y - 12, bx1 - 40, y - 12], fill=LINE, width=2)
    d.text((640, 120), "ABROR BAXTIYAROVICH · AB MEDIA", font=font("mono", 22, "Medium"),
           fill=MUTED, anchor="mm")
    return finish(img)


def card_about(kicker: str, headline: str, chips: tuple[str, str]) -> bytes:
    img, d = canvas()
    st = _photo("stage.jpg").resize((H, H), Image.LANCZOS)
    img.paste(st, (0, 0))
    # o'ng tomonga qorong'i o'tish
    fade = Image.new("RGB", (W, H), BG)
    img.paste(fade, (0, 0), hgrad_mask(W, H, 0.40, 0.58))
    glow(img, 1050, 200, 380, CHROMA, 0.22)
    d = ImageDraw.Draw(img)
    x = 740
    d.text((x, 130), kicker.upper(), font=font("mono", 20, "Medium"), fill=TUNG)
    f, lines = fit_lines(headline.upper(), "display", "ExtraBold", 480, 5, 92, 52)
    y = draw_lines(d, (x, 170), lines, f, FG, 0.92)
    y += 30
    for chip in chips:
        cf = font("body", 24, "SemiBold")
        tw = cf.getlength(chip)
        d.rounded_rectangle([x, y, x + tw + 36, y + 48], radius=6, fill=TUNG)
        d.text((x + 18, y + 24), chip, font=cf, fill=(27, 18, 6), anchor="lm")
        x += tw + 52
    return finish(img)


CASE_GLOW = [(22, 30), (70, 55), (35, 70), (78, 35), (48, 45)]


def card_case(i: int, total: int, client: str, concept: str, executor: str) -> bytes:
    img, d = canvas(BG2)
    gx, gy = CASE_GLOW[i % len(CASE_GLOW)]
    glow(img, int(W * gx / 100), int(H * gy / 100), 560, CHROMA, 0.62)
    glow(img, int(W * (100 - gx) / 100), int(H * 0.9), 480, TUNG, 0.32)
    d = ImageDraw.Draw(img)
    f, lines = fit_lines(client.upper(), "display", "Black", 1080, 2, 190, 96)
    lh = int(f.size * 0.86)
    block = lh * len(lines)
    cf, clines = fit_lines(concept, "body", "Regular", 940, 4, 30, 22)
    total_h = block + 40 + int(cf.size * 1.4) * len(clines)
    y = (H - total_h) // 2 + 10
    for ln in lines:
        d.text((W // 2, y), ln, font=f, fill=FG, anchor="ma")
        y += lh
    y += 40
    for ln in clines:
        d.text((W // 2, y), ln, font=cf, fill=(214, 216, 240), anchor="ma")
        y += int(cf.size * 1.4)
    out = vignette(img, 0.35)
    out = grain(out, 0.06, seed=i)
    d = ImageDraw.Draw(out)
    letterbox(d, 64)
    m = font("mono", 18, "Medium")
    tag = "AB MEDIA · PRODUCTION" if executor.upper() == "AB MEDIA" else f"AB MEDIA × {executor.upper()}"
    d.text((40, H - 32), tag, font=m, fill=FG, anchor="ls")
    d.text((W - 40, H - 32), f"SC {i + 1:02d} / {total:02d}", font=m, fill=FG, anchor="rs")
    d.text((40, 32), "● REC", font=m, fill=REC, anchor="lm")
    d.text((W - 40, 32), timecode(37 + i * 41, (i * 7) % 25), font=m, fill=FG, anchor="rm")
    return to_bytes(out)


def card_journey(title: str, stages: list[tuple[str, str]], focus: list[int],
                 focus_label: str, active: int | None = None) -> bytes:
    """Mijoz yo'li — kino obyektivining fokus shkalasi sifatida."""
    img, d = canvas()
    glow(img, 640, 120, 600, CHROMA, 0.25)
    d = ImageDraw.Draw(img)
    d.text((64, 96), title.upper(), font=font("display", 76, "ExtraBold"), fill=FG)

    # obyektiv barabani
    x0, x1, y0, y1 = 40, W - 40, 300, 580
    d.rounded_rectangle([x0, y0, x1, y1], radius=26, fill=(21, 23, 29), outline=(48, 52, 66), width=2)
    # rifel (knurl)
    for x in range(x0 + 20, x1 - 20, 9):
        d.line([x, y0 + 14, x, y0 + 54], fill=(36, 39, 48), width=3)
    d.line([x0, y0 + 66, x1, y0 + 66], fill=(48, 52, 66), width=2)
    # shkala
    n = len(stages)
    pad = 150
    seg = (x1 - x0 - 2 * pad) / (n - 1)
    for k in range(0, int((x1 - x0 - 120) / 12) + 1):
        x = x0 + 60 + k * 12
        long_ = k % 5 == 0
        d.line([x, y0 + 80, x, y0 + (110 if long_ else 96)], fill=(80, 84, 100), width=2)
    for i, (name, _) in enumerate(stages):
        cx = int(x0 + pad + i * seg)
        on = i in focus
        is_act = active == i
        col = TUNG if on else MUTED
        if is_act:
            d.rounded_rectangle([cx - 110, y0 + 120, cx + 110, y1 - 20], radius=14,
                                outline=TUNG, width=3)
        d.line([cx, y0 + 74, cx, y0 + 126], fill=col, width=4 if on else 2)
        f, lines = fit_lines(name.upper(), "display", "ExtraBold", 210, 1, 54, 30)
        d.text((cx, y0 + 140), lines[0], font=f, fill=col if (on or is_act) else (150, 154, 170), anchor="ma")
        d.text((cx, y0 + 215), f"{i + 1:02d}", font=font("mono", 22, "Medium"), fill=DIM, anchor="ma")
    # fokus belgisi (indeks uchburchagi) — focus bosqichlari ustida
    for i in focus:
        cx = int(x0 + pad + i * seg)
        d.polygon([(cx - 14, y0 - 30), (cx + 14, y0 - 30), (cx, y0 - 8)], fill=TUNG)
        d.text((cx, y0 - 44), focus_label.upper(), font=font("mono", 18, "Medium"), fill=TUNG, anchor="ms")
    # yorug'lik yo'li
    fx = [int(x0 + pad + i * seg) for i in focus]
    if len(fx) == 2:
        d.line([fx[0], y0 - 4, fx[1], y0 - 4], fill=TUNG, width=2)
    return finish(img)


def card_process(title: str, steps: list[tuple[str, str]], active: int) -> bytes:
    """Montaj taymlayni: 5 ta klip, playhead aktiv bosqichda."""
    img, d = canvas()
    glow(img, 300, 200, 480, TUNG, 0.14)
    glow(img, 1100, 650, 520, CHROMA, 0.25)
    d = ImageDraw.Draw(img)
    d.text((64, 90), title.upper(), font=font("mono", 20, "Medium"), fill=MUTED)
    # katta sarlavha
    num = f"{active + 1:02d}"
    d.text((60, 120), num, font=font("display", 220, "Black"), fill=TUNG)
    nx = 60 + font("display", 220, "Black").getlength(num) + 36
    f, lines = fit_lines(steps[active][0].upper(), "display", "ExtraBold", int(W - nx - 60), 2, 120, 64)
    draw_lines(d, (nx, 150), lines, f, FG, 0.9)
    df, dlines = fit_lines(steps[active][1], "body", "Regular", int(W - nx - 60), 3, 30, 22)
    draw_lines(d, (nx, 150 + int(f.size * 0.9) * len(lines) + 18), dlines, df, MUTED, 1.35)

    # taymlayn paneli
    px0, py0, px1, py1 = 40, 430, W - 40, 640
    d.rounded_rectangle([px0, py0, px1, py1], radius=12, fill=BG2, outline=LINE, width=2)
    # chizg'ich
    for x in range(px0 + 20, px1 - 20, 12):
        long_ = (x - px0 - 20) % 60 == 0
        d.line([x, py0 + (18 if long_ else 26), x, py0 + 34], fill=MUTED if long_ else DIM, width=1)
    # klip trek
    n = len(steps)
    tw = (px1 - px0 - 40)
    cw = (tw - (n - 1) * 6) / n
    for i in range(n):
        cx0 = int(px0 + 20 + i * (cw + 6))
        cx1 = int(cx0 + cw)
        on = i == active
        done = i < active
        fill = (77, 56, 34) if on else ((40, 36, 40) if done else BG3)
        d.rounded_rectangle([cx0, py0 + 52, cx1, py0 + 132], radius=6, fill=fill,
                            outline=TUNG if on else LINE, width=2)
        for x in range(cx0 + 4, cx1 - 4, 5):
            d.line([x, py0 + 112, x, py0 + 128], fill=LINE, width=2)
        d.text((cx0 + 12, py0 + 64), steps[i][0].upper(), font=font("body", 17, "SemiBold"),
               fill=FG if (on or done) else DIM)
        d.text((cx0 + 12, py0 + 156), f"V1  ·  C{i + 1:02d}", font=font("mono", 15, "Medium"), fill=DIM)
    # playhead
    phx = int(px0 + 20 + active * (cw + 6) + cw * 0.5)
    d.line([phx, py0 + 10, phx, py1 - 14], fill=TUNG, width=3)
    d.polygon([(phx - 10, py0 + 6), (phx + 10, py0 + 6), (phx, py0 + 20)], fill=TUNG)
    tc = f"00:{active * 12:02d}:{(active * 7) % 25:02d}"
    d.text((min(phx + 12, px1 - 110), py0 + 10), tc, font=font("mono", 17, "Medium"), fill=TUNG)
    return finish(img)


def card_services(kicker: str, a: tuple[str, str], b: tuple[str, str]) -> bytes:
    img, d = canvas()
    glow(img, 320, 360, 460, TUNG, 0.16)
    glow(img, 960, 360, 460, CHROMA, 0.30)
    d = ImageDraw.Draw(img)
    d.text((64, 96), kicker.upper(), font=font("mono", 20, "Medium"), fill=MUTED)
    for col, (letter, (title, items)) in enumerate(zip("AB", (a, b))):
        x = 64 + col * 600
        accent = TUNG if col == 0 else (140, 160, 255)
        d.text((x, 130), letter, font=font("display", 230, "Black"), fill=accent)
        f, lines = fit_lines(title.upper(), "display", "ExtraBold", 520, 2, 76, 48)
        y = draw_lines(d, (x, 380), lines, f, FG, 0.92)
        d.line([x, y + 14, x + 520, y + 14], fill=LINE, width=2)
        itf, il = fit_lines(items, "body", "Medium", 520, 3, 24, 18)
        draw_lines(d, (x, y + 34), il, itf, MUTED, 1.45)
    d.line([640, 150, 640, 620], fill=LINE, width=2)
    return finish(img)


def card_take(n: int, total: int, label: str) -> bytes:
    """Test savoli: xlopushka 'TAKE n'."""
    img, d = canvas()
    glow(img, 640, 380, 540, CHROMA, 0.26)
    glow(img, 200, 680, 360, TUNG, 0.14)
    d = ImageDraw.Draw(img)
    bx0, by0, bx1, by1 = 200, 230, 1080, 610
    slate_stripes(img, (bx0, by0 - 70, bx1, by0 - 6), closed=False, angle=-10 + n)
    slate_stripes(img, (bx0, by0 - 2, bx1, by0 + 64))
    d = ImageDraw.Draw(img)
    d.rectangle([bx0, by0 + 64, bx1, by1], fill=(14, 16, 24), outline=LINE, width=3)
    d.text((bx0 + 36, by0 + 88), label.upper(), font=font("body", 22, "SemiBold"), fill=DIM)
    d.text((bx0 + 36, by0 + 118), "TAKE", font=font("display", 150, "Black"), fill=FG)
    d.text((bx1 - 36, by0 + 118), f"{n:02d}", font=font("display", 150, "Black"), fill=TUNG, anchor="ra")
    # progress
    seg = (bx1 - bx0 - 72 - (total - 1) * 8) / total
    for i in range(total):
        sx = int(bx0 + 36 + i * (seg + 8))
        d.rounded_rectangle([sx, by1 - 52, sx + int(seg), by1 - 36], radius=4,
                            fill=TUNG if i < n else LINE)
    return finish(img)


def card_result(label_a: str, label_t: str, a: int, t: int, verdict: str, kicker: str) -> bytes:
    img, d = canvas()
    glow(img, 1000, 250, 520, CHROMA, 0.30)
    glow(img, 250, 600, 420, TUNG, 0.16)
    d = ImageDraw.Draw(img)
    d.text((64, 96), kicker.upper(), font=font("mono", 20, "Medium"), fill=MUTED)
    f, lines = fit_lines(verdict.upper(), "display", "ExtraBold", 1150, 2, 104, 60)
    y = draw_lines(d, (60, 128), lines, f, FG, 0.9)
    y = max(y + 40, 360)
    for label, val in ((label_a, a), (label_t, t)):
        col = TUNG if val >= 67 else ((240, 200, 150) if val >= 40 else (255, 122, 107))
        d.text((64, y), label.upper(), font=font("display", 52, "ExtraBold"), fill=FG)
        d.text((W - 64, y), f"{val}%", font=font("display", 60, "Black"), fill=col, anchor="ra")
        by = y + 70
        d.rounded_rectangle([64, by, W - 64, by + 22], radius=11, fill=BG3)
        fw = int((W - 128) * max(0.03, val / 100))
        d.rounded_rectangle([64, by, 64 + fw, by + 22], radius=11, fill=col)
        # shkala belgilari
        for k in range(1, 10):
            x = 64 + (W - 128) * k // 10
            d.line([x, by + 28, x, by + 36], fill=DIM, width=1)
        y = by + 70
    return finish(img)


def card_slate_text(kicker: str, big: str, sub: str, closed: bool, take: str) -> bytes:
    """Ariza boshlanishi (ochiq xlopushka) va yakuni — 'CUT!' (yopiq)."""
    img, d = canvas()
    glow(img, 640, 360, 560, TUNG if closed else CHROMA, 0.22 if closed else 0.3)
    d = ImageDraw.Draw(img)
    bx0, by0, bx1, by1 = 180, 230, 1100, 640
    if closed:
        slate_stripes(img, (bx0, by0 - 66, bx1, by0 - 2))
    else:
        slate_stripes(img, (bx0, by0 - 70, bx1, by0 - 6), closed=False, angle=-16)
    slate_stripes(img, (bx0, by0 - 2, bx1, by0 + 64))
    d = ImageDraw.Draw(img)
    d.rectangle([bx0, by0 + 64, bx1, by1], fill=(14, 16, 24), outline=LINE, width=3)
    d.text((bx0 + 36, by0 + 88), kicker.upper(), font=font("body", 22, "SemiBold"), fill=DIM)
    inner_w = bx1 - bx0 - 72
    sf, sl = fit_lines(sub, "body", "Regular", inner_w - 90, 2, 26, 20)
    sub_h = int(sf.size * 1.35) * len(sl)
    avail = (by1 - 34) - (by0 + 124) - sub_h - 22
    size = 130
    while True:
        f, lines = fit_lines(big.upper(), "display", "Black", inner_w, 2, size, 48)
        if int(f.size * 0.88) * len(lines) <= avail or f.size <= 48:
            break
        size = f.size - 4
    y = draw_lines(d, (bx0 + 36, by0 + 124), lines, f, TUNG if closed else FG, 0.88)
    draw_lines(d, (bx0 + 36, y + 14), sl, sf, MUTED, 1.35)
    d.text((bx1 - 36, by1 - 30), take, font=font("mono", 20, "Medium"), fill=FG, anchor="rs")
    if closed:  # ochiq qanot yuqori qismni egallaydi
        d.text((640, 120), "ABROR BAXTIYAROVICH · AB MEDIA", font=font("mono", 22, "Medium"),
               fill=MUTED, anchor="mm")
    return finish(img)
