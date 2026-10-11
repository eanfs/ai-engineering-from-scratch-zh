# pdoom-video 子项目与三集课程样片

根据用户指示新增 `pdoom-video/` Git 子模块，初始代码从 `/Users/lirichen/Work/GithubRepo/pdoom-video` 克隆，上游地址保留为 `https://github.com/mexicat/pdoom-video`。

在此基础上，用 pdoom-video 的代码渲染视频引擎（Three.js Engine + headless Chrome 离线导出器）制作
`docs/plans/2026-10-10-video-series-production-plan.md` 的首批三集样片（Task 10/11/12 的场景表）：

| 集 | 产线 | 场景数 / 档位 | 时长 | 成片 |
|---|---|---|---|---|
| 03-01 感知机 | `pdoom-video/perceptron/` | 12 / T-L | 约 249 s | `out/perceptron/perceptron-1080p.mp4` |
| 07-01 为什么需要 Transformer | `pdoom-video/why-transformers/` | 12 / T-L | 约 255 s | `out/why-transformers/why-transformers-1080p.mp4` |
| 14-01 Agent 循环 | `pdoom-video/codex-agent/` | 9 / T-M | 约 183 s | `out/codex-agent/agent-loop-codex-1080p.mp4` |

三条产线均为 1920×1080、30 fps、无配音（按此前指示跳过音频）：旁白改为按阅读节奏逐段显示的字幕
（每场景 3 段），时长落在对应档位窗口。画面数字全部来自课程代码实跑（`course-run.txt` 保存原始输出）。
分镜与制作细节见各产线的 `SCRIPT.md` 与 `README.md`；验收证据见各产线 `media-validation.json`。

- 分镜：`pdoom-video/{perceptron,why-transformers,codex-agent}/SCRIPT.md`
- 制作与复现：同名目录 `README.md` / `build.py` / `render.py` / `validate.py`
- 共享绘图层：`pdoom-video/app/src/explain-kit.ts`

父仓库分支：`feature/pdoom-video-pilot`；子模块分支：`feature/codex-agent-pilot`。
制作代码在子模块内提交；课程仓库只保存 `.gitmodules` 与子模块 gitlink、以及本说明文档。
原 `/Users/lirichen/Work/GithubRepo/pdoom-video` 工作区未修改。

本轮制作未调用 Hypit 渲染，也未使用原音乐视频的歌曲、歌词或外部计费生成服务。
