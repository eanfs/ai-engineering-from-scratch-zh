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
    s = Sheet(1801)
    s.text(110, 60, "Sora、SD3、Flux 都不是用扩散做的", size=46)
    models = [("Sora", 130), ("Stable Diffusion 3", 420), ("Flux.1", 900)]
    for name, x in models:
        s.box(x, 170, x + 240, 290, r=14, width=9, fill=PAPER)
        s.text(x + 120, 230, name, size=28, anchor="mm")
        s.line([(x + 40, 262), (x + 200, 262)], width=6)
        s.text(x + 120, 320, "不是 DDPM", size=26, anchor="mm", fill=BROWN)

    s.box(130, 390, 1470, 560, r=16, width=10, fill=YELLOW)
    s.streaks((140, 400, 1460, 550), step=50, width=2)
    s.text(800, 450, "它们用流匹配（Flow Matching）", size=40, anchor="mm", stroke=2)
    s.text(800, 520, "采样快 4 到 10 倍", size=34, anchor="mm", stroke=2)

    s.line([(110, 610), (1490, 610)], width=6)
    s.text(110, 650, "过去十二年活下来的生成模型，一共五个家族", size=34)
    s.text(110, 725, "选错家族，你会跟数学搏斗好几周", size=32)
    s.text(110, 800, "这一课把五个桶讲清楚", size=36)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(1802)
    s.text(110, 70, "生成模型的五个家族", size=58)
    s.text(110, 165, "阶段 8 · 第 1 课", size=34)
    s.line([(110, 240), (1490, 240)], width=9)
    s.text(110, 285, "所有生成模型只干一件事：", size=34)
    s.box(110, 355, 1490, 450, r=14, width=9, fill=YELLOW)
    s.streaks((120, 365, 1480, 440), step=46, width=2)
    s.text(800, 402, "学着采样出一个分布 p(x)", size=38, anchor="mm", stroke=2)

    s.text(110, 510, "难的是这个分布住在几百万维的空间里：", size=32)
    s.text(110, 590, "一张 512 × 512 的彩色图 = 78.6 万维", size=34)
    s.text(110, 670, "而模型顶多见过一千万个样本", size=32)
    s.text(110, 760, "硬算密度没指望，所以每个模型都是一种妥协", size=32)
    s.text(110, 835, "妥协的方式不同，就成了五个家族", size=34)
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(1803)
    s.text(110, 55, "五个家族，五种妥协", size=44)

    rows = [("1  显式密度·可解", "概率写得出来、算得出来", YELLOW),
            ("2  显式密度·近似", "只算得出下界（ELBO）", PAPER),
            ("3  隐式密度", "不算概率，只学生成器", PAPER),
            ("4  分数 / 连续时间", "学密度的梯度", PAPER),
            ("5  token 自回归", "先量化成离散 token 再建模", PAPER)]
    for i, (name, note, fill) in enumerate(rows):
        y = 140 + i * 118
        s.box(110, y, 1490, y + 96, r=12, width=8, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 88), step=46, width=2)
        s.text(150, y + 32, name, size=28, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(150, y + 70, note, size=24, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.text(800, 800, "记住这个顺序，后面每课都会用到", size=30, anchor="mm")
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(1804)
    s.text(110, 55, "第一桶：显式密度，可解", size=42)
    s.text(110, 130, "把概率拆成一串条件概率的乘积：", size=30)
    s.box(110, 190, 1490, 290, r=12, width=8, fill=YELLOW)
    s.streaks((120, 200, 1480, 280), step=44, width=2)
    s.text(800, 242, "p(x) = p(x1) · p(x2|x1) · p(x3|x1,x2) ...", size=34, anchor="mm", stroke=2)

    s.text(110, 340, "代表模型：", size=30)
    for i, name in enumerate(["GPT", "WaveNet", "PixelCNN", "RealNVP", "Glow"]):
        x = 140 + i * 260
        s.box(x, 400, x + 230, 500, r=10, width=7, fill=PAPER)
        s.text(x + 115, 450, name, size=24, anchor="mm")

    s.line([(110, 560), (1490, 560)], width=6)
    s.text(110, 595, "优点：似然精确，训练损失干净", size=32)
    s.check(140, 660, r=16, width=8)
    s.text(180, 660, "能算任意一点的概率", size=28, anchor="lm")
    s.text(110, 730, "缺点：自回归推理是顺序的，长序列很慢", size=32)
    s.cross(140, 795, r=16, width=8)
    s.text(180, 795, "生成一个词要等上一个词", size=28, anchor="lm")
    s.text(110, 855, "流模型则要求架构可逆，结构受限", size=28)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(1805)
    s.text(110, 55, "第二桶：显式密度，只能近似", size=42)
    s.text(110, 130, "算不出精确概率，就找一个下界来优化：", size=30)
    s.box(110, 190, 1490, 280, r=12, width=8, fill=PAPER)
    s.text(800, 235, "ELBO ≤ log p(x)", size=36, anchor="mm")

    s.box(110, 330, 730, 580, r=14, width=9, fill=PAPER)
    s.text(420, 370, "变分自编码器 VAE", size=30, anchor="mm")
    s.text(420, 440, "编码器 + 解码器", size=26, anchor="mm")
    s.text(420, 510, "2013 年，第一个能用的", size=24, anchor="mm")

    s.box(790, 330, 1490, 580, r=14, width=9, fill=YELLOW)
    s.streaks((800, 340, 1480, 570), step=48, width=2)
    s.text(1140, 370, "扩散模型 DDPM", size=30, anchor="mm", stroke=2)
    s.text(1140, 440, "训练一个去噪器", size=26, anchor="mm", stroke=2)
    s.text(1140, 510, "2020 年，现在是主流骨干", size=24, anchor="mm", stroke=2)

    s.line([(110, 640), (1490, 640)], width=6)
    s.text(110, 675, "扩散本质上也在优化同一个下界", size=32)
    s.text(110, 745, "只是把「一步一步去噪」当成了训练目标", size=30)
    s.text(110, 820, "到 2026 年，扩散仍是图像、视频、3D 的主流", size=28)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(1806)
    s.text(110, 55, "第三桶：隐式密度，干脆不算概率", size=40)

    s.box(110, 150, 570, 400, r=16, width=9, fill=PAPER)
    s.text(340, 195, "生成器 G", size=32, anchor="mm")
    s.text(340, 270, "从噪声造样本", size=26, anchor="mm")
    s.text(340, 340, "一次前向就出图", size=26, anchor="mm")

    s.box(1030, 150, 1490, 400, r=16, width=9, fill=METAL)
    s.text(1260, 195, "判别器 D", size=32, anchor="mm")
    s.text(1260, 270, "分辨真假", size=26, anchor="mm")
    s.text(1260, 340, "训练时和 G 对抗", size=26, anchor="mm")

    s.arrow(600, 275, 1000, 275, width=9)
    s.text(800, 240, "造样本", size=24, anchor="mb")
    s.arrow(1000, 320, 600, 320, width=9)
    s.text(800, 355, "梯度回传", size=24, anchor="mt")

    s.line([(110, 470), (1490, 470)], width=6)
    s.text(110, 505, "GAN：2014 年，推理最快，训练最难", size=34)
    s.check(140, 575, r=16, width=8)
    s.text(180, 575, "一次前向，没有调度、没有 KV 缓存", size=28, anchor="lm")
    s.cross(140, 640, r=16, width=8)
    s.text(180, 640, "训练极不稳定，参数一碰就崩", size=28, anchor="lm")
    s.text(110, 720, "但 StyleGAN 在人脸这种窄领域，到 2026 年仍是顶尖", size=28)
    s.text(110, 800, "因为它把「一次前向」的优势压到了极致", size=30)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(1807)
    s.text(110, 55, "第四桶：不学密度，学密度的梯度", size=42)
    s.box(110, 140, 1490, 240, r=12, width=8, fill=PAPER)
    s.text(800, 190, "分数 = ∇ log p(x)", size=36, anchor="mm")

    s.text(110, 300, "两条路线：", size=30)
    s.box(110, 360, 730, 620, r=14, width=9, fill=PAPER)
    s.text(420, 400, "分数匹配 / SDE", size=28, anchor="mm")
    s.text(420, 470, "2019 年，把扩散推广成连续时间", size=24, anchor="mm")
    s.text(420, 550, "理论上优雅", size=26, anchor="mm")

    s.box(790, 360, 1490, 620, r=14, width=9, fill=YELLOW)
    s.streaks((800, 370, 1480, 610), step=50, width=2)
    s.text(1140, 400, "流匹配", size=30, anchor="mm", stroke=2)
    s.text(1140, 470, "2023 年提出，路径更直", size=24, anchor="mm", stroke=2)
    s.text(1140, 550, "采样快 4 到 10 倍", size=28, anchor="mm", stroke=2)

    s.line([(110, 680), (1490, 680)], width=6)
    s.text(110, 715, "Stable Diffusion 3、Flux、AudioCraft 2 全都用流匹配", size=30)
    s.text(110, 790, "Sora 的视频骨干也是这一路", size=30)
    s.text(110, 860, "这就是为什么 2024 年之后，「扩散」这个词开始不够用了", size=26)
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(1808)
    s.text(110, 55, "第五桶：先量化，再用 token 自回归", size=40)

    steps = [("1  量化", "VQ-VAE 把图像压成离散 token", PAPER),
             ("2  建模", "Transformer 学 token 序列的概率", YELLOW),
             ("3  生成", "采样 token，再解码回图像", PAPER)]
    for i, (name, note, fill) in enumerate(steps):
        y = 150 + i * 150
        s.box(110, y, 1490, y + 120, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 112), step=46, width=2)
        s.text(160, y + 40, name, size=32, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(160, y + 88, note, size=26, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.line([(110, 620), (1490, 620)], width=6)
    s.text(110, 655, "代表模型：Parti、MuseNet、AudioLM、VALL-E", size=30)
    s.text(110, 725, "Sora 的画面分词器也是这一路", size=30)
    s.text(110, 795, "本质是第一桶，只是多加了一个学出来的分词器", size=30)
    s.text(110, 865, "好处是：离散 token 扩展起来比连续值便宜", size=26)
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(1809)
    s.text(110, 55, "实测：能不能回答「这个点概率多大」", size=38)

    rows = [("方法", "能算 p(x)？", "结果"),
            ("直方图（显式）", "能", "0.0180"),
            ("核密度（显式）", "能", "0.0258"),
            ("GAN 式生成器（隐式）", "不能", "只吐样本")]
    for i, (a, b, c) in enumerate(rows):
        y = 150 + i * 95
        hot = i == 3
        s.box(90, y, 1470, y + 80, r=10, width=7,
              fill=YELLOW if hot else (METAL if i == 0 else PAPER))
        if hot:
            s.streaks((100, y + 8, 1460, y + 72), step=44, width=2)
        s.text(140, y + 40, a, size=26, anchor="lm", stroke=2 if hot else 0)
        s.text(800, y + 40, b, size=26, anchor="lm", stroke=2 if hot else 0)
        s.text(1080, y + 40, c, size=26, anchor="lm", stroke=2 if hot else 0)

    s.line([(110, 570), (1490, 570)], width=6)
    s.text(110, 605, "这就是显式和隐式的真正分界", size=34)
    s.text(110, 675, "不是「哪个效果更好」，而是「能不能问概率」", size=30)
    s.text(110, 745, "要算似然、要做密度估计、要算信息量，只能选显式", size=28)

    s.box(110, 800, 1490, 870, r=12, width=8, fill=PAPER)
    s.text(800, 835, "GAN 给不了概率，但它给了速度 —— 这是它的交换", size=28, anchor="mm")
    s.save("p09")


# ---------------------------------------------------------------- p10
def p10():
    s = Sheet(1810)
    s.text(110, 55, "十二年，五个家族的时间线", size=42)

    events = [("2013", "VAE", "第一个能用的深度生成模型"),
              ("2014", "GAN", "隐式密度，样本极锐"),
              ("2020", "DDPM", "扩散变得实用"),
              ("2022", "潜空间扩散", "文生图白菜化"),
              ("2024", "流匹配", "SD3 / Flux 胜出"),
              ("2026", "一步采样", "蒸馏 + 整流流")]
    for i, (year, name, note) in enumerate(events):
        y = 140 + i * 112
        hot = i >= 4
        s.box(110, y, 1490, y + 92, r=10, width=7,
              fill=YELLOW if hot else PAPER)
        if hot:
            s.streaks((120, y + 8, 1480, y + 84), step=44, width=2)
        s.text(150, y + 46, year, size=28, anchor="lm", stroke=2 if hot else 0)
        s.text(320, y + 46, name, size=28, anchor="lm", stroke=2 if hot else 0)
        s.text(700, y + 46, note, size=24, anchor="lm", stroke=2 if hot else 0)

    s.text(800, 850, "最近三年的变化，全在「采样更快」这一件事上", size=26, anchor="mm")
    s.save("p10")


# ---------------------------------------------------------------- p11
def p11():
    s = Sheet(1811)
    s.text(110, 55, "五问分诊法：读任何论文先问这五个", size=38)

    qs = ["建模的是什么？像素、潜变量、token、3D？",
          "密度是显式还是隐式？写没写出 log p(x)？",
          "采样是一次到位还是迭代？",
          "条件是什么？无条件、类别、文本、姿态？",
          "评测用什么？FID、CLIP 分数、人类偏好？"]
    for i, q in enumerate(qs):
        y = 140 + i * 132
        s.box(110, y, 1490, y + 108, r=12, width=8,
              fill=YELLOW if i == 1 else PAPER)
        if i == 1:
            s.streaks((120, y + 8, 1480, y + 100), step=46, width=2)
        s.text(160, y + 54, f"{i+1}", size=32, anchor="lm", stroke=2 if i == 1 else 0)
        s.text(220, y + 54, q, size=26, anchor="lm", stroke=2 if i == 1 else 0)

    s.text(800, 830, "答完这五个，方法章节就不用猜了", size=28, anchor="mm")
    s.save("p11")


# ---------------------------------------------------------------- p12
def p12():
    s = Sheet(1812)
    s.text(110, 55, "Midjourney v7 属于哪一桶？", size=44)

    s.text(110, 140, "三个产品，你来判断：", size=30)
    opts = [("Midjourney v7", "文生图", PAPER),
            ("Runway Gen-3", "文生视频", PAPER),
            ("ElevenLabs", "语音合成", PAPER)]
    for i, (name, note, fill) in enumerate(opts):
        y = 210 + i * 130
        s.box(110, y, 1490, y + 105, r=14, width=9, fill=fill)
        s.text(180, y + 52, name, size=32, anchor="lm")
        s.text(700, y + 52, note, size=26, anchor="lm")

    s.line([(110, 640), (1490, 640)], width=6)
    s.text(110, 675, "提示：先问「密度显式还是隐式」，就能排除一半", size=30)
    s.text(110, 745, "再问「采样一次到位还是迭代」，答案就出来了", size=30)

    s.box(110, 810, 1490, 870, r=12, width=8, fill=PAPER)
    s.text(800, 840, "下一集：变分自编码器", size=28, anchor="mm")
    s.save("p12")


# ---------------------------------------------------------------- cover
def cover():
    s = Sheet(1800)
    s.text(110, 90, "Sora 用的不是扩散？", size=68)
    s.line([(110, 240), (1490, 240)], width=10)
    s.text(110, 300, "SD3 和 Flux 也不是", size=44)

    s.box(110, 420, 1490, 700, r=20, width=11, fill=YELLOW)
    s.streaks((120, 430, 1480, 690), step=56, width=3)
    s.text(800, 520, "流匹配 Flow Matching", size=52, anchor="mm", stroke=2)
    s.text(800, 620, "采样快 4 到 10 倍", size=44, anchor="mm", stroke=2)

    s.text(110, 790, "生成模型的五个家族", size=40)
    s.save("cover")


if __name__ == "__main__":
    for fn in (cover, p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12):
        fn()
