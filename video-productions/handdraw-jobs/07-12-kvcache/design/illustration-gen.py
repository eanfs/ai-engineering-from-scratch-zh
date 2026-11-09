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
    s = Sheet(1201)
    s.text(110, 55, "为什么 AI 回答的第一个字要等这么久？", size=42)

    s.box(110, 150, 700, 400, r=18, width=9, fill=PAPER)
    s.text(140, 185, "用户", size=26)
    s.text(140, 240, "讲一下 KV 缓存", size=34)

    s.box(110, 430, 700, 620, r=18, width=9, fill=YELLOW)
    s.streaks((120, 440, 690, 610), step=44, width=2)
    s.text(140, 465, "AI", size=26, stroke=2)
    s.text(140, 515, "好的，KV 缓存是...", size=32, stroke=2)
    s.text(140, 575, "（等了 3 秒才出第一个字）", size=26, stroke=2)

    # 右：每个字的耗时柱状图（越来越快 = 柱子越来越矮）
    s.box(760, 150, 1490, 620, r=18, width=9, fill=PAPER)
    s.text(800, 185, "生成每个字花的时间", size=30)
    base = 560
    s.line([(820, base), (1450, base)], width=7)
    bars = [("第1个字", 240, INK), ("第2个", 120, METAL), ("第3个", 64, METAL), ("第4个", 40, METAL)]
    for i, (label, h, fill) in enumerate(bars):
        x = 880 + i * 140
        s.box(x - 45, base - h, x + 45, base, r=8, width=8, fill=fill)
        val = f"{h/100:.1f} 秒" if h >= 100 else f"{h/100:.2f} 秒"
        s.text(x, base - h - 30, val, size=24, anchor="mm")
        s.text(x, base + 24, label, size=22, anchor="mt")

    s.line([(110, 670), (1490, 670)], width=6)
    s.text(110, 705, "第一个字最贵，后面每个字越来越便宜", size=38)
    s.text(110, 775, "秘密就在一张不断变长的表里", size=34)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(1202)
    s.text(110, 70, "KV Cache 与 Flash Attention", size=58)
    s.text(110, 160, "阶段 7 · 第 12 课", size=34)
    s.line([(110, 235), (1490, 235)], width=9)
    s.text(110, 285, "训练 vs 推理，瓶颈完全不同：", size=38)
    s.box(110, 370, 780, 620, r=16, width=9, fill=PAPER)
    s.text(445, 415, "训练", size=40, anchor="mm")
    s.text(445, 490, "并行", size=32, anchor="mm")
    s.text(445, 555, "受算力约束", size=32, anchor="mm")
    s.box(820, 370, 1490, 620, r=16, width=9, fill=YELLOW)
    s.streaks((830, 380, 1480, 610), step=46, width=2)
    s.text(1155, 415, "推理", size=40, anchor="mm", stroke=2)
    s.text(1155, 490, "串行", size=32, anchor="mm", stroke=2)
    s.text(1155, 555, "受显存约束", size=32, anchor="mm", stroke=2)
    s.text(800, 700, "两个优化把推理从「慢」推到「快」", size=40, anchor="mm")
    s.box(110, 760, 1490, 855, r=14, width=7, fill=PAPER)
    s.text(800, 807, "KV 缓存：少重算　·　Flash Attention：少搬运", size=32, anchor="mm")
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(1203)
    s.text(110, 55, "朴素解码：每生成一个词，全部重算", size=40)
    x0, y0, cell = 150, 165, 46
    n = 8
    for r in range(n):
        for c in range(n):
            x, y = x0 + c * cell, y0 + r * cell
            fill = YELLOW if r == n - 1 else (METAL if c <= r else PAPER)
            s.box(x, y, x + cell - 6, y + cell - 6, r=4, width=5, fill=fill)
    s.text(x0, y0 + n * cell + 18, "第 N 步要算 N 个位置，前 N-1 步已经算过", size=24)
    s.box(780, 170, 1490, 560, r=16, width=9, fill=PAPER)
    s.text(820, 210, "运算次数", size=32)
    s.text(820, 290, "1 + 2 + 3 + ... + N", size=36)
    s.text(820, 360, "= N(N+1)/2", size=36)
    s.text(820, 440, "N = 4000 → 约 800 万次", size=30)
    s.text(820, 505, "其中绝大多数是重复的", size=30)
    s.line([(110, 620), (1490, 620)], width=6)
    s.text(110, 660, "一个词的隐藏状态一旦算出来，就永远不变", size=38)
    s.text(110, 730, "那为什么要再算一遍？", size=38)
    s.text(110, 810, "答案：不需要。存下来就行", size=36)
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(1204)
    s.text(110, 55, "KV 缓存：存成一张表，新词只查表", size=42)
    s.text(140, 140, "每个 token 追加一行", size=28)
    x0, y0, cw, ch = 140, 190, 105, 58
    for r in range(5):
        for c in range(2):
            x, y = x0 + c * cw, y0 + r * ch
            fill = YELLOW if r == 4 else PAPER
            s.box(x, y, x + cw - 8, y + ch - 8, r=6, width=6, fill=fill)
            if r == 4:
                s.streaks((x + 6, y + 6, x + cw - 14, y + ch - 14), step=22, width=2)
            label = "K" if c == 0 else "V"
            s.text(x + cw / 2 - 4, y + ch / 2 - 4, label, size=24, anchor="mm",
                   stroke=2 if r == 4 else 0)
    s.text(x0, y0 + 5 * ch + 16, "新 token 只追加，不改旧行", size=24)
    s.box(560, 190, 1490, 540, r=16, width=9, fill=PAPER)
    s.text(600, 225, "新 token 的 query", size=30)
    s.box(600, 280, 760, 360, r=10, width=8, fill=YELLOW)
    s.streaks((610, 290, 750, 350), step=28, width=2)
    s.text(680, 320, "q", size=32, anchor="mm", stroke=2)
    s.arrow(790, 320, 860, 320, width=8)
    s.text(900, 320, "× 整张缓存的 K", size=28, anchor="lm")
    s.text(600, 420, "→ 注意力权重 → 加权 V", size=28)
    s.text(600, 480, "不再重算历史，只做一次矩阵乘", size=28)
    s.line([(110, 620), (1490, 620)], width=6)
    s.text(110, 655, "复杂度：从 N 的平方降到 N", size=40)
    s.text(110, 725, "第一个词之后，每个词只多算一行", size=34)
    s.text(110, 795, "这就是「越往后越快」的原因", size=36)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(1205)
    s.text(110, 55, "代价：表越来越长，显存越来越紧", size=42)
    s.text(110, 140, "每 token、每层、每头都要存 K 和 V：", size=30)
    s.box(110, 200, 1490, 285, r=12, width=8, fill=PAPER)
    s.text(800, 242, "每 token 每层 = 2 × d_head × 精度字节", size=36, anchor="mm")
    s.text(110, 330, "上下文越长，这张表线性增长：", size=30)
    base = 620
    s.line([(150, base), (1450, base)], width=8)
    for i, (label, h, fill) in enumerate([("2K", 60, METAL), ("8K", 120, METAL), ("32K", 300, YELLOW), ("128K", 560, INK)]):
        x = 260 + i * 300
        s.box(x - 90, base - h, x + 90, base, r=10, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((x - 80, base - h + 10, x + 80, base - 10), step=36, width=2)
        s.text(x, base - h - 36, label, size=30, anchor="mm")
        s.text(x, base + 26, label, size=24, anchor="mt")
    s.line([(110, 700), (1490, 700)], width=6)
    s.text(110, 735, "表越长，能同时跑的请求越少", size=36)
    s.text(110, 805, "批量大小和上下文长度，直接抢同一块显存", size=32)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(1206)
    s.text(110, 55, "实测：70B 模型在 128K 上下文要 43 GB", size=40)
    rows = [("模型", "32K", "128K", False),
            ("Llama-3.2-3B", "3.76 GB", "15.03 GB", False),
            ("Llama-3-8B", "4.29 GB", "17.18 GB", False),
            ("Llama-3-70B", "10.74 GB", "42.95 GB", True),
            ("Qwen2.5-72B", "10.74 GB", "42.95 GB", False)]
    for i, (a, b, c, hot) in enumerate(rows):
        y = 150 + i * 82
        s.box(110, y, 1420, y + 70, r=10, width=7, fill=YELLOW if hot else PAPER)
        if hot:
            s.streaks((120, y + 8, 1410, y + 62), step=42, width=2)
        s.text(150, y + 35, a, size=28, anchor="lm", stroke=2 if hot else 0)
        s.text(820, y + 35, b, size=28, anchor="lm", stroke=2 if hot else 0)
        s.text(1150, y + 35, c, size=28, anchor="lm", stroke=2 if hot else 0)
    s.line([(110, 600), (1490, 600)], width=6)
    s.text(110, 635, "42.95 GB 比一张 40 GB 的 A100 还大", size=36)
    s.text(110, 705, "也就是说：光缓存就装不下，模型权重还没算", size=32)
    s.text(110, 780, "fp16 精度，批量大小 1", size=28)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(1207)
    s.text(110, 55, "GQA 与 MLA：为什么现代模型扛得住长上下文", size=38)
    s.text(110, 130, "标准多头注意力（MHA）：64 个查询 = 64 组 KV", size=30)
    for i in range(16):
        x = 140 + i * 82
        s.box(x, 175, x + 66, 255, r=6, width=6, fill=METAL)
    s.text(140, 268, "128K 上下文：32 GB", size=26)
    s.text(110, 320, "GQA：64 个查询共享 8 组 KV", size=30)
    for i in range(16):
        x = 140 + i * 82
        fill = YELLOW if i // 2 < 2 else PAPER
        s.box(x, 365, x + 66, 445, r=6, width=6, fill=fill)
        if fill == YELLOW:
            s.streaks((x + 4, 371, x + 62, 439), step=18, width=2)
    s.text(140, 458, "Llama 3 用的方案", size=26)
    s.text(110, 510, "MLA：把 KV 压成低秩表示", size=30)
    s.box(140, 555, 700, 640, r=10, width=8, fill=YELLOW)
    s.streaks((150, 565, 690, 630), step=40, width=2)
    s.text(420, 597, "压缩后存储，用时还原", size=30, anchor="mm", stroke=2)
    s.line([(110, 690), (1490, 690)], width=6)
    s.text(110, 725, "DeepSeek V3 在 128K 只要 16.37 GB", size=38)
    s.text(110, 795, "是 70B 稠密模型的三分之一", size=34)
    s.text(800, 850, "长上下文便宜，靠的是压缩这张表", size=28, anchor="mm")
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(1208)
    s.text(110, 55, "Flash Attention：真正的问题不是算力", size=42)
    s.text(110, 140, "标准注意力要物化一个 N×N 矩阵：", size=30)
    x0, y0, cell = 140, 195, 26
    n = 12
    for r in range(n):
        for c in range(n):
            s.box(x0 + c * cell, y0 + r * cell, x0 + c * cell + cell - 3,
                  y0 + r * cell + cell - 3, r=2, width=2, fill=METAL)
    s.text(x0, y0 + n * cell + 16, "N=2048 时是 419 万个格子", size=24)
    s.box(620, 195, 1490, 500, r=16, width=9, fill=PAPER)
    s.text(660, 235, "三次显存往返：", size=32)
    s.text(660, 305, "S = Q @ K", size=30)
    s.text(660, 375, "P = softmax(S)", size=30)
    s.text(660, 445, "O = P @ V", size=30)
    s.text(1050, 305, "写 N×N", size=26, anchor="lm")
    s.text(1050, 375, "读写 N×N", size=26, anchor="lm")
    s.text(1050, 445, "读写 N×N", size=26, anchor="lm")
    s.line([(110, 560), (1490, 560)], width=6)
    s.text(110, 595, "N 到两千以上，注意力先卡在显存，不是算力", size=36)
    s.text(110, 665, "经典 kernel 只能跑到现代 GPU 的四分之一到十分之一", size=32)
    s.text(110, 740, "所以关键不是少算，是少搬", size=38)
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(1209)
    s.text(110, 55, "显存墙：每一次往返都是十倍减速", size=42)
    s.text(110, 130, "H100 上的读写带宽：", size=30)

    rows = [("HBM 显存", 3, METAL, "3 TB/s"), ("SRAM 片上", 30, YELLOW, "30 TB/s")]
    for i, (name, val, fill, label) in enumerate(rows):
        y = 230 + i * 190
        s.text(140, y, name, size=32, anchor="lm")
        w = int(val / 30 * 980)
        s.box(400, y - 45, 400 + w, y + 45, r=10, width=8, fill=fill)
        if fill == YELLOW:
            s.streaks((410, y - 35, 400 + w - 10, y + 35), step=42, width=2)
        s.text(400 + w + 30, y, label, size=32, anchor="lm",
               stroke=2 if fill == YELLOW else 0)

    s.text(140, 480, "差 10 倍", size=40)
    s.text(400, 480, "→ 把数据搬一次显存，等于浪费十次片上计算", size=30)

    s.line([(110, 560), (1490, 560)], width=6)
    s.text(110, 595, "H100：显存 80 GB；每 SM 的 SRAM 只有约 256 KB", size=30)
    s.text(110, 665, "SRAM 快但极小，所以要想办法把工作集塞进去", size=32)
    s.text(110, 740, "Flash Attention 的核心：中间结果全部留在片上", size=34)
    s.text(110, 815, "不写回显存，就不用付那十倍的过路费", size=30)
    s.save("p09")


# ---------------------------------------------------------------- p10
def p10():
    s = Sheet(1210)
    s.text(110, 55, "分块把戏：N×N 矩阵永远不落地", size=42)
    s.box(110, 150, 640, 500, r=14, width=9, fill=PAPER)
    s.text(375, 190, "SRAM 片上", size=32, anchor="mm")
    s.box(160, 235, 380, 355, r=8, width=7, fill=YELLOW)
    s.streaks((170, 245, 370, 345), step=30, width=2)
    s.text(270, 295, "Q 块", size=28, anchor="mm", stroke=2)
    s.box(410, 235, 590, 355, r=8, width=7, fill=METAL)
    s.text(500, 295, "K,V 块", size=26, anchor="mm")
    s.text(375, 400, "tile 约 128 × 128", size=26, anchor="mm")
    s.text(375, 455, "在片上算完再加权累加", size=24, anchor="mm")
    s.arrow(660, 325, 730, 325, width=8)
    s.box(750, 150, 1490, 500, r=14, width=9, fill=PAPER)
    s.text(1120, 190, "只写回 O 块", size=32, anchor="mm")
    x0, y0, cell = 990, 240, 40
    for r in range(4):
        for c in range(4):
            s.box(x0 + c * cell, y0 + r * cell, x0 + c * cell + 34,
                  y0 + r * cell + 34, r=3, width=4, fill=YELLOW)
    s.text(1120, 420, "显存占用从 N² 降到 N", size=28, anchor="mm")
    s.text(1120, 465, "反向传播重算，不再存中间值", size=24, anchor="mm")
    s.line([(110, 560), (1490, 560)], width=6)
    s.text(110, 595, "滚动 softmax 跨块维护最大值与累加和", size=32)
    s.text(110, 660, "保证最终归一化是精确的，不是近似", size=32)
    s.text(110, 730, "每个 tile 只做一次显存往返", size=34)
    s.text(800, 830, "Flash 1 → 2 → 3 → 4，四代都在榨这一点", size=28, anchor="mm")
    s.save("p10")


# ---------------------------------------------------------------- p11
def p11():
    s = Sheet(1211)
    s.text(110, 55, "实测：分块结果与标准 softmax 逐位相同", size=38)
    s.text(110, 130, "tile 大小 vs 与标准结果的误差：", size=30)
    for i, (tile, err) in enumerate([("1", "4.44e-16"), ("2", "2.22e-16"), ("4", "2.22e-16"), ("8", "2.22e-16"), ("32", "2.22e-16")]):
        y = 190 + i * 76
        s.box(140, y, 900, y + 62, r=10, width=7, fill=PAPER)
        s.text(200, y + 31, f"tile = {tile}", size=28, anchor="lm")
        s.text(560, y + 31, f"误差 {err}", size=26, anchor="lm")
        if i >= 1:
            s.check(850, y + 31, r=16, width=8)
    s.box(950, 190, 1490, 560, r=16, width=9, fill=YELLOW)
    s.streaks((960, 200, 1480, 550), step=48, width=2)
    s.text(1220, 250, "2.22e-16", size=50, anchor="mm", stroke=2)
    s.text(1220, 330, "是浮点重排的舍入", size=26, anchor="mm", stroke=2)
    s.text(1220, 400, "不是近似算法", size=32, anchor="mm", stroke=2)
    s.text(1220, 480, "数学上与标准注意力等价", size=24, anchor="mm", stroke=2)
    s.line([(110, 620), (1490, 620)], width=6)
    s.text(110, 655, "A100 上墙钟加速 2 到 4 倍", size=36)
    s.text(110, 725, "H100 配 FP8 可以到 5 到 10 倍", size=36)
    s.text(110, 800, "不牺牲任何精度", size=34)
    s.save("p11")


# ---------------------------------------------------------------- p12
def p12():
    s = Sheet(1212)
    s.text(110, 55, "显存只够跑 32K 的 70B 模型，你怎么选？", size=40)
    s.box(110, 160, 730, 520, r=16, width=9, fill=PAPER)
    s.text(420, 205, "压 KV 缓存", size=38, anchor="mm")
    for i, (t, ok) in enumerate([("GQA 共享 KV 头", True), ("MLA 低秩压缩", True), ("KV 量化到 fp8", True), ("要改模型或换模型", False)]):
        y = 285 + i * 58
        (s.check if ok else s.cross)(208, y, r=16, width=8)
        s.text(250, y, t, size=26, anchor="lm")
    s.box(790, 160, 1490, 520, r=16, width=9, fill=YELLOW)
    s.streaks((800, 170, 1480, 510), step=48, width=2)
    s.text(1140, 205, "砍上下文", size=38, anchor="mm", stroke=2)
    for i, (t, ok) in enumerate([("立刻生效，不用改模型", True), ("显存直接省一半以上", True), ("长文档场景就废了", False), ("用户体验下降", False)]):
        y = 285 + i * 58
        (s.check if ok else s.cross)(888, y, r=16, width=8)
        s.text(930, y, t, size=26, anchor="lm", stroke=2)
    s.line([(110, 570), (1490, 570)], width=6)
    s.text(110, 610, "还有第三条路：把请求排队，用连续批处理填满显存", size=32)
    s.text(110, 680, "短回复一结束就换新请求进来，吞吐能提 5 到 10 倍", size=30)
    s.box(110, 750, 1490, 860, r=16, width=8, fill=PAPER)
    s.text(800, 790, "评论区说说你的取舍：压缓存，还是砍上下文？", size=30, anchor="mm")
    s.text(800, 835, "下一集：扩展定律", size=26, anchor="mm")
    s.save("p12")


# ---------------------------------------------------------------- cover
def cover():
    s = Sheet(1200)
    s.text(110, 70, "第一个字为什么最贵？", size=54)
    s.text(110, 158, "KV Cache 与 Flash Attention · 阶段 7 · 第 12 课", size=30)
    s.line([(110, 232), (1490, 232)], width=9)
    s.text(110, 280, "推理是串行的、受显存约束", size=32)
    x0, y0, cell = 130, 350, 57
    for r in range(4):
        for c in range(6):
            fill = YELLOW if c < 2 else METAL
            s.box(x0 + c * cell, y0 + r * cell, x0 + c * cell + cell - 8,
                  y0 + r * cell + cell - 8, r=6, width=7, fill=fill)
    s.text(130, y0 + 4 * cell + 20, "每个 token 追加一行 K、V —— 表越写越长", size=26)
    s.box(700, 350, 1490, 620, r=16, width=9, fill=PAPER)
    s.text(740, 385, "70B 模型在 128K 上下文：", size=28)
    s.text(740, 455, "KV 缓存 42.95 GB", size=40)
    s.text(740, 530, "比一张 A100 还大", size=32)
    s.text(740, 585, "所以现代模型都在压这张表", size=26)
    s.box(110, 720, 1490, 800, r=14, width=8, fill=YELLOW)
    s.streaks((120, 730, 1480, 790), step=46, width=2)
    s.text(800, 760, "KV 缓存少重算 · Flash Attention 少搬运", size=30, anchor="mm", stroke=2)
    s.save("cover")


if __name__ == "__main__":
    for fn in (cover, p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12):
        fn()
