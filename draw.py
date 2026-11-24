"""news-23 b71 front-page-dense: THE WORLD TODAY, Monday 23 November 2026.
Draws a 1024x1024 front-page news image with PIL. 31 stories, all dated 23 Nov 2026.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 12
CW = W - 2 * M  # 1000

FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, lh):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap text; if too many lines, drop words from the end is NOT allowed,
    so instead return lines and let caller shrink font."""
    return wrap(draw, text, fnt, max_w)


def chip(draw, x, y, text, fill):
    fnt = font(SANS_B, 9)
    w = draw.textlength(text, font=fnt) + 10
    h = 14
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=fill)
    draw.text((x + 5, y + 2), text, font=fnt, fill="white")
    return w


img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

BLACK = (0, 0, 0)
RED = (200, 30, 30)
GOLD = (212, 175, 55)
DARKGOLD = (176, 141, 28)
GRAY = (90, 90, 90)
LGRAY = (230, 230, 230)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 62], fill=BLACK)
d.text((M, 8), "THE WORLD TODAY", font=font(SERIF_B, 42), fill="white")
dt = "MONDAY 23 NOVEMBER 2026"
df = font(SANS_B, 19)
d.text((W - M - d.textlength(dt, font=df), 20), dt, font=df, fill=GOLD)

# ---------------------------------------------------------------- kicker
kick = "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B"
d.text((M, 66), kick, font=font(SANS_B, 15), fill=RED)

# ---------------------------------------------------------------- number strip (2 rows x 5)
nums = [
    ("-3.3%", "KOSPI", RED),
    ("5.3", "US-CHINA POWER GAP", (0, 60, 140)),
    ("11,762", "EBOLA CASES, DRC", (0, 120, 60)),
    ("10T won", "SEOUL STABILISATION FUND", (140, 90, 0)),
    ("2%", "BILLIONAIRE TAX IN PARIS", (140, 0, 140)),
    ("$450M", "SKUBAL DEAL", (0, 60, 140)),
    ("165", "RUSSIAN MISSILES/WEEK", (140, 90, 0)),
    ("12,000", "CLEARED IN MANCHESTER", (0, 120, 60)),
    ("264 kg", "EXPLOSIVES SEIZED", (140, 90, 0)),
    ("$107.3B", "ANTHROPIC IPO", (140, 0, 140)),
]
cell_w = CW / 5
for i, (val, lab, col) in enumerate(nums):
    r, c = divmod(i, 5)
    x = M + c * cell_w
    y = 86 + r * 33
    d.text((x + 2, y), val, font=font(SANS_B, 21), fill=col)
    lab_f = font(SANS_B, 8)
    lab_lines = wrap(d, lab, lab_f, cell_w - 6)
    yy = y + 23
    for ln in lab_lines[:1]:
        d.text((x + 2, yy), ln, font=lab_f, fill=BLACK)

# ---------------------------------------------------------------- region bar
regions = [
    ("ASIA-PACIFIC 7", 7, (0, 128, 110)),
    ("AMERICAS 8", 8, (0, 80, 170)),
    ("MIDDLE EAST 6", 6, (150, 110, 30)),
    ("EUROPE 5", 5, (110, 60, 150)),
    ("AFRICA 3", 3, (190, 30, 30)),
    ("WORLD 2", 2, (110, 110, 110)),
]
x = M
y0, y1 = 152, 170
for name, cnt, col in regions:
    w = CW * cnt / 31
    d.rectangle([x, y0, x + w - 1, y1], fill=col)
    fnt = font(SANS_B, 11)
    tw = d.textlength(name, font=fnt)
    if tw <= w - 6:
        d.text((x + (w - tw) / 2, y0 + 3), name, font=fnt, fill="white")
    x += w

# ---------------------------------------------------------------- UTC strip
utc = "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles"
d.text((M, 174), utc, font=font(SANS, 10), fill=GRAY)
ap = "~ APPROX"
d.text((W - M - d.textlength(ap, font=font(SANS, 10)), 174), ap, font=font(SANS, 10), fill=GRAY)

