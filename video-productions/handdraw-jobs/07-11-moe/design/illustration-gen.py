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
    s = Sheet(1101)
    s.text(110, 60, "同样的算力，凭什么塞进二十倍参数？", size=46)
    # left: dense
    s.box(110, 170, 740, 560, r=16, width=9, fill=PAPER)
    s.text(140, 195, "稠密模型", size=40)
    s.text(140, 250, "每个 token 跑完全部参数", size=27)
    for i in range(4):
        s.box(150, 320 + i * 50, 700, 360 + i * 50, r=8, width=7, fill=YELLOW)
        s.streaks((160, 330 + i * 50, 690, 355 + i * 50), step=30, width=2)
    s.text(140, 600, "671B 总参数 → 671B 全部激活", size=32)

    # right: MoE
    s.box(810, 170, 1490, 560, r=16, width=9, fill=PAPER)
    s.text(840, 195, "MoE 模型", size=40)
    s.text(840, 250, "每个 token 只跑 k 个专家", size=27)
    for i in range(8):
        x = 850 + (i % 4) * 155
        y = 320 + (i // 4) * 105
        lit = i in (1, 6)
        s.box(x, y, x + 135, y + 85, r=8, width=8,
              fill=YELLOW if lit else PAPER)
        if lit:
            s.streaks((x + 8, y + 8, x + 127, y + 77), step=26, width=2)
        s.text(x + 67, y + 42, f"E{i+1}", size=26, anchor="mm", stroke=2 if lit else 0)
    s.text(840, 600, "671B 总参数 → 37B 激活（5.5%）", size=32)

    s.line([(110, 690), (1490, 690)], width=6)
    s.text(110, 730, "存储随专家数涨，算力只随激活数涨", size=40)
    s.text(110, 800, "这就是 MoE 把「知识」和「每 token 算力」解耦的方式", size=34)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(1102)
    s.text(110, 70, "Mixture of Experts", size=64)
    s.text(110, 165, "阶段 7 · 第 11 课", size=34)
    s.line([(110, 240), (1490, 240)], width=9)
    s.text(110, 285, "2026 年的前沿模型，几乎全是 MoE：", size=38)
    items = [("DeepSeek-V3", "671B 总 / 37B 激活"), ("Mixtral 8×22B", "141B 总 / 39B 激活"),
             ("Qwen2.5-MoE", "细粒度专家"), ("Llama 4", "原生多模态 MoE"), ("Kimi K2", "1T 总参数")]
    for i, (name, note) in enumerate(items):
        x = 110 + (i % 3) * 460
        y = 370 + (i // 3) * 190
        s.box(x, y, x + 420, y + 155, r=14, width=8, fill=YELLOW if i == 0 else PAPER)
        if i == 0:
            s.streaks((x + 10, y + 10, x + 410, y + 145), step=40, width=2)
        s.text(x + 210, y + 55, name, size=36, anchor="mm", stroke=2 if i == 0 else 0)
        s.text(x + 210, y + 110, note, size=26, anchor="mm", stroke=2 if i == 0 else 0)
    s.text(110, 790, "稀疏，是这十年最重要的扩展思路", size=44)
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(1103)
    s.text(110, 60, "稠密模型：算力 = 参数量 × 2", size=46)
    s.box(110, 170, 700, 420, r=16, width=9, fill=YELLOW)
    s.streaks((120, 180, 690, 410), step=44, width=2)
    s.text(405, 250, "FLOPs", size=52, anchor="mm", stroke=2)
    s.text(405, 320, "= 2 × N_params", size=44, anchor="mm", stroke=2)
    s.text(405, 380, "每个 token 都付全额账单", size=30, anchor="mm", stroke=2)

    s.box(760, 170, 1490, 420, r=16, width=9, fill=PAPER)
    s.text(1125, 250, "把模型做大 → 算力线性涨", size=32, anchor="mm")
    s.line([(830, 380), (1420, 380)], width=7)
    s.line([(830, 380), (830, 300)], width=7)
    for i in range(5):
        h = 20 + i * 18
        s.box(860 + i * 105, 380 - h, 940 + i * 105, 380, r=6, width=6, fill=METAL)

    s.line([(110, 490), (1490, 490)], width=6)
    s.text(110, 530, "2024 年，前沿撞上了这堵墙：", size=40)
    s.text(110, 600, "要变得明显更聪明，每个 token 需要指数级更多 FLOPs", size=34)
    s.text(110, 680, "Mixture of Experts 打断了这个绑定", size=42)
    s.text(110, 760, "把「参数总量」和「每次激活」拆开算", size=34)
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(1104)
    s.text(110, 60, "做法：把每个 FFN 换成 E 个专家", size=46)

    s.box(110, 170, 700, 330, r=14, width=8, fill=PAPER)
    s.text(405, 250, "稠密 block", size=34, anchor="mm")
    s.text(405, 300, "FFN 一个，全部 token 都过", size=26, anchor="mm")

    s.arrow(730, 250, 790, 250, width=8)

    s.box(820, 170, 1490, 330, r=14, width=8, fill=PAPER)
    s.text(1155, 215, "MoE block", size=34, anchor="mm")
    for i in range(6):
        x = 850 + i * 105
        lit = i in (1, 4)
        s.box(x, 245, x + 92, 315, r=8, width=7, fill=YELLOW if lit else PAPER)
        if lit:
            s.streaks((x + 6, 251, x + 86, 309), step=22, width=2)
        s.text(x + 46, 280, f"E{i+1}", size=22, anchor="mm", stroke=2 if lit else 0)

    s.line([(110, 400), (1490, 400)], width=6)
    s.text(110, 440, "三个量必须分清：", size=40)
    rows = [("E", "专家总数", "存储随它涨"), ("k", "每 token 激活数", "算力随它涨"),
            ("E × FFN", "总参数", "671B"), ("k × FFN", "激活参数", "37B")]
    for i, (a, b, c) in enumerate(rows):
        x = 110 + (i % 2) * 700
        y = 520 + (i // 2) * 130
        s.box(x, y, x + 620, y + 105, r=12, width=7, fill=PAPER)
        s.text(x + 30, y + 52, a, size=38, anchor="lm")
        s.text(x + 175, y + 52, b, size=28, anchor="lm")
        s.text(x + 440, y + 52, c, size=24, anchor="lm")
    s.text(810, 830, "2026 典型配置：E=256，k=8", size=36, anchor="mm")
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(1105)
    s.text(110, 60, "路由器：一个线性层，给每个专家打分", size=44)

    s.box(110, 170, 380, 470, r=14, width=9, fill=PAPER)
    s.text(245, 205, "token 向量", size=30, anchor="mm")
    for i in range(5):
        s.box(150, 250 + i * 40, 340, 280 + i * 40, r=6, width=6, fill=METAL)
    s.text(245, 510, "d_model = 7168", size=24, anchor="mm")

    s.arrow(400, 320, 470, 320, width=8)
    s.box(490, 170, 700, 470, r=14, width=9, fill=YELLOW)
    s.streaks((500, 180, 690, 460), step=42, width=2)
    s.text(595, 250, "W_router", size=30, anchor="mm", stroke=2)
    s.text(595, 320, "256 × 7168", size=26, anchor="mm", stroke=2)
    s.text(595, 390, "每个专家一行", size=24, anchor="mm", stroke=2)

    s.arrow(720, 320, 790, 320, width=8)

    s.box(810, 170, 1490, 470, r=14, width=9, fill=PAPER)
    s.text(1150, 205, "256 个分数", size=30, anchor="mm")
    for i in range(8):
        x = 840 + i * 78
        h = 40 + (i * 37) % 150
        lit = i in (2, 5)
        s.box(x, 430 - h, x + 58, 430, r=6, width=6, fill=YELLOW if lit else METAL)
        if lit:
            s.streaks((x + 6, 436 - h, x + 52, 424), step=20, width=2)
    s.text(1150, 505, "取 top-8，其余置零", size=28, anchor="mm")

    s.line([(110, 560), (1490, 560)], width=6)
    s.text(110, 600, "路由器只看当前 token，不看别的 token", size=36)
    s.text(110, 665, "所以它天然可以并行，不需要任何 token 间通信", size=34)
    s.text(110, 740, "但这也埋下隐患：每个 token 只看自己，负载容易扎堆", size=34)
    s.text(110, 815, "这就是下一节要讲的负载均衡问题", size=36)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(1106)
    s.text(110, 60, "门控：选中的专家按权重混合", size=46)

    s.box(110, 170, 700, 400, r=14, width=8, fill=PAPER)
    s.text(405, 205, "8 个专家，选中 E2 和 E6", size=30, anchor="mm")
    for i in range(8):
        x = 140 + i * 68
        lit = i in (1, 5)
        s.box(x, 250, x + 58, 350, r=8, width=7, fill=YELLOW if lit else PAPER)
        if lit:
            s.streaks((x + 6, 256, x + 52, 344), step=22, width=2)
        s.text(x + 29, 300, f"E{i+1}", size=22, anchor="mm", stroke=2 if lit else 0)
        if lit:
            s.text(x + 29, 375, "0.62" if i == 1 else "0.38", size=22, anchor="mt")

    s.arrow(730, 285, 790, 285, width=8)

    s.box(820, 170, 1490, 400, r=14, width=8, fill=PAPER)
    s.text(1155, 210, "输出 = Σ gate_i × Expert_i(x)", size=32, anchor="mm")
    s.box(860, 260, 1250, 360, r=10, width=7, fill=YELLOW)
    s.streaks((870, 270, 1240, 350), step=34, width=2)
    s.text(1055, 310, "0.62 × E2(x)", size=32, anchor="mm", stroke=2)
    s.text(1290, 310, "+", size=44, anchor="mm")
    s.box(1320, 260, 1460, 360, r=10, width=7, fill=METAL)
    s.text(1390, 310, "0.38", size=28, anchor="mm")

    s.line([(110, 480), (1490, 480)], width=6)
    s.text(110, 520, "关键细节：门控权重用的是原始分数", size=40)
    s.text(110, 590, "不是加了偏置之后的分数", size=34)
    s.text(110, 660, "偏置只用来决定「选谁」，不用来加权输出", size=34)
    s.text(110, 740, "DeepSeek V3 就是靠这个把路由和表达解耦的", size=34)
    s.text(110, 810, "下一节看它怎么解决负载均衡", size=36)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(1107)
    s.text(110, 55, "负载均衡：别让一个专家撑死", size=42)
    s.text(110, 115, "不加约束时，路由器偏好少数专家：", size=28)

    base = 460
    s.line([(140, base), (1460, base)], width=8)
    usage = [120, 301, 95, 260, 80, 230, 70, 180]
    for i, u in enumerate(usage):
        x = 200 + i * 160
        h = int(u / 301 * 225)
        s.box(x - 55, base - h, x + 55, base, r=8, width=8,
              fill=YELLOW if u >= 280 else METAL)
        s.text(x, base - h - 30, str(u), size=24, anchor="mm")
        s.text(x, base + 26, f"E{i+1}", size=22, anchor="mt")

    s.line([(110, 520), (1490, 520)], width=6)
    s.text(110, 545, "三种修法：", size=34)
    opts = [("1. 辅助损失", "罚使用率方差，多一个超参和梯度信号"),
            ("2. 容量 + 丢弃", "Switch 的做法，溢出 token 跳过本层"),
            ("3. 无辅助损失", "DeepSeek V3：学到的偏置，只动选择")]
    for i, (t, n) in enumerate(opts):
        y = 600 + i * 88
        s.box(110, y, 1490, y + 76, r=12, width=6, fill=YELLOW if i == 2 else PAPER)
        if i == 2:
            s.streaks((120, y + 8, 1480, y + 68), step=42, width=2)
        s.text(140, y + 38, t, size=28, anchor="lm", stroke=2 if i == 2 else 0)
        s.text(470, y + 38, n, size=25, anchor="lm", stroke=2 if i == 2 else 0)
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(1108)
    s.text(110, 60, "无辅助损失：偏置怎么推", size=46)

    s.text(110, 165, "每个训练步之后，对每个专家：", size=34)
    s.box(110, 230, 720, 400, r=14, width=9, fill=PAPER)
    s.text(415, 285, "使用率 > 目标", size=34, anchor="mm")
    s.text(415, 350, "bias -= γ", size=40, anchor="mm")
    s.box(770, 230, 1490, 400, r=14, width=9, fill=YELLOW)
    s.streaks((780, 240, 1480, 390), step=44, width=2)
    s.text(1130, 285, "使用率 < 目标", size=34, anchor="mm", stroke=2)
    s.text(1130, 350, "bias += γ", size=40, anchor="mm", stroke=2)

    s.line([(110, 460), (1490, 460)], width=6)
    s.text(110, 500, "选择用 scores + bias：", size=38)
    s.box(110, 560, 1490, 650, r=12, width=8, fill=PAPER)
    s.text(800, 605, "top_k = argmax( scores + bias )", size=38, anchor="mm")

    s.text(110, 700, "门控用原始 scores：", size=38)
    s.box(110, 750, 1490, 840, r=12, width=8, fill=PAPER)
    s.text(800, 795, "gate = softmax( scores[top_k] )", size=38, anchor="mm")

    s.text(800, 870, "偏置不影响模型预测，只纠正负载 → 没有第二个梯度信号", size=30, anchor="mm")
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(1109)
    s.text(110, 60, "实跑：1000 个 token，目标每个专家 250", size=42)

    stats = [("250", "目标 / 专家"), ("206–301", "无偏置波动范围"), ("2.079", "ln 8 均匀上限")]
    for i, (big, label) in enumerate(stats):
        x = 110 + i * 460
        s.box(x, 150, x + 420, 330, r=16, width=9, fill=YELLOW if i == 2 else PAPER)
        if i == 2:
            s.streaks((x + 10, 160, x + 410, 320), step=38, width=2)
        s.text(x + 210, 225, big, size=48, anchor="mm", stroke=2 if i == 2 else 0)
        s.text(x + 210, 290, label, size=26, anchor="mm", stroke=2 if i == 2 else 0)

    s.line([(110, 375), (1490, 375)], width=6)
    s.text(110, 405, "加偏置更新后，熵逼近上限：", size=34)
    base = 700
    s.line([(160, base), (1440, base)], width=8)
    ent = [2.072, 2.076, 2.073, 2.076, 2.073]
    for i, v in enumerate(ent):
        h = int((v - 2.05) / 0.03 * 130)
        x = 280 + i * 230
        s.box(x - 70, base - h, x + 70, base, r=8, width=8, fill=METAL)
        s.text(x, base - h - 30, f"{v:.3f}", size=24, anchor="mm")
        s.text(x, base + 26, f"iter {i}", size=22, anchor="mt")
    s.line([(160, base - 160), (1440, base - 160)], width=4, dash=14)
    s.text(1440, base - 200, "ln 8 = 2.079", size=26, anchor="rt")

    s.text(110, 800, "使用率在几个迭代内收敛到接近均匀", size=32)
    s.text(110, 855, "这就是 DeepSeek V3「没有辅助损失」的做法", size=28)
    s.save("p09")


# ---------------------------------------------------------------- p10
def p10():
    s = Sheet(1110)
    s.text(110, 60, "细粒度专家：E 大、k 大、专家窄", size=44)

    s.text(110, 160, "经典 MoE（GShard / Switch）：", size=34)
    for i in range(4):
        x = 130 + i * 190
        s.box(x, 220, x + 160, 400, r=10, width=8, fill=PAPER)
        s.text(x + 80, 310, f"E{i+1}", size=28, anchor="mm")
    s.text(130, 425, "E 小（8–64），k 小（1–2），每个专家 = 完整 FFN", size=28)

    s.arrow(1000, 310, 1010, 310, width=6)
    s.text(110, 490, "现代细粒度（DeepSeek V3 / Qwen-MoE）：", size=34)
    for i in range(16):
        x = 120 + (i % 16) * 84
        lit = i in (2, 7, 11)
        s.box(x, 550, x + 70, 700, r=6, width=6, fill=YELLOW if lit else PAPER)
        if lit:
            s.streaks((x + 4, 556, x + 66, 694), step=18, width=2)
    s.text(120, 730, "E 大（256+），k 大（8+），每个专家 = 1/8 FFN 宽", size=28)

    s.line([(110, 780), (1490, 780)], width=6)
    s.text(800, 820, "同样的总参数，组合数 C(256,8) ≈ 400 万亿种", size=34, anchor="mm")
    s.text(800, 870, "质量上去，每 token 延迟不动", size=34, anchor="mm")
    s.save("p10")


# ---------------------------------------------------------------- p11
def p11():
    s = Sheet(1111)
    s.text(110, 60, "成本画像：参数多、算力少、显存炸", size=44)

    rows = [("配置", "每 token 激活", "总参数", False),
            ("Mixtral 8×22B", "~39B", "141B", False),
            ("Llama 3 70B（稠密）", "70B", "70B", False),
            ("DeepSeek-V3", "37B", "671B", True),
            ("Kimi K2", "~32B", "1T", False)]
    for i, (a, b, c, hot) in enumerate(rows):
        y = 170 + i * 85
        s.box(110, y, 1420, y + 72, r=10, width=7,
              fill=YELLOW if hot else PAPER)
        if hot:
            s.streaks((120, y + 8, 1410, y + 64), step=42, width=2)
        s.text(150, y + 36, a, size=30, anchor="lm", stroke=2 if hot else 0)
        s.text(880, y + 36, b, size=30, anchor="lm", stroke=2 if hot else 0)
        s.text(1200, y + 36, c, size=30, anchor="lm", stroke=2 if hot else 0)

    s.line([(110, 600), (1490, 600)], width=6)
    s.text(110, 635, "V3 在几乎每个基准上打败 Llama 3 70B，每 token 算得更少", size=30)
    s.text(110, 700, "但所有专家都活在 GPU 上，不管有没有点火：", size=32)
    s.text(110, 765, "671B × fp16 ≈ 1.3 TB 显存 → 必须专家并行", size=34)
    s.text(110, 830, "延迟由全对全通信主导，不是矩阵乘", size=28)
    s.save("p11")


# ---------------------------------------------------------------- p12
def p12():
    s = Sheet(1112)
    s.text(110, 60, "如果你只有 8 张卡，会选稠密还是 MoE？", size=42)

    s.box(110, 170, 730, 530, r=16, width=9, fill=PAPER)
    s.text(420, 220, "稠密", size=40, anchor="mm")
    dense = [("部署简单", True), ("延迟稳定", True), ("每 token 全额算力", False)]
    for i, (t, ok) in enumerate(dense):
        y = 310 + i * 70
        if ok:
            s.check(210, y, r=20, width=9)
        else:
            s.cross(210, y, r=20, width=9)
        s.text(260, y, t, size=30, anchor="lm")

    s.box(790, 170, 1490, 530, r=16, width=9, fill=YELLOW)
    s.streaks((800, 180, 1480, 520), step=46, width=2)
    s.text(1140, 220, "MoE", size=40, anchor="mm", stroke=2)
    moe = [("同算力下参数多 20 倍", True), ("前沿质量、更低推理成本", True), ("显存要够、要专家并行", False)]
    for i, (t, ok) in enumerate(moe):
        y = 310 + i * 70
        if ok:
            s.check(890, y, r=20, width=9)
        else:
            s.cross(890, y, r=20, width=9)
        s.text(940, y, t, size=30, anchor="lm", stroke=2)

    s.line([(110, 590), (1490, 590)], width=6)
    s.text(110, 625, "MoE 的质量优势，只在约 6B 激活参数以上才出现", size=32)
    s.text(110, 695, "小模型、边缘部署、延迟敏感的单用户服务：别选 MoE", size=30)

    s.box(110, 760, 1490, 870, r=16, width=8, fill=PAPER)
    s.text(800, 800, "评论区说说你的取舍：显存优先，还是延迟优先？", size=30, anchor="mm")
    s.text(800, 845, "下一集：位置编码怎么外推", size=26, anchor="mm")
    s.save("p12")


# ---------------------------------------------------------------- cover
def cover():
    s = Sheet(1100)
    s.text(110, 70, "671B 参数，只激活 37B", size=54)
    s.text(110, 155, "Mixture of Experts · 阶段 7 · 第 11 课", size=32)
    s.line([(110, 230), (1490, 230)], width=9)
    for i in range(8):
        x = 150 + i * 165
        lit = i in (2, 5)
        s.box(x, 300, x + 135, 520, r=10, width=9, fill=YELLOW if lit else PAPER)
        if lit:
            s.streaks((x + 8, 308, x + 127, 512), step=30, width=2)
        s.text(x + 67, 410, f"E{i+1}", size=30, anchor="mm", stroke=2 if lit else 0)
    s.text(150, 560, "256 个专家，每个 token 只叫醒 8 个", size=34)
    s.text(150, 620, "存储随专家涨，算力只随激活涨", size=32)
    s.box(150, 690, 1450, 790, r=14, width=8, fill=YELLOW)
    s.streaks((160, 700, 1440, 780), step=44, width=2)
    s.text(800, 740, "DeepSeek-V3：671B 总 / 37B 激活（5.5%）", size=36, anchor="mm", stroke=2)
    s.save("cover")


if __name__ == "__main__":
    for fn in (cover, p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12):
        fn()
