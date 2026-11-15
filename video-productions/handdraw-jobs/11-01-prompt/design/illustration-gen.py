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
OUT_W, OUT_H = 2048, 1152  # 大画布：高于 1920x1080 视频分辨率，输出时缩小而非放大
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
        image = self.img.resize((OUT_W, OUT_H), Image.LANCZOS)
        rgb = np.array(image.convert("RGB")).astype(int)
        diff = np.abs(rgb - np.array(PAPER)).max(axis=2)
        alpha = np.clip((diff - 2) / 10 * 255, 0, 255).astype(np.uint8)
        rgba = np.dstack([rgb.astype(np.uint8), alpha])
        Image.fromarray(rgba, "RGBA").save(OUT / f"{name}.png")
        print("wrote", OUT / f"{name}.png")




# ---------------------------------------------------------------- p01
def p01():
    s = Sheet(2101)
    s.text(110, 60, "同一件事，两种写法", size=50)

    s.box(110, 160, 720, 440, r=20, width=11, fill=PAPER)
    s.text(415, 215, "随手写", size=40, anchor="mm")
    s.text(415, 320, "给我写封营销邮件", size=34, anchor="mm")
    s.text(415, 400, "→ 没法用", size=34, anchor="mm")

    s.box(780, 160, 1490, 440, r=20, width=11, fill=YELLOW)
    s.streaks((790, 170, 1480, 430), step=52, width=3)
    s.text(1135, 215, "工程化", size=40, anchor="mm", stroke=2)
    s.text(1135, 300, "角色 + 受众 + 语气", size=34, anchor="mm", stroke=2)
    s.text(1135, 370, "字数 + 指标 + CTA", size=34, anchor="mm", stroke=2)
    s.text(1135, 500, "→ 能直接发", size=36, anchor="mm")

    s.text(110, 620, "同一个模型，同样的参数", size=44)
    s.text(110, 700, "差的只是那几十个字", size=52)
    s.text(110, 800, "这就是提示词工程", size=44)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(2102)
    s.text(110, 70, "Prompt Engineering", size=64)
    s.text(110, 165, "阶段 11 · 第 1 课", size=36)
    s.line([(110, 250), (1490, 250)], width=10)

    s.text(110, 300, "每次调用有三个部分", size=44)
    parts = [("System", "设定身份与规则", YELLOW),
             ("User", "每轮的任务", PAPER),
             ("Prefill", "给回复开头", PAPER)]
    for i, (name, note, fill) in enumerate(parts):
        y = 400 + i * 150
        s.box(110, y, 1490, y + 125, r=18, width=10, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 117), step=50, width=3)
        s.text(180, y + 40, name, size=42, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(180, y + 95, note, size=34, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.text(800, 880, "大多数人只写 User", size=36, anchor="mm")
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(2103)
    s.text(110, 55, "「你是专家」为什么管用", size=50)
    s.text(110, 135, "它是个激活函数", size=44)
    s.box(110, 210, 1490, 320, r=18, width=10, fill=YELLOW)
    s.streaks((120, 220, 1480, 310), step=50, width=3)
    s.text(800, 265, "把采样偏向专家那一端", size=46, anchor="mm", stroke=2)

    s.text(140, 380, "泛泛的助手", size=34)
    base = 620
    s.line([(160, base), (1400, base)], width=9)
    import random
    random.seed(2103)
    for i in range(17):
        x = 190 + i * 72
        h = int(70 + random.random() * 90)
        s.box(x, base - h, x + 54, base, r=6, width=5, fill=METAL)

    s.text(140, 670, "具体角色", size=34)
    base2 = 900
    s.line([(160, base2), (1400, base2)], width=9)
    random.seed(2104)
    for i in range(17):
        x = 190 + i * 72
        center = abs(x - 640) / 640
        h = int(210 * max(0.04, 1 - center * 2.1) + random.random() * 24)
        s.box(x, base2 - h, x + 54, base2, r=6, width=5,
              fill=YELLOW if h > 120 else METAL)
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(2104)
    s.text(110, 55, "角色越具体越好，但有限", size=48)

    rows = [("你是个助手", "泛泛的中位数", METAL),
            ("你是软件工程师", "仍然宽泛", PAPER),
            ("你是 Stripe 支付后端", "窄、高质量", YELLOW),
            ("你是弦拓扑第一人", "一本正经胡说", PAPER)]
    for i, (role, effect, fill) in enumerate(rows):
        y = 150 + i * 160
        s.box(110, y, 1490, y + 135, r=18, width=10, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 127), step=50, width=3)
        s.text(180, y + 45, role, size=38, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(180, y + 100, effect, size=32, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.text(110, 810, "甜区：领域具体、语料充足", size=42)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(2105)
    s.text(110, 55, "模糊 vs 具体", size=50)

    s.text(110, 140, "模糊", size=36)
    s.box(110, 190, 1490, 290, r=16, width=10, fill=PAPER)
    s.text(160, 240, "写一封营销邮件", size=40)

    s.text(110, 330, "工程化", size=36)
    s.box(110, 380, 1490, 660, r=16, width=10, fill=YELLOW)
    s.streaks((120, 390, 1480, 650), step=60, width=3)
    lines = ["B2B SaaS 资深文案", "受众：B 轮工程经理", "语气：技术、不推销",
             "150 词 + 一个指标", "结尾只留一个 CTA"]
    for i, ln in enumerate(lines):
        s.text(180, 430 + i * 46, ln, size=34, stroke=2)

    s.text(110, 720, "前者激活泛泛的分布", size=40)
    s.text(110, 800, "后者激活高质量的切片", size=44)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(2106)
    s.text(110, 55, "每处歧义都是一个分叉点", size=46)

    s.text(110, 135, "「总结这篇文章」", size=38)
    forks = ["一段话", "长文", "十个要点"]
    for i, f in enumerate(forks):
        x = 180 + i * 430
        s.box(x, 200, x + 360, 330, r=18, width=10, fill=METAL)
        s.text(x + 180, 265, f, size=38, anchor="mm")
    s.text(110, 400, "→ 模型自己选，选错要重写", size=34)

    s.line([(110, 470), (1490, 470)], width=9)
    s.text(110, 510, "加上约束", size=38)
    s.box(110, 570, 1490, 700, r=18, width=10, fill=YELLOW)
    s.streaks((120, 580, 1480, 690), step=52, width=3)
    s.text(800, 635, "三要点 · 每条 ≤20 词 · 只讲数据", size=38, anchor="mm", stroke=2)

    s.text(110, 760, "模糊版把选择权给模型", size=40)
    s.text(110, 840, "具体版收回来", size=44)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(2107)
    s.text(110, 55, "四种常用模式", size=50)

    rows = [("角色", "收窄分布", YELLOW),
            ("少样本", "给两三个例子", PAPER),
            ("思维链", "先写推理再答", PAPER),
            ("护栏", "圈外一律拒绝", PAPER)]
    for i, (name, note, fill) in enumerate(rows):
        y = 150 + i * 155
        s.box(110, y, 1490, y + 130, r=18, width=10, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 122), step=50, width=3)
        s.text(180, y + 42, name, size=42, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(180, y + 98, note, size=34, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.text(800, 850, "四种可以叠加，不是互斥", size=40, anchor="mm")
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(2108)
    s.text(110, 55, "护栏：给模型画个圈", size=50)

    s.box(110, 150, 1490, 380, r=20, width=11, fill=YELLOW)
    s.streaks((120, 160, 1480, 370), step=56, width=3)
    s.text(800, 210, "你是 Python 助教", size=44, anchor="mm", stroke=2)
    s.text(800, 285, "只答 Python 问题", size=40, anchor="mm", stroke=2)
    s.text(800, 345, "圈外一律拒绝", size=40, anchor="mm", stroke=2)

    s.line([(110, 450), (1490, 450)], width=9)
    s.check(150, 540, r=22, width=11)
    s.text(210, 540, "问 Python → 正常作答", size=40, anchor="lm")
    s.cross(150, 650, r=22, width=11)
    s.text(210, 650, "问法律 → 拒绝", size=40, anchor="lm")

    s.text(110, 760, "面向用户的产品必须有这层", size=42)
    s.text(110, 840, "否则它什么都答", size=40)
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(2109)
    s.text(110, 55, "提示词也要测试", size=50)

    s.text(110, 135, "改完怎么知道变好还是变坏", size=38)
    steps = [("建用例集", "每个一份预期输出", PAPER),
             ("全部跑分", "同一套跑所有候选", YELLOW),
             ("看排名", "赢几次、输在哪类", PAPER)]
    for i, (name, note, fill) in enumerate(steps):
        y = 210 + i * 150
        s.box(110, y, 1490, y + 125, r=18, width=10, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 117), step=50, width=3)
        s.text(180, y + 42, name, size=40, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(180, y + 96, note, size=32, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.box(110, 690, 1490, 830, r=20, width=11, fill=PAPER)
    s.text(800, 740, "实测：gpt-4o 五战全胜", size=44, anchor="mm")
    s.text(800, 795, "另两个各有短板", size=32, anchor="mm")
    s.save("p09")


# ---------------------------------------------------------------- p10
def p10():
    s = Sheet(2110)
    s.text(110, 55, "三个常见病症", size=50)

    rows = [("幻觉", "编事实", "约束太少", YELLOW),
            ("拒答", "能答却拒", "护栏太宽", PAPER),
            ("格式违规", "多加解释", "缺示例", PAPER)]
    for i, (name, symptom, cause, fill) in enumerate(rows):
        y = 150 + i * 165
        s.box(110, y, 1490, y + 140, r=18, width=10, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 132), step=50, width=3)
        s.text(180, y + 45, name, size=40, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(180, y + 100, symptom, size=34, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(1430, y + 72, cause, size=32, anchor="rm", stroke=2 if fill == YELLOW else 0)

    s.text(110, 720, "三个病症，三个修法", size=42)
    s.text(110, 800, "改错地方会更糟", size=40)
    s.save("p10")


# ---------------------------------------------------------------- p11
def p11():
    s = Sheet(2111)
    s.text(110, 55, "同一套测试，三个模型", size=46)

    rows = [("模型", "分数", "token", "延迟"),
            ("gpt-4o", "0.500", "195", "850ms"),
            ("claude-3.5", "0.500", "185", "720ms"),
            ("gemini-1.5", "0.500", "197", "900ms")]
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

    s.line([(110, 640), (1490, 640), ], width=9)
    s.text(110, 680, "分数一样，成本和速度不同", size=42)
    s.text(110, 760, "测试集不只看分数", size=40)
    s.save("p11")


# ---------------------------------------------------------------- p12
def p12():
    s = Sheet(2112)
    s.text(110, 55, "你最常漏掉哪一部分？", size=50)

    opts = [("角色", "告诉它你是谁", YELLOW),
            ("示例", "给两三个样例", PAPER),
            ("输出格式", "限定结构与长度", PAPER)]
    for i, (name, note, fill) in enumerate(opts):
        y = 170 + i * 155
        s.box(110, y, 1490, y + 130, r=18, width=10, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 122), step=50, width=3)
        s.text(200, y + 65, name, size=42, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(700, y + 65, note, size=34, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.text(110, 700, "三个都加上，质量通常翻倍", size=42)
    s.text(110, 780, "成本只是多打几十个字", size=40)

    s.box(110, 850, 1490, 930, r=14, width=9, fill=PAPER)
    s.text(800, 890, "下一集：少样本与思维链", size=34, anchor="mm")
    s.save("p12")


# ---------------------------------------------------------------- cover (大画布 1920x1080)
def cover():
    base = Image.new("RGB", (OUT_W, OUT_H), PAPER)
    d = ImageDraw.Draw(base)
    title_font = ImageFont.truetype(FONT, 120)
    sub_font = ImageFont.truetype(FONT, 66)
    meta_font = ImageFont.truetype(FONT, 34)
    d.text((128, 170), "加一句", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((128, 320), "你是专家", font=title_font, fill=INK, stroke_width=3, stroke_fill=INK)
    d.text((128, 490), "输出为什么就变好了", font=sub_font, fill=INK)
    d.rectangle([128, 608, 746, 619], fill=INK)
    d.text((128, 650), "11-01 · LLM Engineering", font=meta_font, fill=INK)
    art = Image.open(OUT / "p01.png").convert("RGB")
    art = art.resize((1109, 624), Image.LANCZOS)
    base.paste(art, (853, 427))
    base.save(OUT / "cover.png")
    print("wrote", OUT / "cover.png")


if __name__ == "__main__":
    for fn in (cover, p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12):
        fn()
