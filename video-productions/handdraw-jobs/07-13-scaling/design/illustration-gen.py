#!/usr/bin/env python3
"""Author the 07-05 illustrations locally as industrial-marker diagrams.

No image API is used. Every page is drawn on warm paper with dark marker
outlines, warm-yellow fills and brown streaks, then downsampled so the
hand-drawn strokes stay crisp.
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
    def __init__(self, seed=705):
        self.img = Image.new("RGB", (W * S, H * S), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.rng = random.Random(seed)

    # ---------------------------------------------------------------- primitives
    def line(self, pts, width=8, fill=INK, dash=None):
        pts = [(sc(x), sc(y)) for x, y in pts]
        if not dash:
            for pass_index in range(2):
                jittered = [(x + self.rng.uniform(-2.0, 2.0) * S,
                             y + self.rng.uniform(-2.0, 2.0) * S) for x, y in pts]
                stroke = max(1, sc(width * (1.0 if pass_index == 0 else 0.55)))
                self.d.line(jittered, fill=fill, width=stroke, joint="curve")
            return
        for a, b in zip(pts, pts[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            length = math.hypot(dx, dy)
            if length == 0:
                continue
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

    def box(self, x1, y1, x2, y2, r=16, width=9, fill=None, outline=INK):
        self.d.rounded_rectangle([sc(x1), sc(y1), sc(x2), sc(y2)], radius=sc(r),
                                 fill=fill, outline=outline, width=sc(width))
        dx, dy = self.rng.uniform(-2, 2), self.rng.uniform(-2, 2)
        self.d.rounded_rectangle([sc(x1 + dx), sc(y1 + dy), sc(x2 + dx), sc(y2 + dy)],
                                 radius=sc(r), outline=outline, width=max(1, sc(width * 0.45)))

    def circle(self, cx, cy, r, width=9, fill=None, outline=INK):
        self.d.ellipse([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)],
                       fill=fill, outline=outline, width=sc(width))
        dx, dy = self.rng.uniform(-2, 2), self.rng.uniform(-2, 2)
        self.d.ellipse([sc(cx - r + dx), sc(cy - r + dy), sc(cx + r + dx), sc(cy + r + dy)],
                       outline=outline, width=max(1, sc(width * 0.45)))

    def streaks(self, box, base=YELLOW, color=BROWN, step=38, width=2, angle=35):
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

    def hatch(self, box, step=26, width=3, angle=45, fill=INK):
        x1, y1, x2, y2 = box
        mask = Image.new("L", self.img.size, 0)
        ImageDraw.Draw(mask).rectangle([sc(x1), sc(y1), sc(x2), sc(y2)], fill=255)
        hatch = Image.new("RGB", self.img.size, PAPER)
        hd = ImageDraw.Draw(hatch)
        diag = math.hypot(x2 - x1, y2 - y1)
        dx, dy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        n = int(diag * 1.6 / step) + 2
        ox, oy = (x1 + x2) / 2, (y1 + y2) / 2
        for i in range(-n, n):
            px, py = ox - dy * i * step, oy + dx * i * step
            hd.line([(sc(px - dx * diag), sc(py - dy * diag)), (sc(px + dx * diag), sc(py + dy * diag))],
                    fill=fill, width=sc(width))
        self.img.paste(hatch, (0, 0), mask)
        self.d = ImageDraw.Draw(self.img)

    def text(self, x, y, s, size=42, fill=INK, anchor="lt", stroke=0, stroke_fill=PAPER):
        self.d.text((sc(x), sc(y)), s, font=font(size), fill=fill, anchor=anchor,
                    stroke_width=sc(stroke) if stroke else 0, stroke_fill=stroke_fill)

    def width_of(self, s, size):
        return self.d.textlength(s, font=font(size)) / S

    def cross(self, cx, cy, r=30, width=11, fill=INK):
        self.line([(cx - r, cy - r), (cx + r, cy + r)], width=width, fill=fill)
        self.line([(cx - r, cy + r), (cx + r, cy - r)], width=width, fill=fill)

    def check(self, cx, cy, r=30, width=11, fill=INK):
        self.line([(cx - r, cy), (cx - r * 0.15, cy + r * 0.75), (cx + r, cy - r * 0.65)],
                  width=width, fill=fill)

    def chip(self, x, y, label, size=30, fill=None, pad=22):
        w = self.width_of(label, size) + pad * 2
        h = size * 1.9
        self.box(x, y, x + w, y + h, r=h / 2, width=6, fill=fill)
        self.text(x + w / 2, y + h / 2, label, size=size, anchor="mm")
        return w

    def card(self, x1, y1, x2, y2, title, note, title_size=40, note_size=27):
        self.box(x1, y1, x2, y2, r=14, width=8, fill=None)
        self.text((x1 + x2) / 2, y1 + 36, title, size=title_size, anchor="mt")
        if note:
            self.text((x1 + x2) / 2, y2 - 40, note, size=note_size, anchor="mb")

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        image = self.img.resize((W, H), Image.LANCZOS)
        rgb = np.array(image.convert("RGB")).astype(int)
        diff = np.abs(rgb - np.array(PAPER)).max(axis=2)
        alpha = np.clip((diff - 2) / 10 * 255, 0, 255).astype(np.uint8)
        rgba = np.dstack([rgb.astype(np.uint8), alpha])
        Image.fromarray(rgba, "RGBA").save(OUT / f"{name}.png")
        print("wrote", OUT / f"{name}.png")




# ---------------------------------------------------------------- p01
def p01():
    s = Sheet(1301)
    s.text(110, 55, "GPT-3 有 1750 亿参数，为什么还说训练不足？", size=40)
    s.box(110, 150, 700, 470, r=16, width=9, fill=PAPER)
    s.text(405, 195, "GPT-3", size=40, anchor="mm")
    s.text(405, 260, "1750 亿参数", size=34, anchor="mm")
    s.text(405, 330, "训练数据 3000 亿 token", size=26, anchor="mm")
    s.text(405, 400, "每参数只配 1.7 个 token", size=26, anchor="mm")
    s.box(760, 150, 1490, 470, r=16, width=9, fill=YELLOW)
    s.streaks((770, 160, 1480, 460), step=46, width=2)
    s.text(1125, 210, "论文的结论", size=32, anchor="mm", stroke=2)
    s.text(1125, 310, "训练不足 10 倍", size=52, anchor="mm", stroke=2)
    s.text(1125, 400, "最优是每参数 20 个 token", size=26, anchor="mm", stroke=2)
    s.line([(110, 540), (1490, 540)], width=6)
    s.text(110, 580, "参数够多，但被喂得不够", size=38)
    s.text(110, 655, "同样一笔算力，堆参数和堆数据有个最优配比", size=32)
    s.text(110, 730, "这就是 Scaling Laws 要回答的问题", size=34)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(1302)
    s.text(110, 70, "Scaling Laws：算力该怎么分？", size=56)
    s.text(110, 160, "阶段 7 · 第 13 课", size=34)
    s.line([(110, 235), (1490, 235)], width=9)
    s.text(110, 285, "两篇论文，两个相反的结论：", size=36)
    s.box(110, 370, 780, 620, r=16, width=9, fill=PAPER)
    s.text(445, 405, "2020 Kaplan", size=34, anchor="mm")
    s.text(445, 480, "使劲堆参数", size=32, anchor="mm")
    s.text(445, 555, "GPT-3 就是这么做的", size=26, anchor="mm")
    s.box(820, 370, 1490, 620, r=16, width=9, fill=YELLOW)
    s.streaks((830, 380, 1480, 610), step=46, width=2)
    s.text(1155, 405, "2022 Hoffmann", size=34, anchor="mm", stroke=2)
    s.text(1155, 480, "数据也得跟上", size=32, anchor="mm", stroke=2)
    s.text(1155, 555, "Chinchilla 纠正了偏差", size=26, anchor="mm", stroke=2)
    s.text(800, 700, "同一个问题：给定算力，怎么配最优", size=36, anchor="mm")
    s.text(800, 800, "答案决定了千亿美元的投入方向", size=30, anchor="mm")
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(1303)
    s.text(110, 55, "算力分进两个桶：参数和数据", size=42)
    s.box(110, 160, 700, 300, r=14, width=9, fill=PAPER)
    s.text(800, 230, "C ≈ 6 × N × D", size=40, anchor="mm")
    s.text(110, 400, "同样一笔算力，可以这样分：", size=30)

    # 左：参数多数据少
    s.box(110, 470, 700, 830, r=14, width=9, fill=PAPER)
    s.text(405, 505, "方案 A：堆参数", size=30, anchor="mm")
    s.box(180, 550, 380, 780, r=8, width=7, fill=METAL)
    s.text(280, 665, "N 大", size=28, anchor="mm")
    s.box(430, 700, 630, 780, r=8, width=7, fill=YELLOW)
    s.streaks((440, 710, 620, 770), step=26, width=2)
    s.text(530, 740, "D 小", size=26, anchor="mm", stroke=2)

    # 右：数据多参数少
    s.box(790, 470, 1490, 830, r=14, width=9, fill=YELLOW)
    s.streaks((800, 480, 1480, 820), step=54, width=2)
    s.text(1140, 505, "方案 B：堆数据", size=30, anchor="mm", stroke=2)
    s.box(850, 660, 1050, 780, r=8, width=7, fill=PAPER)
    s.text(950, 720, "N 小", size=26, anchor="mm")
    s.box(1110, 550, 1410, 780, r=8, width=7, fill=PAPER)
    s.text(1260, 665, "D 大", size=28, anchor="mm")

    s.text(800, 870, "哪个损失更低？这就是要算的", size=30, anchor="mm")
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(1304)
    s.text(110, 55, "2020 的答案：把参数往死里推", size=42)
    bars = [("GPT-1", 117, 2018), ("GPT-2", 1542, 2019), ("GPT-3", 175000, 2020)]
    base = 640
    s.line([(160, base), (1440, base)], width=9)
    for i, (name, params, year) in enumerate(bars):
        x = 350 + i * 380
        h = int(params / 175000 * 420)
        h = max(h, 40)
        s.box(x - 110, base - h, x + 110, base, r=10, width=9,
              fill=YELLOW if i == 2 else METAL)
        if i == 2:
            s.streaks((x - 100, base - h + 12, x + 100, base - 12), step=40, width=2)
        label = "1.17 亿" if params == 117 else ("15 亿" if params == 1542 else "1750 亿")
        s.text(x, base - h - 40, label, size=28, anchor="mm",
               stroke=2 if i == 2 else 0)
        s.text(x, base + 30, name, size=26, anchor="mt")
    s.line([(110, 720), (1490, 720)], width=6)
    s.text(110, 755, "三年涨了 1500 倍参数", size=36)
    s.text(110, 830, "但没人认真算过：数据该涨多少", size=32)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(1305)
    s.text(110, 55, "2022 的答案：每参数 20 个 token", size=42)

    s.text(110, 140, "GPT-3 的比例：", size=30)
    s.box(110, 190, 1490, 290, r=12, width=8, fill=PAPER)
    s.text(180, 240, "1.7", size=44, anchor="lm")
    s.text(320, 240, "token / 参数", size=28, anchor="lm")
    s.text(700, 240, "训练不足 10 倍", size=30, anchor="lm")

    s.text(110, 340, "Chinchilla 的最优比例：", size=30)
    s.box(110, 390, 1490, 490, r=12, width=8, fill=YELLOW)
    s.streaks((120, 400, 1480, 480), step=44, width=2)
    s.text(180, 440, "20", size=44, anchor="lm", stroke=2)
    s.text(320, 440, "token / 参数", size=28, anchor="lm", stroke=2)
    s.text(700, 440, "数据要涨 12 倍", size=30, anchor="lm", stroke=2)

    s.line([(110, 560), (1490, 560)], width=6)
    s.text(110, 600, "于是训了一个 700 亿参数的 Chinchilla", size=36)
    s.text(110, 675, "配 1.4 万亿 token，正好是每参数 20 个", size=34)
    s.text(110, 760, "结果：参数少一半，全面打败 GPT-3", size=38)
    s.text(110, 835, "推理成本还只有它的四成", size=32)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(1306)
    s.text(110, 55, "Chinchilla 定律：损失由两部分组成", size=42)
    s.box(110, 160, 1490, 300, r=14, width=9, fill=PAPER)
    s.text(800, 230, "L(N, D) = A / N^α + B / D^β + E", size=44, anchor="mm")

    items = [("A / N^α", "参数不够的惩罚", "α ≈ 0.34"),
             ("B / D^β", "数据不够的惩罚", "β ≈ 0.28"),
             ("E", "不可约的下限", "E ≈ 1.69")]
    for i, (f, name, val) in enumerate(items):
        y = 360 + i * 130
        s.box(110, y, 1490, y + 105, r=12, width=7, fill=YELLOW if i == 2 else PAPER)
        if i == 2:
            s.streaks((120, y + 8, 1480, y + 96), step=44, width=2)
        s.text(160, y + 52, f, size=34, anchor="lm", stroke=2 if i == 2 else 0)
        s.text(620, y + 52, name, size=28, anchor="lm", stroke=2 if i == 2 else 0)
        s.text(1180, y + 52, val, size=28, anchor="lm", stroke=2 if i == 2 else 0)

    s.text(800, 830, "两项互相权衡，算力固定时求最小", size=32, anchor="mm")
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(1307)
    s.text(110, 55, "实测：最优比例随算力变化", size=42)
    rows = [("算力", "参数量", "token 数", "D/N"),
            ("1e18", "78.4M", "2.1B", "27.1"),
            ("1e20", "659M", "25.3B", "38.3"),
            ("1e22", "5.1B", "329.9B", "65.3"),
            ("1e24", "42.5B", "3.9T", "92.4"),
            ("1e25", "117.6B", "14.2T", "120.5")]
    for i, (a, b, c, d) in enumerate(rows):
        y = 150 + i * 82
        s.box(110, y, 1420, y + 70, r=10, width=7,
              fill=METAL if i == 0 else PAPER)
        s.text(160, y + 35, a, size=28, anchor="lm")
        s.text(520, y + 35, b, size=28, anchor="lm")
        s.text(860, y + 35, c, size=28, anchor="lm")
        s.text(1200, y + 35, d, size=28, anchor="lm")

    s.line([(110, 620), (1490, 620)], width=6)
    s.text(110, 655, "论文说的 20，是它采样范围内（1e22 到 1e23）的拟合值", size=28)
    s.text(110, 725, "往外推，比例会漂移，所以外推要谨慎", size=30)
    s.text(110, 800, "这也是为什么不同论文给出的比例不一样", size=28)
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(1308)
    s.text(110, 55, "2026 年：反而要大幅过训", size=42)
    s.text(110, 140, "Llama 3 8B：每参数 1875 个 token，是 Chinchilla 的 94 倍", size=30)

    s.box(110, 210, 1490, 380, r=14, width=9, fill=YELLOW)
    s.streaks((120, 220, 1480, 370), step=48, width=2)
    s.text(800, 260, "为什么？训练成本只付一次", size=32, anchor="mm", stroke=2)
    s.text(800, 330, "推理成本付一辈子", size=40, anchor="mm", stroke=2)

    s.line([(110, 440), (1490, 440)], width=6)
    s.text(110, 480, "实测：1e24 算力下", size=32)
    s.box(140, 540, 1450, 640, r=12, width=8, fill=PAPER)
    s.text(200, 590, "最优方案", size=28, anchor="lm")
    s.text(500, 590, "42.5B 参数 / 3.9T token", size=28, anchor="lm")
    s.text(1050, 590, "loss 1.911", size=28, anchor="lm")
    s.box(140, 660, 1450, 760, r=12, width=8, fill=PAPER)
    s.text(200, 710, "过训 10 倍", size=28, anchor="lm")
    s.text(500, 710, "4.2B 参数 / 39.2T token", size=28, anchor="lm")
    s.text(1050, 710, "loss 1.971", size=28, anchor="lm")

    s.text(110, 810, "损失只多 0.059，推理却便宜 10 倍 —— 这笔买卖划算", size=32)
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(1309)
    s.text(110, 55, "真实模型的比例，差距有 1100 倍", size=42)
    s.text(110, 130, "每参数配多少个 token：", size=30)

    rows = [("GPT-3", "1.7", 40, "1700 亿参数 · 训练不足", PAPER),
            ("Chinchilla", "20", 110, "700 亿参数 · 刚好最优", METAL),
            ("Llama 3 8B", "1875", 400, "80 亿参数 · 过训 94 倍", YELLOW)]
    base = 700
    s.line([(160, base), (1440, base)], width=9)
    for i, (name, ratio, h, note, fill) in enumerate(rows):
        x = 350 + i * 400
        s.box(x - 115, base - h, x + 115, base, r=10, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((x - 105, base - h + 12, x + 105, base - 12), step=40, width=2)
        s.text(x, base - h - 44, ratio, size=38, anchor="mm",
               stroke=2 if fill == YELLOW else 0)
        s.text(x, base + 30, name, size=26, anchor="mt")
        s.text(x, base + 68, note, size=21, anchor="mt")

    s.text(110, 810, "左边训练不足，右边为了推理省钱拼命过训", size=30)
    s.text(110, 870, "柱高做了压缩，实际差距 1100 倍", size=24)
    s.save("p09")


# ---------------------------------------------------------------- p10
def p10():
    s = Sheet(1310)
    s.text(110, 55, "怎么选：看模型会被用多久", size=42)

    s.box(110, 160, 730, 560, r=16, width=9, fill=PAPER)
    s.text(420, 200, "只训一次", size=36, anchor="mm")
    s.text(420, 270, "贴 Chinchilla", size=32, anchor="mm")
    for i, (t, ok) in enumerate([("省训练算力", True), ("模型更大但更笨", False),
                                  ("适合一次性实验", True)]):
        y = 350 + i * 62
        (s.check if ok else s.cross)(210, y, r=16, width=8)
        s.text(255, y, t, size=26, anchor="lm")

    s.box(790, 160, 1490, 560, r=16, width=9, fill=YELLOW)
    s.streaks((800, 170, 1480, 550), step=48, width=2)
    s.text(1140, 200, "要长期服务", size=36, anchor="mm", stroke=2)
    s.text(1140, 270, "拼命过训", size=32, anchor="mm", stroke=2)
    for i, (t, ok) in enumerate([("推理便宜好几倍", True), ("能塞进消费级显卡", True),
                                  ("训练多花一点", False)]):
        y = 350 + i * 62
        (s.check if ok else s.cross)(890, y, r=16, width=8)
        s.text(935, y, t, size=26, anchor="lm", stroke=2)

    s.line([(110, 610), (1490, 610)], width=6)
    s.text(110, 650, "还有第三条路：把数据质量提上去", size=32)
    s.text(110, 720, "精选好 token 能换来 2 倍以上的有效算力", size=30)

    s.box(110, 790, 1490, 870, r=14, width=8, fill=PAPER)
    s.text(800, 830, "一句话：训练最优 ≠ 部署最优", size=32, anchor="mm")
    s.save("p10")


# ---------------------------------------------------------------- p11
def p11():
    s = Sheet(1311)
    s.text(110, 55, "还有一件事：涌现可能是假的", size=42)

    s.text(110, 140, "有人说某些能力会在某个规模突然蹦出来：", size=30)
    s.box(110, 200, 1490, 300, r=12, width=8, fill=PAPER)
    s.text(800, 250, "算术、多步推理、思维链跟随", size=34, anchor="mm")

    s.text(110, 350, "但 2023 年的论文认为这是测量假象：", size=30)
    s.box(110, 410, 1490, 510, r=12, width=8, fill=YELLOW)
    s.streaks((120, 420, 1480, 500), step=44, width=2)
    s.text(800, 460, "用精确匹配这种离散指标，会把平滑曲线看成跳变", size=32, anchor="mm", stroke=2)

    s.line([(110, 570), (1490, 570)], width=6)
    s.text(110, 610, "换成连续的交叉熵，曲线一直是平滑的", size=34)
    s.text(110, 685, "所以规划预算时，要按连续指标看", size=32)
    s.text(110, 760, "基准上的跳跃，往往只是打分器的问题", size=30)
    s.text(800, 840, "这个结论改变了整个行业做预测的方式", size=28, anchor="mm")
    s.save("p11")


# ---------------------------------------------------------------- p12
def p12():
    s = Sheet(1312)
    s.text(110, 55, "如果模型只用一次比赛，你会怎么配比例？", size=40)

    s.box(110, 160, 730, 500, r=16, width=9, fill=PAPER)
    s.text(420, 205, "贴 Chinchilla", size=38, anchor="mm")
    s.text(420, 275, "每参数 20 个 token", size=28, anchor="mm")
    s.text(420, 360, "省训练算力", size=30, anchor="mm")
    s.text(420, 430, "模型大、参数多", size=28, anchor="mm")

    s.box(790, 160, 1490, 500, r=16, width=9, fill=YELLOW)
    s.streaks((800, 170, 1480, 490), step=48, width=2)
    s.text(1140, 205, "拼命过训", size=38, anchor="mm", stroke=2)
    s.text(1140, 275, "每参数上千个 token", size=28, anchor="mm", stroke=2)
    s.text(1140, 360, "训练贵但推理便宜", size=30, anchor="mm", stroke=2)
    s.text(1140, 430, "模型小、部署容易", size=28, anchor="mm", stroke=2)

    s.line([(110, 550), (1490, 550)], width=6)
    s.text(110, 590, "真实答案取决于：你打算服务多少 token", size=32)
    s.text(110, 660, "服务量大 → 过训；只跑一次 → 贴最优", size=30)

    s.box(110, 740, 1490, 860, r=16, width=8, fill=PAPER)
    s.text(800, 785, "评论区说说你的取舍：训练省，还是推理省？", size=30, anchor="mm")
    s.text(800, 830, "下一集：注意力变体", size=26, anchor="mm")
    s.save("p12")


# ---------------------------------------------------------------- cover
def cover():
    s = Sheet(1300)
    s.text(110, 75, "1750 亿参数，居然还训练不足？", size=48)
    s.text(110, 165, "Scaling Laws · 阶段 7 · 第 13 课", size=28)
    s.line([(110, 235), (1490, 235)], width=9)

    bars = [("1.7", "GPT-3", PAPER), ("20", "Chinchilla", METAL), ("1875", "Llama 3 8B", YELLOW)]
    base = 650
    s.line([(160, base), (1440, base)], width=9)
    for i, (ratio, name, fill) in enumerate(bars):
        x = 350 + i * 400
        full = {"1.7": 34, "20": 96, "1875": 265}[ratio]
        s.box(x - 110, base - full, x + 110, base, r=10, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((x - 100, base - full + 12, x + 100, base - 12), step=40, width=2)
        s.text(x, base - full - 62, ratio, size=32, anchor="mm",
               stroke=2 if fill == YELLOW else 0)
        s.text(x, base - full - 26, "token/参数", size=20, anchor="mm")
        s.text(x, base + 28, name, size=26, anchor="mt")

    s.box(110, 720, 1490, 810, r=14, width=8, fill=YELLOW)
    s.streaks((120, 730, 1480, 800), step=46, width=2)
    s.text(800, 762, "算力的两个桶：参数和数据，怎么分？", size=30, anchor="mm", stroke=2)
    s.save("cover")


if __name__ == "__main__":
    for fn in (cover, p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12):
        fn()
