# pdoom-video 子项目与三集课程样片

根据用户指示新增 `pdoom-video/` Git 子模块，初始代码从 `/Users/lirichen/Work/GithubRepo/pdoom-video` 克隆。
上游是 `https://github.com/mexicat/pdoom-video`（保留为本机 `origin`，用于同步上游），推送目标为 fork
`https://github.com/eanfs/pdoom-video`；`.gitmodules` 指向 fork，否则新克隆取不到本仓推送的样片提交。

在此基础上，用 pdoom-video 的代码渲染视频引擎（Three.js Engine + headless Chrome 离线导出器）制作
`docs/plans/2026-10-10-video-series-production-plan.md` 的首批三集样片（Task 10/11/12 的场景表）：

| 集 | 产线 | 场景数 / 档位 | 时长 | 成片 |
|---|---|---|---|---|
| 03-01 感知机 | `pdoom-video/perceptron/` | 12 / T-L | 约 249 s | `out/perceptron/perceptron-1080p.mp4` |
| 07-01 为什么需要 Transformer | `pdoom-video/why-transformers/` | 12 / T-L | 约 255 s | `out/why-transformers/why-transformers-1080p.mp4` |
| 14-01 Agent 循环 | `pdoom-video/codex-agent/` | 9 / T-M | 约 183 s | `out/codex-agent/agent-loop-codex-1080p.mp4` |

三条产线均为 1920×1080、30 fps。2026-10-11 晚起按用户指示接入火山豆包语音配音
（zh_female_cancan_mars_bigtts，逐句合成、按实测时长定轴，`aieng-tts/narrate.py`，密钥只经环境变量传入）：
字幕与语音共用同一份 cues 时间轴，时长落在对应档位窗口（241.2 / 243.8 / 180.5 秒）。2026-10-11 起统一为亮色纸感主题（纸底 `#f7f6f1`、白面板、
墨色正文、深绿 `#2e7d4f` 强调），场景切换带方向交替的纸色擦除动画（绿色前缘，约 0.55 秒）。
画面数字全部来自课程代码实跑（`course-run.txt` 保存原始输出）。
分镜与制作细节见各产线的 `SCRIPT.md` 与 `README.md`；验收证据见各产线 `media-validation.json`。

- 分镜：`pdoom-video/{perceptron,why-transformers,codex-agent}/SCRIPT.md`
- 制作与复现：同名目录 `README.md` / `build.py` / `render.py` / `validate.py`
- 共享绘图层：`pdoom-video/app/src/explain-kit.ts`

父仓库分支：`feature/pdoom-video-pilot`；子模块分支：`feature/codex-agent-pilot`。
制作代码在子模块内提交；课程仓库只保存 `.gitmodules` 与子模块 gitlink、以及本说明文档。
原 `/Users/lirichen/Work/GithubRepo/pdoom-video` 工作区未修改。

本轮制作未调用 Hypit 渲染，也未使用原音乐视频的歌曲、歌词或外部计费生成服务。
