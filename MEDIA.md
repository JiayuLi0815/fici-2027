# 媒体素材库数据说明

数据文件：`content/media.json`。前端在 `assets/media.js` 中读取，列表页与详情页都由它渲染。

素材库是独立的内部页面（`media.html`），不进入官网导航、首页或页脚，页面带 `noindex`；与嘉宾欢迎页互不链接，只能通过直接链接访问。

## 顶层结构

```json
{
  "updated": "2026-11-23",
  "credit": "素材版权归……媒体使用时请注明来源。",
  "sections": []
}
```

| 字段 | 说明 |
| --- | --- |
| `updated` | 素材库最近更新日期，显示在页面顶部 |
| `credit` | 版权与转载说明，显示在每条详情底部 |
| `sections` | 板块数组，顺序即页面顺序，也是顶部跳转栏的顺序 |

## 板块

```json
{
  "id": "main",
  "name": "主论坛",
  "en": "Main Forum",
  "lead": "板块简介，一句话即可",
  "groups": {
    "materials": [],
    "reports": []
  }
}
```

| 字段 | 说明 |
| --- | --- |
| `id` | URL 参数用，英文小写，不要重复 |
| `name` / `en` | 中英文名称 |
| `lead` | 板块简介，显示在素材库首页与列表页 |
| `groups.materials` | 活动简介及素材集锦 |
| `groups.reports` | 相关报道 |

主题论坛按场次拆成 10 个独立板块（`theme-01` … `theme-10`），每个分论坛的图片与新闻稿分开归档。新增分论坛时照此增加一个板块即可，`short` 用于顶部跳转栏的短标签。

## 素材条目

### 图片 / 图集

```json
{
  "id": "main-forum-01",
  "title": "主论坛现场（第一批）",
  "date": "2027-01-09",
  "kind": "gallery",
  "source": "2027新年论坛组委会",
  "summary": "主论坛开幕式与主旨演讲现场图片，共 12 张。",
  "images": [
    {
      "src": "uploads/program/20270109-main-forum-01.jpg",
      "cap": "主论坛现场",
      "file": "uploads/program/20270109-main-forum-01.jpg"
    }
  ],
  "files": [
    {
      "name": "主论坛现场图集（ZIP）",
      "href": "uploads/doc/20270109-main-forum-photos.zip",
      "meta": "ZIP · 48.6 MB"
    }
  ]
}
```

- `images`：详情页图片网格；`src` 是展示图，`file` 是“下载原图”的地址，可以相同。
- `files`：详情页“文件下载”列表，放 ZIP、PDF、DOCX 等。
- 列表页只显示 `title`、`summary`、`date`、`kind`、`source`。

### 新闻稿 / 文字稿

```json
{
  "id": "main-press-release",
  "title": "2027新年论坛主论坛新闻稿",
  "date": "2027-01-09",
  "kind": "article",
  "source": "2027新年论坛组委会",
  "summary": "一句话导语。",
  "body": [
    "第一段……",
    "第二段……"
  ],
  "files": [
    {
      "name": "新闻稿（DOCX）",
      "href": "uploads/doc/20270109-main-press.docx",
      "meta": "DOCX · 32 KB"
    }
  ]
}
```

`body` 会渲染成正文，并提供“复制全文”按钮。

### 外部报道

```json
{
  "id": "report-01",
  "title": "媒体报道标题",
  "date": "2027-01-10",
  "kind": "link",
  "source": "媒体名称",
  "url": "https://……",
  "summary": "报道摘要。"
}
```

带 `url` 的条目在列表页直接新窗口打开原文，不进入详情页。

## 字段速查

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `id` | 是 | 板块内唯一，用于详情页 URL |
| `title` | 是 | 条目标题 |
| `date` | 建议 | `YYYY-MM-DD` |
| `kind` | 建议 | `image` / `gallery` / `article` / `link` / `file`，决定列表上的类型标签 |
| `summary` | 建议 | 列表页与详情页摘要都用它 |
| `source` | 否 | 来源单位 |
| `images` | 否 | 图片数组 |
| `files` | 否 | 下载文件数组 |
| `body` | 否 | 新闻稿正文段落数组 |
| `url` | 否 | 外部报道链接，存在时列表直接跳转 |

## 上传流程

1. 按 `uploads/README.md` 的命名规则把文件放进 `uploads/` 对应目录。
2. 在 `content/media.json` 对应板块的 `groups.materials` 或 `groups.reports` 里新增条目。
3. 刷新 `media.html` 检查。素材库首页的计数与列表会自动更新。

## 接后端

`assets/media.js` 顶部：

```js
var DATA_URL = 'content/media.json';
```

改成后端接口地址即可，接口返回同样的 JSON 结构。列表页与详情页都通过 `section`、`type`、`id` 三个查询参数定位数据，后端如改为按参数返回数据，保持字段不变同样适用。
