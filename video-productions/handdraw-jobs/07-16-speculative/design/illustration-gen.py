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
    s = Sheet(1601)
    s.text(110, 55, "一次前向，凭什么能出五个词？", size=44)
    s.box(110, 160, 700, 400, r=16, width=9, fill=PAPER)
    s.text(405, 205, "直接生成", size=34, anchor="mm")
    for i in range(5):
        s.box(160 + i * 100, 260, 240 + i * 100, 340, r=8, width=7, fill=METAL)
        s.text(200 + i * 100, 300, "1", size=22, anchor="mm")
    s.text(405, 375, "5 次前向 → 5 个词", size=26, anchor="mm")

    s.box(760, 160, 1490, 400, r=16, width=9, fill=YELLOW)
    s.streaks((770, 170, 1480, 390), step=46, width=2)
    s.text(1125, 205, "投机解码", size=34, anchor="mm", stroke=2)
    for i in range(5):
        s.box(810 + i * 100, 260, 890 + i * 100, 340, r=8, width=7, fill=PAPER)
        s.text(850 + i * 100, 300, "1", size=22, anchor="mm")
    s.text(1125, 375, "1 次前向 → 最多 5 个词", size=26, anchor="mm", stroke=2)

    s.line([(110, 470), (1490, 470)], width=6)
    s.text(110, 510, "大模型生成一个词，要跑一次完整前向", size=34)
    s.text(110, 580, "如果能一次前向出五个，速度就快五倍", size=34)
    s.text(110, 655, "这就是投机解码", size=38)
    s.text(110, 730, "而且它的输出分布，和大模型自己生成完全一样", size=28)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(1602)
    s.text(110, 70, "投机解码", size=62)
    s.text(110, 165, "阶段 7 · 第 16 课", size=34)
    s.line([(110, 240), (1490, 240)], width=9)
    s.text(110, 290, "自回归解码的瓶颈是串行：", size=36)
    s.box(110, 370, 1490, 470, r=14, width=9, fill=YELLOW)
    s.streaks((120, 380, 1480, 460), step=44, width=2)
    s.text(800, 420, "每个词都要等上一个词算完", size=40, anchor="mm", stroke=2)

    s.text(110, 520, "投机解码的思路：", size=34)
    rows = [("草稿", "廉价模型先猜 N 个词"),
            ("验证", "昂贵模型一次前向验证全部"),
            ("接受", "对了就用，错了重来")]
    for i, (a, b) in enumerate(rows):
        y = 590 + i * 90
        s.box(110, y, 1490, y + 76, r=12, width=7, fill=PAPER)
        s.text(160, y + 38, a, size=30, anchor="lm")
        s.text(400, y + 38, b, size=28, anchor="lm")
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(1603)
    s.text(110, 55, "先算一笔账", size=44)

    s.text(110, 140, "70B 模型：每个词约 30 毫秒", size=32)
    s.text(110, 210, "3B 草稿模型：每个词约 3 毫秒", size=32)

    s.box(110, 290, 730, 520, r=16, width=9, fill=PAPER)
    s.text(420, 330, "直接生成 5 个词", size=30, anchor="mm")
    s.text(420, 400, "5 × 30 ms", size=40, anchor="mm")
    s.text(420, 470, "= 150 ms", size=36, anchor="mm")

    s.box(790, 290, 1490, 520, r=16, width=9, fill=YELLOW)
    s.streaks((800, 300, 1480, 510), step=48, width=2)
    s.text(1140, 330, "草稿 + 一次验证", size=30, anchor="mm", stroke=2)
    s.text(1140, 400, "5 × 3 + 30 ms", size=40, anchor="mm", stroke=2)
    s.text(1140, 470, "= 45 ms", size=36, anchor="mm", stroke=2)

    s.line([(110, 570), (1490, 570)], width=6)
    s.text(110, 605, "快了 3.3 倍", size=44)
    s.text(110, 690, "代价是多一份草稿模型的显存", size=30)
    s.text(110, 760, "而且必须保证输出分布不变", size=32)
    s.text(110, 830, "否则就是拿质量换速度", size=30)
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(1604)
    s.text(110, 55, "三步：起草、验证、接受", size=44)

    steps = [("1  起草", "草稿模型自回归提出 5 个词，带各自概率", PAPER),
             ("2  验证", "大模型对整段跑一次前向，得到自己的概率", PAPER),
             ("3  接受", "从左到右逐个判断，遇到拒绝就截断", YELLOW)]
    for i, (name, note, fill) in enumerate(steps):
        y = 140 + i * 150
        s.box(110, y, 1490, y + 120, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 112), step=46, width=2)
        s.text(160, y + 40, name, size=32, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(160, y + 90, note, size=25, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.line([(110, 630), (1490, 630)], width=6)
    s.text(110, 665, "关键在于第三步：怎么判断接受", size=34)
    s.text(110, 735, "以及被拒绝之后，怎么保证分布不变", size=32)
    s.text(110, 805, "这是整篇论文最漂亮的地方", size=30)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(1605)
    s.text(110, 55, "接受规则：概率之比的较小值", size=42)

    s.box(110, 150, 1490, 280, r=14, width=9, fill=YELLOW)
    s.streaks((120, 160, 1480, 270), step=46, width=2)
    s.text(800, 215, "接受概率 = min( 1, q(词) / p(词) )", size=38, anchor="mm", stroke=2)

    s.text(110, 330, "两种情形：", size=32)
    s.box(110, 390, 730, 600, r=14, width=9, fill=PAPER)
    s.text(420, 430, "大模型概率更高", size=30, anchor="mm")
    s.text(420, 500, "q > p", size=32, anchor="mm")
    s.text(420, 560, "接受概率 = 1，直接收", size=26, anchor="mm")
    s.check(180, 500, r=20, width=8)

    s.box(790, 390, 1490, 600, r=14, width=9, fill=PAPER)
    s.text(1140, 430, "草稿概率更高", size=30, anchor="mm")
    s.text(1140, 500, "p > q", size=32, anchor="mm")
    s.text(1140, 560, "按 q/p 打折接受", size=26, anchor="mm")
    s.cross(860, 500, r=20, width=8)

    s.line([(110, 660), (1490, 660)], width=6)
    s.text(110, 695, "一旦拒绝，后面的草稿全部丢弃", size=32)
    s.text(110, 765, "但被拒绝的位置不是简单重来", size=32)
    s.text(110, 835, "而是从残差分布里重采样 —— 下一节讲", size=30)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(1606)
    s.text(110, 55, "那个数学洞见：残差分布", size=42)

    s.box(110, 150, 1490, 260, r=14, width=9, fill=PAPER)
    s.text(800, 205, "残差 = max( 0, q - p )", size=40, anchor="mm")

    s.text(110, 310, "为什么这样能保证分布不变：", size=32)
    s.text(110, 390, "接受的部分，贡献了 min(p, q)", size=30)
    s.text(110, 460, "拒绝的部分，从残差里补回来", size=30)
    s.text(110, 530, "两者相加，正好等于大模型的 q", size=30)

    s.box(110, 600, 1490, 720, r=14, width=9, fill=YELLOW)
    s.streaks((120, 610, 1480, 710), step=48, width=2)
    s.text(800, 660, "所以输出分布 = 大模型自己生成", size=36, anchor="mm", stroke=2)

    s.text(110, 770, "这不是近似，是严格的数学等价", size=32)
    s.text(110, 840, "没有质量损失，只是更快", size=34)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(1607)
    s.text(110, 55, "实测：五万个样本，分布一致", size=42)

    s.text(110, 125, "验证器概率分布：", size=26)
    qs = [0.350, 0.200, 0.150, 0.100, 0.080, 0.060, 0.040, 0.020]
    base = 470
    s.line([(160, base), (1400, base)], width=8)
    for i, q in enumerate(qs):
        x = 220 + i * 150
        h = int(q * 480)
        s.box(x - 45, base - h, x + 45, base, r=6, width=6, fill=METAL)
        s.text(x, base + 26, f"w{i}", size=18, anchor="mt")

    s.box(110, 530, 1490, 650, r=14, width=9, fill=PAPER)
    s.text(150, 565, "投机解码计数：17515  10063  7536  4931  3991 ...", size=22)
    s.text(150, 615, "直接采样计数：17526   9940  7610  4891  4037 ...", size=22)

    s.box(140, 690, 1460, 770, r=12, width=9, fill=YELLOW)
    s.streaks((150, 700, 1450, 760), step=46, width=2)
    s.text(800, 730, "卡方 = 4.64，自由度 7 → 分布一致", size=32, anchor="mm", stroke=2)

    s.text(110, 810, "结论：投机解码的输出和大模型直出一模一样，没有质量代价", size=26)
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(1608)
    s.text(110, 55, "接受率决定一切", size=44)

    rows = [("KL 散度", "接受率 α"),
            ("0.002", "0.980"),
            ("0.207", "0.915"),
            ("0.850", "0.878"),
            ("1.864", "0.798"),
            ("4.577", "0.485"),
            ("5.905", "0.478")]
    for i, (a, b) in enumerate(rows):
        y = 140 + i * 88
        hot = i in (1, 6)
        s.box(140, y, 1400, y + 74, r=10, width=7,
              fill=YELLOW if hot else PAPER)
        if hot:
            s.streaks((150, y + 8, 1390, y + 66), step=44, width=2)
        s.text(200, y + 37, a, size=28, anchor="lm", stroke=2 if hot else 0)
        s.text(900, y + 37, b, size=28, anchor="lm", stroke=2 if hot else 0)

    s.line([(110, 780), (1490, 780)], width=6)
    s.text(110, 815, "草稿越像验证器，接受率越高", size=32)
    s.text(110, 875, "差得太远时，加速几乎归零", size=28)
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(1609)
    s.text(110, 55, "每次验证能出几个词", size=44)

    rows = [("α", "N=1", "N=5", "N=10"),
            ("0.30", "1.30", "1.43", "1.43"),
            ("0.50", "1.50", "1.97", "2.00"),
            ("0.70", "1.70", "2.94", "3.27"),
            ("0.85", "1.85", "4.15", "5.55"),
            ("0.95", "1.95", "5.30", "8.62")]
    for i, (a, b, c, d) in enumerate(rows):
        y = 150 + i * 90
        hot = i == 4
        s.box(140, y, 1420, y + 76, r=10, width=7,
              fill=YELLOW if hot else (METAL if i == 0 else PAPER))
        if hot:
            s.streaks((150, y + 8, 1410, y + 68), step=44, width=2)
        for j, v in enumerate([a, b, c, d]):
            s.text(220 + j * 300, y + 38, v, size=28, anchor="lm",
                   stroke=2 if hot else 0)

    s.line([(110, 720), (1490, 720)], width=6)
    s.text(110, 755, "接受率 0.85、草稿 5 个：每次验证出 4.15 个词", size=30)
    s.text(110, 825, "也就是大模型前向次数少四倍", size=30)
    s.text(110, 880, "接受率 0.5 时就只有 2 个词，加速减半", size=26)
    s.save("p09")


# ---------------------------------------------------------------- p10
def p10():
    s = Sheet(1610)
    s.text(110, 55, "四类实现方案", size=44)

    rows = [("朴素投机", "独立草稿模型 + 验证器", "同族效果最好"),
            ("Medusa", "验证器上挂多个预测头", "不需要第二个模型"),
            ("EAGLE", "复用验证器隐藏状态", "典型 3 到 4 倍"),
            ("前瞻解码", "Jacobi 迭代，自投机", "无需草稿模型")]
    for i, (a, b, c) in enumerate(rows):
        y = 150 + i * 145
        hot = i == 2
        s.box(90, y, 1470, y + 120, r=14, width=8,
              fill=YELLOW if hot else PAPER)
        if hot:
            s.streaks((100, y + 8, 1460, y + 112), step=46, width=2)
        s.text(140, y + 40, a, size=30, anchor="lm", stroke=2 if hot else 0)
        s.text(140, y + 88, b, size=24, anchor="lm", stroke=2 if hot else 0)
        s.text(1430, y + 40, c, size=22, anchor="rm", stroke=2 if hot else 0)

    s.text(800, 790, "2026 年生产推理栈默认都开", size=30, anchor="mm")
    s.text(800, 855, "vLLM、TensorRT-LLM、SGLang、llama.cpp 都支持", size=26, anchor="mm")
    s.save("p10")


# ---------------------------------------------------------------- p11
def p11():
    s = Sheet(1611)
    s.text(110, 55, "什么时候有效，什么时候白干", size=42)

    s.box(110, 150, 730, 620, r=16, width=9, fill=YELLOW)
    s.streaks((120, 160, 720, 610), step=48, width=2)
    s.text(420, 195, "接受率高", size=34, anchor="mm", stroke=2)
    items1 = [("代码补全", "结构可预测"), ("格式化输出", "JSON 模式固定"),
              ("同族草稿", "训练数据接近"), ("贪心解码", "容易匹配")]
    for i, (a, b) in enumerate(items1):
        y = 285 + i * 80
        s.check(178, y, r=16, width=8)
        s.text(215, y, a, size=26, anchor="lm", stroke=2)
        s.text(430, y, b, size=20, anchor="lm", stroke=2)

    s.box(790, 150, 1490, 620, r=16, width=9, fill=PAPER)
    s.text(1140, 195, "接受率低", size=34, anchor="mm")
    items2 = [("自由创作", "下一步太发散"), ("高温采样", "概率分布变平"),
              ("跨族草稿", "差异太大"), ("边缘部署", "草稿也占显存")]
    for i, (a, b) in enumerate(items2):
        y = 285 + i * 80
        s.cross(858, y, r=16, width=8)
        s.text(895, y, a, size=26, anchor="lm")
        s.text(1110, y, b, size=20, anchor="lm")

    s.line([(110, 660), (1490, 660)], width=6)
    s.text(110, 695, "一句话：草稿越像验证器，加速越明显", size=32)
    s.save("p11")


# ---------------------------------------------------------------- p12
def p12():
    s = Sheet(1612)
    s.text(110, 55, "要低延迟，你选独立草稿还是 Medusa？", size=40)

    s.box(110, 170, 730, 520, r=16, width=9, fill=PAPER)
    s.text(420, 215, "独立草稿模型", size=36, anchor="mm")
    s.text(420, 290, "接受率高", size=28, anchor="mm")
    s.text(420, 355, "同族效果最好", size=26, anchor="mm")
    s.text(420, 425, "但要额外显存", size=28, anchor="mm")

    s.box(790, 170, 1490, 520, r=16, width=9, fill=YELLOW)
    s.streaks((800, 180, 1480, 510), step=48, width=2)
    s.text(1140, 215, "Medusa / EAGLE", size=36, anchor="mm", stroke=2)
    s.text(1140, 290, "不用第二个模型", size=28, anchor="mm", stroke=2)
    s.text(1140, 355, "复用隐藏状态", size=26, anchor="mm", stroke=2)
    s.text(1140, 425, "要额外微调", size=28, anchor="mm", stroke=2)

    s.line([(110, 570), (1490, 570), ], width=6)
    s.text(110, 605, "显存紧选 Medusa，追求极限速度选同族草稿", size=30)
    s.text(110, 675, "两者都能保住输出分布不变", size=30)

    s.box(110, 750, 1490, 860, r=16, width=8, fill=PAPER)
    s.text(800, 790, "评论区说说你的取舍：省显存，还是省延迟？", size=30, anchor="mm")
    s.text(800, 835, "阶段 7 · 完", size=26, anchor="mm")
    s.save("p12")


# ---------------------------------------------------------------- cover
def cover():
    s = Sheet(1600)
    s.text(110, 75, "一次前向，凭什么出五个词？", size=50)
    s.text(110, 170, "投机解码 · 阶段 7 · 第 16 课", size=28)
    s.line([(110, 240), (1490, 240)], width=9)

    s.text(140, 285, "草稿 5 个", size=26)
    for i in range(5):
        s.box(150 + i * 130, 340, 250 + i * 130, 430, r=8, width=7, fill=METAL)

    s.arrow(830, 385, 900, 385, width=9)

    s.box(930, 320, 1460, 450, r=14, width=9, fill=YELLOW)
    s.streaks((940, 330, 1450, 440), step=46, width=2)
    s.text(1195, 385, "1 次验证全收", size=32, anchor="mm", stroke=2)

    s.box(110, 510, 1490, 620, r=14, width=9, fill=PAPER)
    s.text(800, 565, "30ms × 5 = 150ms  →  3ms × 5 + 30 = 45ms", size=30, anchor="mm")

    s.box(110, 660, 1490, 780, r=14, width=9, fill=PAPER)
    s.text(800, 700, "快 3.3 倍", size=40, anchor="mm")
    s.text(800, 755, "而且输出分布完全不变", size=28, anchor="mm")

    s.text(110, 825, "实测卡方 4.64，自由度 7 —— 分布一致", size=26)
    s.save("cover")


if __name__ == "__main__":
    for fn in (cover, p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12):
        fn()
