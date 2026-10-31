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
    s = Sheet(701)
    # left: one attention layer
    s.text(120, 70, "一层注意力", size=52)
    s.box(120, 160, 620, 420, r=20, width=10, fill=PAPER)
    s.text(370, 235, "自注意力", size=56, anchor="mm")
    s.text(370, 330, "特征提取器", size=44, anchor="mm")
    s.text(370, 490, "一次 matmul 的容量", size=34, anchor="mm")
    s.text(370, 545, "喂不饱语言", size=34, anchor="mm")
    s.arrow(370, 425, 370, 462, width=8)

    # right: the stack
    s.text(860, 70, "可堆叠的 block", size=52)
    for i in range(4):
        y = 500 - i * 108
        fill = YELLOW if i == 3 else None
        s.box(900, y, 1380, y + 92, r=12, width=8, fill=fill)
        if fill:
            s.streaks((908, y + 8, 1372, y + 84), step=34, width=2)
            s.text(1140, y + 46, "block", size=38, anchor="mm", stroke=2)
        else:
            s.text(1140, y + 46, "block", size=38, anchor="mm")
    s.arrow(1140, 592, 1140, 636, width=9)
    s.box(980, 636, 1300, 726, r=14, width=9, fill=METAL)
    s.text(1140, 681, "语言模型", size=40, anchor="mm", stroke=2)
    s.line([(860, 800), (1500, 800)], width=6)
    s.text(1180, 828, "深度 = 容量", size=38, anchor="mm")
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(702)
    cards = [
        ("嵌入 + 位置", "token → 向量"),
        ("自注意力", "跨位置混合"),
        ("前馈 FFN", "逐位置变换"),
        ("残差", "x + 子层(x)"),
        ("归一化", "稳住残差流"),
        ("交叉注意力", "只在解码器"),
    ]
    x0, y0, cw, ch = 110, 150, 450, 250
    for i, (title, note) in enumerate(cards):
        cx = x0 + (i % 3) * (cw + 60)
        cy = y0 + (i // 3) * (ch + 60)
        s.card(cx, cy, cx + cw, cy + ch, title, note)
        s.circle(cx + 40, cy + 40, 26, width=7, fill=YELLOW)
        s.text(cx + 40, cy + 40, str(i + 1), size=28, anchor="mm")
    s.text(800, 810, "六个部件，一副骨架", size=44, anchor="mm")
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(703)

    def block_row(x0, y, layers, box_w, gap, size):
        x = x0
        centers = []
        for name in layers:
            fill = YELLOW if name in ("自注意力", "交叉注意力") else None
            s.box(x, y, x + box_w, y + 92, r=12, width=8, fill=fill)
            if fill:
                s.streaks((x + 8, y + 8, x + box_w - 8, y + 84), step=30, width=2)
            s.text(x + box_w / 2, y + 46, name, size=size, anchor="mm", stroke=2 if fill else 0)
            centers.append(x + box_w / 2)
            if name != layers[-1]:
                s.arrow(x + box_w, y + 46, x + box_w + gap, y + 46, width=7)
            x += box_w + gap
        return centers, x - gap

    s.text(80, 100, "编码器", size=40)
    enc_centers, enc_end = block_row(260, 150, ["LN", "自注意力", "LN", "FFN"], 180, 50, 34)
    s.text(260, 292, "双向，无掩码：每个位置看到所有位置", size=32)

    s.text(80, 390, "解码器", size=40)
    dec_centers, dec_end = block_row(260, 440, ["LN", "掩码自注意", "LN", "交叉注意", "LN", "FFN"], 160, 40, 28)
    s.text(260, 570, "三个子层；中间那层是编码器信息唯一入口", size=32)

    # encoder output rides a bus down into the cross-attention layer
    bus_x = enc_end + 60
    cross_x = dec_centers[3]
    s.line([(bus_x, 242), (bus_x, 372)], width=7, dash=16)
    s.line([(bus_x, 372), (cross_x, 372)], width=7, dash=16)
    s.arrow(cross_x, 372, cross_x, 436, width=7, dash=16)
    s.text(bus_x + 16, 300, "K, V", size=32, anchor="lm")

    # pure decoder note
    s.box(260, 640, 1400, 790, r=16, width=8, fill=None)
    s.text(300, 672, "纯解码器（GPT）", size=38)
    s.text(300, 730, "删掉交叉注意力：只剩掩码自注意力 + FFN", size=34)
    s.cross(1320, 700, r=26, width=9)
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(704)
    s.text(110, 55, "残差：让梯度穿过去", size=46)
    # main path
    y = 300
    s.box(160, y - 70, 560, y + 70, r=14, width=9, fill=PAPER)
    s.text(360, y - 20, "子层 f(x)", size=44, anchor="mm")
    s.text(360, y + 38, "注意力或 FFN", size=30, anchor="mm")
    s.circle(700, y, 46, width=9, fill=YELLOW)
    s.text(700, y, "+", size=56, anchor="mm")
    s.arrow(130, y, 160, y, width=8)
    s.arrow(560, y, 654, y, width=8)
    s.arrow(746, y, 860, y, width=8)
    s.text(900, y, "x + f(x)", size=44, anchor="lm")
    # bypass
    s.line([(230, y), (230, 205), (700, 205), (700, y - 46)], width=7, dash=16)
    s.text(430, 172, "残差旁路", size=30, anchor="mm")
    s.text(110, 400, "没有它，梯度大约过了 6 层就消失", size=36)
    # norm comparison
    s.line([(110, 470), (1500, 470)], width=5)
    s.text(110, 505, "归一化放哪儿", size=44)
    # post-norm
    s.box(160, 585, 660, 800, r=14, width=9, fill=None)
    s.text(410, 610, "post-norm（原论文）", size=36, anchor="mt")
    s.text(410, 690, "LN( x + 子层(x) )", size=40, anchor="mm")
    s.text(410, 760, "要小心热身才训得深", size=30, anchor="mm")
    # pre-norm
    s.box(820, 585, 1400, 800, r=14, width=9, fill=YELLOW)
    s.streaks((828, 593, 1392, 792), step=36, width=2)
    s.text(1110, 610, "pre-norm（现代默认）", size=36, anchor="mt", stroke=2)
    s.text(1110, 690, "x + 子层( LN(x) )", size=40, anchor="mm", stroke=2)
    s.text(1110, 760, "Llama · Qwen · GPT-3+", size=30, anchor="mm", stroke=2)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(705)
    s.text(110, 60, "2017 vs 2026：同一个 block", size=48)
    s.text(470, 140, "2017", size=38, anchor="mm")
    s.text(900, 140, "2026", size=38, anchor="mm")
    s.line([(110, 190), (1490, 190)], width=7)
    rows = [
        ("归一化", "LayerNorm", "RMSNorm"),
        ("FFN 激活", "ReLU", "SwiGLU"),
        ("FFN 扩展", "4×", "2.6×"),
        ("位置", "正弦绝对", "RoPE"),
        ("注意力", "完整 MHA", "GQA"),
        ("偏置项", "有", "无"),
    ]
    for i, (k, old, new) in enumerate(rows):
        y = 250 + i * 100
        s.text(110, y, k, size=34, anchor="lm")
        s.text(470, y, old, size=36, anchor="mm")
        s.arrow(660, y, 730, y, width=7)
        fill = YELLOW if i in (0, 1, 3, 4) else None
        s.box(760, y - 38, 1040, y + 38, r=12, width=7, fill=fill)
        s.text(900, y, new, size=34, anchor="mm", stroke=2 if fill else 0)
    s.text(1160, 300, "SwiGLU 三个矩阵", size=32)
    s.text(1160, 350, "才对齐 4× 参数量", size=32)
    s.text(1160, 430, "RMSNorm 少一次减法", size=32)
    s.text(1160, 560, "GQA 省 KV cache", size=32)
    s.text(1160, 610, "无偏置少一点参数", size=32)
    s.text(800, 830, "骨架没变，默认值换了", size=42, anchor="mm")
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(706)
    s.text(110, 60, "实跑：d = 8，编码器 2 层 + 解码器 2 层", size=44)

    def tokens(x, y, n, label, fill=PAPER):
        for i in range(n):
            s.box(x + i * 86, y, x + i * 86 + 70, y + 70, r=10, width=7, fill=fill)
        s.text(x, y + 92, label, size=30)

    tokens(200, 150, 6, "源 6 个 token")
    tokens(200, 420, 5, "目标 5 个 token")
    # encoder
    s.box(830, 140, 1060, 230, r=12, width=9, fill=YELLOW)
    s.streaks((838, 148, 1052, 222), step=30, width=2)
    s.text(945, 185, "编码器 ×2", size=36, anchor="mm", stroke=2)
    s.arrow(730, 185, 826, 185, width=8)
    s.arrow(1064, 185, 1160, 185, width=8)
    s.box(1160, 140, 1440, 230, r=12, width=8, fill=PAPER)
    s.text(1300, 185, "(6, 8)", size=40, anchor="mm")
    # decoder
    s.box(830, 410, 1060, 500, r=12, width=9, fill=YELLOW)
    s.streaks((838, 418, 1052, 492), step=30, width=2)
    s.text(945, 455, "解码器 ×2", size=36, anchor="mm", stroke=2)
    s.arrow(720, 455, 826, 455, width=8)
    s.arrow(1064, 455, 1160, 455, width=8)
    # cross input: encoder output runs down and into the decoder block
    s.line([(1300, 235), (1300, 340)], width=7, dash=16)
    s.line([(1300, 340), (945, 340)], width=7, dash=16)
    s.arrow(945, 340, 945, 404, width=7, dash=16)
    s.text(1316, 300, "K, V", size=30, anchor="lm")
    # output grid 5x8
    s.box(1160, 380, 1470, 530, r=12, width=8, fill=PAPER)
    gx, gy = 1188, 400
    for r in range(5):
        for c in range(8):
            s.d.rectangle([sc(gx + c * 34), sc(gy + r * 25), sc(gx + c * 34 + 28), sc(gy + r * 25 + 19)],
                          outline=INK, width=sc(2))
    s.text(1315, 552, "输出 (5, 8)", size=32, anchor="mt")
    # bottom notes
    s.line([(110, 630), (1490, 630)], width=5)
    s.text(110, 665, "前向一次，不训练：这一课只关心接线", size=36)
    s.text(110, 735, "pre-norm · RMSNorm · SwiGLU · 无偏置", size=36)
    s.text(110, 805, "整齐的形状，就是 2026 年的骨架", size=36)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(707)
    s.text(110, 60, "一层有多少参数", size=52)
    s.box(110, 160, 760, 300, r=14, width=9, fill=PAPER)
    s.text(435, 178, "多头注意力", size=36, anchor="mt")
    s.text(435, 262, "4 · d²", size=42, anchor="mm")
    s.box(840, 160, 1490, 300, r=14, width=9, fill=YELLOW)
    s.streaks((848, 168, 1482, 292), step=36, width=2)
    s.text(1165, 178, "SwiGLU 前馈", size=36, anchor="mt", stroke=2)
    s.text(1165, 262, "3 · r · d²", size=42, anchor="mm", stroke=2)
    s.circle(800, 230, 34, width=8, fill=PAPER)
    s.text(800, 230, "+", size=44, anchor="mm")

    s.text(110, 360, "d = 4096，r = 2.6", size=44)
    s.text(110, 425, "4 · 16.8M  +  3 × 2.6 × 16.8M", size=38)
    s.text(110, 490, "≈ 67M + 131M ≈ 198M 每一层", size=42)
    s.box(110, 545, 800, 675, r=14, width=9, fill=PAPER)
    s.text(455, 562, "198M × 32 层", size=34, anchor="mt")
    s.text(455, 640, "≈ 6.3B", size=38, anchor="mm")

    s.arrow(820, 610, 940, 610, width=8)
    s.circle(1090, 640, 92, width=12, fill=YELLOW)
    s.text(1090, 615, "≈ 7B", size=52, anchor="mm")
    s.text(1090, 678, "含嵌入", size=26, anchor="mm")
    s.text(1200, 640, "Llama 3 8B", size=34, anchor="lm")
    s.text(110, 740, "手算得出来的账，和公开数字对得上", size=38)
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(708)
    cols = [
        ("纯编码器", "分类 · 嵌入 · 检索", ["BERT", "ModernBERT", "DeBERTa"], False),
        ("纯解码器", "生成 · 对话 · 代码", ["GPT", "Llama", "Claude · Qwen"], True),
        ("编码器 + 解码器", "翻译 · 摘要 · 语音", ["T5", "BART", "Whisper"], False),
    ]
    for i, (title, use, names, hot) in enumerate(cols):
        x = 100 + i * 480
        fill = YELLOW if hot else None
        s.box(x, 130, x + 420, 660, r=18, width=10, fill=fill)
        if fill:
            s.streaks((x + 10, 140, x + 410, 650), step=40, width=2)
        s.text(x + 210, 180, title, size=44, anchor="mt", stroke=2 if hot else 0)
        s.text(x + 210, 250, use, size=30, anchor="mt", stroke=2 if hot else 0)
        for j, name in enumerate(names):
            s.box(x + 40, 320 + j * 100, x + 380, 400 + j * 100, r=10, width=6, fill=PAPER)
            s.text(x + 210, 360 + j * 100, name, size=34, anchor="mm")
        s.text(x + 210, 632, "赢下语言" if hot else "各自的主场", size=28, anchor="mm",
               stroke=2 if hot else 0)
    s.text(800, 740, "同一副骨架，三种接线", size=44, anchor="mm")
    s.text(800, 810, "输入有明确源序列时，编码器解码器仍然最好", size=34, anchor="mm")
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(709)
    s.text(110, 60, "生产里为什么不直接调现成层", size=46)
    # left: library layer
    s.box(110, 160, 760, 640, r=18, width=9, fill=None)
    s.text(435, 195, "PyTorch nn.Transformer", size=34, anchor="mt")
    items = ["Flash Attention", "GQA / MLA", "RoPE", "RMSNorm · SwiGLU"]
    for i, item in enumerate(items):
        s.text(160, 280 + i * 78, item, size=34, anchor="lm")
        s.cross(700, 280 + i * 78, r=20, width=8)
    s.text(435, 590, "都不是默认值", size=32, anchor="mm")
    # right: own block
    s.box(850, 160, 1490, 640, r=18, width=10, fill=YELLOW)
    s.streaks((860, 170, 1480, 630), step=44, width=2)
    s.text(1170, 195, "自己写 block", size=40, anchor="mt", stroke=2)
    for i, item in enumerate(items):
        s.text(900, 290 + i * 78, item, size=32, anchor="lm", stroke=2)
        s.check(1430, 290 + i * 78, r=22, width=9)
    # bottom
    s.box(850, 680, 1490, 790, r=14, width=8, fill=PAPER)
    s.text(1170, 735, "modeling_llama.py ≈ 500 行", size=34, anchor="mm")
    s.text(110, 720, "读一遍规范实现", size=40)
    s.text(110, 780, "比背组件清单管用", size=40)
    s.save("p09")


# ---------------------------------------------------------------- cover
def cover():
    base = Image.new("RGB", (1920, 1080), PAPER)
    d = ImageDraw.Draw(base)
    title_font = ImageFont.truetype(FONT, 112)
    sub_font = ImageFont.truetype(FONT, 62)
    meta_font = ImageFont.truetype(FONT, 32)
    d.text((120, 160), "完整的", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((120, 300), "Transformer", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((120, 460), "编码器 + 解码器", font=sub_font, fill=INK)
    d.rectangle([120, 570, 700, 580], fill=INK)
    d.text((120, 610), "07-05 · Transformers Deep Dive", font=meta_font, fill=INK)
    art = Image.open(OUT / "p01.png").convert("RGB")
    art = art.resize((1040, 585), Image.LANCZOS)
    # keep the paper colour so the composite stays flat
    base.paste(art, (800, 400))
    base.save(OUT / "cover.png")
    print("wrote", OUT / "cover.png")


if __name__ == "__main__":
    for fn in (p01, p02, p03, p04, p05, p06, p07, p08, p09):
        fn()
    cover()
