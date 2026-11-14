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
    s = Sheet(2101)
    s.text(110, 60, "同一件事，两种写法，输出天差地别", size=44)

    s.box(110, 170, 720, 400, r=16, width=10, fill=PAPER)
    s.text(405, 210, "大多数人这么写", size=28, anchor="mm")
    s.text(405, 285, "给我写一封营销邮件", size=32, anchor="mm")
    s.text(405, 355, "→ 泛泛而谈，没法用", size=24, anchor="mm")

    s.box(780, 170, 1490, 400, r=16, width=10, fill=YELLOW)
    s.streaks((790, 180, 1480, 390), step=50, width=2)
    s.text(1125, 210, "工程化这么写", size=28, anchor="mm", stroke=2)
    s.text(1125, 265, "角色 + 受众 + 语气", size=26, anchor="mm", stroke=2)
    s.text(1125, 315, "字数 + 指标 + 一个 CTA", size=26, anchor="mm", stroke=2)
    s.text(1125, 365, "→ 能直接发出去", size=24, anchor="mm", stroke=2)

    s.line([(110, 470), (1490, 470)], width=7)
    s.text(110, 510, "同一个模型，同样的参数", size=34)
    s.text(110, 585, "差的只是你发出去的那几十个字", size=36)
    s.text(110, 665, "这就是提示词工程", size=38)
    s.text(110, 745, "它不是花招，是意图和机器能力之间最主要的接口", size=28)
    s.save("p01")


