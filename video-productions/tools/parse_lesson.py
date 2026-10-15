#!/usr/bin/env python3
# 用法：parse_lesson.py <集号如 14-01> <作品目录>  —— 从 hypit 的 lesson.json 生成 讲稿.md / scenes.json / 稿子.txt
import json, os, re, sys

slug, work = sys.argv[1], sys.argv[2]
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EPISODES = os.environ.get("DASHI_EPISODES", os.path.join(ROOT, "hypit-productions", "ai-engineering-zh", "episodes"))
LESSON = os.path.join(EPISODES, slug, "lesson.json")
data = json.load(open(LESSON, encoding="utf-8"))
lines_all = [l for sc in data for l in sc["lines"]]
for sc in data:
    assert len(sc["lines"]) == 3, (sc["id"], len(sc["lines"]))

md = [f"# {slug}（讲稿）", ""]
for sc in data:
    md += [f"## {sc['id']} {sc['title']}", ""]
    md += [f"{i}. {l}" for i, l in enumerate(sc["lines"], 1)] + [""]
os.makedirs(work, exist_ok=True)
open(os.path.join(work, "讲稿.md"), "w", encoding="utf-8").write("\n".join(md))
json.dump(data, open(os.path.join(work, "scenes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(os.path.join(work, "稿子.txt"), "w", encoding="utf-8").write("\n".join(lines_all) + "\n")
chars = sum(len(re.sub(r"\s+", "", l)) for l in lines_all)
print(f"{slug}: 场景 {len(data)}，句子 {len(lines_all)}，去空白字符 {chars}")
for sc in data:
    print(" ", sc["id"], sc["title"], sum(len(re.sub(r"\s+", "", l)) for l in sc["lines"]))
