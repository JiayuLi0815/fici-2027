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
AGENDA = load("agenda.json")
PUBLICATIONS = load("publications.json")
GALLERY = load("gallery.json")
HISTORY = load("history.json")
SPEECHES = load("speeches.json")


# ------------------------------------------------------------------ 公共部件

def nav(active):
    out = []
    for n in SITE["nav"]:
        cls = ' class="is-active"' if n["href"] == active else ""
        out.append('<li%s><a href="%s">%s</a></li>' % (cls, n["href"], esc(n["label"])))
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
        <a href="gallery.html">论坛风采</a>
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


MEDIA_HEADER = """
<header class="media-topbar">
  <div class="media-topbar-inner">
    <a class="media-brand" href="media.html">
      <span class="media-brand-mark" aria-hidden="true">24</span>
      <span class="media-brand-text">
        <strong>2027 新年论坛 · 媒体素材库</strong>
        <small>Media Library</small>
      </span>
    </a>
    <span class="media-private">媒体内部链接</span>
  </div>
</header>
"""

MEDIA_FOOTER = """
<footer class="media-footer">
  <div class="media-footer-inner">
    <p>2027 中国文化产业新年论坛组委会</p>
    <p>媒体素材库 · 仅供媒体报道使用</p>
  </div>
</footer>
"""


def media_shell(filename, title, desc, body):
    doc = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>%s</title>
<meta name="description" content="%s">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/media.css">
</head>
<body id="top" class="is-media">

%s

<main>
%s
</main>

%s