# ---------------------------------------------------------------- p02
def p02():
    s = Sheet(2102)
    s.text(110, 70, "Prompt Engineering", size=58)
    s.text(110, 165, "阶段 11 · 第 1 课", size=34)
    s.line([(110, 240), (1490, 240)], width=9)
    s.text(110, 285, "每次调用都有三个部分：", size=34)

    parts = [("System", "设定身份、规则、约束", "跨轮次持续，最高优先级", YELLOW),
             ("User", "实际任务或问题", "每轮变化", PAPER),
             ("Assistant prefill", "给回复开头", "直接逼出你要的格式", PAPER)]
    for i, (name, note, detail, fill) in enumerate(parts):
        y = 370 + i * 145
        s.box(110, y, 1490, y + 120, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 112), step=48, width=2)
        s.text(160, y + 42, name, size=30, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(160, y + 90, note, size=24, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(1430, y + 42, detail, size=22, anchor="rm", stroke=2 if fill == YELLOW else 0)

    s.text(800, 850, "大多数人只写 User，另外两个才是杠杆", size=28, anchor="mm")
    s.save("p02")


# ---------------------------------------------------------------- p03
def p03():
    s = Sheet(2103)
    s.text(110, 55, "「你是一名专家」为什么管用", size=44)
    s.text(110, 140, "它不是魔咒，是一个激活函数：", size=30)
    s.box(110, 200, 1490, 310, r=14, width=9, fill=PAPER)
    s.text(800, 255, "把采样分布偏向训练数据里专家那一端", size=36, anchor="mm")

    # 宽分布
    s.text(140, 360, "泛泛的助手：宽分布、中位质量", size=26)
    base = 610
    s.line([(160, base), (1400, base)], width=8)
    import random
    random.seed(2103)
    for i in range(26):
        x = 190 + i * 46
        h = int(60 + random.random() * 90)
        s.box(x, base - h, x + 34, base, r=4, width=4, fill=METAL)

    # 窄分布
    s.text(140, 660, "具体角色：窄分布、高质量切片", size=26)
    base2 = 850
    s.line([(160, base2), (1400, base2)], width=8)
    random.seed(2104)
    for i in range(26):
        x = 190 + i * 46
        center = abs(x - 620) / 620
        h = int(180 * max(0.05, 1 - center * 2.2) + random.random() * 20)
        s.box(x, base2 - h, x + 34, base2, r=4, width=4,
              fill=YELLOW if h > 100 else METAL)
    s.save("p03")


# ---------------------------------------------------------------- p04
def p04():
    s = Sheet(2104)
    s.text(110, 55, "角色越具体越好，但有上限", size=42)

    rows = [("你是一个乐于助人的助手", "泛泛的中位数回答", METAL),
            ("你是一名软件工程师", "代码更好，但仍然宽泛", PAPER),
            ("你是 Stripe 专攻支付的资深后端工程师", "狭窄、高质量、领域专属", YELLOW),
            ("你是量子引力弦拓扑全球第一", "一本正经的胡说", PAPER)]
    for i, (role, effect, fill) in enumerate(rows):
        y = 150 + i * 150
        s.box(110, y, 1490, y + 125, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 117), step=48, width=2)
        s.text(160, y + 40, role, size=26, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(160, y + 92, effect, size=24, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.text(110, 780, "具体到几乎没训练样本匹配时，模型只能编", size=30)
    s.text(110, 855, "甜区是「领域具体、语料充足」", size=32)
    s.save("p04")


# ---------------------------------------------------------------- p05
def p05():
    s = Sheet(2105)
    s.text(110, 55, "模糊 vs 具体：一封营销邮件", size=42)

    s.text(110, 130, "模糊版：", size=28)
    s.box(110, 180, 1490, 260, r=12, width=8, fill=PAPER)
    s.text(160, 220, "Write a marketing email for our new product.", size=28)

    s.text(110, 300, "工程化版：", size=28)
    s.box(110, 350, 1490, 560, r=12, width=9, fill=YELLOW)
    s.streaks((120, 360, 1480, 550), step=52, width=2)
    lines = ["你是 B2B SaaS 公司的资深文案",
             "受众：B 轮公司的工程经理",
             "语气：自信、技术、不推销",
             "长度 150 词，含一个具体指标 3.2 倍",
             "结尾只留一个 CTA"]
    for i, ln in enumerate(lines):
        s.text(170, 390 + i * 33, ln, size=22, stroke=1)

    s.line([(110, 600), (1490, 600)], width=7)
    s.text(110, 635, "前者激活的是一片泛泛的营销邮件分布", size=30)
    s.text(110, 705, "后者激活的是一个狭窄、高质量的切片", size=30)
    s.text(110, 780, "合法输出越少，拿到你要那个的概率越高", size=32)
    s.save("p05")


# ---------------------------------------------------------------- p06
def p06():
    s = Sheet(2106)
    s.text(110, 55, "每一处歧义，都是模型要去猜的分叉点", size=38)

    s.text(110, 130, "「总结这篇文章」：", size=28)
    forks = ["一段话", "五百字长文", "十个要点"]
    for i, f in enumerate(forks):
        x = 180 + i * 300
        s.box(x, 190, x + 250, 280, r=12, width=8, fill=METAL)
        s.text(x + 125, 235, f, size=26, anchor="mm")
    s.text(110, 310, "→ 模型自己选，选错你就得重写", size=24)

    s.line([(110, 360), (1490, 360), ], width=7)
    s.text(110, 400, "加上约束：", size=28)
    s.box(110, 460, 1490, 560, r=12, width=9, fill=YELLOW)
    s.streaks((120, 470, 1480, 550), step=50, width=2)
    s.text(800, 510, "三个要点 · 每条一句 ≤ 20 词 · 只讲定量发现", size=28, anchor="mm", stroke=2)

    s.line([(110, 620), (1490, 620)], width=7)
    s.text(110, 655, "模糊版把选择权交给模型", size=32)
    s.text(110, 725, "具体版把选择权收回来", size=32)
    s.text(110, 800, "这一步的成本是几十个字，收益是省下二十分钟重写", size=26)
    s.save("p06")


# ---------------------------------------------------------------- p07
def p07():
    s = Sheet(2107)
    s.text(110, 55, "四种常用模式", size=44)

    rows = [("1  角色", "告诉它你是谁，收窄分布", YELLOW),
            ("2  少样本", "给两三个例子，照着学", PAPER),
            ("3  思维链", "先写推理，再给答案", PAPER),
            ("4  护栏", "画一个圈，圈外一律拒绝", PAPER)]
    for i, (name, note, fill) in enumerate(rows):
        y = 150 + i * 140
        s.box(110, y, 1490, y + 115, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 107), step=48, width=2)
        s.text(160, y + 38, name, size=30, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(160, y + 85, note, size=24, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.text(110, 750, "四种可以叠加，不是互斥选项", size=32)
    s.text(110, 825, "实测里同一个任务叠上角色和示例，分数能翻倍", size=28)
    s.save("p07")


# ---------------------------------------------------------------- p08
def p08():
    s = Sheet(2108)
    s.text(110, 55, "护栏：给模型画一个圈", size=44)

    s.box(110, 150, 1490, 320, r=14, width=9, fill=YELLOW)
    s.streaks((120, 160, 1480, 310), step=50, width=2)
    s.text(800, 195, "你是一个 Python 编程助教", size=32, anchor="mm", stroke=2)
    s.text(800, 250, "只回答 Python 编程问题", size=28, anchor="mm", stroke=2)
    s.text(800, 295, "圈外的问题一律礼貌拒绝", size=28, anchor="mm", stroke=2)

    s.line([(110, 380), (1490, 380)], width=7)
    s.text(110, 415, "实测：加上护栏之后，被问别的领域时会明确说不", size=30)
    s.check(140, 490, r=16, width=8)
    s.text(185, 490, "问 Python 问题 → 正常作答", size=28, anchor="lm")
    s.cross(140, 560, r=16, width=8)
    s.text(185, 560, "问法律问题 → 拒绝并说明范围", size=28, anchor="lm")

    s.text(110, 640, "面向用户的产品必须有这一层", size=32)
    s.text(110, 715, "否则它会替你做客服以外的一切事", size=30)
    s.text(110, 790, "包括你不希望它回答的那些", size=28)
    s.save("p08")


# ---------------------------------------------------------------- p09
def p09():
    s = Sheet(2109)
    s.text(110, 55, "提示词也要测试", size=44)

    s.text(110, 130, "改了提示词，怎么知道是变好还是变坏？", size=30)
    steps = [("1  建用例集", "每个用例一份预期输出", PAPER),
             ("2  跑分", "同一套用例跑所有候选模型", PAPER),
             ("3  看排名", "赢几次、输在哪类用例", YELLOW)]
    for i, (name, note, fill) in enumerate(steps):
        y = 200 + i * 130
        s.box(110, y, 1490, y + 110, r=12, width=8, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 102), step=46, width=2)
        s.text(160, y + 38, name, size=30, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(160, y + 85, note, size=24, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.box(110, 630, 1490, 760, r=14, width=9, fill=PAPER)
    s.text(800, 675, "实测：gpt-4o 五战全胜", size=38, anchor="mm")
    s.text(800, 725, "另外两个模型各有短板", size=26, anchor="mm")

    s.text(110, 810, "没有测试集，你改提示词全靠感觉", size=30)
    s.save("p09")


# ---------------------------------------------------------------- p10
def p10():
    s = Sheet(2110)
    s.text(110, 55, "三个常见病症", size=44)

    rows = [("幻觉", "编了不存在的事实", "约束太少", YELLOW),
            ("拒答", "明明能答却拒绝", "护栏写得太宽", PAPER),
            ("格式违规", "让它出 JSON，它加了解释", "缺 prefill 或缺示例", PAPER)]
    for i, (name, symptom, cause, fill) in enumerate(rows):
        y = 150 + i * 175
        s.box(110, y, 1490, y + 145, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 137), step=48, width=2)
        s.text(160, y + 42, name, size=32, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(160, y + 98, symptom, size=24, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(1430, y + 42, cause, size=22, anchor="rm", stroke=2 if fill == YELLOW else 0)

    s.text(110, 720, "三个病症，三个不同的修法", size=32)
    s.text(110, 795, "改错地方会比不改更糟", size=30)
    s.text(110, 865, "所以上一页的测试集是前提", size=28)
    s.save("p10")


# ---------------------------------------------------------------- p11
def p11():
    s = Sheet(2111)
    s.text(110, 55, "同一套测试，三个模型的分数", size=40)

    rows = [("模型", "得分", "token", "延迟"),
            ("gpt-4o", "0.500", "195", "850ms"),
            ("claude-3.5-sonnet", "0.500", "185", "720ms"),
            ("gemini-1.5-pro", "0.500", "197", "900ms")]
    for i, (a, b, c, d) in enumerate(rows):
        y = 150 + i * 100
        hot = i == 1
        s.box(90, y, 1470, y + 84, r=10, width=7,
              fill=YELLOW if hot else (METAL if i == 0 else PAPER))
        if hot:
            s.streaks((100, y + 8, 1460, y + 76), step=44, width=2)
        for j, v in enumerate([a, b, c, d]):
            s.text(140 + j * 340, y + 42, v, size=26 if j else 24, anchor="lm",
                   stroke=2 if hot else 0)

    s.line([(110, 600), (1490, 600), ], width=7)
    s.text(110, 635, "分数相同，但延迟和 token 消耗不同", size=30)
    s.text(110, 705, "claude 最省 token 也最快，gemini 最慢", size=28)
    s.text(110, 775, "测试集不只看分数，还要看成本和速度", size=30)
    s.save("p11")


# ---------------------------------------------------------------- p12
def p12():
    s = Sheet(2112)
    s.text(110, 55, "你写提示词时，最常漏掉哪一部分？", size=42)

    opts = [("角色", "告诉它你是谁", YELLOW),
            ("示例", "给两三个样例", PAPER),
            ("输出格式", "限定结构、字数、结尾", PAPER)]
    for i, (name, note, fill) in enumerate(opts):
        y = 170 + i * 150
        s.box(110, y, 1490, y + 120, r=14, width=9, fill=fill)
        if fill == YELLOW:
            s.streaks((120, y + 8, 1480, y + 112), step=46, width=2)
        s.text(180, y + 60, name, size=34, anchor="lm", stroke=2 if fill == YELLOW else 0)
        s.text(660, y + 60, note, size=26, anchor="lm", stroke=2 if fill == YELLOW else 0)

    s.line([(110, 640), (1490, 640), ], width=7)
    s.text(110, 675, "三个都加上，输出质量通常能翻倍", size=30)
    s.text(110, 745, "成本只是多打几十个字", size=30)

    s.box(110, 810, 1490, 870, r=12, width=8, fill=PAPER)
    s.text(800, 840, "下一集：少样本、思维链与思维树", size=26, anchor="mm")
    s.save("p12")


# ---------------------------------------------------------------- cover
def cover():
    s = Sheet(2100)
    s.text(110, 85, "加一句「你是专家」", size=56)
    s.text(110, 175, "输出为什么就变好了？", size=56)
    s.line([(110, 300), (1490, 300)], width=10)

    s.box(110, 370, 1490, 620, r=20, width=11, fill=YELLOW)
    s.streaks((120, 380, 1480, 610), step=56, width=3)
    s.text(800, 450, "它是个激活函数", size=54, anchor="mm", stroke=2)
    s.text(800, 550, "把采样收窄到专家那一端", size=40, anchor="mm", stroke=2)

    s.text(110, 700, "提示词工程 · 阶段 11 · 第 1 课", size=30)
    s.save("cover")


if __name__ == "__main__":
    for fn in (cover, p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12):
        fn()
