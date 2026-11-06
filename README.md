# 2027 第二十四届中国文化产业新年论坛 · 官网

纯静态站点。每个栏目一个独立页面，页面上的图片与文件都从 `content/*.json` 读取。
没有数据库、没有后台，任何静态服务器（包括 GitHub Pages）都能直接托管。

## 页面结构

| 页面 | 导航入口 | 内容来源 |
| --- | --- | --- |
| `index.html` | 首页 | `content/site.json`、`programs.json`、`news.json`、`gallery.json` |
| `about.html` | 论坛简介 | `content/site.json` |
| `news.html` | 最新消息 | `content/news.json` |
| `agenda.html` | 简要日程 | `content/programs.json` 各板块的 `agenda` |
| `program.html` | 论坛板块 | `content/programs.json` |
| `program-main.html` 等 5 页 | 各板块 | `content/programs.json` 对应条目 |
| `speeches.html` | 演讲集萃 | `content/speeches.json` |
| `publication.html` | 出版物 | `content/publications.json` |
| `gallery.html` | 论坛风采 | `content/gallery.json` |
| `history.html` | 历届论坛 | `content/history.json` |
| `service.html` | 参会服务 | `content/documents.json`、`content/site.json` |

## 目录

```
content/     内容，全部是 json（改这里）
tools/build.py   把 json 生成为 html
assets/      样式、脚本、主视觉海报
uploads/     图片与文件，命名见 uploads/README.md
*.html       生成结果（不要手改，会被覆盖）
```

## 怎么改内容

1. 改 `content/` 下对应的 json；
2. 在项目根目录运行 `python3 tools/build.py`；
3. 页面重新生成，提交即可。

**加一条最新消息**：在 `content/news.json` 数组最前面加一项

```json
{
  "date": "2026-11-20",
  "tag": "公告",
  "title": "标题",
  "summary": "一两句话的摘要",
  "img": "uploads/news/20261120-jiedu.jpg"
}
```

`img` 留空则显示默认图形。

**给板块加一张现场照片**：在 `content/programs.json` 里找到该板块的 `images`，
加一项 `{ "img": "uploads/program/xxx.jpg", "cap": "图注", "note": "届次" }`。

**上传一个可下载文件**：把文件放进 `uploads/doc/`，然后在对应 json 的 `docs`
（或 `content/documents.json`）里把 `file` 填成 `uploads/doc/xxx.pdf`。
`file` 为空时页面显示"即将上线"。

## 配色

变量集中在 `assets/style.css` 顶部 `:root`：

| 变量 | 色值 | 用途 |
| --- | --- | --- |
| `--cream` | `#FFF9ED` | 页面底色 |
| `--crimson` | `#AB2848` | 主色（导航、标题、入口卡） |
| `--peri` / `--peri-ink` | `#738EFF` / `#4553C4` | 辅助色（英文标题、链接） |
| `--yellow` | `#FFD839` | 点缀（导航高亮、倒计时） |

主视觉海报 `assets/hero-poster.png` 换图后可整站同步更新；手机端使用文字版海报，
文字在 `tools/build.py` 的 `banner-mobile` 段内。

## 部署

- GitHub Pages：仓库 `Settings → Pages` 选 `main` / `/ (root)`，地址 `https://jiayuli0815.github.io/fici-2027/`。
- 自有服务器：把仓库内容放到站点根目录即可，无需任何运行时。
