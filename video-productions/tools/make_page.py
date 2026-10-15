#!/usr/bin/env python3
# 用法：make_page.py <作品目录> <场景文件目录> [场景文件数] [--common <公共底座.js>]
# index.html = 手绘笔记模板底座(1-738 行) + 公共底座 common.js + 场景代码 + 模板底座续(829-912 行，场景入口改成 drawScenes)
# 依赖 dashi-animationstyle skill 的 styles/手绘笔记/模板.html；用环境变量 DASHI_SKILL 指定 skill 根目录。
import os, sys

SKILL = os.environ.get("DASHI_SKILL", os.path.expanduser("~/video-skills/dashi-animationstyle"))
argv = sys.argv[1:]
common = None
if "--common" in argv:
    i = argv.index("--common")
    common = argv[i + 1]
    del argv[i:i + 2]
else:
    default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "common.js")
    common = default if os.path.exists(default) else None
work, srcdir = os.path.abspath(argv[0]), os.path.abspath(argv[1])
n = int(argv[2]) if len(argv) > 2 else 2
tpl = open(os.path.join(SKILL, "styles/手绘笔记/模板.html"), encoding="utf-8").read().splitlines(keepends=True)
head, tail = "".join(tpl[:738]), "".join(tpl[828:])
assert "drawSections(t, v);" in tail, "模板尾部找不到场景入口"
tail = tail.replace("drawSections(t, v);", "drawScenes(t, v);")
open(os.path.join(work, "index_模板备份.html"), "w", encoding="utf-8").write("".join(tpl))
if not (common and os.path.exists(common)):
    raise SystemExit("找不到公共底座 common.js（用 --common 指定）")
parts = [open(common, encoding="utf-8").read()]
parts += [open(os.path.join(srcdir, f"scenes_{i}.js"), encoding="utf-8").read() for i in range(1, n + 1)]
html = head + "".join(parts) + tail
open(os.path.join(work, "index.html"), "w", encoding="utf-8").write(html)
print(f"index.html 行数 {html.count(chr(10)) + 1}（公共底座 + {n} 个场景文件）")
