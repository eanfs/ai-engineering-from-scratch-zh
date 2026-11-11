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
    s = Sheet(1501)
    s.text(110, 55, "每个词真的都要看前面所有词吗？", size=44)
    s.text(110, 145, "完整注意力：", size=30)
    x0, y0, cell = 140, 200, 42
    for r in range(10):
        for c in range(10):
            if c <= r:
                s.box(x0 + c * cell, y0 + r * cell, x0 + c * cell + cell - 4,
                      y0 + r * cell + cell - 4, r=3, width=3, fill=METAL)
    s.text(140, 640, "每个位置都要看前面全部", size=26)

    s.arrow(620, 400, 700, 400, width=9)

    s.text(740, 145, "只跳附近几个：", size=30)
    for r in range(10):
        for c in range(10):
            if 0 <= r - c < 3:
                s.box(760 + c * cell, y0 + r * cell, 760 + c * cell + cell - 4,
                      y0 + r * cell + cell - 4, r=3, width=3, fill=YELLOW)
    s.text(760, 640, "只看窗口内的三个", size=26)

    s.line([(110, 700), (1490, 700)], width=6)
    s.text(110, 740, "如果只看附近，效果会差多少？", size=38)
    s.text(110, 815, "这一课讲四种把注意力掰弯的办法", size=32)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(1502)
    s.text(110, 70, "注意力变体", size=62)
    s.text(110, 165, "阶段 7 · 第 15 课", size=34)
    s.line([(110, 240), (1490, 240)], width=9)
    s.text(110, 290, "完整注意力的问题是平方：", size=36)
    s.box(110, 370, 1490, 470, r=14, width=9, fill=YELLOW)
    s.streaks((120, 380, 1480, 460), step=44, width=2)
    s.text(800, 420, "显存 O(N²)、算力 O(N²)", size=40, anchor="mm", stroke=2)
    s.text(110, 520, "128K 上下文的 70B 模型，每层 160 亿个注意力条目", size=28)
    rows = [("1  滑动窗口", "只看固定窗口，缓存降 128 倍", YELLOW),
            ("2  稀疏 / 块", "预先设计稀疏模式，省一半", PAPER),
            ("3  差分注意力", "两张图相减，清掉注意力汇", PAPER)]
    for i, (name, note, fill) in enumerate(rows):
        y = 600 + i * 90
        s.box(110, y, 1490, y + 76, r=12, width=7, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 68), step=44, width=2)
        s.text(150, y + 38, name, size=28, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(560, y + 38, note, size=25, anchor="lm", stroke=2 if fill == YELLOW else 0)
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(1503)
    s.text(110, 55, "平方的代价有多大", size=44)
    s.box(110, 150, 1490, 270, r=14, width=9, fill=PAPER)
    s.text(800, 210, "128K 上下文 × 80 层 × 70B 模型", size=34, anchor="mm")
    s.text(110, 320, "每层注意力条目：", size=30)
    s.box(140, 380, 1460, 480, r=12, width=8, fill=PAPER)
    s.text(200, 430, "128,000 × 128,000", size=36, anchor="lm")
    s.text(900, 430, "= 160 亿", size=36, anchor="lm")

    s.text(110, 530, "乘以 80 层：", size=30)
    s.box(140, 590, 1460, 690, r=12, width=8, fill=YELLOW)
    s.streaks((150, 600, 1450, 680), step=44, width=2)
    s.text(200, 640, "160 亿 × 80", size=36, anchor="lm", stroke=2)
    s.text(900, 640, "= 1.28 万亿", size=36, anchor="lm", stroke=2)

    s.line([(110, 730), (1490, 730)], width=6)
    s.text(110, 765, "Flash Attention 藏掉了激活显存", size=32)
    s.text(110, 835, "但每个词仍然要看其他每个词，算术成本没变", size=30)
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(1504)
    s.text(110, 55, "滑动窗口：只看前面 W 个词", size=42)

    s.text(140, 140, "完整因果", size=26)
    x0, y0, cell = 140, 190, 36
    for r in range(9):
        for c in range(9):
            if c <= r:
                s.box(x0 + c * cell, y0 + r * cell, x0 + c * cell + cell - 4,
                      y0 + r * cell + cell - 4, r=2, width=3, fill=METAL)

    s.text(560, 140, "窗口 W = 4", size=26)
    for r in range(9):
        for c in range(9):
            if 0 <= r - c < 4:
                s.box(560 + c * cell, y0 + r * cell, 560 + c * cell + cell - 4,
                      y0 + r * cell + cell - 4, r=2, width=3, fill=YELLOW)

    s.box(960, 190, 1490, 520, r=14, width=9, fill=PAPER)
    s.text(1000, 230, "窗口外置为负无穷", size=28)
    s.text(1000, 300, "不参与 softmax", size=26)
    s.text(1000, 380, "N=8192、W=1024 时", size=26)
    s.text(1000, 450, "非零行少 8 倍", size=32)

    s.line([(110, 570), (1490, 570)], width=6)
    s.text(110, 605, "更大的收益在 KV 缓存：每层只留最后 W 个词", size=32)
    s.text(110, 675, "128K 上下文的缓存可以直接砍掉两个数量级", size=30)
    s.text(110, 745, "这是长上下文最便宜的一招", size=34)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(1505)
    s.text(110, 55, "实测：KV 缓存从 42.9 GB 降到 0.3 GB", size=38)

    rows = [("方案", "缓存", "省了多少"),
            ("完整注意力", "42.9 GB", "—"),
            ("滑动窗口 W=4096", "1.3 GB", "32 倍"),
            ("滑动窗口 W=1024", "0.3 GB", "128 倍"),
            ("Gemma 3 混合 (5:1)", "7.4 GB", "5.8 倍"),
            ("差分注意力", "85.9 GB", "反而 2 倍")]
    for i, (a, b, c) in enumerate(rows):
        y = 140 + i * 88
        hot = i == 3
        s.box(90, y, 1470, y + 74, r=10, width=7, fill=YELLOW if hot else PAPER)
        if hot:
            s.streaks((100, y + 8, 1460, y + 66), step=44, width=2)
        s.text(140, y + 37, a, size=28, anchor="lm", stroke=2 if hot else 0)
        s.text(900, y + 37, b, size=28, anchor="lm", stroke=2 if hot else 0)
        s.text(1230, y + 37, c, size=28, anchor="lm", stroke=2 if hot else 0)

    s.line([(110, 700), (1490, 700)], width=6)
    s.text(110, 735, "70B 模型、128K 上下文、fp16、8 个 KV 头", size=28)
    s.text(110, 805, "纯滑动窗口最省，但会牺牲长程检索", size=30)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(1506)
    s.text(110, 55, "但纯滑动窗口会看不见远处", size=42)

    s.box(110, 150, 730, 500, r=16, width=9, fill=PAPER)
    s.text(420, 195, "纯滑动窗口", size=34, anchor="mm")
    s.text(420, 275, "省 128 倍显存", size=28, anchor="mm")
    s.text(420, 350, "但看不到很远的上下文", size=26, anchor="mm")
    s.text(420, 430, "长文档检索会瞎", size=28, anchor="mm")
    s.cross(180, 350, r=20, width=9)

    s.box(790, 150, 1490, 500, r=16, width=9, fill=YELLOW)
    s.streaks((800, 160, 1480, 490), step=48, width=2)
    s.text(1140, 195, "混合结构", size=34, anchor="mm", stroke=2)
    s.text(1140, 275, "五层滑动 + 一层全局", size=28, anchor="mm", stroke=2)
    s.text(1140, 350, "既省显存又保留检索", size=26, anchor="mm", stroke=2)
    s.text(1140, 430, "Gemma 3 的默认做法", size=28, anchor="mm", stroke=2)

    s.line([(110, 570), (1490, 570)], width=6)
    s.text(110, 605, "Mistral 7B 走另一条路：全栈用滑动窗口", size=30)
    s.text(110, 675, "信息靠层与层的重叠窗口往前传", size=30)
    s.text(110, 745, "L 层之后，有效感受野是 L 乘 W", size=32)
    s.text(110, 820, "所以深度本身就是一种长程机制", size=30)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(1507)
    s.text(110, 55, "稀疏注意力：画出想要的形状", size=42)

    s.text(140, 140, "局部 + 跨步：", size=28)
    x0, y0, cell = 140, 190, 42
    n = 9
    for r in range(n):
        for c in range(n):
            on = (0 <= r - c < 2) or (c % 3 == 0)
            if on:
                s.box(x0 + c * cell, y0 + r * cell, x0 + c * cell + cell - 4,
                      y0 + r * cell + cell - 4, r=2, width=3, fill=YELLOW)
            else:
                s.box(x0 + c * cell, y0 + r * cell, x0 + c * cell + cell - 4,
                      y0 + r * cell + cell - 4, r=2, width=2, fill=PAPER)

    s.box(620, 190, 1490, 520, r=14, width=9, fill=PAPER)
    s.text(660, 230, "三种经典形状：", size=30)
    s.text(660, 300, "1. 局部 + 跨步", size=26)
    s.text(660, 360, "2. Longformer / BigBird", size=26)
    s.text(660, 420, "3. 原生稀疏（DeepSeek）", size=26)
    s.text(660, 480, "算力降到 N 的 1.5 次方", size=28)

    s.line([(110, 570), (1490, 570)], width=6)
    s.text(110, 605, "数学很简单：把不需要的位置掩掉", size=32)
    s.text(110, 675, "难的是 kernel：让零块根本不进显存", size=32)
    s.text(110, 745, "胜利来自不加载，不是不算", size=34)
    s.text(110, 820, "FlashAttention-3 和 FlexAttention 让自定义模式成为一等公民", size=26)
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(1508)
    s.text(110, 55, "一个怪现象：注意力总是跑到第一个词", size=40)

    s.text(110, 140, "单条注意力权重分布：", size=30)
    weights = [0.018, 0.068, 0.335, 0.031, 0.054, 0.112, 0.156, 0.227]
    base = 420
    s.line([(160, base), (1200, base)], width=8)
    for i, w in enumerate(weights):
        x = 220 + i * 130
        h = int(w * 620)
        hot = i == 2
        s.box(x - 50, base - h, x + 50, base, r=8, width=8,
              fill=YELLOW if hot else METAL)
        if hot:
            s.streaks((x - 42, base - h + 10, x + 42, base - 10), step=28, width=2)
        s.text(x, base - h - 30, f"{w:.3f}", size=22, anchor="mm")
        s.text(x, base + 26, f"p{i}", size=20, anchor="mt")

    s.text(1250, 250, "第一个词", size=28)
    s.text(1250, 310, "权重 0.335", size=28)
    s.text(1250, 370, "但它毫无意义", size=24)

    s.line([(110, 560), (1490, 560)], width=6)
    s.text(110, 595, "这叫注意力汇：模型需要一个「什么都别看」的出口", size=30)
    s.text(110, 665, "它把浪费的权重倒进第一个词，污染了检索", size=30)
    s.text(110, 735, "差分注意力就是来清这个的", size=34)
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(1509)
    s.text(110, 55, "差分注意力：两张图相减", size=42)

    s.box(110, 150, 1490, 290, r=14, width=9, fill=PAPER)
    s.text(800, 220, "A = softmax(Q₁K₁) − λ · softmax(Q₂K₂)", size=38, anchor="mm")

    s.text(110, 340, "减完之后，汇点那个成分被抵消：", size=30)
    rows = [("位置", "单张注意力", "差分后"),
            ("p2（汇点）", "0.335", "0.169"),
            ("p7", "0.227", "0.112"),
            ("p6", "0.156", "0.097")]
    for i, (a, b, c) in enumerate(rows):
        y = 410 + i * 82
        hot = i == 1
        s.box(140, y, 1400, y + 68, r=10, width=7, fill=YELLOW if hot else PAPER)
        if hot:
            s.streaks((150, y + 8, 1390, y + 60), step=42, width=2)
        s.text(200, y + 34, a, size=26, anchor="lm", stroke=2 if hot else 0)
        s.text(700, y + 34, b, size=26, anchor="lm", stroke=2 if hot else 0)
        s.text(1080, y + 34, c, size=26, anchor="lm", stroke=2 if hot else 0)

    s.line([(110, 740), (1490, 740)], width=6)
    s.text(110, 775, "差值可以带负号，这是它和普通注意力的关键区别", size=30)
    s.text(110, 845, "代价是算两张图，KV 缓存翻倍", size=30)
    s.save("p09")


# ---------------------------------------------------------------- p10
def p10():
    s = Sheet(1510)
    s.text(110, 55, "四种方案怎么选", size=44)

    rows = [("方案", "省多少", "代价"),
            ("纯滑动窗口", "128 倍", "长程检索变差"),
            ("Gemma 3 混合", "5.8 倍", "要调层数配比"),
            ("稀疏 / 块", "省一半以上", "kernel 工程复杂"),
            ("差分注意力", "反而 2 倍", "换更干净的检索")]
    for i, (a, b, c) in enumerate(rows):
        y = 150 + i * 95
        s.box(90, y, 1470, y + 80, r=10, width=7,
              fill=METAL if i == 0 else PAPER)
        s.text(140, y + 40, a, size=28, anchor="lm")
        s.text(760, y + 40, b, size=28, anchor="lm")
        s.text(1080, y + 40, c, size=26, anchor="lm")

    s.line([(110, 660), (1490, 660)], width=6)
    s.text(110, 695, "2026 年的前沿模型通常混着用", size=32)
    s.text(110, 765, "多数层滑动窗口，每五层一次全局，少数头做差分", size=30)
    s.text(110, 835, "没有单一最优，要看任务形态", size=30)
    s.save("p10")


# ---------------------------------------------------------------- p11
def p11():
    s = Sheet(1511)
    s.text(110, 55, "长上下文的成本地图", size=44)

    bars = [("完整", 42.9, INK), ("混合 5:1", 7.4, YELLOW),
            ("SWA-4096", 1.3, METAL), ("SWA-1024", 0.3, METAL)]
    base = 620
    s.line([(160, base), (1440, base)], width=9)
    for i, (name, gb, fill) in enumerate(bars):
        x = 280 + i * 300
        h = int(min(gb / 42.9, 1) * 380)
        h = max(h, 26)
        s.box(x - 100, base - h, x + 100, base, r=10, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((x - 90, base - h + 12, x + 90, base - 12), step=38, width=2)
        s.text(x, base - h - 36, f"{gb} GB", size=26, anchor="mm",
               stroke=2 if fill == YELLOW else 0)
        s.text(x, base + 28, name, size=24, anchor="mt")

    s.line([(110, 700), (1490, 700)], width=6)
    s.text(110, 735, "同样的模型、同样的上下文，缓存差 140 倍", size=32)
    s.text(110, 805, "这就是为什么长上下文产品都在调注意力结构", size=30)
    s.save("p11")


# ---------------------------------------------------------------- p12
def p12():
    s = Sheet(1512)
    s.text(110, 55, "做超长文档检索，你会选哪种注意力？", size=40)

    opts = [("纯滑动窗口", "最省，但会丢远处信息", PAPER),
            ("Gemma 3 混合", "平衡，需要调层配比", YELLOW),
            ("差分注意力", "检索最干净，缓存翻倍", PAPER)]
    for i, (name, note, fill) in enumerate(opts):
        y = 170 + i * 150
        s.box(110, y, 1490, y + 120, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 112), step=46, width=2)
        s.text(180, y + 60, name, size=34, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(640, y + 60, note, size=26, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.line([(110, 640), (1490, 640)], width=6)
    s.text(110, 675, "先看缓存预算，再看检索精度要求", size=32)
    s.text(110, 745, "两个都紧的话，混合结构是默认答案", size=30)

    s.box(110, 810, 1490, 870, r=12, width=8, fill=PAPER)
    s.text(800, 840, "下一集：投机解码", size=28, anchor="mm")
    s.save("p12")


# ---------------------------------------------------------------- cover
def cover():
    s = Sheet(1500)
    s.text(110, 75, "每个词都要看每个词吗？", size=52)
    s.text(110, 170, "注意力变体 · 阶段 7 · 第 15 课", size=28)
    s.line([(110, 240), (1490, 240)], width=9)

    s.text(140, 280, "完整注意力", size=24)
    x0, y0, cell = 140, 320, 30
    for r in range(8):
        for c in range(8):
            if c <= r:
                s.box(x0 + c * cell, y0 + r * cell, x0 + c * cell + cell - 4,
                      y0 + r * cell + cell - 4, r=2, width=3, fill=METAL)

    s.text(520, 280, "滑动窗口", size=24)
    for r in range(8):
        for c in range(8):
            if 0 <= r - c < 3:
                s.box(520 + c * cell, y0 + r * cell, 520 + c * cell + cell - 4,
                      y0 + r * cell + cell - 4, r=2, width=3, fill=YELLOW)

    s.box(860, 320, 1490, 570, r=16, width=9, fill=PAPER)
    s.text(900, 360, "KV 缓存 @ 128K", size=28)
    s.text(900, 430, "42.9 GB → 0.3 GB", size=36)
    s.text(900, 500, "降 128 倍", size=32)

    s.box(110, 640, 1490, 760, r=14, width=9, fill=YELLOW)
    s.streaks((120, 650, 1480, 750), step=48, width=2)
    s.text(800, 700, "长上下文最便宜的一招", size=34, anchor="mm", stroke=2)

    s.text(110, 810, "滑动窗口 · 稀疏 · 差分，三种掰弯注意力的办法", size=26)
    s.save("cover")


if __name__ == "__main__":
    for fn in (cover, p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12):
        fn()