<script src="assets/media.js"></script>
</body>
</html>
""" % (esc(title), esc(desc), MEDIA_HEADER, body, MEDIA_FOOTER)
    (ROOT / filename).write_text(doc, encoding="utf-8")


def shell(filename, title, desc, active, body, is_home=False, extra_head="", extra_scripts=""):
    doc = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s</title>
<meta name="description" content="%s">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/style.css">
%s
</head>
<body id="top"%s>

%s

<main>
%s
</main>

%s

<script src="assets/main.js"></script>
%s
</body>
</html>
""" % (
        esc(title), esc(desc), extra_head,
        "" if is_home else ' class="is-sub"',
        HEADER % (esc(SITE["brand"]), nav(active)),
        body,
        FOOTER, extra_scripts,
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
        <p>中国文化产业新年论坛创办于 2003 年，由北京大学主办、北京大学文化产业研究院承办，是国内最早发起、持续关注中国文化产业发展的专业论坛之一。论坛以促进文化产业领域内政府、企业与学界之间的交流为宗旨，坚持“学术与现实的交融、战略与发展的创新”的发展理念，致力于推动文化产业重大政策、前沿理论与产业实践的互动发展。第二十四届论坛将在往届基础上进一步聚焦年度主题的学理阐释与实践路径，围绕主论坛、十场主题论坛、青年学者研讨会与智库对话组织研讨。</p>
      </div>

      <aside class="about-aside">
        <div class="countdown-card">
          <p class="cd-eyebrow">距离论坛开幕</p>
          <p class="cd-num" id="countdown" aria-live="polite">—</p>
          <p class="cd-unit">天</p>
          <p class="cd-date">2027.01.09 · 北京</p>
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
    <div class="program-grid%s">%s
    </div>
  </div>
</section>""" % (head("Forum Sessions", "论坛板块"),
                " is-even" if len(PROGRAMS) % 3 else "", "".join(cards))

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

    hero = """
<section class="hero" aria-label="主视觉">
  <div class="hero-poster-wrap">
    <img class="hero-poster" src="assets/hero-poster.jpg" alt="2027第二十四届中国文化产业新年论坛主视觉海报" width="2401" height="1030">
  </div>
  <div class="hero-bar" aria-hidden="true"></div>
</section>"""

    shell("index.html",
          "%s | %s" % (SITE["name"], SITE["nameEn"]),
          "%s，主题：%s。%s，%s。主办单位：%s；承办单位：%s。"
          % (SITE["name"], SITE["theme"], SITE["dateFull"], SITE["place"],
             SITE["host"], SITE["organizer"]),
          "index.html",
          hero + about + program + gallery,
          is_home=True)




# ------------------------------------------------------------------ 简要日程

def build_agenda():
    cols = []
    for d in AGENDA["days"]:
        rows = []
        for slot in d["slots"]:
            entries = []
            for it in slot["items"]:
                meta = "　·　".join(x for x in (it.get("host"), it.get("venue")) if x)
                block = '<p class="ag-title">%s</p>' % esc(it["title"])
                if meta:
                    block += '<p class="ag-meta">%s</p>' % esc(meta)
                if it.get("desc"):
                    block += '<p class="ag-desc">%s</p>' % esc(it["desc"])
                entries.append(block)
            rows.append('<li><time>%s</time><div>%s</div></li>'
                        % (esc(slot["time"]), "\n".join(entries)))
        cols.append("""
        <div class="agenda-day">
          <div class="agenda-day-head">
            <span class="day-index">%s<em>%s</em></span>
            <span class="day-date">%s</span>
          </div>
          <ol class="agenda-list">
%s
          </ol>
        </div>""" % (esc(d["day"]), esc(d.get("name", "")), esc(d["date"]), "\n".join(rows)))

    body = page_hero('<a href="index.html">首页</a><span>/</span>简要日程',
                     "Programme at a Glance", "简要日程", AGENDA["lead"]) + """
<section class="section">
  <div class="container">
    <div class="agenda-grid is-single">%s
    </div>
    <p class="micro-note">%s</p>
  </div>
</section>""" % ("".join(cols), esc(AGENDA["note"]))
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
                     "本届论坛由一场主论坛、十场主题论坛，以及青年学者研讨会与智库对话组成。") + """
<section class="section">
  <div class="container">
    <div class="program-grid%s">%s
    </div>
  </div>
</section>""" % (" is-even" if len(PROGRAMS) % 3 else "", "".join(cards))
    shell("program.html", "论坛板块 | %s" % SITE["name"],
          "2027第二十四届中国文化产业新年论坛板块设置。", "program.html", body)


def forum_cards():
    """主题论坛十场，直接取自议程数据，避免两处维护。"""
    cards = []
    for day in AGENDA["days"]:
        for slot in day["slots"]:
            for it in slot["items"]:
                if not it["title"].startswith("主题论坛"):
                    continue
                name, _, theme = it["title"].partition(" · ")
                when = "%s %s" % (day["name"], slot["time"])
                place = " · ".join(x for x in (when, it.get("venue")) if x)
                detail = "　·　".join(x for x in (it.get("host"), it.get("desc")) if x)
                cards.append("""
      <article class="forum-card">
        <span class="chip">%s</span>
        <h4>%s</h4>
        <p class="arch-meta">%s</p>
        <p>%s</p>
      </article>""" % (esc(name), esc(theme), esc(place), esc(detail)))
    return '<div class="forum-grid">%s\n    </div>' % "".join(cards)


def build_program_page(p):
    blocks = []

    if p["slug"] == "theme":
        blocks.append('<h3 class="sub-title">十场主题论坛</h3>\n    %s' % forum_cards())

    if p["topics"]:
        blocks.append('<h3 class="sub-title">议题方向</h3>\n    <ul class="topic-list">%s</ul>'
                      % "".join('<li>%s</li>' % esc(t) for t in p["topics"]))

    if p["agenda"]:
        blocks.append('<h3 class="sub-title">议程安排</h3>\n    %s\n'
                      '    <p class="micro-note">具体时间、地点与出席嘉宾以组委会正式公布为准。</p>'
                      % agenda_cols(p["agenda"]))

    body = page_hero('<a href="index.html">首页</a><span>/</span>'
                     '<a href="program.html">论坛板块</a><span>/</span>%s' % esc(p["name"]),
                     p["en"], p["name"]) + """
<section class="section">
  <div class="container">

    <div class="page-prose">
      <p>%s</p>
    </div>

    %s

    <h3 class="sub-title">现场图片</h3>
    <div class="shot-grid">%s
    </div>

    <h3 class="sub-title">相关文件</h3>
    %s

    <a class="back-link" href="program.html">← 返回论坛板块</a>
  </div>
</section>""" % (
        esc("".join([p["lead"]] + p["intro"])),
        "\n\n    ".join(blocks),
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
    bb = PUBLICATIONS["bluebook"]
    iters = "".join("""
      <article class="iter-card">
        <p class="iter-ver">%s</p>
        <h4>%s</h4>
        <p>%s</p>
      </article>""" % (esc(i["ver"]), esc(i["title"]), esc(i["desc"])) for i in bb["iterations"])
    mods = "".join("""
      <div class="mod-card">
        <span class="mod-role">%s</span>
        <h4>%s</h4>
        <p>%s</p>
      </div>""" % (esc(m["role"]), esc(m["name"]), esc(m["desc"])) for m in bb["modules"])

    rp = PUBLICATIONS["report"]
    layers = "".join("""
      <div class="layer-card">
        <h4>%s</h4>
        <p>%s</p>
      </div>""" % (esc(l["name"]), esc(l["desc"])) for l in rp["layers"])
    term_blocks = []
    for lst in rp["lists"]:
        items = "".join("<li>%s</li>" % esc(x) for x in lst["items"])
        term_blocks.append("""
      <div class="term-block is-%s">
        <p class="term-head">%s</p>
        <ul class="term-list">%s</ul>
      </div>""" % (esc(lst["tone"]), esc(lst["title"]), items))

    arch = "".join("""
      <div class="arch-card">
        <span class="chip">%s</span>
        <h4>%s</h4>
        <p class="arch-meta">%s</p>
        <p>%s</p>
      </div>""" % (esc(a["tag"]), esc(a["title"]), esc(a["meta"]), esc(a["desc"]))
        for a in PUBLICATIONS["archives"])

    body = page_hero('<a href="index.html">首页</a><span>/</span>出版物',
                     "Publications", "出版物",
                     "论坛出版物包括每年一本的文化产业蓝皮书、“北大报告”，以及系列指数、白皮书与研究报告。"
                     "多数成果在论坛上首次发布。") + """
<section class="section">
  <div class="container">

    <h3 class="sub-title">%s</h3>
    <p class="page-lead">%s</p>
    <div class="iter-grid">%s
    </div>
    <div class="mod-grid">%s
    </div>

    <h3 class="sub-title">%s</h3>
    <p class="page-lead">%s</p>
    <div class="layer-grid">%s
    </div>
    <div class="term-stack">%s
    </div>

    <h3 class="sub-title">历届重点成果</h3>
    <div class="arch-grid">%s
    </div>
    <p class="micro-note">%s</p>

  </div>
</section>""" % (
        esc(bb["title"]), esc(bb["lead"]), iters, mods,
        esc(rp["title"]), esc(rp["lead"]), layers, "".join(term_blocks),
        arch, esc(PUBLICATIONS["note"]),
    )
    shell("publication.html", "出版物 | %s" % SITE["name"],
          "文化产业蓝皮书、“北大报告”年度热词、特征与趋势，以及历届论坛发布的指数、白皮书与研究报告。",
          "publication.html", body)


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
    stages = {s["id"]: s for s in HISTORY["stages"]}
    phase_cards = "".join("""
      <article class="phase-card">
        <p class="phase-num">%s</p>
        <h3>%s</h3>
        <p class="phase-range">%s</p>
        <p class="phase-desc">%s</p>
        <div class="kw-list">%s</div>
      </article>""" % (esc(s["no"]), esc(s["name"]), esc(s["range"]), esc(s["desc"]),
                        "".join("<span>%s</span>" % esc(k) for k in s["keywords"]))
        for s in HISTORY["stages"])

    rows = []
    for e in HISTORY["editions"]:
        st = e["stage"]
        if st == "summit":
            rowcls = ' class="is-summit"'
            stage_html = '<span class="stage-chip is-summit">地方峰会</span>'
        elif st == "transit":
            rowcls = ""
            stage_html = '<span class="stage-chip is-transit">过渡</span>'
        else:
            rowcls = ""
            stage_html = '<span class="stage-chip">%s</span>' % esc(stages[st]["label"])
        if e.get("link"):
            ed_html = ('<a class="ed-link" href="%s" target="_blank" rel="noopener">%s'
                       '<span aria-hidden="true">↗</span></a>' % (esc(e["link"]), esc(e["edition"])))
        else:
            ed_html = '<span class="ed-plain">%s</span>' % esc(e["edition"])
        rows.append('          <tr%s><td class="ed">%s</td><td class="yr">%s</td>'
                    '<td class="thm">%s</td><td>%s</td></tr>'
                    % (rowcls, ed_html, esc(e["date"]), esc(e["theme"]), stage_html))

    miles = "".join("""
      <article class="mile-card">
        <p class="mile-year">%s</p>
        <p class="mile-meta">%s<span>·</span>%s</p>
        <h3>%s</h3>
        <p>%s</p>
      </article>""" % (esc(m["year"]), esc(m["edition"]), esc(m["tag"]), esc(m["title"]), esc(m["desc"]))
        for m in HISTORY["milestones"])

    topic_rows = "".join("""
          <tr><td class="thm" data-label="议题">%s</td><td class="yr" data-label="首次出现">%s</td><td data-label="中期演进">%s</td><td data-label="当前认知（2026）">%s</td></tr>"""
        % (esc(t["topic"]), esc(t["first"]), esc(t["mid"]), esc(t["now"])) for t in HISTORY["topics"])

    body = page_hero('<a href="index.html">首页</a><span>/</span>历届论坛',
                     "Past Forums", "历届论坛", HISTORY["lead"]) + """
<section class="section">
  <div class="container">

    <h3 class="sub-title">三个阶段</h3>
    <div class="phase-grid">%s
    </div>

    <h3 class="sub-title">历届主题（2003—2026）</h3>
    <div class="table-wrap">
      <table class="data-table is-history">
        <thead><tr><th>届次</th><th>时间</th><th>主题</th><th>阶段</th></tr></thead>
        <tbody>
%s
        </tbody>
      </table>
    </div>
    <p class="micro-note">%s</p>

    <h3 class="sub-title">里程碑届次</h3>
    <div class="mile-grid">%s
    </div>

    <h3 class="sub-title">同一议题的认知深化</h3>
    <div class="table-wrap">
      <table class="data-table is-topics">
        <thead><tr><th>议题</th><th>首次出现</th><th>中期演进</th><th>当前认知（2026）</th></tr></thead>
        <tbody>%s
        </tbody>
      </table>
    </div>
    <p class="micro-note">同一个议题讨论得越久，落点越具体：从国家层面落到具体场景，从做什么落到怎么做、谁来评估。</p>

  </div>
</section>""" % (phase_cards, "\n".join(rows), esc(HISTORY["note"]), miles, topic_rows)
    shell("history.html", "历届论坛 | %s" % SITE["name"],
          "中国文化产业新年论坛历届主题、阶段演变与里程碑届次（2003—2026）。", "history.html", body)


# ------------------------------------------------------------------ 媒体素材库

def build_media():
    body = page_hero(
        '媒体素材',
        "Media Library", "媒体素材库",
        "2027 新年论坛各板块的图片、新闻稿件与相关报道，按板块集中归档，供官方媒体检索、预览和下载使用。"
    ) + """
<section class="section">
  <div class="container">

    <div class="media-toolbar">
      <p class="media-updated">更新于 <span id="mediaUpdated">—</span></p>
      <p class="media-total">共 <b id="mediaTotal">—</b> 项素材</p>
      <p class="media-toolbar-note">媒体内部链接 · 仅供报道使用</p>
    </div>

    <nav class="media-jump" id="mediaJump" aria-label="按板块浏览素材"></nav>

    <div class="media-sections" id="mediaSections" aria-live="polite">
      <p class="media-loading">素材加载中……</p>
    </div>

    <div class="media-empty" id="mediaError" hidden>
      <p class="media-empty-title">素材暂时无法加载</p>
      <p>请稍后刷新页面，或联系论坛组委会获取素材。</p>
    </div>

    <noscript>
      <div class="media-empty">
        <p class="media-empty-title">需要开启 JavaScript</p>
        <p>开启后即可按板块浏览媒体素材。</p>
      </div>
    </noscript>

  </div>
</section>"""
    media_shell("media.html", "媒体素材库 | %s" % SITE["name"],
                "2027第二十四届中国文化产业新年论坛媒体素材库：各板块现场图片、新闻稿件与相关报道，供官方媒体检索下载。",
                body)


def build_media_list():
    body = """
<section class="page-hero">
  <div class="container">
    <p class="crumb" id="listCrumb"><a href="media.html">媒体素材</a></p>
    <p class="eyebrow" id="listEyebrow">Media Library</p>
    <h1 class="page-title" id="listTitle">素材列表</h1>
    <span class="title-rule"><i></i><i></i><i></i></span>
    <p class="page-lead" id="listLead"></p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="media-list-top">
      <div class="media-tabs" id="mediaTabs"></div>
      <p class="media-count" id="mediaCount"></p>
    </div>
    <div class="media-list" id="mediaList" aria-live="polite">
      <p class="media-loading">素材加载中……</p>
    </div>
    <p class="media-back"><a class="btn-ghost" href="media.html">← 返回媒体素材库</a></p>
  </div>
</section>"""
    media_shell("media-list.html", "素材列表 | 媒体素材库 | %s" % SITE["name"],
                "2027新年论坛媒体素材列表。", body)


def build_media_detail():
    body = """
<section class="page-hero">
  <div class="container">
    <p class="crumb" id="detailCrumb"><a href="media.html">媒体素材</a></p>
    <p class="eyebrow" id="detailEyebrow">Media Library</p>
    <h1 class="page-title" id="detailTitle">素材详情</h1>
    <span class="title-rule"><i></i><i></i><i></i></span>
  </div>
</section>
<section class="section">
  <div class="container media-detail-wrap">
    <article class="media-detail" id="mediaDetail" aria-live="polite">
      <p class="media-loading">素材加载中……</p>
    </article>
    <p class="media-back" id="detailBack"><a class="btn-ghost" href="media.html">← 返回媒体素材库</a></p>
  </div>
</section>"""
    media_shell("media-detail.html", "素材详情 | 媒体素材库 | %s" % SITE["name"],
                "2027新年论坛媒体素材详情。", body)


# ------------------------------------------------------------------ 构建

def main():
    build_index()
    build_agenda()
    build_program()
    for p in PROGRAMS:
        build_program_page(p)
    build_speeches()
    build_publication()
    build_gallery()
    build_history()
    build_media()
    build_media_list()
    build_media_detail()
    files = sorted(x.name for x in ROOT.glob("*.html"))
    print("已生成 %d 个页面：%s" % (len(files), "、".join(files)))


if __name__ == "__main__":
    main()
