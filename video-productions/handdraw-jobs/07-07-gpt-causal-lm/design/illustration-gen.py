#!/usr/bin/env python3
"""Author the 07-07 illustrations locally as industrial-marker diagrams.

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
    s = Sheet(707)
    s.text(110, 60, "预测下一个词，就是全部训练信号", size=46)
    # GPT card
    s.box(110, 170, 790, 500, r=16, width=9, fill=PAPER)
    s.text(140, 195, "GPT 只看左边", size=32)
    words = ["今天", "天气", "很"]
    for i, w in enumerate(words):
        s.box(150 + i * 150, 320, 280 + i * 150, 410, r=10, width=7, fill=PAPER)
        s.text(215 + i * 150, 365, w, size=34, anchor="mm")
    s.arrow(595, 365, 620, 365, width=7)
    s.box(630, 320, 760, 410, r=10, width=8, fill=YELLOW)
    s.streaks((638, 328, 752, 402), step=28, width=2)
    s.text(695, 365, "好", size=38, anchor="mm", stroke=2)
    s.text(140, 445, "下一个词，就是训练标签", size=30)
    # training card
    s.box(840, 170, 1490, 500, r=16, width=9, fill=PAPER)
    s.text(870, 195, "训练时：整段一次前向", size=32)
    s.box(880, 300, 1450, 390, r=14, width=8, fill=YELLOW)
    s.streaks((890, 310, 1440, 380), step=32, width=2)
    s.text(1165, 345, "一次前向 → N 个位置的损失", size=34, anchor="mm", stroke=2)
    s.text(870, 445, "推理时：一次只生成一个 token", size=30)
    # bottom band
    s.box(110, 570, 1490, 720, r=16, width=9, fill=PAPER)
    s.text(800, 600, "每个位置只能看前面", size=42, anchor="mt")
    s.text(800, 662, "否则就是在偷看答案", size=30, anchor="mt")
    s.text(110, 740, "约束的来源，就是一行三角掩码", size=34)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(708)
    s.text(110, 60, "三角掩码：未来填负无穷", size=44)
    n, cell, x0, y0 = 6, 72, 140, 180
    for i in range(n):
        for j in range(n):
            x, y = x0 + j * cell, y0 + i * cell
            future = j > i
            diag = j == i
            s.box(x, y, x + cell, y + cell, r=6, width=5,
                  fill=METAL if future else (YELLOW if diag else PAPER))
            label = "-∞" if future else "·"
            s.text(x + cell / 2, y + cell / 2, label, size=26, anchor="mm",
                   stroke=1 if diag else 0)
    s.text(x0 + n * cell / 2, y0 - 34, "查询的列  j", size=24, anchor="mt")
    s.text(x0 - 12, y0 + n * cell / 2, "i", size=24, anchor="rm")
    # right column
    s.text(720, 180, "mask[i, j] = -∞  当 j > i", size=32)
    s.text(720, 240, "加到 softmax 之前", size=30)
    s.box(720, 310, 1460, 390, r=14, width=8, fill=PAPER)
    s.text(1090, 350, "exp(-∞) = 0", size=36, anchor="mm")
    s.box(720, 420, 1460, 500, r=14, width=8, fill=YELLOW)
    s.streaks((730, 430, 1450, 490), step=34, width=2)
    s.text(1090, 460, "未来位置的权重 = 0", size=36, anchor="mm", stroke=2)
    s.text(720, 550, "第一行：只看自己", size=30)
    s.text(720, 600, "最后一行：看满六个位置", size=30)
    s.text(720, 650, "每行权重加起来 = 1.000", size=30)
    s.text(110, 760, "整段序列只做一次，就得到 N 个并行的预测", size=34)
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(709)
    s.text(110, 60, "实跑：6 × 6 注意力矩阵", size=46)
    rows = [
        ["1.000", "0.000", "0.000", "0.000", "0.000", "0.000"],
        ["0.646", "0.354", "0.000", "0.000", "0.000", "0.000"],
        ["0.547", "0.317", "0.136", "0.000", "0.000", "0.000"],
        ["0.269", "0.232", "0.439", "0.060", "0.000", "0.000"],
        ["0.295", "0.097", "0.180", "0.158", "0.270", "0.000"],
        ["0.327", "0.041", "0.013", "0.101", "0.074", "0.444"],
    ]
    x0, y0, cw, ch = 170, 170, 190, 84
    s.box(x0 - 10, y0 + 5 * ch - 6, x0 + 6 * cw + 10, y0 + 6 * ch + 6, r=10, width=3, outline=BROWN)
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            x, y = x0 + j * cw, y0 + i * ch
            future = j > i
            s.text(x + cw / 2, y + ch / 2, v, size=30, anchor="mm",
                   fill=METAL if future else INK)
    s.text(x0 + 3 * cw, y0 - 30, "j ≤ i 的列都有概率；上三角恒为 0", size=26, anchor="mt")
    s.text(110, 740, "最后一行把 0.327、0.041 一路分到 0.444", size=32)
    s.text(110, 800, "每一行的和都是 1.000，位置越靠后，能看到的内容越多", size=30)
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(710)
    s.text(110, 60, "三角从哪来：前缀平均", size=46)
    panels = [
        (110, "① 均匀平均", "每个过去的词一样重要"),
        (585, "② 学到权重", "权重可以训练，形状不变"),
        (1060, "③ Q · K 转置", "权重由 token 内容决定"),
    ]
    for x, title, note in panels:
        s.box(x, 170, x + 430, 540, r=16, width=8, fill=PAPER)
        s.text(x + 215, 200, title, size=32, anchor="mt")
        # mini 4x4 matrix
        cx, cy, cell = x + 110, 280, 52
        for i in range(4):
            for j in range(4):
                px, py = cx + j * cell, cy + i * cell
                fill = PAPER if j <= i else METAL
                s.box(px, py, px + cell, py + cell, r=4, width=4, fill=fill)
        s.text(x + 215, 500, note, size=24, anchor="mt")
    s.text(110, 620, "三步都只是用下三角矩阵乘序列", size=40)
    s.text(110, 700, "掩码不是后来打的补丁，它从第一次平均就在", size=32)
    s.text(110, 760, "换掉的只是「权重怎么来」，不是「能看多远」", size=30)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(711)
    s.text(110, 60, "并行训练，串行推理", size=46)
    # training side
    s.box(110, 170, 780, 620, r=16, width=9, fill=PAPER)
    s.text(140, 195, "训练", size=36)
    s.box(150, 270, 740, 350, r=10, width=7, fill=YELLOW)
    s.streaks((158, 278, 732, 342), step=32, width=2)
    s.text(445, 310, "整段序列：t1 t2 t3 t4", size=30, anchor="mm", stroke=2)
    for k in range(4):
        x = 180 + k * 145
        s.arrow(x + 55, 360, x + 55, 440, width=7)
        s.box(x, 445, x + 110, 515, r=10, width=6, fill=PAPER)
        s.text(x + 55, 480, f"损失{k + 1}", size=24, anchor="mm")
    s.text(140, 555, "一次前向，N 个位置同时算", size=28)
    # inference side
    s.box(830, 170, 1490, 620, r=16, width=9, fill=PAPER)
    s.text(860, 195, "推理", size=36)
    for i, label in enumerate(["t1", "t2", "t3"]):
        x = 870 + i * 190
        s.box(x, 300, x + 130, 380, r=10, width=7, fill=PAPER)
        s.text(x + 65, 340, label, size=30, anchor="mm")
        if i < 2:
            s.arrow(x + 136, 340, x + 184, 340, width=7)
    s.arrow(1386, 340, 1452, 340, width=7)
    s.arrow(1452, 340, 1452, 476, width=7)
    s.box(1340, 480, 1470, 550, r=10, width=8, fill=YELLOW)
    s.text(1405, 515, "t4", size=30, anchor="mm", stroke=2)
    s.text(860, 555, "KV 缓存：省掉重复计算", size=28)
    s.text(110, 690, "串行深度 = 输出长度，这就是自回归税", size=38)
    s.text(110, 755, "训练能扩展，是因为一整批 token 在一次 GPU 通过里并行", size=28)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(712)
    s.text(110, 60, "损失：错位一格", size=46)
    s.text(160, 160, "输入", size=28)
    for i, t in enumerate(["t1", "t2", "t3"]):
        x = 160 + i * 170
        s.box(x, 200, x + 130, 280, r=10, width=7, fill=PAPER)
        s.text(x + 65, 240, t, size=30, anchor="mm")
    s.text(160, 310, "目标", size=28)
    for i, t in enumerate(["t2", "t3", "t4"]):
        x = 260 + i * 170
        s.box(x, 350, x + 130, 430, r=10, width=8, fill=YELLOW)
        s.streaks((x + 8, 358, x + 122, 422), step=26, width=2)
        s.text(x + 65, 390, t, size=30, anchor="mm", stroke=2)
        s.arrow(x - 30, 286, x + 65, 344, width=6)
    # stats
    stats = [("1.145", "偏置 logits"), ("2.418", "随机 logits"), ("2.303", "ln 10 基线")]
    for i, (v, label) in enumerate(stats):
        y = 160 + i * 145
        s.box(900, y, 1490, y + 120, r=12, width=8, fill=PAPER if i < 2 else METAL)
        s.text(1195, y + 42, v, size=40, anchor="mm")
        s.text(1195, y + 92, label, size=24, anchor="mm")
    s.text(110, 520, "每个位置预测下一个词，求和就是整段交叉熵", size=32)
    s.box(110, 600, 1490, 700, r=16, width=9, fill=YELLOW)
    s.streaks((120, 610, 1480, 690), step=36, width=2)
    s.text(800, 650, "预训练、SFT、RLHF，用的都是这一个损失", size=34, anchor="mm", stroke=2)
    s.text(110, 760, "错位一格，是为了让模型永远预测「还没见过的下一个」", size=30)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(713)
    s.text(110, 60, "同一组 logits，六种取法", size=46)
    bars = [("the", 0.380), ("dog", 0.255), ("mat", 0.127), ("jump", 0.069),
            ("cat", 0.047), ("ran", 0.038)]
    base = 580
    s.line([(140, base), (700, base)], width=8)
    for i, (w, p) in enumerate(bars):
        x = 165 + i * 90
        h = p * 900
        s.box(x - 28, base - h, x + 28, base, r=8, width=7, fill=YELLOW if i == 0 else PAPER)
        s.text(x, base - h - 24, f"{p:.3f}", size=22, anchor="mb")
        s.text(x, base + 26, w, size=24, anchor="mt")
    rows = [
        ("贪心", "the"),
        ("温度 0.7", "jumped"),
        ("温度 2.0", "mat"),
        ("top-k = 3", "the"),
        ("top-p = 0.9", "the"),
        ("min-p = 0.1", "dog"),
    ]
    for i, (label, out) in enumerate(rows):
        y = 165 + i * 80
        s.box(820, y, 1490, y + 64, r=12, width=7, fill=PAPER if i == 0 else (YELLOW if i == 5 else PAPER))
        s.text(860, y + 32, label, size=28, anchor="lm", stroke=2 if i == 5 else 0)
        s.arrow(1120, y + 32, 1240, y + 32, width=5)
        s.text(1280, y + 32, out, size=30, anchor="lm", stroke=2 if i == 5 else 0)
    s.text(110, 690, "采样只决定语气，不改变模型学到了什么", size=34)
    s.text(110, 755, "2026 年常见的默认：min-p + 温度 0.7", size=30)
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(714)
    s.text(110, 60, "GPT 配方：架构几乎没变", size=46)
    # scale axis
    s.line([(180, 620), (180, 190)], width=7)
    for i, (label, y) in enumerate([("124M", 560), ("1.5B", 450), ("175B", 330), ("数万亿", 210)]):
        s.circle(180, y, 12, width=0, fill=INK)
        s.text(150, y, label, size=26, anchor="rm")
    s.text(180, 660, "参数量", size=26, anchor="mt")
    cards = [
        ("纯解码器", "每层一次注意力 + 一次前馈"),
        ("扩展", "同样的循环，重复到万亿参数"),
        ("上下文学习", "少样本示例，不用微调"),
        ("RLHF", "人类偏好，把预训练文本变成助手"),
    ]
    for i, (title, note) in enumerate(cards):
        x = 430 + (i % 2) * 540
        y = 180 + (i // 2) * 230
        s.box(x, y, x + 500, y + 190, r=14, width=8, fill=YELLOW if i == 0 else PAPER)
        s.text(x + 32, y + 28, title, size=32)
        s.text(x + 32, y + 110, note, size=24)
    s.text(430, 700, "稳定的训练配方：pre-norm + RoPE + SwiGLU", size=30)
    s.text(430, 760, "真正拉开差距的，是数据、规模和后训练", size=30)
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(715)
    s.text(110, 60, "GPT vs BERT：损失决定能不能生成", size=42)
    s.box(110, 170, 780, 560, r=16, width=9, fill=PAPER)
    s.text(140, 195, "GPT", size=38)
    s.text(140, 260, "P(x_t | x_<t)", size=34)
    s.text(140, 330, "只看左边，预测下一个", size=28)
    s.check(180, 460, r=24, width=8)
    s.text(230, 460, "能自回归生成", size=34, anchor="lm")
    s.box(820, 170, 1490, 560, r=16, width=9, fill=PAPER)
    s.text(850, 195, "BERT", size=38)
    s.text(850, 260, "P(x_masked | 其余)", size=34)
    s.text(850, 330, "两边都看，补中间", size=28)
    s.cross(890, 460, r=22, width=8)
    s.text(940, 460, "不能自回归输出", size=34, anchor="lm")
    s.line([(110, 620), (1490, 620)], width=6)
    s.text(110, 660, "同一个 Transformer，换一个损失，就换一种能力", size=36)
    s.text(110, 730, "从 GPT-1 到 GPT-5，核心循环没有变", size=32)
    s.text(110, 790, "变的是数据、规模，以及后训练", size=32)
    s.save("p09")


# ---------------------------------------------------------------- cover
def cover():
    base = Image.new("RGB", (1920, 1080), PAPER)
    d = ImageDraw.Draw(base)
    title_font = ImageFont.truetype(FONT, 112)
    sub_font = ImageFont.truetype(FONT, 62)
    meta_font = ImageFont.truetype(FONT, 32)
    d.text((120, 160), "GPT", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((120, 300), "因果语言建模", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((120, 460), "那个三角掩码", font=sub_font, fill=INK)
    d.rectangle([120, 570, 700, 580], fill=INK)
    d.text((120, 610), "07-07 · Transformers Deep Dive", font=meta_font, fill=INK)
    art = Image.open(OUT / "p01.png").convert("RGB")
    art = art.resize((1040, 585), Image.LANCZOS)
    base.paste(art, (800, 400))
    base.save(OUT / "cover.png")
    print("wrote", OUT / "cover.png")


if __name__ == "__main__":
    for fn in (p01, p02, p03, p04, p05, p06, p07, p08, p09):
        fn()
    cover()
