#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成官网静态页面。

用法：  python3 tools/build.py
内容：  content/*.json
输出：  根目录下的 *.html（不要手改，会被覆盖）
"""

import json
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
esc = html.escape


def load(n):
    return json.loads((CONTENT / n).read_text(encoding="utf-8"))


SITE = load("site.json")
PROGRAMS = load("programs.json")
NEWS = load("news.json")
PUBLICATIONS = load("publications.json")
GALLERY = load("gallery.json")
DOCUMENTS = load("documents.json")
HISTORY = load("history.json")
SPEECHES = load("speeches.json")


# ------------------------------------------------------------------ 公共部件

def nav(active):
    out = []
    for n in SITE["nav"]:
        cls = ' class="is-active"' if n["href"] == active else ""
        out.append('<li><a href="%s"%s>%s</a></li>' % (n["href"], cls, esc(n["label"])))
    return "\n        ".join(out)


HEADER = """
<header class="site-header" id="siteHeader">
  <div class="nav-wrap">
    <a class="brand" href="index.html">
      <span class="brand-text">
        <strong>%s</strong>
        <small>The 24th Forum on International Cultural Industries</small>
      </span>
    </a>

    <nav class="nav" id="nav" aria-label="主导航">
      <ul class="nav-list">
        %s
      </ul>
    </nav>

    <button class="nav-toggle" id="navToggle" aria-label="打开菜单" aria-expanded="false" aria-controls="nav">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
<div class="nav-scrim" id="navScrim" hidden></div>
"""

FOOTER = """
<footer class="site-footer">
  <div class="container footer-inner">
    <div class="footer-links">
      <div>
        <p class="fl-title">快速导航</p>
        <a href="agenda.html">简要日程</a>
        <a href="program.html">论坛板块</a>
        <a href="service.html">参会服务</a>
      </div>
      <div>
        <p class="fl-title">相关链接</p>
        <a href="http://www.fici.org.cn/" target="_blank" rel="noopener">北京大学文化产业研究院</a>
        <a href="https://www.pku.edu.cn/" target="_blank" rel="noopener">北京大学</a>
        <a href="history.html">历届论坛</a>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p>© 2027 中国文化产业新年论坛组委会　保留所有权利</p>
      <p>主办单位：%s　·　承办单位：%s</p>
    </div>
  </div>
</footer>

<a class="to-top" id="toTop" href="#top" aria-label="回到顶部">↑</a>
""" % (
    esc(SITE["host"]), esc(SITE["organizer"]),
)


def shell(filename, title, desc, active, body, is_home=False):
    doc = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s</title>
<meta name="description" content="%s">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/style.css">
</head>
<body id="top"%s>

%s

<main>
%s
</main>

%s

<script src="assets/main.js"></script>
</body>
</html>
""" % (
        esc(title), esc(desc),
        "" if is_home else ' class="is-sub"',
        HEADER % (esc(SITE["brand"]), nav(active)),
        body,
        FOOTER,
    )
    (ROOT / filename).write_text(doc, encoding="utf-8")


def head(eyebrow, title, rule=True):
    r = '<span class="title-rule"><i></i><i></i><i></i></span>' if rule else ""
    return """
      <div class="section-head">
        <p class="eyebrow">%s</p>
        <h2 class="section-title">%s</h2>
        %s
      </div>""" % (esc(eyebrow), esc(title), r)


def page_hero(crumb, eyebrow, title, lead=""):
    lead_html = '<p class="page-lead">%s</p>' % esc(lead) if lead else ""
    return """
<section class="page-hero">
  <div class="container">
    <p class="crumb">%s</p>
    <p class="eyebrow">%s</p>
    <h1 class="page-title">%s</h1>
    <span class="title-rule"><i></i><i></i><i></i></span>
    %s
  </div>
</section>""" % (crumb, esc(eyebrow), esc(title), lead_html)


def shot(item):
    if item.get("img"):
        inner = '<img src="%s" alt="%s" loading="lazy">' % (
            esc(item["img"]), esc(item.get("cap", "")))
    else:
        inner = '<span class="shot-ph" aria-hidden="true"></span>'
    note = item.get("note", "")
    note_html = '<span>%s</span>' % esc(note) if note else ""
    return ('<figure class="shot">%s<figcaption><b>%s</b>%s</figcaption></figure>'
            % (inner, esc(item.get("cap", "")), note_html))


def doc_row(item):
    meta = item.get("meta", "")
    ico = "DOC" if meta.upper().startswith("DOC") else "PDF"
    if item.get("file"):
        action = '<a class="doc-dl" href="%s" download>下载</a>' % esc(item["file"])
    else:
        action = '<span class="doc-dl is-off">即将上线</span>'
    return """        <li class="doc-row">
          <span class="doc-ico" aria-hidden="true">%s</span>
          <span class="doc-title">%s</span>
          <span class="doc-meta">%s</span>
          %s
        </li>""" % (ico, esc(item["title"]), esc(meta), action)


def doc_list(items, empty=""):
    if not items:
        return '<p class="micro-note">%s</p>' % esc(empty)
    return '<ul class="doc-list">\n%s\n      </ul>' % "\n".join(doc_row(i) for i in items)


def agenda_cols(days):
    cols = []
    for d in days:
        items = "\n".join(
            '<li><time>%s</time><div><p class="ag-title">%s</p><p class="ag-meta">%s</p></div></li>'
            % (esc(it["time"]), esc(it["title"]), esc(it["meta"]))
            for it in d["items"])
        cols.append("""
        <div class="agenda-day">
          <div class="agenda-day-head">
            <span class="day-index">%s</span>
            <span class="day-date">%s</span>
          </div>
          <ol class="agenda-list">
%s
          </ol>
        </div>""" % (esc(d["day"]), esc(d["date"]), items))
    return '<div class="agenda-grid">%s\n      </div>' % "".join(cols)


# ------------------------------------------------------------------ 首页

def build_index():
    about = """
<section class="section" id="about">
  <div class="container">
    <div class="about-grid">
      <div class="about-body">
%s
        <p>中国文化产业新年论坛创办于 2003 年，由北京大学主办、北京大学文化产业研究院承办，是国内最早发起、持续关注中国文化产业发展的专业论坛之一。论坛以促进文化产业领域内政府、企业与学界之间的交流为宗旨，坚持“学术与现实的交融、战略与发展的创新”的发展理念，致力于推动文化产业重大政策、前沿理论与产业实践的互动发展。第二十四届论坛将在往届基础上进一步聚焦年度主题的学理阐释与实践路径，围绕主论坛、平行论坛、专题对话等板块组织研讨。</p>
      </div>

      <aside class="about-aside">
        <div class="countdown-card">
          <p class="cd-eyebrow">距离论坛开幕</p>
          <p class="cd-num" id="countdown" aria-live="polite">—</p>
          <p class="cd-unit">天</p>
          <p class="cd-date">2027.01.09 · 北京</p>
        </div>
        <div class="aside-note">
          <p class="aside-note-title">参会提示</p>
          <p>本届论坛参会报名、媒体注册与议程发布通道将于近期开放，具体安排以组委会公告为准。</p>
          <a class="btn-ghost" href="service.html">查看参会服务</a>
        </div>
      </aside>
    </div>
  </div>
</section>""" % head("About the Forum", "论坛简介")

    cards = []
    for i, p in enumerate(PROGRAMS):
        main = " prog-card-main" if p["slug"] == "main" else ""
        cards.append("""
      <a class="prog-card%s" href="program-%s.html">
        <span class="chip">%s</span>
        <h3>%s</h3>
        <p class="prog-en">%s</p>
        <p class="prog-desc">%s</p>
        <span class="prog-cta">板块详情 <span aria-hidden="true">→</span></span>
      </a>""" % (main, p["slug"], esc(p["badge"]), esc(p["name"]), esc(p["en"]), esc(p["lead"])))

    program = """
<section class="section section-alt" id="program">
  <div class="container">
%s
    <div class="program-grid">%s
    </div>
  </div>
</section>""" % (head("Forum Sessions", "论坛板块"), "".join(cards))

    news_cards = []
    for n in NEWS[:3]:
        news_cards.append("""
      <a class="news-card" href="news.html">
        <div class="ph-media news-thumb"></div>
        <div class="news-card-body">
          <div class="news-meta"><time>%s</time></div>
          <h3>%s</h3>
          <p>%s</p>
        </div>
      </a>""" % (esc(n["date"]), esc(n["title"]), esc(n["summary"])))
    news = """
<section class="section" id="news">
  <div class="container">
    <div class="section-head section-head-row">
      <div>
        <p class="eyebrow">Latest News</p>
        <h2 class="section-title">最新消息</h2>
        <span class="title-rule"><i></i><i></i><i></i></span>
      </div>
      <a class="more-link" href="news.html">全部消息<span aria-hidden="true">→</span></a>
    </div>
    <div class="news-grid">%s
    </div>
  </div>
</section>""" % "".join(news_cards)

    photos = [shot(g) for g in GALLERY[:4]]
    gallery = """
<section class="section section-alt" id="gallery">
  <div class="container">
    <div class="section-head section-head-row">
      <div>
        <p class="eyebrow">Moments</p>
        <h2 class="section-title">论坛风采</h2>
        <span class="title-rule"><i></i><i></i><i></i></span>
      </div>
      <a class="more-link" href="gallery.html">全部图片<span aria-hidden="true">→</span></a>
    </div>
    <div class="shot-grid shot-grid--4">%s
    </div>
  </div>
</section>""" % "\n      ".join(photos)

    service = """
<section class="section" id="service">
  <div class="container">
%s
    <div class="service-grid">
      <a class="service-card" href="service.html">
        <span class="svc-icon" aria-hidden="true">◎</span>
        <h3>会场与交通</h3>
        <p>会场地址、交通指引与校园平面图，会前随议程一并发布。</p>
        <span class="svc-link">查看详情 →</span>
      </a>
      <a class="service-card" href="service.html">
        <span class="svc-icon" aria-hidden="true">✎</span>
        <h3>在线报名</h3>
        <p>参会报名与媒体注册通道，预计于 2026 年 12 月开放。</p>
        <span class="svc-link">查看详情 →</span>
      </a>
      <a class="service-card" href="service.html">
        <span class="svc-icon" aria-hidden="true">↓</span>
        <h3>下载专区</h3>
        <p>论坛手册、征稿启事、参会表格等文件集中下载。</p>
        <span class="svc-link">查看详情 →</span>
      </a>
    </div>

    <div class="contact-band">
      <div>
        <p class="contact-label">组委会联系方式</p>
        <p class="contact-line">%s　·　%s</p>
      </div>
      <a class="btn-solid" href="service.html">参会服务</a>
    </div>
  </div>
</section>""" % (head("Attendance", "参会服务"), esc(SITE["contact"]["secretariat"]), esc(SITE["contact"]["address"]))

    hero = """
<section class="hero" aria-label="主视觉">
  <div class="hero-poster-wrap">
    <img class="hero-poster" src="assets/hero-poster.png" alt="2027第二十四届中国文化产业新年论坛主视觉海报" width="2002" height="858">
  </div>
  <div class="hero-bar" aria-hidden="true"></div>
</section>"""

    shell("index.html",
          "%s | %s" % (SITE["name"], SITE["nameEn"]),
          "%s，主题：%s。%s，%s。主办单位：%s；承办单位：%s。"
          % (SITE["name"], SITE["theme"], SITE["dateFull"], SITE["place"],
             SITE["host"], SITE["organizer"]),
          "index.html",
          hero + about + program + news + gallery + service,
          is_home=True)


# ------------------------------------------------------------------ 最新消息

def build_news():
    rows = []
    for n in NEWS:
        rows.append("""
      <li class="news-row">
        <div class="news-row-date"><b>%s</b><span>%s</span></div>
        <div class="news-row-body">
          <h3>%s</h3>
          <p>%s</p>
        </div>
      </li>""" % (esc(n["date"][5:].replace("-", ".")), esc(n["date"][:4]),
                  esc(n["title"]), esc(n["summary"])))
    body = page_hero('<a href="index.html">首页</a><span>/</span>最新消息',
                     "Latest News", "最新消息") + """
<section class="section">
  <div class="container">
    <ul class="news-rows">%s
    </ul>
  </div>
</section>""" % "".join(rows)
    shell("news.html", "最新消息 | %s" % SITE["name"],
          "2027第二十四届中国文化产业新年论坛最新公告、学术动态与媒体报道。",
          "news.html", body)


# ------------------------------------------------------------------ 简要日程

def build_agenda():
    merged = {}
    for p in PROGRAMS:
        for d in p["agenda"]:
            slot = merged.setdefault(d["date"], {"day": d["day"], "date": d["date"], "slots": {}})
            for it in d["items"]:
                slot["slots"].setdefault(it["time"], []).append(
                    dict(it, owner=p["name"]))
    days = [merged[k] for k in sorted(merged)]

    cols = []
    for d in days:
        rows = []
        for t in sorted(d["slots"]):
            entries = "\n".join(
                '<p class="ag-title">%s</p><p class="ag-meta">%s　·　%s</p>'
                % (esc(it["title"]), esc(it["owner"]), esc(it["meta"]))
                for it in d["slots"][t])
            rows.append('<li><time>%s</time><div>%s</div></li>' % (esc(t), entries))
        cols.append("""
        <div class="agenda-day">
          <div class="agenda-day-head">
            <span class="day-index">%s</span>
            <span class="day-date">%s</span>
          </div>
          <ol class="agenda-list">
%s
          </ol>
        </div>""" % (esc(d["day"]), esc(d["date"]), "\n".join(rows)))

    body = page_hero('<a href="index.html">首页</a><span>/</span>简要日程',
                     "Programme at a Glance", "简要日程",
                     "以下为日程框架，各环节的具体时间、地点与出席嘉宾以组委会正式公布为准。") + """
<section class="section">
  <div class="container">
    <div class="agenda-grid">%s
    </div>
  </div>
</section>""" % "".join(cols)
    shell("agenda.html", "简要日程 | %s" % SITE["name"],
          "2027第二十四届中国文化产业新年论坛日程安排。", "agenda.html", body)


# ------------------------------------------------------------------ 论坛板块总览

def build_program():
    cards = []
    for p in PROGRAMS:
        main = " prog-card-main" if p["slug"] == "main" else ""
        cards.append("""
      <a class="prog-card%s" href="program-%s.html">
        <span class="chip">%s</span>
        <h3>%s</h3>
        <p class="prog-en">%s</p>
        <p class="prog-desc">%s</p>
        <span class="prog-cta">板块详情 <span aria-hidden="true">→</span></span>
      </a>""" % (main, p["slug"], esc(p["badge"]), esc(p["name"]), esc(p["en"]), esc(p["lead"])))
    body = page_hero('<a href="index.html">首页</a><span>/</span>论坛板块',
                     "Forum Sessions", "论坛板块",
                     "本届论坛设六个板块，分别面向全体会议、并行议题、产业实践、青年学术、政策研判与成果发布。") + """
<section class="section">
  <div class="container">
    <div class="program-grid">%s
    </div>
  </div>
</section>""" % "".join(cards)
    shell("program.html", "论坛板块 | %s" % SITE["name"],
          "2027第二十四届中国文化产业新年论坛板块设置。", "program.html", body)


def build_program_page(p):
    topics = "".join('<li>%s</li>' % esc(t) for t in p["topics"])
    body = page_hero('<a href="index.html">首页</a><span>/</span>'
                     '<a href="program.html">论坛板块</a><span>/</span>%s' % esc(p["name"]),
                     p["en"], p["name"]) + """
<section class="section">
  <div class="container">

    <div class="page-prose">
%s
    </div>

    <h3 class="sub-title">议题方向</h3>
    <ul class="topic-list">%s</ul>

    <h3 class="sub-title">议程安排</h3>
    %s
    <p class="micro-note">具体时间、地点与出席嘉宾以组委会正式公布为准。</p>

    <h3 class="sub-title">现场图片</h3>
    <div class="shot-grid">%s
    </div>

    <h3 class="sub-title">相关文件</h3>
    %s

    <a class="back-link" href="program.html">← 返回论坛板块</a>
  </div>
</section>""" % (
        "      <p>%s</p>" % esc("".join([p["lead"]] + p["intro"])),
        topics,
        agenda_cols(p["agenda"]),
        "\n      ".join(shot(i) for i in p["images"]),
        doc_list(p["docs"], "相关文件将陆续发布。"),
    )
    shell("program-%s.html" % p["slug"], "%s | %s" % (p["name"], SITE["name"]),
          "%s：%s" % (p["name"], p["lead"][:60]), "program.html", body)


# ------------------------------------------------------------------ 演讲集萃

def build_speeches():
    body = page_hero('<a href="index.html">首页</a><span>/</span>演讲集萃',
                     "Speeches", "演讲集萃") + """
<section class="section">
  <div class="container">
    <div class="shot-grid">%s
    </div>
    <p class="micro-note">更多往届演讲实录可在历届论坛专题页查阅。</p>
  </div>
</section>""" % "\n      ".join(shot(dict(s, note=s.get("topic", ""))) for s in SPEECHES)
    shell("speeches.html", "演讲集萃 | %s" % SITE["name"],
          "2027第二十四届中国文化产业新年论坛演讲嘉宾与往届演讲影像。", "speeches.html", body)


# ------------------------------------------------------------------ 出版物

def build_publication():
    cards = []
    for i, p in enumerate(PUBLICATIONS):
        if p.get("file"):
            action = '<a class="pub-dl" href="%s" download>下载 PDF</a>' % esc(p["file"])
        else:
            action = '<span class="pub-dl is-off">%s</span>' % esc(p.get("meta", ""))
        cards.append("""
      <article class="pub-card">
        <div class="ph-cover cover-%d"></div>
        <div class="pub-body">
          <span class="chip">%s</span>
          <h3>%s</h3>
          <p>%s</p>
          %s
        </div>
      </article>""" % ((i % 3) + 1, esc(p["tag"]), esc(p["title"]), esc(p["desc"]), action))
    body = page_hero('<a href="index.html">首页</a><span>/</span>出版物',
                     "Publications", "出版物") + """
<section class="section">
  <div class="container">
    <div class="pub-grid">%s
    </div>
  </div>
</section>""" % "".join(cards)
    shell("publication.html", "出版物 | %s" % SITE["name"],
          "中国文化产业年度发展报告、中国文化产业评论与本年度前沿报告。", "publication.html", body)


# ------------------------------------------------------------------ 论坛风采

def build_gallery():
    body = page_hero('<a href="index.html">首页</a><span>/</span>论坛风采',
                     "Moments", "论坛风采") + """
<section class="section">
  <div class="container">
    <div class="shot-grid shot-grid--wide">%s
    </div>
  </div>
</section>""" % "\n      ".join(shot(g) for g in GALLERY)
    shell("gallery.html", "论坛风采 | %s" % SITE["name"],
          "中国文化产业新年论坛历届现场影像。", "gallery.html", body)


# ------------------------------------------------------------------ 历届论坛

def build_history():
    items = []
    for h in HISTORY:
        label = h.get("year") or "专题页"
        if h["status"] == "current":
            items.append('<li class="year-current"><b>%s</b><span>%s · 本届</span></li>'
                         % (esc(h["edition"]), esc(h["year"])))
        elif h["status"] == "pending":
            items.append('<li class="year-pending"><b>%s</b><span>%s · 暂无专题页</span></li>'
                         % (esc(h["edition"]), esc(h["year"])))
        elif h["link"]:
            items.append('<li><a href="%s" target="_blank" rel="noopener"><b>%s</b><span>%s</span></a></li>'
                         % (esc(h["link"]), esc(h["edition"]), esc(label)))
        else:
            items.append('<li class="year-pending"><b>%s</b><span>%s</span></li>'
                         % (esc(h["edition"]), esc(label)))
    body = page_hero('<a href="index.html">首页</a><span>/</span>历届论坛',
                     "Past Forums", "历届论坛") + """
<section class="section">
  <div class="container">
    <ul class="year-grid">%s
    </ul>
  </div>
</section>""" % "\n      ".join(items)
    shell("history.html", "历届论坛 | %s" % SITE["name"],
          "中国文化产业新年论坛历届专题页面。", "history.html", body)


# ------------------------------------------------------------------ 参会服务

def build_service():
    body = page_hero('<a href="index.html">首页</a><span>/</span>参会服务',
                     "Attendance", "参会服务") + """
<section class="section">
  <div class="container">

    <h3 class="sub-title">会场与交通</h3>
    <div class="service-grid">
      <div class="service-card">
        <h3>会场地址</h3>
        <p>%s</p>
      </div>
      <div class="service-card">
        <h3>交通指引</h3>
        <p>地铁与公交线路、周边停车信息将随议程一并发布。</p>
      </div>
      <div class="service-card">
        <h3>校园平面图</h3>
        <p>会场位置与行进路线示意图，可在下载专区获取。</p>
      </div>
    </div>

    <h3 class="sub-title">报名与注册</h3>
    <div class="service-grid">
      <div class="service-card">
        <h3>参会报名</h3>
        <p>面向学界与产业界开放，报名通道预计于 2026 年 12 月开启。</p>
      </div>
      <div class="service-card">
        <h3>媒体注册</h3>
        <p>境内外媒体记者可提交注册申请，凭确认函领取采访证件。</p>
      </div>
      <div class="service-card">
        <h3>论文投稿</h3>
        <p>青年学者研讨会征稿，具体要求见下载专区的征稿启事。</p>
      </div>
    </div>

    <h3 class="sub-title">下载专区</h3>
    %s

    <h3 class="sub-title">联系方式</h3>
    <div class="contact-band">
      <div>
        <p class="contact-label">%s</p>
        <p class="contact-line">通讯地址：%s　·　联络方式：%s</p>
      </div>
      <a class="btn-solid" href="index.html">返回首页</a>
    </div>

  </div>
</section>""" % (
        esc(SITE["place"]),
        doc_list(DOCUMENTS, "下载文件将陆续上线。"),
        esc(SITE["contact"]["secretariat"]),
        esc(SITE["contact"]["address"]),
        esc(SITE["contact"]["channel"]),
    )
    shell("service.html", "参会服务 | %s" % SITE["name"],
          "2027第二十四届中国文化产业新年论坛参会服务：会场交通、报名注册、资料下载与联系方式。",
          "service.html", body)


# ------------------------------------------------------------------ 构建

def main():
    build_index()
    build_news()
    build_agenda()
    build_program()
    for p in PROGRAMS:
        build_program_page(p)
    build_speeches()
    build_publication()
    build_gallery()
    build_history()
    build_service()
    files = sorted(x.name for x in ROOT.glob("*.html"))
    print("已生成 %d 个页面：%s" % (len(files), "、".join(files)))


if __name__ == "__main__":
    main()