# ---------------------------------------------------------------- heroes
hero_w = (CW - 2 * 8) / 3  # ~328
hero_x = [M, M + hero_w + 8, M + 2 * (hero_w + 8)]
SY0, SY1 = 188, 328        # scene
STRIP_Y0, STRIP_Y1 = 328, 344
HL_Y = 350                 # headline top (clear gap below black strip)
BODY_Y = 398
SRC_Y = 438

# --- scene 1: Kospi skyline + chart
sx = hero_x[0]
d.rectangle([sx, SY0, sx + hero_w, SY1], fill=(11, 30, 58))
import random
random.seed(71)
bx = sx + 6
while bx < sx + hero_w - 14:
    bw = random.randint(18, 30)
    bh = random.randint(45, 95)
    by = SY1 - bh
    d.rectangle([bx, by, bx + bw, SY1], fill=(18, 48, 92))
    for wy in range(by + 6, SY1 - 6, 12):
        for wx in range(bx + 4, bx + bw - 3, 9):
            if random.random() < 0.55:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
    bx += bw + 4
pts = [(sx + 8, 268), (sx + 50, 252), (sx + 95, 262), (sx + 140, 240),
       (sx + 185, 252), (sx + 230, 232), (sx + 275, 244), (sx + hero_w - 8, 226)]
d.line(pts, fill=(255, 150, 40), width=3)
for px, py in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 200, 90))
d.text((sx + 8, SY0 + 6), "-3.3%", font=font(SANS_B, 28), fill=(255, 70, 60))

# --- scene 2: Guterres globe
sx = hero_x[1]
d.rectangle([sx, SY0, sx + hero_w, SY1], fill=(14, 122, 107))
d.text((sx + 10, SY0 + 12), "150 DELEGATES", font=font(SANS_B, 25), fill=(255, 210, 80))
d.text((sx + 10, SY0 + 42), "BACK A RISK", font=font(SANS_B, 25), fill=(255, 210, 80))
d.text((sx + 10, SY0 + 72), "FRAMEWORK", font=font(SANS_B, 25), fill=(255, 210, 80))
cx, cy, r = sx + hero_w - 62, SY0 + 92, 44
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline="white", width=2)
d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline="white", width=2)
d.line([cx - r, cy, cx + r, cy], fill="white", width=2)
d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360, fill="white", width=2)
d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 180, 360, fill="white", width=2)

# --- scene 3: Power Index bars
sx = hero_x[2]
d.rectangle([sx, SY0, sx + hero_w, SY1], fill=(253, 243, 216))
d.text((sx + 8, SY0 + 6), "NARROWEST SINCE 2018", font=font(SANS_B, 11), fill=BLACK)
g = "GAP 5.3"
d.text((sx + hero_w - d.textlength(g, font=font(SANS_B, 11)) - 8, SY0 + 6), g,
       font=font(SANS_B, 11), fill=DARKGOLD)
base = SY1 - 8
bars = [("78.9", "US", (10, 30, 80), 92), ("73.6", "CHINA", (180, 30, 30), 86),
        ("40.5", "INDIA", (200, 160, 40), 48)]
bw = 62
gap = (hero_w - 3 * bw) / 4
for i, (val, lab, col, bh) in enumerate(bars):
    bx = sx + gap + i * (bw + gap)
    d.text((bx + (bw - d.textlength(val, font=font(SANS_B, 15))) / 2, base - bh - 20),
           val, font=font(SANS_B, 15), fill=BLACK)
    d.rectangle([bx, base - bh, bx + bw, base], fill=col)
    d.text((bx + (bw - d.textlength(lab, font=font(SANS_B, 11))) / 2, base - 18),
           lab, font=font(SANS_B, 11), fill="white")

