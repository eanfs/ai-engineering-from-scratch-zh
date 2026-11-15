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
    s = Sheet(2201)
    s.text(110, 60, "加五个字，78% 变 91%", size=48)
    s.box(110, 160, 1490, 300, r=20, width=11, fill=YELLOW)
    s.streaks((120, 170, 1480, 290), step=52, width=3)
    s.text(800, 230, "Let's think step by step", size=46, anchor="mm", stroke=2)

    s.box(110, 350, 720, 600, r=20, width=11, fill=PAPER)
    s.text(415, 400, "不加", size=38, anchor="mm")
    s.text(415, 495, "78%", size=72, anchor="mm")
    s.text(415, 570, "零样本", size=32, anchor="mm")

    s.box(780, 350, 1490, 600, r=20, width=11, fill=YELLOW)
    s.streaks((790, 360, 1480, 590), step=52, width=3)
    s.text(1135, 400, "加上", size=38, anchor="mm", stroke=2)
    s.text(1135, 495, "91%", size=72, anchor="mm", stroke=2)
    s.text(1135, 570, "同一个模型", size=32, anchor="mm", stroke=2)

    s.text(110, 670, "唯一差别是给了模型一张草稿纸", size=44)
    s.text(110, 760, "这不是 hack", size=48)
    s.text(110, 845, "这就是推理的运作方式", size=44)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(2202)
    s.text(110, 70, "少样本与思维链", size=64)
    s.text(110, 165, "阶段 11 · 第 2 课", size=36)
    s.line([(110, 250), (1490, 250)], width=10)

    rows = [("示例", "被压缩过的指令", YELLOW),
            ("思维链", "把推理写成 token", PAPER),
            ("自洽", "多采样再表决", PAPER)]
    for i, (name, note, fill) in enumerate(rows):
        y = 340 + i * 165
        s.box(110, y, 1490, y + 140, r=18, width=10, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 132), step=52, width=3)
        s.text(180, y + 45, name, size=44, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(180, y + 105, note, size=34, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.text(800, 880, "告诉它做什么是提示，教它怎么想是工程", size=34, anchor="mm")
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(2203)
    s.text(110, 55, "少样本什么时候真管用", size=50)

    s.box(110, 150, 730, 480, r=20, width=10, fill=PAPER)
    s.text(420, 205, "简单任务", size=42, anchor="mm")
    s.text(420, 300, "情感分类", size=36, anchor="mm")
    s.text(420, 400, "差不到 2 点", size=38, anchor="mm")

    s.box(790, 150, 1490, 480, r=20, width=10, fill=YELLOW)
    s.streaks((800, 160, 1480, 470), step=56, width=3)
    s.text(1140, 205, "复杂任务", size=42, anchor="mm", stroke=2)
    s.text(1140, 300, "多步算术", size=36, anchor="mm", stroke=2)
    s.text(1140, 400, "提 10 到 25 点", size=38, anchor="mm", stroke=2)

    s.line([(110, 550), (1490, 550)], width=9)
    s.text(110, 595, "示例是被压缩过的指令", size=44)
    s.text(110, 680, "与其描述格式，不如展示格式", size=40)
    s.text(110, 760, "与其解释推理，不如演示一遍", size=40)
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(2204)
    s.text(110, 55, "示例怎么挑", size=50)

    rows = [("语义相似", "离输入最近", YELLOW),
            ("标签多样", "覆盖所有类别", PAPER),
            ("难度匹配", "匹配复杂度", PAPER)]
    for i, (name, note, fill) in enumerate(rows):
        y = 150 + i * 155
        s.box(110, y, 1490, y + 130, r=18, width=10, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 122), step=50, width=3)
        s.text(180, y + 42, name, size=42, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(180, y + 98, note, size=34, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.line([(110, 640), (1490, 640), ], width=9)
    s.text(110, 685, "最优数量：3 到 5 个", size=48)
    s.text(110, 770, "少于 3 个提取不出模式", size=38)
    s.text(110, 850, "多于 5 个收益递减", size=38)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(2205)
    s.text(110, 55, "思维链为什么管用", size=50)

    s.box(110, 145, 730, 430, r=20, width=10, fill=PAPER)
    s.text(420, 195, "标准", size=40, anchor="mm")
    s.text(420, 285, "问题 → 答案", size=36, anchor="mm")
    s.text(420, 375, "压进一次前向", size=34, anchor="mm")

    s.box(790, 145, 1490, 430, r=20, width=10, fill=YELLOW)
    s.streaks((800, 155, 1480, 420), step=54, width=3)
    s.text(1140, 195, "思维链", size=40, anchor="mm", stroke=2)
    for i, st in enumerate(["问题", "推理一步", "再一步", "答案"]):
        s.text(1140, 255 + i * 44, st, size=32, anchor="mm", stroke=2)

    s.line([(110, 500), (1490, 500)], width=9)
    s.text(110, 545, "每个推理 token 都是下一个 token 的上下文", size=40)
    s.text(110, 630, "token 叠加 = 计算深度延展", size=42)
    s.text(110, 720, "人类不会一个念头跳完多步", size=38)
    s.text(110, 800, "transformer 也不会", size=38)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(2206)
    s.text(110, 55, "GSM8K 上的三级跳", size=50)

    rows = [("模型", "零样本", "+CoT", "少样本"),
            ("GPT-4o", "78%", "91%", "95%"),
            ("GPT-5", "94%", "97%", "98%"),
            ("Llama 4", "80%", "89%", "94%"),
            ("DeepSeek", "89%", "94%", "96%")]
    for i, (a, b, c, d) in enumerate(rows):
        y = 150 + i * 115
        hot = i == 1
        s.box(90, y, 1470, y + 98, r=14, width=9,
              fill=YELLOW if hot else (METAL if i == 0 else PAPER))
        if hot:
            s.streaks((100, y + 8, 1460, y + 90), step=48, width=3)
        for j, v in enumerate([a, b, c, d]):
            s.text(150 + j * 340, y + 49, v, size=36 if j else 32, anchor="lm",
                   stroke=2 if hot else 0)

    s.line([(110, 740), (1490, 740), ], width=9)
    s.text(110, 785, "GPT-4o 从 78 到 95，17 个点", size=40)
    s.text(110, 860, "小模型提升更明显", size=36)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(2207)
    s.text(110, 55, "推理模型不需要这一招", size=48)

    s.box(110, 150, 1490, 360, r=20, width=10, fill=PAPER)
    s.text(800, 205, "o3 · o4-mini · DeepSeek R1", size=42, anchor="mm")
    s.text(800, 290, "内部已经跑过思维链", size=38, anchor="mm")

    s.line([(110, 430), (1490, 430)], width=9)
    s.text(110, 475, "再加「一步步思考」：", size=40)
    s.cross(150, 570, r=24, width=12)
    s.text(215, 570, "多余", size=42, anchor="lm")
    s.cross(150, 680, r=24, width=12)
    s.text(215, 680, "有时帮倒忙", size=42, anchor="lm")

    s.text(110, 790, "先问：这是推理模型吗？", size=44)
    s.text(110, 870, "这一条能省不少无效 token", size=38)
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(2208)
    s.text(110, 55, "自洽性：多采样再表决", size=48)

    s.box(110, 140, 1490, 230, r=16, width=10, fill=PAPER)
    s.text(800, 185, "48 个苹果，周一卖 1/3，周二卖 1/4", size=34, anchor="mm")

    paths = [("24", YELLOW), ("24", YELLOW), ("24", YELLOW), ("27", METAL), ("24", YELLOW)]
    for i, (ans, fill) in enumerate(paths):
        x = 130 + i * 275
        s.arrow(800, 240, x + 110, 300, width=8)
        s.box(x, 310, x + 220, 460, r=16, width=10, fill=fill)
        if fill == YELLOW:
            s.streaks((x + 10, 320, x + 210, 450), step=42, width=3)
        s.text(x + 110, 385, ans, size=48, anchor="mm", stroke=2 if fill == YELLOW else 0)

    s.box(400, 520, 1100, 640, r=18, width=11, fill=YELLOW)
    s.streaks((410, 530, 1090, 630), step=52, width=3)
    s.text(750, 580, "24 得 4 票 → 最终 24", size=42, anchor="mm", stroke=2)

    s.text(110, 700, "单条路径可能出错", size=40)
    s.text(110, 780, "采样五条，错误相互抵消", size=42)
    s.text(110, 860, "代价是五倍 token", size=36)
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(2209)
    s.text(110, 55, "思维树：探索再剪枝", size=50)

    s.box(680, 130, 1120, 220, r=16, width=10, fill=PAPER)
    s.text(900, 175, "问题", size=36, anchor="mm")

    layer1 = [(280, "想法 A"), (800, "想法 B")]
    for x, name in layer1:
        s.arrow(900, 230, x + 140, 290, width=8)
        s.box(x, 300, x + 280, 410, r=14, width=9, fill=METAL)
        s.text(x + 140, 355, name, size=34, anchor="mm")

    layer2 = [(200, "A1", YELLOW), (480, "A2", PAPER), (720, "B1", PAPER), (1000, "B2", YELLOW)]
    for x, name, fill in layer2:
        parent = 280 if name.startswith("A") else 800
        s.arrow(parent + 140, 420, x + 110, 470, width=7)
        s.box(x, 480, x + 220, 600, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((x + 8, 488, x + 212, 592), step=38, width=3)
        s.text(x + 110, 540, name, size=36, anchor="mm", stroke=2 if fill == YELLOW else 0)

    s.text(110, 670, "每层生成候选，打分，剪掉差的", size=40)
    s.text(110, 750, "像人在草稿纸上涂改", size=42)
    s.text(110, 830, "成本更高：每个分支一次调用", size=36)
    s.save("p09")


# ---------------------------------------------------------------- p10
def p10():
    s = Sheet(2210)
    s.text(110, 55, "什么时候帮倒忙", size=50)

    s.box(110, 150, 730, 530, r=20, width=10, fill=PAPER)
    s.text(420, 205, "别用", size=44, anchor="mm")
    for i, t in enumerate(["事实回忆", "单步分类", "速度优先"]):
        y = 300 + i * 75
        s.cross(180, y, r=20, width=10)
        s.text(240, y, t, size=36, anchor="lm")

    s.box(790, 150, 1490, 530, r=20, width=10, fill=YELLOW)
    s.streaks((800, 160, 1480, 520), step=54, width=3)
    s.text(1140, 205, "该用", size=44, anchor="mm", stroke=2)
    for i, t in enumerate(["多步算术", "符号推理", "要展示过程"]):
        y = 300 + i * 75
        s.check(860, y, r=20, width=10)
        s.text(920, y, t, size=36, anchor="lm", stroke=2)

    s.line([(110, 600), (1490, 600)], width=9)
    s.text(110, 645, "每次多 50 到 200 个 token", size=42)
    s.text(110, 730, "一天百万次调用，成本翻倍", size=40)
    s.text(110, 810, "算完这笔账再决定", size=38)
    s.save("p10")


# ---------------------------------------------------------------- p11
def p11():
    s = Sheet(2211)
    s.text(110, 55, "三种策略的成本", size=50)

    rows = [("策略", "调用", "token", "准确率"),
            ("零样本", "1", "1x", "78%"),
            ("零样本 CoT", "1", "3x", "91%"),
            ("少样本 CoT", "1", "5x", "95%"),
            ("自洽性 x5", "5", "15x", "96%")]
    for i, (a, b, c, d) in enumerate(rows):
        y = 150 + i * 115
        hot = i == 3
        s.box(90, y, 1470, y + 98, r=14, width=9,
              fill=YELLOW if hot else (METAL if i == 0 else PAPER))
        if hot:
            s.streaks((100, y + 8, 1460, y + 90), step=48, width=3)
        for j, v in enumerate([a, b, c, d]):
            s.text(150 + j * 340, y + 49, v, size=36 if j else 32, anchor="lm",
                   stroke=2 if hot else 0)

    s.line([(110, 740), (1490, 740), ], width=9)
    s.text(110, 785, "少样本 CoT 是性价比拐点", size=42)
    s.text(110, 865, "5 倍 token 换 17 个点", size=38)
    s.save("p11")


# ---------------------------------------------------------------- p12
def p12():
    s = Sheet(2212)
    s.text(110, 55, "加思维链，赚还是亏？", size=50)

    opts = [("多步推理", "加，提升明显", YELLOW),
            ("简单分类", "不加，纯浪费", PAPER),
            ("推理模型", "不加，它想过了", PAPER)]
    for i, (name, note, fill) in enumerate(opts):
        y = 170 + i * 155
        s.box(110, y, 1490, y + 130, r=18, width=10, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 122), step=50, width=3)
        s.text(200, y + 65, name, size=42, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(760, y + 65, note, size=34, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.text(110, 700, "判断标准：任务是几步", size=44)
    s.text(110, 790, "两步以上，通常划算", size=40)

    s.box(110, 850, 1490, 930, r=14, width=9, fill=PAPER)
    s.text(800, 890, "下一集：结构化输出", size=34, anchor="mm")
    s.save("p12")


# ---------------------------------------------------------------- cover (大画布 1920x1080)
def cover():
    base = Image.new("RGB", (1920, 1080), PAPER)
    d = ImageDraw.Draw(base)
    title_font = ImageFont.truetype(FONT, 112)
    sub_font = ImageFont.truetype(FONT, 62)
    meta_font = ImageFont.truetype(FONT, 32)
    d.text((120, 160), "加五个字", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((120, 300), "78% → 91%", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((120, 460), "思维链为什么管用", font=sub_font, fill=INK)
    d.rectangle([120, 570, 700, 580], fill=INK)
    d.text((120, 610), "11-02 · LLM Engineering", font=meta_font, fill=INK)
    art = Image.open(OUT / "p01.png").convert("RGB")
    art = art.resize((1040, 585), Image.LANCZOS)
    base.paste(art, (800, 400))
    base.save(OUT / "cover.png")
    print("wrote", OUT / "cover.png")


if __name__ == "__main__":
    for fn in (cover, p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12):
        fn()
