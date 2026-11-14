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
    s.text(110, 60, "加五个字，准确率从 78% 涨到 91%", size=42)
    s.box(110, 170, 1490, 290, r=16, width=10, fill=YELLOW)
    s.streaks((120, 180, 1480, 280), step=50, width=2)
    s.text(800, 230, "Let's think step by step", size=42, anchor="mm", stroke=2)

    s.box(110, 330, 720, 560, r=16, width=10, fill=PAPER)
    s.text(415, 375, "不加这句", size=30, anchor="mm")
    s.text(415, 465, "78%", size=64, anchor="mm")
    s.text(415, 530, "零样本", size=24, anchor="mm")

    s.box(780, 330, 1490, 560, r=16, width=10, fill=YELLOW)
    s.streaks((790, 340, 1480, 550), step=50, width=2)
    s.text(1135, 375, "加上这句", size=30, anchor="mm", stroke=2)
    s.text(1135, 465, "91%", size=64, anchor="mm", stroke=2)
    s.text(1135, 530, "同一个模型，同样的温度", size=24, anchor="mm", stroke=2)

    s.line([(110, 620), (1490, 620)], width=7)
    s.text(110, 660, "唯一的差别是，你给了模型一张草稿纸", size=34)
    s.text(110, 735, "这不是 hack，这就是推理的运作方式", size=32)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(2202)
    s.text(110, 70, "少样本、思维链与思维树", size=54)
    s.text(110, 165, "阶段 11 · 第 2 课", size=34)
    s.line([(110, 240), (1490, 240)], width=9)
    s.text(110, 285, "三句话概括这一课：", size=34)
    rows = [("示例", "被压缩过的指令，比描述更可靠", YELLOW),
            ("思维链", "把中间计算写成 token，延展计算深度", PAPER),
            ("自洽 / 思维树", "多采样、多数表决、探索分支", PAPER)]
    for i, (name, note, fill) in enumerate(rows):
        y = 370 + i * 145
        s.box(110, y, 1490, y + 120, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 112), step=48, width=2)
        s.text(160, y + 42, name, size=30, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(160, y + 90, note, size=24, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.text(800, 850, "告诉模型做什么是提示，教它怎么想是工程", size=28, anchor="mm")
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(2203)
    s.text(110, 55, "少样本什么时候真正管用", size=42)

    s.box(110, 150, 730, 480, r=16, width=9, fill=PAPER)
    s.text(420, 195, "简单任务", size=32, anchor="mm")
    s.text(420, 275, "情感分类", size=26, anchor="mm")
    s.text(420, 345, "差不到 2 个点", size=28, anchor="mm")
    s.text(420, 420, "示例可有可无", size=24, anchor="mm")

    s.box(790, 150, 1490, 480, r=16, width=9, fill=YELLOW)
    s.streaks((800, 160, 1480, 470), step=50, width=2)
    s.text(1140, 195, "复杂任务", size=32, anchor="mm", stroke=2)
    s.text(1140, 275, "多步算术、符号推理", size=26, anchor="mm", stroke=2)
    s.text(1140, 345, "提升 10 到 25 个点", size=28, anchor="mm", stroke=2)
    s.text(1140, 420, "示例几乎是必需的", size=24, anchor="mm", stroke=2)

    s.line([(110, 540), (1490, 540)], width=7)
    s.text(110, 580, "直觉：示例是被压缩过的指令", size=36)
    s.text(110, 655, "与其描述输出格式，不如直接展示格式", size=30)
    s.text(110, 725, "与其解释推理过程，不如直接演示一遍", size=30)
    s.text(110, 800, "模型做模式匹配，比解读抽象指令可靠得多", size=28)
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(2204)
    s.text(110, 55, "示例怎么挑：三条原则", size=44)

    rows = [("1  语义相似", "挑 embedding 空间里离输入最近的", YELLOW),
            ("2  标签多样", "示例要覆盖所有输出类别", PAPER),
            ("3  难度匹配", "匹配目标问题的复杂度", PAPER)]
    for i, (name, note, fill) in enumerate(rows):
        y = 150 + i * 145
        s.box(110, y, 1490, y + 120, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 112), step=48, width=2)
        s.text(160, y + 42, name, size=30, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(160, y + 90, note, size=24, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.line([(110, 600), (1490, 600)], width=7)
    s.text(110, 635, "最优数量：3 到 5 个", size=36)
    s.text(110, 710, "少于 3 个，模型提取不出模式", size=30)
    s.text(110, 780, "多于 5 个，收益递减，还白占上下文", size=30)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(2205)
    s.text(110, 55, "思维链为什么管用：一张草稿纸", size=40)

    s.box(110, 140, 730, 420, r=16, width=9, fill=PAPER)
    s.text(420, 180, "标准提示", size=30, anchor="mm")
    s.text(420, 245, "问题 → 答案", size=28, anchor="mm")
    s.text(420, 320, "所有推理压进", size=24, anchor="mm")
    s.text(420, 365, "一次前向传播", size=24, anchor="mm")

    s.box(790, 140, 1490, 420, r=16, width=9, fill=YELLOW)
    s.streaks((800, 150, 1480, 410), step=50, width=2)
    s.text(1140, 180, "思维链", size=30, anchor="mm", stroke=2)
    steps = ["问题", "先写一步推理", "再写一步", "最后给答案"]
    for i, st in enumerate(steps):
        s.text(1140, 240 + i * 42, st, size=22, anchor="mm", stroke=2)

    s.line([(110, 480), (1490, 480)], width=7)
    s.text(110, 515, "每个推理 token 都成为下一个 token 的上下文", size=30)
    s.text(110, 590, "token 一层层叠加，等于把计算深度延展开", size=30)
    s.text(110, 665, "人类不会一个念头跳完多步问题，transformer 也不会", size=28)
    s.text(110, 745, "逼它写出中间步骤，它才是真的一步步算", size=30)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(2206)
    s.text(110, 55, "实测：GSM8K 上的三级跳", size=42)

    rows = [("模型", "零样本", "+CoT", "+少样本 CoT"),
            ("GPT-4o", "78%", "91%", "95%"),
            ("GPT-5", "94%", "97%", "98%"),
            ("Llama 4 70B", "80%", "89%", "94%"),
            ("DeepSeek-V3.1", "89%", "94%", "96%")]
    for i, (a, b, c, d) in enumerate(rows):
        y = 150 + i * 100
        hot = i == 1
        s.box(90, y, 1470, y + 84, r=10, width=7,
              fill=YELLOW if hot else (METAL if i == 0 else PAPER))
        if hot:
            s.streaks((100, y + 8, 1460, y + 76), step=44, width=2)
        for j, v in enumerate([a, b, c, d]):
            s.text(150 + j * 340, y + 42, v, size=26 if j else 24, anchor="lm",
                   stroke=2 if hot else 0)

    s.line([(110, 660), (1490, 660), ], width=7)
    s.text(110, 695, "GPT-4o 从 78 加到 95，整整 17 个点", size=30)
    s.text(110, 765, "Llama 4 从 80 加到 94，小模型提升更明显", size=28)
    s.text(110, 835, "八千五百道小学数学题，同一套提示策略", size=26)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(2207)
    s.text(110, 55, "但推理模型不需要这一招", size=42)

    s.box(110, 150, 1490, 330, r=16, width=9, fill=PAPER)
    s.text(800, 195, "o3、o4-mini、DeepSeek R1", size=34, anchor="mm")
    s.text(800, 265, "内部已经跑过思维链", size=28, anchor="mm")
    s.text(800, 315, "答案之前先自己想一遍", size=24, anchor="mm")

    s.line([(110, 380), (1490, 380)], width=7)
    s.text(110, 415, "再给它们加「让我们一步步思考」：", size=30)
    s.cross(140, 495, r=18, width=9)
    s.text(185, 495, "多余，因为它们已经做过这件事", size=28, anchor="lm")
    s.cross(140, 570, r=18, width=9)
    s.text(185, 570, "有时帮倒忙，多花 token 还扰乱格式", size=28, anchor="lm")

    s.text(110, 660, "所以第一步是问：我用的是推理模型还是普通模型？", size=30)
    s.text(110, 735, "普通模型加思维链，推理模型直接给任务", size=30)
    s.text(110, 810, "这一条能省掉不少无效 token", size=28)
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(2208)
    s.text(110, 55, "自洽性：多采样，一次表决", size=42)

    s.box(110, 140, 1490, 220, r=12, width=8, fill=PAPER)
    s.text(800, 180, "48 个苹果，周一卖 1/3，周二卖剩余 1/4", size=26, anchor="mm")

    paths = [("路径 1", "24", YELLOW), ("路径 2", "24", YELLOW),
             ("路径 3", "24", YELLOW), ("路径 4", "27", METAL),
             ("路径 5", "24", YELLOW)]
    for i, (name, ans, fill) in enumerate(paths):
        x = 130 + i * 275
        s.arrow(800, 230, x + 110, 300, width=7)
        s.box(x, 310, x + 220, 420, r=12, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((x + 8, 318, x + 212, 412), step=40, width=2)
        s.text(x + 110, 345, name, size=22, anchor="mm", stroke=2 if fill == YELLOW else 0)
        s.text(x + 110, 390, ans, size=32, anchor="mm", stroke=2 if fill == YELLOW else 0)

    s.box(400, 470, 1100, 570, r=14, width=9, fill=YELLOW)
    s.streaks((410, 480, 1090, 560), step=48, width=2)
    s.text(750, 520, "多数表决：24 得 4 票 → 最终 24", size=30, anchor="mm", stroke=2)

    s.text(110, 620, "单条路径可能含推理错误", size=30)
    s.text(110, 690, "采样五条，错误会相互抵消", size=30)
    s.text(110, 765, "代价是五倍的 token，换来更稳的答案", size=28)
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(2209)
    s.text(110, 55, "思维树：探索分支再剪枝", size=44)

    # 简单的树结构
    s.box(620, 130, 980, 200, r=12, width=8, fill=PAPER)
    s.text(800, 165, "问题", size=26, anchor="mm")

    layer1 = [(280, "想法 A"), (620, "想法 B"), (960, "想法 C")]
    for x, name in layer1:
        s.arrow(800, 210, x + 110, 270, width=7)
        s.box(x, 280, x + 220, 360, r=10, width=7, fill=METAL)
        s.text(x + 110, 320, name, size=24, anchor="mm")

    layer2 = [(180, "A1"), (400, "A2"), (620, "B1"), (840, "B2")]
    for x, name in layer2:
        parent = 280 if name.startswith("A") else 620
        s.arrow(parent + 110, 370, x + 90, 420, width=6)
        fill = YELLOW if name in ("A1", "B2") else PAPER
        s.box(x, 430, x + 180, 500, r=10, width=7, fill=fill)
        if fill == YELLOW:
            s.streaks((x + 8, 438, x + 172, 492), step=34, width=2)
        s.text(x + 90, 465, name, size=22, anchor="mm", stroke=2 if fill == YELLOW else 0)

    s.text(110, 560, "每一层生成几个候选，评估打分，剪掉差的分支", size=28)
    s.text(110, 630, "它更像人在草稿纸上涂改", size=30)
    s.text(110, 700, "而不是一口气写到底", size=30)
    s.text(110, 775, "成本也更高：每个分支都要一次模型调用", size=26)
    s.save("p09")


# ---------------------------------------------------------------- p10
def p10():
    s = Sheet(2210)
    s.text(110, 55, "什么时候思维链帮倒忙", size=42)

    s.box(110, 150, 730, 520, r=16, width=9, fill=PAPER)
    s.text(420, 195, "别用", size=32, anchor="mm")
    items1 = ["简单事实回忆", "单步分类", "速度优先的批量任务"]
    for i, t in enumerate(items1):
        y = 290 + i * 70
        s.cross(180, y, r=16, width=8)
        s.text(225, y, t, size=26, anchor="lm")

    s.box(790, 150, 1490, 520, r=16, width=9, fill=YELLOW)
    s.streaks((800, 160, 1480, 510), step=50, width=2)
    s.text(1140, 195, "该用", size=32, anchor="mm", stroke=2)
    items2 = ["多步算术", "符号推理", "需要展示过程的场景"]
    for i, t in enumerate(items2):
        y = 290 + i * 70
        s.check(860, y, r=16, width=8)
        s.text(905, y, t, size=26, anchor="lm", stroke=2)

    s.line([(110, 580), (1490, 580)], width=7)
    s.text(110, 615, "每次查询多出 50 到 200 个 token 的推理开销", size=28)
    s.text(110, 690, "高吞吐、低复杂度的任务上，那就是白花的钱", size=28)
    s.text(110, 765, "算一下：一天一百万次调用，每次多 100 token", size=26)
    s.text(110, 835, "等于每天多花几美元到几十美元", size=26)
    s.save("p10")


# ---------------------------------------------------------------- p11
def p11():
    s = Sheet(2211)
    s.text(110, 55, "三种策略的成本对比", size=44)

    rows = [("策略", "调用次数", "token 倍数", "准确率"),
            ("零样本", "1", "1x", "78%"),
            ("零样本 CoT", "1", "3x", "91%"),
            ("少样本 CoT", "1", "5x", "95%"),
            ("自洽性 ×5", "5", "15x", "96%")]
    for i, (a, b, c, d) in enumerate(rows):
        y = 150 + i * 100
        hot = i == 2
        s.box(90, y, 1470, y + 84, r=10, width=7,
              fill=YELLOW if hot else (METAL if i == 0 else PAPER))
        if hot:
            s.streaks((100, y + 8, 1460, y + 76), step=44, width=2)
        for j, v in enumerate([a, b, c, d]):
            s.text(150 + j * 330, y + 42, v, size=26 if j else 24, anchor="lm",
                   stroke=2 if hot else 0)

    s.line([(110, 660), (1490, 660), ], width=7)
    s.text(110, 695, "少样本 CoT 是性价比拐点：5 倍 token 换 17 个点", size=30)
    s.text(110, 765, "自洽性再往上加，边际收益就很小了", size=28)
    s.text(110, 835, "先上少样本 CoT，不够再上自洽性", size=30)
    s.save("p11")


# ---------------------------------------------------------------- p12
def p12():
    s = Sheet(2212)
    s.text(110, 55, "你的场景里，加思维链是赚还是亏？", size=42)

    opts = [("多步推理", "加，提升明显", YELLOW),
            ("简单分类", "不加，纯浪费", PAPER),
            ("用推理模型", "不加，它自己想过了", PAPER)]
    for i, (name, note, fill) in enumerate(opts):
        y = 170 + i * 150
        s.box(110, y, 1490, y + 120, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 112), step=46, width=2)
        s.text(180, y + 60, name, size=34, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(660, y + 60, note, size=26, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.line([(110, 640), (1490, 640), ], width=7)
    s.text(110, 675, "判断标准很简单：任务是几步？", size=30)
    s.text(110, 745, "两步以上，思维链通常划算", size=30)

    s.box(110, 810, 1490, 870, r=12, width=8, fill=PAPER)
    s.text(800, 840, "下一集：结构化输出", size=28, anchor="mm")
    s.save("p12")


# ---------------------------------------------------------------- cover
def cover():
    s = Sheet(2200)
    s.text(110, 90, "加五个字", size=64)
    s.text(110, 190, "78% → 91%", size=64)
    s.line([(110, 320), (1490, 320)], width=11)

    s.box(110, 390, 1490, 640, r=20, width=11, fill=YELLOW)
    s.streaks((120, 400, 1480, 630), step=56, width=3)
    s.text(800, 470, "Let's think step by step", size=44, anchor="mm", stroke=2)
    s.text(800, 570, "同一模型，同一温度", size=36, anchor="mm", stroke=2)

    s.text(110, 720, "思维链 · 少样本 · 思维树", size=34)
    s.save("cover")


if __name__ == "__main__":
    for fn in (cover, p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12):
        fn()