heroes = [
    ("KOSPI 4,708.54  \u00b7  -161 PTS",
     "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE", "REPORTED", (0, 90, 180)),
    ("UN  \u00b7  BRIDGETOWN",
     "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS", "REPORTED", (0, 90, 180)),
    ("ASIA POWER INDEX 2026",
     "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE", "REPORTED", (0, 90, 180)),
]
for k, (strip, hl, body, src, chipt, chipcol) in enumerate(heroes):
    sx = hero_x[k]
    d.rectangle([sx, STRIP_Y0, sx + hero_w, STRIP_Y1], fill=BLACK)
    d.text((sx + 6, STRIP_Y0 + 2), strip, font=font(SANS_B, 11), fill="white")
    # number badge
    d.ellipse([sx - 2, HL_Y - 2, sx + 20, HL_Y + 20], fill=RED)
    d.text((sx + 3, HL_Y), str(k + 1), font=font(SANS_B, 14), fill="white")
    hl_f = font(SANS_B, 19)
    hl_lines = wrap(d, hl, hl_f, hero_w - 28)
    y = HL_Y
    for ln in hl_lines[:2]:
        d.text((sx + 26, y), ln, font=hl_f, fill=BLACK)
        y += 22
    body_f = font(SANS, 12)
    y = BODY_Y
    for ln in wrap(d, body, body_f, hero_w - 4)[:2]:
        d.text((sx + 2, y), ln, font=body_f, fill=BLACK)
        y += 15
    d.text((sx + 2, SRC_Y + 2), src, font=font(SANS, 10), fill=GRAY)
    cw = chip(d, sx + hero_w - 74, SRC_Y, chipt, chipcol)

# ---------------------------------------------------------------- 10 stories header
d.rectangle([M, 462, W - M, 480], fill=BLACK)
d.text((M + 6, 465), "MORE OF THE DAY  \u2014  10 STORIES", font=font(SANS_B, 13), fill="white")

# ---------------------------------------------------------------- cards (5 x 2)
cards = [
    ("AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED", (0, 90, 180), (170, 30, 30)),
    ("FBI", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED", (150, 30, 30), (170, 30, 30)),
    ("WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED", (120, 80, 10), (170, 30, 30)),
    ("MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED", (0, 90, 180), (170, 30, 30)),
    ("SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", (170, 30, 30), (170, 30, 30)),
    ("SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED", (170, 30, 30), (170, 30, 30)),
    ("LEGAL", "STATES SUE SPACEX", "Ten states challenge AI claims.", "AP", "REPORTED", (110, 60, 150), (170, 30, 30)),
    ("TECH", "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", "REPORTED", (0, 120, 120), (170, 30, 30)),
    ("EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.", "AP", "CLAIM", (110, 60, 150), (200, 30, 30)),
    ("SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM", (90, 90, 90), (200, 30, 30)),
]
card_w = (CW - 4 * 5) / 5  # 196
card_h = 92
for i, (cat, hl, body, src, chipt, catcol, chipcol) in enumerate(cards):
    r, c = divmod(i, 5)
    x = M + c * (card_w + 5)
    y = 480 + r * card_h
    d.rectangle([x, y, x + card_w, y + 15], fill=catcol)
    cat_txt = f"{cat}  {i + 1}"
    d.text((x + 4, y + 2), cat_txt, font=font(SANS_B, 9), fill="white")
    num = str(i + 1)
    d.text((x + card_w - d.textlength(num, font=font(SANS_B, 9)) - 4, y + 2),
           num, font=font(SANS_B, 9), fill="white")
    hl_f = font(SANS_B, 12)
    hl_lines = wrap(d, hl, hl_f, card_w - 6)
    yy = y + 18
    for ln in hl_lines[:2]:
        d.text((x + 3, yy), ln, font=hl_f, fill=BLACK)
        yy += 14
    body_f = font(SANS, 10)
    yy = y + 48
    for ln in wrap(d, body, body_f, card_w - 6)[:1]:
        d.text((x + 3, yy), ln, font=body_f, fill=BLACK)
    d.text((x + 3, y + card_h - 18), src, font=font(SANS, 9), fill=GRAY)
    chip(d, x + card_w - 62, y + card_h - 20, chipt, chipcol)

# ---------------------------------------------------------------- map + ALSO headers
map_w = 330
d.rectangle([M, 670, M + map_w, 688], fill=BLACK)
d.text((M + 6, 673), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill="white")
d.rectangle([M + map_w + 8, 670, W - M, 688], fill=BLACK)
d.text((M + map_w + 14, 673), "ALSO ON MONDAY", font=font(SANS_B, 13), fill="white")

# ---------------------------------------------------------------- map
mx0, my0, mx1, my1 = M, 688, M + map_w, 878
d.rectangle([mx0, my0, mx1, my1], outline=(200, 200, 200))
for gx in range(mx0, mx1 + 1, 22):
    d.line([gx, my0, gx, my1], fill=(235, 235, 235))
for gy in range(my0, my1 + 1, 22):
    d.line([mx0, gy, mx1, gy], fill=(235, 235, 235))
GREEN = (178, 214, 150)
# Americas blob
d.polygon([(30, 720), (90, 700), (150, 712), (180, 745), (165, 800), (120, 845),
           (70, 855), (35, 820), (22, 770)], fill=GREEN)
# Eurasia blob
d.polygon([(195, 700), (250, 688), (310, 700), (335, 735), (320, 775), (270, 800),
           (220, 790), (195, 750)], fill=GREEN)
# Australia blob
d.ellipse([275, 825, 325, 860], fill=GREEN)
pins = [
    (1, 295, 722), (2, 55, 818), (3, 310, 702), (4, 95, 788), (5, 115, 758),
    (6, 225, 758), (7, 85, 743), (8, 35, 773), (9, 70, 798), (10, 85, 823),
    (11, 205, 712), (12, 220, 733), (13, 245, 708),
]
for n, px, py in pins:
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(200, 30, 30), outline="white", width=1)
    t = str(n)
    d.text((px - d.textlength(t, font=font(SANS_B, 9)) / 2, py - 7),
           t, font=font(SANS_B, 9), fill="white")
