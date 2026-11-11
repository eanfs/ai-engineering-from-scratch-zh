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
    s = Sheet(1401)
    s.text(110, 55, "十三课拆开学，拼起来会得到什么？", size=44)
    for i in range(13):
        x = 130 + (i % 7) * 190
        y = 170 + (i // 7) * 130
        s.box(x, y, x + 160, y + 105, r=10, width=7, fill=METAL)
        s.text(x + 80, y + 52, f"第{i+1}课", size=22, anchor="mm")
    s.arrow(760, 400, 760, 470, width=9)
    s.box(400, 490, 1120, 640, r=16, width=10, fill=YELLOW)
    s.streaks((410, 500, 1110, 630), step=48, width=2)
    s.text(760, 550, "一个完整的 Transformer", size=36, anchor="mm", stroke=2)
    s.text(760, 605, "八十一万参数，六分钟训完", size=26, anchor="mm", stroke=2)
    s.line([(110, 690), (1490, 690)], width=6)
    s.text(110, 730, "还是个会模仿莎士比亚的模型", size=38)
    s.text(110, 805, "这就是收官项目", size=34)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(1402)
    s.text(110, 70, "从零构建 Transformer", size=60)
    s.text(110, 160, "阶段 7 · 第 14 课 · 收官项目", size=32)
    s.line([(110, 235), (1490, 235)], width=9)
    s.text(110, 285, "也叫 nanoGPT", size=36)
    s.box(110, 360, 780, 620, r=16, width=9, fill=PAPER)
    s.text(445, 400, "不原创", size=32, anchor="mm")
    s.text(445, 475, "Karpathy 的教程是参考实现", size=24, anchor="mm")
    s.text(445, 555, "但每个人都该写一遍", size=26, anchor="mm")
    s.box(820, 360, 1490, 620, r=16, width=9, fill=YELLOW)
    s.streaks((830, 370, 1480, 610), step=46, width=2)
    s.text(1155, 400, "但它真实", size=32, anchor="mm", stroke=2)
    s.text(1155, 475, "同一条代码路径，放大就是前沿预训练", size=24, anchor="mm", stroke=2)
    s.text(1155, 555, "不是玩具", size=26, anchor="mm", stroke=2)
    s.text(800, 700, "它读莎士比亚，然后写新的莎士比亚", size=36, anchor="mm")
    s.text(800, 790, "小到能在笔记本上十分钟跑完", size=30, anchor="mm")
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(1403)
    s.text(110, 55, "架构全景：从 token 到概率", size=44)

    items = [("输入 token", "（批次 × 长度）", PAPER),
             ("词嵌入 + 位置嵌入", "第 4 课", METAL),
             ("Block × L", "归一化 + 注意力 + 前馈", YELLOW),
             ("最终归一化", "第 5 课", METAL),
             ("输出头（绑定嵌入）", "第 7 课", PAPER),
             ("logits", "每个词一个分数", PAPER)]
    for i, (name, note, fill) in enumerate(items):
        y = 130 + i * 118
        s.box(240, y, 1360, y + 96, r=12, width=8, fill=fill)
        if fill == YELLOW:
            s.streaks((250, y + 8, 1350, y + 88), step=48, width=2)
        s.text(320, y + 48, name, size=30, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(1160, y + 48, note, size=24, anchor="lm", stroke=2 if fill == YELLOW else 0)
        if i < len(items) - 1:
            s.arrow(800, y + 96, 800, y + 118, width=7)
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(1404)
    s.text(110, 55, "每个零件都来自前面某一课", size=42)
    rows = [("注意力", "第 3 课"), ("多头拆分", "第 10 课"), ("因果掩码", "第 7 课"),
            ("归一化 / 前馈", "第 5 课"), ("位置编码", "第 4 课"), ("嵌入", "第 4 课")]
    for i, (a, b) in enumerate(rows):
        x = 130 + (i % 2) * 690
        y = 160 + (i // 2) * 150
        s.box(x, y, x + 620, y + 120, r=14, width=8, fill=PAPER)
        s.text(x + 40, y + 60, a, size=32, anchor="lm")
        s.text(x + 560, y + 60, b, size=26, anchor="rm")

    s.line([(110, 640), (1490, 640)], width=6)
    s.text(110, 675, "没有新的东西，全是已知零件的重新装配", size=34)
    s.text(110, 745, "这正是这一课的意义：验证你真的理解了每一块", size=32)
    s.text(110, 815, "任何一块没吃透，模型都训不起来", size=30)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(1405)
    s.text(110, 55, "数据：一兆莎士比亚，六十五个字", size=42)

    s.box(110, 150, 1490, 330, r=14, width=9, fill=PAPER)
    s.text(160, 195, "语料：tinyshakespeare.txt", size=30)
    s.text(160, 255, "约 1.1 MB 文本，2015 年以来的标准玩具语料", size=26)
    s.text(160, 305, "每个字符语言模型教程都用它", size=24)

    s.text(110, 380, "字符级分词：", size=30)
    s.box(140, 440, 1460, 540, r=12, width=8, fill=YELLOW)
    s.streaks((150, 450, 1450, 530), step=44, width=2)
    s.text(180, 490, "abcdefg...ROMEO:", size=28, anchor="lm", stroke=2)
    s.text(900, 490, "去重后 65 个字符", size=28, anchor="lm", stroke=2)

    s.line([(110, 590), (1490, 590)], width=6)
    s.text(110, 625, "词表只有 65，不需要 BPE，不需要分词器", size=32)
    s.text(110, 695, "省掉了现代模型最麻烦的一整层工程", size=30)
    s.text(110, 765, "代价是词表太小，表达效率低", size=30)
    s.text(110, 835, "但对演示原理来说刚好", size=28)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(1406)
    s.text(110, 55, "模型规模：只要八十一万参数", size=42)

    rows = [("配置", "词表", "层", "头", "维度", "参数量", False),
            ("nano", "65", "4", "4", "128", "81 万", True),
            ("mini", "65", "6", "6", "192", "269 万", False),
            ("small", "65", "12", "12", "384", "2133 万", False),
            ("base", "50257", "12", "12", "768", "1.24 亿", False)]
    for i, (a, b, c, d, e, f, hot) in enumerate(rows):
        y = 150 + i * 85
        s.box(90, y, 1470, y + 72, r=10, width=7, fill=YELLOW if hot else PAPER)
        if hot:
            s.streaks((100, y + 8, 1460, y + 64), step=44, width=2)
        for j, v in enumerate([a, b, c, d, e, f]):
            s.text(130 + j * 225, y + 36, v, size=26, anchor="lm",
                   stroke=2 if hot else 0)

    s.line([(110, 600), (1490, 600)], width=6)
    s.text(110, 635, "八十一万参数，是大模型的万分之六", size=32)
    s.text(110, 705, "但它在笔记本上六分钟就能训完", size=32)
    s.text(110, 775, "代码路径完全一样，只是规模不同", size=30)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(1407)
    s.text(110, 55, "训练循环：四步，重复两千次", size=42)

    steps = [("1  取批次", "长度 256 的窗口，随机采样", PAPER),
             ("2  前向", "算 logits，错位一格算交叉熵", PAPER),
             ("3  反向", "求梯度，裁剪范数到 1.0", PAPER),
             ("4  更新", "AdamW + 余弦学习率", YELLOW)]
    for i, (name, note, fill) in enumerate(steps):
        y = 140 + i * 145
        s.box(130, y, 1470, y + 115, r=12, width=8, fill=fill)
        if fill == YELLOW:
            s.streaks((140, y + 8, 1460, y + 107), step=46, width=2)
        s.text(180, y + 58, name, size=32, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(560, y + 58, note, size=26, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.text(800, 760, "循环重复两千次，大约六分钟", size=32, anchor="mm")
    s.text(800, 830, "这就是一个语言模型的全部训练过程", size=30, anchor="mm")
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(1408)
    s.text(110, 55, "损失从 4.2 降到 1.5", size=44)

    base = 620
    s.line([(180, base), (1420, base)], width=9)
    s.line([(180, base), (180, 180)], width=9)
    s.text(180, 720, "第 0 步", size=24, anchor="mt")
    s.text(1300, 720, "第 2000 步", size=24, anchor="mt")

    pts = [(180, 220), (330, 330), (480, 400), (640, 450), (800, 483),
           (980, 508), (1160, 525), (1340, 537)]
    for i in range(len(pts) - 1):
        s.line([pts[i], pts[i + 1]], width=8, fill=INK)
    for x, y in pts:
        s.circle(x, y, 9, width=6, fill=YELLOW)

    s.text(250, 285, "4.2（瞎猜）", size=26)
    s.text(1150, 470, "1.5", size=30)

    s.line([(110, 750), (1490, 750)], width=6)
    s.text(110, 785, "验证损失和训练损失贴得很近", size=32)
    s.text(110, 855, "这个规模、这个预算下没有过拟合", size=30)
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(1409)
    s.text(110, 55, "训完之后，它开始写莎士比亚", size=42)

    s.box(110, 150, 1490, 560, r=16, width=9, fill=PAPER)
    s.text(160, 200, "ROMEO:", size=32)
    lines = ["Away and mild will not thy friend,",
             "that thou shalt wit:",
             "The chief that well shame and hath",
             "been his friends,"]
    for i, ln in enumerate(lines):
        s.text(160, 270 + i * 55, ln, size=28)

    s.line([(110, 610), (1490, 610)], width=6)
    s.text(110, 645, "有古英语的词、有换行、有专名", size=32)
    s.text(110, 715, "它不是莎士比亚，但语法结构是对的", size=32)
    s.text(110, 785, "对八十一万参数、六分钟训练来说，这是明确的胜利", size=30)
    s.save("p09")


# ---------------------------------------------------------------- p10
def p10():
    s = Sheet(1410)
    s.text(110, 55, "三个扩展，把它推向真东西", size=42)

    exts = [("1  换分词器", "BPE 把词表从 65 扩到 5 万", "第 4 课的知识"),
            ("2  换大语料", "1.25 亿参数训 100 亿 token，一张 A100 一天", "需要更多算力"),
            ("3  加推理优化", "RoPE + KV 缓存 + Flash Attention", "第 12 课的知识")]
    for i, (name, note, tag) in enumerate(exts):
        y = 150 + i * 190
        s.box(110, y, 1490, y + 160, r=14, width=9, fill=YELLOW if i == 2 else PAPER)
        if i == 2:
            s.streaks((120, y + 8, 1480, y + 152), step=48, width=2)
        s.text(160, y + 55, name, size=34, anchor="lm", stroke=2 if i == 2 else 0)
        s.text(160, y + 115, note, size=26, anchor="lm", stroke=2 if i == 2 else 0)
        s.text(1420, y + 55, tag, size=22, anchor="rm", stroke=2 if i == 2 else 0)

    s.text(800, 790, "做完这三步，你会得到一个能流畅写英语的 1.25 亿参数模型", size=26, anchor="mm")
    s.text(800, 850, "不是前沿模型，但代码路径一模一样", size=26, anchor="mm")
    s.save("p10")


# ---------------------------------------------------------------- p11
def p11():
    s = Sheet(1411)
    s.text(110, 55, "同一套代码，参数量差 150 倍", size=42)

    bars = [("nano", 81, "81 万"), ("mini", 269, "269 万"),
            ("small", 2133, "2133 万"), ("base", 12400, "1.24 亿")]
    base = 640
    s.line([(160, base), (1440, base)], width=9)
    for i, (name, val, label) in enumerate(bars):
        x = 320 + i * 300
        h = int((val ** 0.42) / (12400 ** 0.42) * 380)
        h = max(h, 30)
        fill = YELLOW if i == 3 else METAL
        s.box(x - 100, base - h, x + 100, base, r=10, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((x - 90, base - h + 12, x + 90, base - 12), step=38, width=2)
        s.text(x, base - h - 38, label, size=26, anchor="mm",
               stroke=2 if fill == YELLOW else 0)
        s.text(x, base + 28, name, size=26, anchor="mt")

    s.line([(110, 720), (1490, 720)], width=6)
    s.text(110, 755, "从八十一万到一亿两千四百万，只改配置", size=32)
    s.text(110, 825, "Karpathy、EleutherAI 训研究模型走的就是这条路径", size=28)
    s.save("p11")


# ---------------------------------------------------------------- p12
def p12():
    s = Sheet(1412)
    s.text(110, 55, "给你一台笔记本，你最想加哪个能力？", size=42)

    opts = [("换分词器", "词表大一倍，表达效率高", PAPER),
            ("加 RoPE", "位置编码更灵活，能外推", PAPER),
            ("上 KV 缓存", "生成快 5 到 20 倍", YELLOW)]
    for i, (name, note, fill) in enumerate(opts):
        y = 170 + i * 150
        s.box(110, y, 1490, y + 120, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 112), step=46, width=2)
        s.text(180, y + 60, name, size=34, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(640, y + 60, note, size=26, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.line([(110, 640), (1490, 640)], width=6)
    s.text(110, 675, "三个都能加，但顺序有讲究", size=32)
    s.text(110, 745, "先换分词器，再上 RoPE，最后加 KV 缓存", size=30)

    s.box(110, 810, 1490, 870, r=12, width=8, fill=PAPER)
    s.text(800, 840, "下一集：注意力变体", size=28, anchor="mm")
    s.save("p12")


# ---------------------------------------------------------------- cover
def cover():
    s = Sheet(1400)
    s.text(110, 75, "十三课拼起来，能训出什么？", size=50)
    s.text(110, 165, "从零构建 Transformer · 阶段 7 · 第 14 课", size=28)
    s.line([(110, 235), (1490, 235)], width=9)

    for i in range(7):
        x = 130 + i * 195
        fill = YELLOW if i == 3 else METAL
        s.box(x, 280, x + 165, 380, r=10, width=7, fill=fill)
        if fill == YELLOW:
            s.streaks((x + 6, 286, x + 159, 374), step=26, width=2)

    s.box(240, 430, 1360, 560, r=16, width=9, fill=PAPER)
    s.text(800, 480, "81 万参数 · 6 分钟 · 笔记本", size=32, anchor="mm")
    s.text(800, 530, "损失 4.2 → 1.5", size=28, anchor="mm")

    s.box(110, 610, 1490, 730, r=14, width=9, fill=YELLOW)
    s.streaks((120, 620, 1480, 720), step=48, width=2)
    s.text(400, 670, "ROMEO:", size=30, anchor="lm", stroke=2)
    s.text(620, 670, "Away and mild will not thy friend", size=26, anchor="lm", stroke=2)

    s.text(110, 790, "它真的会写莎士比亚", size=34)
    s.save("cover")


if __name__ == "__main__":
    for fn in (cover, p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12):
        fn()
