#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成官网的静态页面。

用法：
    python3 tools/build.py

内容全部来自 content/*.json。改完 json 跑一次这个脚本，页面就会重新生成。
生成的 html 直接提交即可，GitHub Pages / 服务器都不需要 Python 环境。
"""

import json
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

esc = html.escape


def load(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


SITE = load("site.json")
PROGRAMS = load("programs.json")
NEWS = load("news.json")
PUBLICATIONS = load("publications.json")
GALLERY = load("gallery.json")
DOCUMENTS = load("documents.json")
HISTORY = load("history.json")
SPEECHES = load("speeches.json")


# ---------------------------------------------------------------- 公共部件

def nav_html(active):
    out = []
    for item in SITE["nav"]:
        cls = ' class="is-active"' if item["href"] == active else ""
        out.append('<li><a href="%s"%s>%s</a></li>' % (item["href"], cls, esc(item["label"])))
    return "\n        ".join(out)


def footer_html():
    return """
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <p class="footer-title">%s</p>
      <p class="footer-en">%s</p>
      <p class="footer-host">主办单位：%s　·　承办单位：%s</p>
    </div>
    <div class="footer-links">
      <div>
        <p class="fl-title">栏目导航</p>
        <a href="about.html">论坛简介</a>
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
    <p>© 2027 中国文化产业新年论坛组委会　保留所有权利</p>
  </div>
</footer>
<a class="to-top" id="toTop" href="#top" aria-label="回到顶部">↑</a>
""" % (
        esc(SITE["name"]),
        esc(SITE["nameEn"]),
        esc(SITE["host"]),
        esc(SITE["organizer"]),
    )


def page(filename, title, desc, active, body, slim=True, crumb=""):
    banner_cls = "banner banner--slim" if slim else "banner"
    crumb_html = ""
    if crumb:
        crumb_html = '<p class="crumb">%s</p>' % crumb
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
<body id="top">

<header class="%s">
  <img src="assets/hero-poster.png" alt="%s" width="2002" height="858">
  <div class="banner-mobile">
    <p class="bm-en">The 24th Forum on International Cultural Industries</p>
    <p class="bm-title">2027 第二十四届<br>中国文化产业新年论坛</p>
    <p class="bm-theme">%s</p>
    <p class="bm-meta">%s　·　%s</p>
  </div>
</header>

<div class="navbar" id="navbar">
  <div class="nav-inner">
    <a class="nav-brand" href="index.html">
      <span class="nav-mark">24</span>
      <span class="nav-brand-text">%s</span>
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
</div>
<div class="nav-scrim" id="navScrim" hidden></div>

<main class="page">
  <div class="panel">
    %s
%s
  </div>
</main>

%s

<script src="assets/main.js"></script>
</body>
</html>
""" % (
        esc(title),
        esc(desc),
        banner_cls,
        esc(SITE["name"] + "主视觉海报"),
        esc(SITE["theme"]),
        esc(SITE["date"]),
        esc(SITE["place"]),
        esc(SITE["nameShort"]),
        nav_html(active),
        crumb_html,
        body,
        footer_html(),
    )
    (ROOT / filename).write_text(doc, encoding="utf-8")


def head(title, en):
    return """
    <div class="page-head">
      <h1>%s</h1>
      <p class="page-en">%s</p>
      <span class="rule"></span>
    </div>""" % (esc(title), esc(en))


def shot(item, cls=""):
    if item.get("img"):
        inner = '<img src="%s" alt="%s" loading="lazy">' % (
            esc(item["img"]), esc(item.get("cap", "")))
    else:
        inner = '<span class="shot-ph" aria-hidden="true"></span>'
    note = item.get("note", "")
    cap = item.get("cap", "")
    note_html = '<span>%s</span>' % esc(note) if note else ""
    return ('<figure class="shot %s">%s<figcaption><b>%s</b>%s</figcaption></figure>'
            % (cls, inner, esc(cap), note_html))


def doc_row(item):
    if item.get("file"):
        action = '<a class="doc-dl" href="%s" download>下载</a>' % esc(item["file"])
    else:
        action = '<span class="doc-dl is-off">即将上线</span>'
    meta = item.get("meta", "")
    ico = "DOC" if meta.upper().startswith("DOC") else "PDF"
    return """      <li class="doc-row">
        <span class="doc-ico" aria-hidden="true">%s</span>
        <span class="doc-title">%s</span>
        <span class="doc-meta">%s</span>
        %s
      </li>""" % (ico, esc(item["title"]), esc(meta), action)


def doc_list(items, empty_note=""):
    if not items:
        return '<p class="note">%s</p>' % esc(empty_note)
    return '<ul class="doc-list">\n%s\n    </ul>' % "\n".join(doc_row(i) for i in items)


def block(title, en, inner, note=""):
    note_html = '<p class="block-note">%s</p>' % esc(note) if note else ""
    return """
    <section class="block">
      <h2 class="block-title">%s<span class="block-en">%s</span></h2>
      %s
%s
    </section>""" % (esc(title), esc(en), note_html, inner)


# ---------------------------------------------------------------- 首页

def build_index():
    facts = [
        ("论坛名称", SITE["name"]),
        ("英文名称", SITE["nameEn"]),
        ("年度主题", SITE["theme"]),
        ("举办时间", SITE["dateFull"]),
        ("举办地点", SITE["place"]),
        ("主办单位", SITE["host"]),
        ("承办单位", SITE["organizer"]),
    ]
    fact_html = "\n".join(
        '<li><span class="fact-k">%s</span><span class="fact-v">%s</span></li>' % (esc(k), esc(v))
        for k, v in facts
    )

    intro = """
    <div class="page-head">
      <h1>论坛简介</h1>
      <p class="page-en">About the Forum</p>
      <span class="rule"></span>
    </div>
    <div class="intro-grid">
      <div class="intro-body">
        <p class="lede">中国文化产业新年论坛创办于 2003 年，由北京大学主办、北京大学文化产业研究院承办，是国内最早发起、持续关注中国文化产业发展的专业论坛之一。</p>
        <p>论坛以促进文化产业领域内政府、企业与学界之间的交流为宗旨，坚持“学术与现实的交融、战略与发展的创新”的发展理念，致力于推动文化产业重大政策、前沿理论与产业实践的互动发展。</p>
        <p>第二十四届论坛将在往届基础上进一步聚焦年度主题的学理阐释与实践路径，围绕主论坛、平行论坛、创意管理峰会、青年学者研讨会与智库对话等板块组织研讨。</p>
        <ul class="fact-list">
%s
        </ul>
        <a class="btn-ghost" href="about.html">查看论坛简介</a>
      </div>
      <aside class="intro-aside">
        <div class="countdown-card">
          <p class="cd-eyebrow">距离论坛开幕</p>
          <p class="cd-num" id="countdown" aria-live="polite">—</p>
          <p class="cd-unit">天</p>
          <p class="cd-date">%s · %s</p>
        </div>
        <div class="aside-note">
          <p class="aside-note-title">参会提示</p>
          <p>本届论坛参会报名、媒体注册与议程发布通道将于近期开放，具体安排见参会服务栏目。</p>
          <a class="btn-ghost" href="service.html">参会服务</a>
        </div>
      </aside>
    </div>
""" % (fact_html, esc(SITE["date"]), esc(SITE["place"]))

    entries = []
    for p in PROGRAMS:
        entries.append("""
      <a class="entry-card" href="program-%s.html">
        <span class="entry-badge">%s</span>
        <strong>%s</strong>
        <em>%s</em>
        <span class="entry-arrow" aria-hidden="true">→</span>
      </a>""" % (p["slug"], esc(p["badge"]), esc(p["name"]), esc(p["en"])))
    program_block = block("论坛板块", "Forum Sessions",
                          '<div class="entry-grid">%s\n    </div>' % "".join(entries),
                          note="点击进入各板块页面，查看议题、议程、现场图片与相关文件。")

    news_cards = []
    for n in NEWS[:3]:
        news_cards.append("""
      <a class="news-card" href="news.html">
        <div class="news-thumb"><span class="shot-ph" aria-hidden="true"></span></div>
        <div class="news-body">
          <p class="news-meta"><span class="tag">%s</span><time>%s</time></p>
          <h3>%s</h3>
          <p>%s</p>
        </div>
      </a>""" % (esc(n["tag"]), esc(n["date"]), esc(n["title"]), esc(n["summary"])))
    news_block = """
    <section class="block">
      <div class="block-head-row">
        <h2 class="block-title">最新消息<span class="block-en">Latest News</span></h2>
        <a class="more" href="news.html">全部消息 →</a>
      </div>
      <div class="news-grid">%s
      </div>
    </section>""" % "".join(news_cards)

    gallery_block = """
    <section class="block">
      <div class="block-head-row">
        <h2 class="block-title">论坛风采<span class="block-en">Moments</span></h2>
        <a class="more" href="gallery.html">全部图片 →</a>
      </div>
      <div class="shot-grid">%s
      </div>
    </section>""" % "".join(shot(g) for g in GALLERY[:4])

    service_block = """
    <section class="block">
      <h2 class="block-title">参会服务<span class="block-en">Attendance</span></h2>
      <div class="service-grid">
        <a class="service-card" href="service.html">
          <h3>会场与交通</h3>
          <p>会场地址、交通指引与校园平面图，会前随议程一并发布。</p>
        </a>
        <a class="service-card" href="service.html">
          <h3>在线报名</h3>
          <p>参会报名与媒体注册通道，预计于 2026 年 12 月开放。</p>
        </a>
        <a class="service-card" href="service.html">
          <h3>下载专区</h3>
          <p>论坛手册、征稿启事、参会表格等文件集中下载。</p>
        </a>
      </div>
    </section>"""

    body = intro + program_block + news_block + gallery_block + service_block
    page("index.html",
         "%s | %s" % (SITE["name"], SITE["nameEn"]),
         "%s，主题：%s。%s，%s。主办单位：%s；承办单位：%s。"
         % (SITE["name"], SITE["theme"], SITE["dateFull"], SITE["place"],
            SITE["host"], SITE["organizer"]),
         "index.html", body, slim=False)


# ---------------------------------------------------------------- 论坛简介

def build_about():
    body = """
    <div class="page-head">
      <h1>论坛简介</h1>
      <p class="page-en">About the Forum</p>
      <span class="rule"></span>
    </div>
    <div class="prose">
      <p class="lede">中国文化产业新年论坛创办于 2003 年，由北京大学主办、北京大学文化产业研究院承办，是国内最早发起、持续关注中国文化产业发展的专业论坛之一。</p>
      <p>论坛以促进文化产业领域内政府、企业与学界之间的交流为宗旨，坚持“学术与现实的交融、战略与发展的创新”的发展理念，致力于推动文化产业重大政策、前沿理论与产业实践的互动发展。</p>
      <p>历届论坛均围绕当年文化发展的重大问题设定年度主题，邀请国内外学者、政策制定者与产业界代表共同研讨，并通过年度报告、专题评论与前沿报告等出版物沉淀研讨成果。</p>
      <p>第二十四届论坛以“新格局：文化发展的多元共生与全球对话”为年度主题，在往届基础上进一步聚焦文化发展的多元路径、文明交流互鉴与数字技术带来的产业变革，围绕主论坛、平行论坛、创意管理峰会、青年学者研讨会与智库对话等板块组织研讨。</p>
    </div>

    <section class="block">
      <h2 class="block-title">论坛信息<span class="block-en">Fact Sheet</span></h2>
      <ul class="fact-list fact-list--wide">
        <li><span class="fact-k">论坛名称</span><span class="fact-v">%s</span></li>
        <li><span class="fact-k">英文名称</span><span class="fact-v">%s</span></li>
        <li><span class="fact-k">届　　次</span><span class="fact-v">%s</span></li>
        <li><span class="fact-k">年度主题</span><span class="fact-v">%s</span></li>
        <li><span class="fact-k">举办时间</span><span class="fact-v">%s</span></li>
        <li><span class="fact-k">举办地点</span><span class="fact-v">%s</span></li>
        <li><span class="fact-k">主办单位</span><span class="fact-v">%s</span></li>
        <li><span class="fact-k">承办单位</span><span class="fact-v">%s</span></li>
      </ul>
    </section>

    <section class="block">
      <h2 class="block-title">组织与联络<span class="block-en">Contact</span></h2>
      <div class="contact-grid">
        <div><p class="contact-k">组委会</p><p class="contact-v">%s</p></div>
        <div><p class="contact-k">通讯地址</p><p class="contact-v">%s</p></div>
        <div><p class="contact-k">联络方式</p><p class="contact-v">%s</p></div>
      </div>
    </section>
""" % (
        esc(SITE["name"]), esc(SITE["nameEn"]), esc(SITE["edition"]), esc(SITE["theme"]),
        esc(SITE["dateFull"]), esc(SITE["place"]), esc(SITE["host"]), esc(SITE["organizer"]),
        esc(SITE["contact"]["secretariat"]), esc(SITE["contact"]["address"]), esc(SITE["contact"]["channel"]),
    )
    page("about.html", "论坛简介 | %s" % SITE["name"],
         "中国文化产业新年论坛简介：创办于 2003 年，由北京大学主办、北京大学文化产业研究院承办。",
         "about.html", body, crumb='<a href="index.html">首页</a><span>/</span>论坛简介')


# ---------------------------------------------------------------- 最新消息

def build_news():
    rows = []
    for n in NEWS:
        rows.append("""
      <li class="news-row">
        <div class="news-row-date"><b>%s</b><span>%s</span></div>
        <div class="news-row-body">
          <p class="news-meta"><span class="tag">%s</span></p>
          <h3>%s</h3>
          <p>%s</p>
        </div>
      </li>""" % (esc(n["date"][5:].replace("-", ".")), esc(n["date"][:4]),
                  esc(n["tag"]), esc(n["title"]), esc(n["summary"])))
    body = head("最新消息", "Latest News") + """
    <ul class="news-rows">%s
    </ul>""" % "".join(rows)
    page("news.html", "最新消息 | %s" % SITE["name"],
         "2027第二十四届中国文化产业新年论坛最新公告、学术动态与媒体报道。",
         "news.html", body, crumb='<a href="index.html">首页</a><span>/</span>最新消息')


# ---------------------------------------------------------------- 简要日程

def build_agenda():
    days = []
    for p in PROGRAMS:
        for d in p["agenda"]:
            days.append((d, p["name"]))
    by_date = {}
    for d, name in days:
        by_date.setdefault(d["date"], {"date": d["date"], "items": [], "day": d["day"]})
        for it in d["items"]:
            by_date[d["date"]]["items"].append((it, name))

    cols = []
    for i, key in enumerate(sorted(by_date)):
        g = by_date[key]
        items = []
        for it, name in g["items"]:
            items.append("""
          <li><time>%s</time><div><p class="ag-title">%s</p><p class="ag-meta">%s　·　%s</p></div></li>"""
                         % (esc(it["time"]), esc(it["title"]), esc(name), esc(it["meta"])))
        cols.append("""
      <div class="agenda-day">
        <div class="agenda-day-head">
          <span class="day-index">Day %d</span>
          <span class="day-date">%s</span>
        </div>
        <ol class="agenda-list">%s
        </ol>
      </div>""" % (i + 1, esc(g["date"]), "".join(items)))

    body = head("简要日程", "Programme at a Glance") + """
    <div class="agenda-grid">%s
    </div>
    <p class="note">以上为日程框架，各环节的具体时间、地点与出席嘉宾以组委会正式公布为准。</p>
""" % "".join(cols)
    page("agenda.html", "简要日程 | %s" % SITE["name"],
         "2027第二十四届中国文化产业新年论坛日程安排。", "agenda.html", body,
         crumb='<a href="index.html">首页</a><span>/</span>简要日程')


# ---------------------------------------------------------------- 论坛板块总览

def build_program():
    cards = []
    for p in PROGRAMS:
        cards.append("""
      <a class="entry-card" href="program-%s.html">
        <span class="entry-badge">%s</span>
        <strong>%s</strong>
        <em>%s</em>
        <span class="entry-arrow" aria-hidden="true">→</span>
      </a>""" % (p["slug"], esc(p["badge"]), esc(p["name"]), esc(p["en"])))
    body = head("论坛板块", "Forum Sessions") + """
    <p class="lead">本届论坛设五个板块，分别面向全体会议、并行议题、产业实践、青年学术与政策研判。点击卡片进入板块页面，可查看议题方向、议程安排、现场图片与相关文件。</p>
    <div class="entry-grid">%s
    </div>
""" % "".join(cards)
    page("program.html", "论坛板块 | %s" % SITE["name"],
         "2027第二十四届中国文化产业新年论坛板块设置：主论坛、平行论坛、创意管理峰会、青年学者研讨会、智库对话。",
         "program.html", body, crumb='<a href="index.html">首页</a><span>/</span>论坛板块')


# ---------------------------------------------------------------- 单个板块

def build_program_page(p):
    topics = "".join("<li>%s</li>" % esc(t) for t in p["topics"])

    days = []
    for d in p["agenda"]:
        items = "".join(
            '<li><time>%s</time><div><p class="ag-title">%s</p><p class="ag-meta">%s</p></div></li>'
            % (esc(it["time"]), esc(it["title"]), esc(it["meta"]))
            for it in d["items"])
        days.append("""
      <div class="agenda-day">
        <div class="agenda-day-head">
          <span class="day-index">%s</span>
          <span class="day-date">%s</span>
        </div>
        <ol class="agenda-list">%s
        </ol>
      </div>""" % (esc(d["day"]), esc(d["date"]), items))

    body = """
    <p class="crumb"><a href="index.html">首页</a><span>/</span><a href="program.html">论坛板块</a><span>/</span>%s</p>
    <div class="page-head">
      <h1>%s</h1>
      <p class="page-en">%s</p>
      <span class="rule"></span>
    </div>
    <p class="lead">%s</p>
    <div class="prose">%s</div>

    <section class="block">
      <h2 class="block-title">议题方向<span class="block-en">Topics</span></h2>
      <ul class="topic-list">%s</ul>
    </section>

    <section class="block">
      <h2 class="block-title">议程安排<span class="block-en">Agenda</span></h2>
      <div class="agenda-grid">%s
      </div>
      <p class="note">具体时间、地点与出席嘉宾以组委会正式公布为准。</p>
    </section>

    <section class="block">
      <h2 class="block-title">现场图片<span class="block-en">Gallery</span></h2>
      <div class="shot-grid">%s
      </div>
    </section>

    <section class="block">
      <h2 class="block-title">相关文件<span class="block-en">Documents</span></h2>
      %s
    </section>

    <a class="back-link" href="program.html">← 返回论坛板块</a>
""" % (
        esc(p["name"]), esc(p["name"]), esc(p["en"]), esc(p["lead"]),
        "".join("<p>%s</p>" % esc(x) for x in p["intro"]),
        topics,
        "".join(days),
        "".join(shot(i) for i in p["images"]),
        doc_list(p["docs"], "相关文件将陆续发布。"),
    )
    page("program-%s.html" % p["slug"], "%s | %s" % (p["name"], SITE["name"]),
         "%s：%s" % (p["name"], p["lead"][:60]), "program.html", body)


# ---------------------------------------------------------------- 演讲集萃

def build_speeches():
    body = head("演讲集萃", "Speeches") + """
    <p class="lead">论坛历年邀请国内外文化政策、文化产业、文化科技等领域的学者与业界代表发表演讲。本届演讲嘉宾与题目将于会前陆续公布，以下为往届演讲影像选摘。</p>
    <div class="shot-grid">%s
    </div>
    <p class="note">更多往届演讲实录可在历届论坛专题页查阅。</p>
""" % "".join(shot(s) for s in SPEECHES)
    page("speeches.html", "演讲集萃 | %s" % SITE["name"],
         "2027第二十四届中国文化产业新年论坛演讲嘉宾与往届演讲影像。",
         "speeches.html", body, crumb='<a href="index.html">首页</a><span>/</span>演讲集萃')


# ---------------------------------------------------------------- 出版物

def build_publication():
    cards = []
    for p in PUBLICATIONS:
        if p.get("file"):
            action = '<a class="pub-dl" href="%s" download>下载 PDF</a>' % esc(p["file"])
        else:
            action = '<span class="pub-dl is-off">%s</span>' % esc(p.get("meta", ""))
        cards.append("""
      <article class="pub-card">
        <div class="pub-cover"><span class="shot-ph" aria-hidden="true"></span></div>
        <div class="pub-body">
          <span class="tag">%s</span>
          <h3>%s</h3>
          <p>%s</p>
          %s
        </div>
      </article>""" % (esc(p["tag"]), esc(p["title"]), esc(p["desc"]), action))
    body = head("出版物", "Publications") + """
    <p class="lead">论坛每年围绕年度主题组织编撰年度报告、专题评论与前沿报告，会议成果同步沉淀为公开出版物。</p>
    <div class="pub-grid">%s
    </div>
""" % "".join(cards)
    page("publication.html", "出版物 | %s" % SITE["name"],
         "中国文化产业年度发展报告、中国文化产业评论与本年度前沿报告。",
         "publication.html", body, crumb='<a href="index.html">首页</a><span>/</span>出版物')


# ---------------------------------------------------------------- 论坛风采

def build_gallery():
    body = head("论坛风采", "Moments") + """
    <p class="lead">以下为历届论坛现场影像，本届论坛图片将于会后陆续上传。</p>
    <div class="shot-grid shot-grid--wide">%s
    </div>
""" % "".join(shot(g) for g in GALLERY)
    page("gallery.html", "论坛风采 | %s" % SITE["name"],
         "中国文化产业新年论坛历届现场影像。", "gallery.html", body,
         crumb='<a href="index.html">首页</a><span>/</span>论坛风采')


# ---------------------------------------------------------------- 历届论坛

def build_history():
    items = []
    for h in HISTORY:
        cls = ""
        label = h.get("year") or "专题页"
        if h["status"] == "current":
            cls = " is-current"
            label = "%s · 本届" % h["year"]
            inner = "<b>%s</b><span>%s</span>" % (esc(h["edition"]), esc(label))
            items.append('<li class="year-item%s">%s</li>' % (cls, inner))
        elif h["status"] == "pending":
            label = "%s · 暂无专题页" % h["year"]
            inner = "<b>%s</b><span>%s</span>" % (esc(h["edition"]), esc(label))
            items.append('<li class="year-item is-pending">%s</li>' % inner)
        elif h["link"]:
            items.append(
                '<li class="year-item"><a href="%s" target="_blank" rel="noopener"><b>%s</b><span>%s</span></a></li>'
                % (esc(h["link"]), esc(h["edition"]), esc(label)))
        else:
            items.append('<li class="year-item is-pending"><b>%s</b><span>%s</span></li>'
                         % (esc(h["edition"]), esc(label)))
    body = head("历届论坛", "Past Forums") + """
    <p class="lead">自 2003 年创办至今，新年论坛已连续举办二十三届。点击可进入历届专题页面，回顾往届议题、嘉宾与成果。</p>
    <ul class="year-grid">%s
    </ul>
""" % "".join(items)
    page("history.html", "历届论坛 | %s" % SITE["name"],
         "中国文化产业新年论坛历届专题页面。", "history.html", body,
         crumb='<a href="index.html">首页</a><span>/</span>历届论坛')


# ---------------------------------------------------------------- 参会服务

def build_service():
    body = head("参会服务", "Attendance") + """
    <p class="lead">参会报名、媒体注册与资料下载将在本栏目统一发布。</p>

    <section class="block">
      <h2 class="block-title">会场与交通<span class="block-en">Venue</span></h2>
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
    </section>

    <section class="block">
      <h2 class="block-title">报名与注册<span class="block-en">Registration</span></h2>
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
    </section>

    <section class="block">
      <h2 class="block-title">下载专区<span class="block-en">Downloads</span></h2>
      %s
    </section>

    <section class="block">
      <h2 class="block-title">联系方式<span class="block-en">Contact</span></h2>
      <div class="contact-grid">
        <div><p class="contact-k">组委会</p><p class="contact-v">%s</p></div>
        <div><p class="contact-k">通讯地址</p><p class="contact-v">%s</p></div>
        <div><p class="contact-k">联络方式</p><p class="contact-v">%s</p></div>
      </div>
    </section>
""" % (
        esc(SITE["place"]),
        doc_list(DOCUMENTS, "下载文件将陆续上线。"),
        esc(SITE["contact"]["secretariat"]),
        esc(SITE["contact"]["address"]),
        esc(SITE["contact"]["channel"]),
    )
    page("service.html", "参会服务 | %s" % SITE["name"],
         "2027第二十四届中国文化产业新年论坛参会服务：会场交通、报名注册、资料下载与联系方式。",
         "service.html", body, crumb='<a href="index.html">首页</a><span>/</span>参会服务')


# ---------------------------------------------------------------- 构建

def main():
    build_index()
    build_about()
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
