# 07-04 位置编码 · handdrawn-explainer-video 任务

## 状态：已完成

- 旁白：用户提供的完整 mp3，转成 `inputs/narration/master.wav`（48 kHz 单声道），
  `alignment.json` 记录逐句时间；成片 333.80 秒 / 8011 帧。
- 画幅：1280×720 · 24 fps；画风：12 工业设计马克笔手绘；手部：teacher-pen。
- 11 页 / 83 句，插图全部由本地 PIL 绘制（`design/illustration-gen.py`），不调生图接口。
- 成片 sha256 前 8 位 `c8fae78e`；`review.json` 五类检查均已通过，`finalize` 状态为
  `delivery_review_completed`。

## 重建

插图与合同文件入库，配音、配乐、`work/` 与 `outputs/film.mp4` 按 `.gitignore` 不入库。
按仓库 `video-productions/README.md` 的「逐笔手绘版」命令顺序重建即可。