leg = ["Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing",
       "4 Washington \u00b7 5 New York \u00b7 6 Tehran \u00b7 7 Chicago",
       "8 SF \u00b7 9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 Kyiv \u00b7 13 Moscow"]
ly = 848
for ln in leg:
    d.text((mx0 + 2, ly), ln, font=font(SANS, 9), fill=BLACK)
    ly += 11

# ---------------------------------------------------------------- ALSO list (18 items, 2 cols x 9)
also = [
    "Paris: 100+ back 2% billionaire tax",
    "Manchester: 12,000 cleared",
    "Zelenskyy: 165 missiles in a week",
    "COP31: the day after pact rejected",
    "Benghazi: UN demands port probe",
    "Israel unity talks resume",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives",
    "Bahrain: strike hits plant, 2 hurt",
    "Sudan: defences down drones",
    "DRC: fighting traps Ebola teams",
    "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits in exam row",
    "SK Telecom -7.3% as hype cools",
    "China eases margin rules",
    "Seoul readies 10T-won fund",
]
ax0 = M + map_w + 14
col_w = (W - M - ax0 - 8) / 2
for i, item in enumerate(also):
    c = i // 9
    r = i % 9
    x = ax0 + c * col_w
    y = 694 + r * 21
    d.text((x, y), f"{14 + i}. {item}", font=font(SANS, 11), fill=BLACK)

# ---------------------------------------------------------------- DATE CHECK
d.rectangle([M, 884, W - M, 946], outline=RED, width=2)
d.text((M + 8, 888), "DATE CHECK", font=font(SANS_B, 13), fill=RED)
rd = "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY"
d.text((W - M - d.textlength(rd, font=font(SANS_B, 10)) - 8, 890),
       rd, font=font(SANS_B, 10), fill=RED)
d.text((M + 8, 908),
       "LEFT OUT \u2014 NOT 23 NOV: Dems 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 El Chapo (22 Nov) \u00b7 EU-Indonesia pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar (19 Nov)",
       font=font(SANS, 11), fill=BLACK)
d.text((M + 8, 926),
       "NOT YET: Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
       font=font(SANS, 11), fill=BLACK)

# ---------------------------------------------------------------- footer
d.text((M, 952),
       "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
       font=font(SANS, 9), fill=GRAY)
d.text((M, 964),
       "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.",
       font=font(SANS, 9), fill=GRAY)
d.text((M, 976),
       "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=font(SANS, 9), fill=GRAY)

# ---------------------------------------------------------------- bottom bar
d.rectangle([0, 992, W, H], fill=BLACK)
fb = "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
ff = font(SANS_B, 15)
d.text(((W - d.textlength(fb, font=ff)) / 2, 1002), fb, font=ff, fill=GOLD)

out = os.environ.get("DRAW_OUT", "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
