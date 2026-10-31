#!/usr/bin/env python3
"""Author the 14-04 illustrations locally as black-ink diagrams.

No image API is used. Each page is drawn on pure white with heavy black ink
lines, solid black accents and hatch shading, then downsampled for clean edges.
Run with the handdrawn-explainer-video venv Python.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import random
import numpy as np

W, H, S = 1600, 900, 2
OUT = Path(__file__).resolve().parent.parent / "inputs"
FONT = "/Applications/MiniMax Design.app/Contents/Resources/app-resources/fonts/NotoSansCJKsc-Regular.otf"
INK = (43, 47, 51)
PAPER = (253, 253, 247)
YELLOW = (232, 184, 75)
BROWN = (138, 106, 59)
METAL = (154, 163, 168)
GREY = (120, 116, 106)


def font(size):
    return ImageFont.truetype(FONT, int(size * S))


def sc(v):
    return int(round(v * S))


class Sheet:
    def __init__(self, seed=1404):
        self.img = Image.new("RGB", (W * S, H * S), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.rng = random.Random(seed)

    def line(self, pts, width=8, fill=INK, dash=None):
        pts = [(sc(x), sc(y)) for x, y in pts]
        if not dash:
            # Two slightly offset passes: a dark marker line with a rough edge.
            for pass_index in range(2):
                jittered = [(x + self.rng.uniform(-2.0, 2.0) * S,
                             y + self.rng.uniform(-2.0, 2.0) * S) for x, y in pts]
                stroke = max(1, sc(width * (1.0 if pass_index == 0 else 0.55)))
                self.d.line(jittered, fill=fill, width=stroke, joint="curve")
            return
        for a, b in zip(pts, pts[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            length = math.hypot(dx, dy)
            ux, uy = dx / length, dy / length
            t = 0.0
            while t < length:
                e = min(t + sc(dash), length)
                self.d.line([(a[0] + ux * t, a[1] + uy * t), (a[0] + ux * e, a[1] + uy * e)],
                            fill=fill, width=sc(width))
                t = e + sc(dash * 0.7)

    def arrow(self, x1, y1, x2, y2, width=8, head=22, fill=INK, dash=None):
        ang = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - head * 0.9 * math.cos(ang), y2 - head * 0.9 * math.sin(ang)
        self.line([(x1, y1), (bx, by)], width=width, fill=fill, dash=dash)
        h = head
        p1 = (sc(x2), sc(y2))
        p2 = (sc(x2 - h * math.cos(ang - 0.45)), sc(y2 - h * math.sin(ang - 0.45)))
        p3 = (sc(x2 - h * math.cos(ang + 0.45)), sc(y2 - h * math.sin(ang + 0.45)))
        self.d.polygon([p1, p2, p3], fill=fill)

    def box(self, x1, y1, x2, y2, r=18, width=10, fill=None, outline=INK):
        self.d.rounded_rectangle([sc(x1), sc(y1), sc(x2), sc(y2)], radius=sc(r),
                                 fill=fill, outline=outline, width=sc(width))
        dx, dy = self.rng.uniform(-2, 2), self.rng.uniform(-2, 2)
        self.d.rounded_rectangle([sc(x1 + dx), sc(y1 + dy), sc(x2 + dx), sc(y2 + dy)],
                                 radius=sc(r), outline=outline, width=max(1, sc(width * 0.45)))

    def circle(self, cx, cy, r, width=10, fill=None, outline=INK):
        self.d.ellipse([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)],
                       fill=fill, outline=outline, width=sc(width))
        dx, dy = self.rng.uniform(-2, 2), self.rng.uniform(-2, 2)
        self.d.ellipse([sc(cx - r + dx), sc(cy - r + dy), sc(cx + r + dx), sc(cy + r + dy)],
                       outline=outline, width=max(1, sc(width * 0.45)))

    def streaks(self, box, base=YELLOW, color=BROWN, step=38, width=2, angle=35):
        """Marker streaks over a solid fill, clipped to an inner rectangle."""
        x1, y1, x2, y2 = box
        layer = Image.new("RGB", self.img.size, base)
        ld = ImageDraw.Draw(layer)
        diag = math.hypot(x2 - x1, y2 - y1)
        dx, dy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        n = int(diag * 1.8 / step) + 2
        ox, oy = (x1 + x2) / 2, (y1 + y2) / 2
        for i in range(-n, n):
            px, py = ox - dy * i * step, oy + dx * i * step
            ld.line([(sc(px - dx * diag), sc(py - dy * diag)), (sc(px + dx * diag), sc(py + dy * diag))],
                    fill=color, width=sc(width))
        mask = Image.new("L", self.img.size, 0)
        ImageDraw.Draw(mask).rectangle([sc(x1), sc(y1), sc(x2), sc(y2)], fill=255)
        self.img.paste(layer, (0, 0), mask)
        self.d = ImageDraw.Draw(self.img)

    def text(self, x, y, s, size=44, fill=INK, anchor="lt", stroke=0, stroke_fill=PAPER):
        self.d.text((sc(x), sc(y)), s, font=font(size), fill=fill, anchor=anchor,
                    stroke_width=sc(stroke) if stroke else 0, stroke_fill=stroke_fill)

    def hatch(self, box, step=26, width=3, angle=45, fill=INK):
        x1, y1, x2, y2 = box
        mask = Image.new("L", self.img.size, 0)
        md = ImageDraw.Draw(mask)
        md.rectangle([sc(x1), sc(y1), sc(x2), sc(y2)], fill=255)
        hatch = Image.new("RGB", self.img.size, PAPER)
        hd = ImageDraw.Draw(hatch)
        diag = math.hypot(x2 - x1, y2 - y1)
        dx, dy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        n = int(diag * 1.6 / step) + 2
        for i in range(-n, n):
            ox, oy = x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2
            px, py = ox - dy * i * step, oy + dx * i * step
            hd.line([(sc(px - dx * diag), sc(py - dy * diag)), (sc(px + dx * diag), sc(py + dy * diag))],
                    fill=fill, width=sc(width))
        self.img.paste(hatch, (0, 0), mask)
        self.d = ImageDraw.Draw(self.img)

    def cross(self, cx, cy, r=34, width=12):
        self.line([(cx - r, cy - r), (cx + r, cy + r)], width=width)
        self.line([(cx - r, cy + r), (cx + r, cy - r)], width=width)

    def check(self, cx, cy, r=30, width=12):
        self.line([(cx - r, cy), (cx - r * 0.15, cy + r * 0.75), (cx + r, cy - r * 0.65)], width=width)

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        image = self.img.resize((W, H), Image.LANCZOS)
        # The film paper shows through: keep only the drawn ink opaque.
        rgb = np.array(image.convert("RGB")).astype(int)
        diff = np.abs(rgb - np.array(PAPER)).max(axis=2)
        alpha = np.clip((diff - 2) / 10 * 255, 0, 255).astype(np.uint8)
        rgba = np.dstack([rgb.astype(np.uint8), alpha])
        Image.fromarray(rgba, "RGBA").save(OUT / f"{name}.png")
        print("wrote", OUT / f"{name}.png")


# ---------------------------------------------------------------- p01
def p01():
    s = Sheet()
    # left: a single chain that cannot go back
    s.text(130, 90, "思维链", size=62)
    xs, ys = 300, [200, 360, 520]
    for i, y in enumerate(ys):
        s.box(xs - 120, y, xs + 120, y + 100, fill=YELLOW)
        s.text(xs, y + 50, f"第 {i + 1} 步", size=40, anchor="mm")
    for y in ys[:-1]:
        s.arrow(xs, y + 100, xs, y + 160, width=9)
    s.cross(xs + 120, ys[1] + 50, r=26, width=10)
    s.text(xs, 700, "错了也回不去", size=48, anchor="mm", stroke=0)
    s.line([(xs - 150, 680), (xs + 150, 720)], width=6)
    # right: a tree that backtracks
    s.text(900, 90, "树", size=62)
    root = (1120, 200)
    kids = [(940, 360), (1120, 360), (1300, 360)]
    grand = [(880, 520), (1000, 520), (1180, 520), (1240, 520)]
    s.circle(*root, 48, fill=INK)
    for k in kids:
        s.arrow(root[0], root[1] + 48, k[0], k[1] - 44, width=8)
        s.circle(*k, 44, fill=PAPER)
    s.cross(kids[0][0], kids[0][1], r=24, width=9)
    s.text(kids[0][0] - 70, kids[0][1] + 58, "死路", size=38, anchor="mm")
    for g in grand:
        parent = kids[1] if g[0] < 1100 else kids[2]
        s.arrow(parent[0], parent[1] + 44, g[0], g[1] - 34, width=7)
        s.circle(*g, 34, fill=PAPER)
    s.circle(grand[3][0], grand[3][1], 46, fill=YELLOW, width=12)
    s.text(grand[3][0], grand[3][1], "24", size=38, anchor="mm")
    s.arrow(grand[1][0], grand[1][1] + 40, grand[1][0] - 20, 700, width=7, dash=18)
    s.arrow(grand[1][0] - 20, 700, grand[3][0] - 50, grand[3][1] + 50, width=7, dash=18)
    s.text(1010, 640, "回溯", size=46, anchor="mm")
    s.line([(860, 780), (1360, 780)], width=6)
    s.text(1110, 810, "换一条分支继续搜", size=42, anchor="mm")
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet()
    nums = ["4", "6", "4", "1"]
    ops = ["+", "−", "×", "÷"]
    for i, (n, op) in enumerate(zip(nums, ops)):
        x = 170 + i * 190
        s.box(x - 62, 60, x + 62, 184, fill=PAPER, width=11)
        s.text(x, 122, n, size=92, anchor="mm")
        s.text(x + 95, 122, op, size=64, anchor="mm", stroke=2)
    s.text(910, 122, "→", size=100, anchor="mm")
    s.circle(1150, 122, 72, fill=YELLOW, width=14)
    s.text(1150, 122, "24", size=66, anchor="mm")
    # two bars
    base = 800
    s.line([(220, base), (1380, base)], width=9)
    left_h, right_h = 70, 470
    s.box(360, base - left_h, 560, base, fill=INK, width=0, outline=INK)
    s.text(460, base - left_h - 54, "4%", size=82, anchor="mm")
    s.text(460, base + 46, "CoT", size=54, anchor="mm")
    s.box(900, base - right_h, 1100, base, fill=YELLOW, width=12)
    s.streaks((916, base - right_h + 14, 1084, base - 12), base=YELLOW, color=BROWN, step=36, width=2)
    s.text(1000, base - right_h - 54, "74%", size=82, anchor="mm")
    s.text(1000, base + 46, "ToT", size=54, anchor="mm")
    s.text(620, 280, "Game of 24 · GPT-4", size=44, anchor="mm")
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet()
    root = (800, 170)
    s.box(root[0] - 200, root[1] - 66, root[0] + 200, root[1] + 66, fill=YELLOW, width=13)
    s.text(root[0], root[1], "4,6,4,1 → 24", size=48, anchor="mm")
    kids = [(520, 430), (800, 430), (1080, 430)]
    labels = ["思考 A", "思考 B", "思考 C"]
    scores = ["0.7", "0.4", "0.9"]
    for (k, lab, score) in zip(kids, labels, scores):
        s.arrow(root[0], root[1] + 66, k[0], k[1] - 58, width=9)
        s.box(k[0] - 130, k[1] - 58, k[0] + 130, k[1] + 58, fill=PAPER, width=10)
        s.text(k[0], k[1], lab, size=44, anchor="mm")
        s.box(k[0] + 146, k[1] - 34, k[0] + 238, k[1] + 34, fill=YELLOW, width=7)
        s.text(k[0] + 192, k[1], score, size=38, anchor="mm")
        s.line([(k[0] + 130, k[1]), (k[0] + 146, k[1])], width=6)
    # legend
    s.box(110, 590, 650, 870, fill=PAPER, width=9)
    s.text(160, 620, "三件套", size=46)
    s.circle(200, 700, 24, fill=INK)
    s.text(250, 700, "节点 = 一个思考", size=38, anchor="lm")
    s.arrow(172, 755, 238, 755, width=8)
    s.text(250, 755, "边 = 展开", size=38, anchor="lm")
    s.text(160, 800, "价值 = 有多大希望", size=38)
    s.text(1080, 650, "展开 K 个子思考", size=48, anchor="mm")
    s.arrow(1080, 700, 1080, 750, width=9)
    s.text(1080, 790, "K = 分支数", size=46, anchor="mm")
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet()
    root = (800, 130)
    s.circle(*root, 42, fill=INK)
    kids = [(560, 300), (800, 300), (1040, 300)]
    leaves = [(470, 480), (650, 480), (720, 480), (880, 480), (960, 480), (1120, 480)]
    for k in kids:
        s.arrow(root[0], root[1] + 42, k[0], k[1] - 36, width=8)
        s.circle(*k, 40, fill=YELLOW, width=10)
    for i, g in enumerate(leaves):
        parent = kids[i // 2]
        s.arrow(parent[0], parent[1] + 36, g[0], g[1] - 30, width=7)
        s.circle(*g, 30, fill=PAPER)
    # scores live inside the self-evaluated nodes
    for k, sc_ in zip(kids, ["7", "3", "9"]):
        s.text(k[0], k[1], sc_, size=42, anchor="mm")
    # magnifier on the right node
    mx, my = 1040, 300
    s.circle(mx + 120, my - 90, 78, width=12)
    s.line([(mx + 178, my - 34), (mx + 250, my + 40)], width=16)
    s.text(mx + 120, my - 90, "自评", size=38, anchor="mm")
    # traversals
    s.text(250, 700, "BFS", size=56, anchor="mm")
    s.text(800, 700, "DFS", size=56, anchor="mm")
    s.text(1330, 700, "beam", size=56, anchor="mm")
    s.arrow(250, 740, 420, 740, width=8)
    s.arrow(800, 740, 800, 800, width=8)
    s.arrow(1330, 740, 1160, 740, width=8)
    s.text(640, 840, "论文最常用 BFS", size=44, anchor="mm")
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet()
    # dense tree, one highlighted path to 27
    root = (760, 120)
    s.circle(*root, 30, fill=INK)
    level1 = [(420, 260), (640, 260), (860, 260), (1080, 260)]
    level2 = [(330, 400), (470, 400), (570, 400), (710, 400), (790, 400), (930, 400), (1010, 400), (1150, 400)]
    for k in level1:
        s.arrow(root[0], root[1] + 30, k[0], k[1] - 26, width=6)
        s.circle(*k, 26, fill=PAPER)
    for i, g in enumerate(level2):
        p = level1[i // 2]
        s.arrow(p[0], p[1] + 26, g[0], g[1] - 22, width=5)
        s.circle(*g, 22, fill=PAPER)
    # highlighted path
    path = [(760, 120), (860, 260), (930, 400)]
    s.line(path, width=14)
    s.circle(930, 400, 24, fill=YELLOW)
    s.arrow(930, 424, 980, 520, width=12)
    s.box(890, 520, 1090, 610, fill=YELLOW, width=14, outline=BROWN)
    s.text(990, 565, "27", size=66, anchor="mm")
    # target 24
    s.text(1160, 565, "≠", size=70, anchor="mm")
    s.circle(1320, 565, 72, fill=YELLOW, width=13)
    s.text(1320, 565, "24", size=64, anchor="mm")
    s.text(760, 730, "152 次展开", size=64, anchor="mm")
    s.text(760, 810, "最好轨迹停在 27，不是 24", size=44, anchor="mm")
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet()
    steps = [("选择", (800, 160)), ("扩展", (1160, 420)), ("模拟", (800, 680)), ("回传", (440, 420))]
    boxes = []
    for name, (cx, cy) in steps:
        s.box(cx - 150, cy - 66, cx + 150, cy + 66, fill=PAPER, width=11)
        s.text(cx, cy, name, size=54, anchor="mm")
        boxes.append((cx, cy))
    # clockwise arrows
    s.arrow(950, 200, 1080, 340, width=10)
    s.arrow(1120, 486, 950, 620, width=10)
    s.arrow(650, 640, 520, 510, width=10)
    s.arrow(520, 350, 670, 210, width=10)
    # center roles
    s.circle(800, 420, 170, width=9, fill=(210, 213, 208))
    s.text(800, 320, "策略", size=38, anchor="mm")
    s.text(800, 420, "价值", size=38, anchor="mm")
    s.text(800, 520, "自省", size=38, anchor="mm")
    s.text(800, 810, "每次迭代四步", size=46, anchor="mm")
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet()
    s.text(160, 110, "6 × 4 = 24", size=76)
    # nodes and arrows
    chain = [(300, 330), (620, 330), (940, 330), (1260, 330)]
    labels = ["6", "×4", "24", "×1"]
    for (cx, cy), lab in zip(chain, labels):
        s.circle(cx, cy, 78, fill=YELLOW, width=13)
        s.text(cx, cy, lab, size=58, anchor="mm")
    for a, b in zip(chain, chain[1:]):
        s.arrow(a[0] + 78, 330, b[0] - 78, 330, width=10)
    s.check(1420, 330, r=56, width=16)
    s.box(1120, 480, 1420, 590, fill=YELLOW, width=14)
    s.text(1270, 535, "24", size=80, anchor="mm")
    s.text(460, 540, "286 次展开", size=66, anchor="mm")
    s.text(460, 640, "找到 6 × 4 = 24", size=48, anchor="mm")
    s.text(1040, 700, "HumanEval pass@1", size=46, anchor="mm")
    s.text(1040, 790, "92.7%", size=96, anchor="mm")
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet()
    # log-scale cost bars
    bars = [("CoT", 1, 60), ("ToT", 100, 220), ("LATS", 1000, 400)]
    base = 780
    s.line([(160, base), (1460, base)], width=9)
    for i, (name, mult, h) in enumerate(bars):
        x = 260 + i * 400
        fill = {"CoT": PAPER, "ToT": YELLOW, "LATS": BROWN}[name]
        s.box(x - 90, base - h, x + 90, base, fill=fill, width=12)
        if name == "CoT":
            s.hatch((x - 70, base - h + 16, x + 70, base - 12), step=24, width=3)
        elif name == "ToT":
            s.streaks((x - 74, base - h + 14, x + 74, base - 12), base=YELLOW, color=BROWN, step=32, width=2)
        s.text(x, base - h - 52, ("1×" if mult == 1 else f"{mult}×"), size=60, anchor="mm")
        s.text(x, base + 42, name, size=46, anchor="mm")
    s.text(800, 60, "token 成本（对数感）", size=50, anchor="mm")
    s.box(160, 120, 1440, 225, fill=PAPER, width=8)
    s.text(230, 172, "噪声评估器 → 高分错误答案", size=42, anchor="lm")
    s.cross(1392, 172, r=22, width=8)

    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet()
    s.text(140, 100, "2026 生产现场", size=54)
    # left main path
    s.box(120, 260, 620, 560, fill=PAPER, width=11)
    s.text(370, 330, "ReAct", size=66, anchor="mm")
    s.text(370, 410, "+ 工具验证", size=48, anchor="mm")
    s.text(370, 500, "大多数生产 agent", size=38, anchor="mm")
    # gate
    s.box(730, 220, 940, 720, fill=INK, width=0, outline=INK)
    s.text(835, 470, "阈值", size=52, fill=PAPER, anchor="mm")
    # right behind gate
    s.box(980, 260, 1460, 560, fill=YELLOW, width=11)
    s.text(1220, 330, "搜索", size=66, anchor="mm")
    s.text(1220, 410, "ToT / LATS", size=48, anchor="mm")
    s.text(1220, 500, "单元测试当价值函数", size=38, anchor="mm")
    s.arrow(655, 410, 725, 410, width=11)
    s.arrow(945, 410, 965, 410, width=11)
    s.text(800, 810, "值不值得为一次推理付 100× token？", size=50, anchor="mm")
    s.save("p09")




# ---------------------------------------------------------------- cover
def cover():
    base = Image.new("RGB", (1920, 1080), PAPER)
    d = ImageDraw.Draw(base)
    # Left: typographic title block
    title_font = ImageFont.truetype(FONT, 118)
    sub_font = ImageFont.truetype(FONT, 64)
    meta_font = ImageFont.truetype(FONT, 34)
    d.text((120, 170), "Tree of Thoughts", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((120, 310), "与 LATS", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((120, 470), "把推理变成搜索", font=sub_font, fill=INK)
    d.rectangle([120, 580, 700, 590], fill=INK)
    d.text((120, 620), "14-04 · Agent Engineering", font=meta_font, fill=INK)
    # Right: the reviewed p01 main visual
    art = Image.open(OUT / "p01.png").convert("RGB")
    art = art.resize((1040, 585), Image.LANCZOS)
    base.paste(art, (800, 400))
    (OUT / "cover.png").parent.mkdir(parents=True, exist_ok=True)
    base.save(OUT / "cover.png")
    print("wrote", OUT / "cover.png")

if __name__ == "__main__":
    for fn in (p01, p02, p03, p04, p05, p06, p07, p08, p09):
        fn()
    cover()
