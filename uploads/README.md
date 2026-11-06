# 素材投放目录

所有图片和文件都放这里，页面通过 `content/*.json` 里的路径引用。

## 目录

```
uploads/
  banner/     主视觉、横幅
  program/    各板块现场照片
  gallery/    论坛风采图片
  news/       新闻配图
  doc/        可下载文件（PDF / DOCX / PPT）
```

## 命名规则

`日期-栏目-简述.扩展名`，全部小写，不要用中文、空格和括号：

```
20270109-main-forum-01.jpg
20270109-main-forum-02.jpg
20261201-pingxing-forum-topic.pdf
```

## 图片规格

- 现场照片：长边 1600px 以上，JPG，单张控制在 500KB 以内；
- 新闻配图：16:9，宽 1200px；
- 展板 / 海报：保留原始尺寸，另存一份 1200px 宽的网页版一起放进来。

## 文件规格

- 文档优先 PDF（Word 转 PDF 再上传，避免不同电脑打开排版错位）；
- 需要填写的表格保留 DOCX；
- 单个文件不超过 30MB，超过请先压缩或拆分。

## 上传方式

不需要装任何软件：在 GitHub 仓库页面进入对应目录 →
`Add file` → `Upload files` → 拖进去 → `Commit changes`。
把文件名告诉负责更新页面的同学，由其在 `content/*.json` 里登记。
