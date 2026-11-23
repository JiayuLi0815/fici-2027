# 2027 第二十四届中国文化产业新年论坛 · 官网

静态站点，页面由 `content/*.json` 经 `tools/build.py` 生成。

## 本地预览

```bash
cd fici-2027
python3 -m http.server 5199
```

打开 `http://localhost:5199/`。媒体素材库通过 `fetch` 读取 `content/media.json`，需要用本地服务打开，直接双击 HTML 会读不到数据。

## 文件

```
index.html            首页
agenda.html           简要日程
program.html          论坛板块
program-*.html        各板块详情（由 programs.json 生成）
media.html            媒体素材库
media-list.html       素材列表（?section=main&type=materials）
media-detail.html     素材详情（?section=main&type=materials&id=xxx）
speeches.html         演讲集萃
publication.html      出版物
gallery.html          论坛风采
history.html          历届论坛

assets/style.css      全站样式与色板
assets/media.css      媒体素材库样式
assets/main.js        导航、倒计时、滚动进场
assets/media.js       媒体素材库渲染、图片灯箱、复制全文
assets/hero-poster.jpg 主视觉海报

content/*.json        页面数据
content/media.json    媒体素材库数据
tools/build.py        生成 HTML
uploads/              图片与文件存放目录（见 uploads/README.md）
```

## 重新生成页面

```bash
python3 tools/build.py
```

会覆盖根目录下的 `*.html`（含 `media*.html`）。改导航、页脚、首页板块，请改 `content/site.json` 和 `tools/build.py`，不要直接改生成的 HTML。

## 板块

首页 / 简要日程 / 论坛板块 / 媒体素材 / 演讲集萃 / 出版物 / 论坛风采 / 历届论坛

原“参会服务”板块已整体移除。

## 媒体素材库

- 入口：`media.html`，按“论坛视觉 / 主论坛 / 主题论坛 / 青年学者研讨会 / 智库对话”分板块。
- 每个板块分两组：`materials`（活动简介及素材集锦）、`reports`（相关报道）。
- 素材文件放在 `uploads/` 下，条目登记在 `content/media.json`，字段说明见 [MEDIA.md](MEDIA.md)。
- 接后端时，把 `assets/media.js` 顶部的 `DATA_URL` 换成接口地址，返回结构保持不变即可，其余页面无需改动。

## 配色

取自主视觉配色方案（`2027新年论坛_主视觉与配色方案_RGB`），变量集中在 `style.css` 顶部 `:root`：

| 变量 | 色值 | 用途 |
| --- | --- | --- |
| `--bg` | `#F6F3FD` | 页面淡紫底色 |
| `--crimson` | `#2A3FA8` | 主色（标题、主按钮、信息条） |
| `--crimson-deep` | `#1E2F85` | 深色渐变、页脚背景 |
| `--peri` / `--peri-ink` | `#8E8AF6` / `#5A55C9` | 辅助色（小标题、链接） |
| `--rose` | `#FF448D` | 霓虹玫红点缀 |
| `--pink-soft` | `#FBEAF8` | 柔粉浅调 |
| `--cream` | `#FFF5E8` | 深色底文字、反白按钮 |

## 替换内容时注意

- 大部分板块仍是占位文案，直接替换 `content/*.json` 后重新生成即可。
- 图片位目前是渐变占位块，换成 `<img>` 时保持外层 class，宽高比会被沿用。
- 历届论坛的年份与链接已按官方站核对；第二十二、二十三届暂无专题页。
- 媒体素材库目前只有主视觉与论坛简介两条真实条目，其余板块显示“素材正在整理”，上传后在 `media.json` 登记即可。
