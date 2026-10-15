# 来源与版本

本目录是第三方开源 Claude Skill **dashi-animationstyle** 的收录，供本仓库制作课程视频使用。

| 项 | 值 |
|---|---|
| 上游仓库 | https://github.com/chuspeeism/dashi-animationstyle |
| 收录版本 | commit `aa620f3b859aa5d191b783b2eb0fb59263731c76`（2026-10-13，"skill 改名为 dashi-animationstyle"） |
| 许可 | MIT，版权归 Dashi AI Lab（《大师的AI小灶》）——见 `LICENSE` |
| 收录日期 | 2026-10-15 |
| 收录方式 | 完整收录代码与文档；**上游的展示类素材未随仓库分发**，见下节 |

## 未随仓库分发的素材

下列文件只用于展示，不影响 skill 运行，为控制仓库体积已剔除（共约 31 MB）：

| 路径 | 内容 | 体积 |
|---|---|---|
| `docs/*.gif` | README 里的 7 张风格演示动图 | 约 14 MB |
| `styles/*/静帧/*.jpg` | 7 套风格各 3 张高清截图 | 约 13 MB |
| `examples/token/口播.wav` | Token 示例的配音 | 约 3.6 MB |

因此根 `README.md` 的动图在仓库内会显示为裂图 —— 要看效果请按下面的方式取回，或直接看制作好的成片（`video-productions/`）。

## 目录

| 路径 | 内容 |
|---|---|
| `SKILL.md` | 技能主文件：三种用法、页面约定、字幕/分镜字段、render.mjs 参数 |
| `pipeline/` | `新建作品.mjs`、`字幕.mjs`、`生成timeline.mjs`、`render.mjs`（无头 Chrome 逐帧截图）、`动效部件.js`、`自检.mjs`、`丰富度检查.mjs` |
| `styles/<风格>/` | 7 套风格的 `模板.html`、`示例_Token.html`、`风格卡.md` |
| `knowledge/` | 风格词典、讲解动画通用规则、动效和画面变化、从 11 套里学到的 |
| `examples/token/` | Token 例子的分镜、字幕、时间线（口播.wav 未收录） |

## 使用

读 `SKILL.md`。先跑环境自检：

```bash
node skills/dashi-animationstyle/pipeline/自检.mjs
```

写页面时 **不要往本目录写东西**：作品目录建在仓库外的制作机目录（见 `video-productions/README.md`）。

## 升级 / 取回完整素材

```bash
git clone --depth 1 https://github.com/chuspeeism/dashi-animationstyle /tmp/dashi-animationstyle
# 只更新代码与文档（不含展示素材）
rsync -a --exclude '.git' --exclude '.DS_Store' \
  --exclude 'docs/' --exclude '*/静帧/' --exclude '口播.wav' \
  /tmp/dashi-animationstyle/ skills/dashi-animationstyle/
```

要单独看风格动图，直接从 `/tmp/dashi-animationstyle/docs/` 打开即可，不必入库。

升级后请更新上表的 commit 与日期。
