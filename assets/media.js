/* =========================================================
   2027 新年论坛 — 媒体素材库
   数据源：content/media.json
   接入后端时，只需把 DATA_URL 换成接口地址，返回结构保持一致。
   ========================================================= */
(function () {
  'use strict';

  var DATA_URL = 'content/media.json';
  var GROUPS = {
    materials: { name: '活动简介及素材集锦', short: '素材集锦', desc: '现场图片、新闻稿件与可下载文件' },
    reports: { name: '相关报道', short: '相关报道', desc: '官方媒体发布与转载报道' }
  };
  var KINDS = { image: '图片', gallery: '图集', article: '新闻稿', link: '报道', file: '文件' };

  var cache = null;
  var lightbox = null;
  var lightboxItems = [];
  var lightboxIndex = 0;

  /* ---------- 工具 ---------- */
  function $(id) { return document.getElementById(id); }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function param(name) {
    try { return new URLSearchParams(location.search).get(name); }
    catch (e) { return null; }
  }

  function pad(n) { return (n < 10 ? '0' : '') + n; }

  function loadData() {
    if (!cache) {
      cache = fetch(DATA_URL, { cache: 'no-cache' }).then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      });
    }
    return cache;
  }

  function groupItems(sec, type) {
    return (sec && sec.groups && sec.groups[type]) || [];
  }

  function totalOf(sec) {
    return groupItems(sec, 'materials').length + groupItems(sec, 'reports').length;
  }

  function listHref(sec, type) {
    return 'media-list.html?section=' + encodeURIComponent(sec.id) + '&type=' + encodeURIComponent(type);
  }

  function detailHref(sec, type, item) {
    return 'media-detail.html?section=' + encodeURIComponent(sec.id) +
      '&type=' + encodeURIComponent(type) + '&id=' + encodeURIComponent(item.id);
  }

  function itemHref(sec, type, item) {
    return item.url ? item.url : detailHref(sec, type, item);
  }

  function isExternal(item) { return !!item.url; }

  function findSection(data, id) {
    for (var i = 0; i < data.sections.length; i++) {
      if (data.sections[i].id === id) return data.sections[i];
    }
    return null;
  }

  function findItem(sec, type, id) {
    var arr = groupItems(sec, type);
    for (var i = 0; i < arr.length; i++) {
      if (arr[i].id === id) return arr[i];
    }
    return null;
  }

  function errorBlock(title, text, backHref) {
    return '<div class="media-empty">' +
      '<p class="media-empty-title">' + esc(title) + '</p>' +
      '<p>' + esc(text) + '</p>' +
      '<p class="media-empty-action"><a class="btn-ghost" href="' + esc(backHref || 'media.html') + '">返回媒体素材库</a></p>' +
      '</div>';
  }

  /* ---------- 媒体素材库首页 ---------- */
  function renderIndex(data) {
    var sectionsEl = $('mediaSections');
    var jumpEl = $('mediaJump');
    if (!sectionsEl) return;

    var total = 0;
    var jump = [];
    var html = '';

    data.sections.forEach(function (sec, i) {
      var m = groupItems(sec, 'materials').length;
      var r = groupItems(sec, 'reports').length;
      total += m + r;

      jump.push('<a class="media-jump-link" href="#sec-' + esc(sec.id) + '" title="' + esc(sec.name) + '">' +
        esc(sec.short || sec.name) + '<i>' + (m + r) + '</i></a>');

      html += '<article class="media-sec" id="sec-' + esc(sec.id) + '">' +
        '<header class="media-sec-head">' +
          '<span class="media-sec-index" aria-hidden="true">' + pad(i + 1) + '</span>' +
          '<div class="media-sec-title">' +
            '<h2>' + esc(sec.name) + '</h2>' +
            '<p class="media-sec-en">' + esc(sec.en || '') + '</p>' +
          '</div>' +
          '<p class="media-sec-lead">' + esc(sec.lead || '') + '</p>' +
        '</header>' +
        '<div class="media-entries">' +
          entryCard(sec, 'materials', m) +
          entryCard(sec, 'reports', r) +
        '</div>' +
      '</article>';
    });

    sectionsEl.innerHTML = html;
    jumpEl.innerHTML = jump.join('');

    if ($('mediaUpdated')) $('mediaUpdated').textContent = data.updated || '—';
    if ($('mediaTotal')) $('mediaTotal').textContent = total;
  }

  function entryCard(sec, type, count) {
    var g = GROUPS[type];
    return '<a class="media-entry' + (count ? '' : ' is-empty') + '" href="' + esc(listHref(sec, type)) + '">' +
      '<span class="media-entry-top">' +
        '<span class="media-entry-k">' + esc(g.name) + '</span>' +
        '<span class="media-entry-n">' + (count ? count + ' 项' : '暂无') + '</span>' +
      '</span>' +
      '<span class="media-entry-d">' + esc(g.desc) + '</span>' +
      '<span class="media-entry-go">' + (count ? '查看' : '进入') + ' <span aria-hidden="true">→</span></span>' +
    '</a>';
  }

  /* ---------- 素材列表 ---------- */
  function renderList(data) {
    var listEl = $('mediaList');
    if (!listEl) return;

    var sections = data.sections;
    var sec = findSection(data, param('section')) || sections[0];
    var type = param('type');
    if (type !== 'materials' && type !== 'reports') type = 'materials';
    if (!sec) {
      listEl.innerHTML = errorBlock('未找到该板块', '该板块可能已调整，请返回素材库重新选择。');
      return;
    }

    var g = GROUPS[type];
    var items = groupItems(sec, type);
    var listUrl = listHref(sec, type);

    document.title = sec.name + ' · ' + g.name + ' | 媒体素材库';
    if ($('listTitle')) $('listTitle').textContent = sec.name;
    if ($('listEyebrow')) $('listEyebrow').textContent = g.name;
    if ($('listLead')) $('listLead').textContent = sec.lead || '';
    if ($('listCrumb')) {
      $('listCrumb').innerHTML =
        '<a href="index.html">首页</a><span>/</span>' +
        '<a href="media.html">媒体素材</a><span>/</span>' +
        '<span class="crumb-now">' + esc(sec.name) + '</span>';
    }

    if ($('mediaTabs')) {
      $('mediaTabs').innerHTML = ['materials', 'reports'].map(function (t) {
        return '<a class="media-tab' + (t === type ? ' is-active' : '') + '" href="' + esc(listHref(sec, t)) + '">' +
          esc(GROUPS[t].name) + '<span>' + groupItems(sec, t).length + '</span></a>';
      }).join('');
    }

    if ($('mediaCount')) {
      $('mediaCount').textContent = items.length ? '共 ' + items.length + ' 项' : '';
    }

    if (!items.length) {
      listEl.innerHTML = '<div class="media-empty">' +
        '<p class="media-empty-title">该板块素材正在整理</p>' +
        '<p>素材上传后将在此更新，供媒体报道使用。</p>' +
        '<p class="media-empty-action">' +
          '<a class="btn-ghost" href="' + esc(listHref(sec, type === 'materials' ? 'reports' : 'materials')) + '">' +
            '查看' + esc(GROUPS[type === 'materials' ? 'reports' : 'materials'].name) +
          '</a>' +
        '</p>' +
      '</div>';
      return;
    }

    listEl.innerHTML = items.map(function (item) {
      var href = itemHref(sec, type, item);
      return '<a class="media-row" href="' + esc(href) + '"' +
        (isExternal(item) ? ' target="_blank" rel="noopener"' : '') + '>' +
        '<span class="media-row-main">' +
          '<span class="media-row-kicker">' +
            '<span class="media-kind">' + esc(KINDS[item.kind] || '素材') + '</span>' +
            (item.source ? '<span class="media-row-source">' + esc(item.source) + '</span>' : '') +
          '</span>' +
          '<span class="media-row-title">' + esc(item.title) + '</span>' +
          (item.summary ? '<span class="media-row-sum">' + esc(item.summary) + '</span>' : '') +
        '</span>' +
        '<span class="media-row-side">' +
          '<time>' + esc(item.date || '') + '</time>' +
          '<span class="media-row-go">' + (isExternal(item) ? '阅读 ↗' : '查看 →') + '</span>' +
        '</span>' +
      '</a>';
    }).join('');

    var back = document.querySelector('.media-back a');
    if (back) back.href = 'media.html';
  }

  /* ---------- 素材详情 ---------- */
  function renderDetail(data) {
    var wrap = $('mediaDetail');
    if (!wrap) return;

    var sec = findSection(data, param('section'));
    var type = param('type') === 'reports' ? 'reports' : 'materials';
    var item = sec ? findItem(sec, type, param('id')) : null;

    if (!sec || !item) {
      wrap.innerHTML = errorBlock('未找到该素材', '素材可能已更新或调整，请返回素材库重新选择。');
      return;
    }

    document.title = item.title + ' | 媒体素材库';
    if ($('detailTitle')) $('detailTitle').textContent = item.title;
    if ($('detailEyebrow')) $('detailEyebrow').textContent = (KINDS[item.kind] || '素材') + ' · ' + GROUPS[type].short;
    if ($('detailCrumb')) {
      $('detailCrumb').innerHTML =
        '<a href="index.html">首页</a><span>/</span>' +
        '<a href="media.html">媒体素材</a><span>/</span>' +
        '<a href="' + esc(listHref(sec, type)) + '">' + esc(sec.name) + '</a><span>/</span>' +
        '<span class="crumb-now">' + esc(GROUPS[type].short) + '</span>';
    }
    if ($('detailBack')) {
      $('detailBack').innerHTML = '<a class="btn-ghost" href="' + esc(listHref(sec, type)) + '">← 返回' + esc(sec.name) + GROUPS[type].short + '</a>';
    }

    var html = '<div class="media-detail-meta">' +
      (item.date ? '<span>' + esc(item.date) + '</span>' : '') +
      (item.source ? '<span>' + esc(item.source) + '</span>' : '') +
      '<span>' + esc(KINDS[item.kind] || '素材') + '</span>' +
    '</div>';

    if (item.summary) html += '<p class="media-detail-sum">' + esc(item.summary) + '</p>';

    if (item.body && item.body.length) {
      html += '<div class="media-article">' +
        item.body.map(function (p) { return '<p>' + esc(p) + '</p>'; }).join('') +
      '</div>' +
      '<p class="media-copy-row"><button class="media-copy" type="button">复制全文</button></p>';
    }

    if (item.images && item.images.length) {
      html += '<section class="media-gallery-sec"><h2>图片素材</h2>' +
        '<div class="media-gallery' + (item.images.length === 1 ? ' is-single' : '') + '">' +
          item.images.map(function (img, i) {
            return '<figure class="media-shot">' +
              '<button class="media-shot-btn" type="button" data-index="' + i + '" aria-label="放大查看：' + esc(img.cap || '素材图片') + '">' +
                '<img src="' + esc(img.src) + '" alt="' + esc(img.cap || '') + '" loading="lazy">' +
              '</button>' +
              '<figcaption>' +
                '<span>' + esc(img.cap || '') + '</span>' +
                (img.file ? '<a href="' + esc(img.file) + '" download>下载原图</a>' : '') +
              '</figcaption>' +
            '</figure>';
          }).join('') +
        '</div></section>';
    }

    if (item.files && item.files.length) {
      html += '<section class="media-files-sec"><h2>文件下载</h2><ul class="media-files">' +
        item.files.map(function (f) {
          return '<li><span class="media-file-ico">' + esc(fileIco(f.name, f.meta)) + '</span>' +
            '<span class="media-file-name">' + esc(f.name) + '</span>' +
            '<span class="media-file-meta">' + esc(f.meta || '') + '</span>' +
            '<a class="media-file-dl" href="' + esc(f.href) + '" download>下载</a></li>';
        }).join('') +
      '</ul></section>';
    }

    if (item.url) {
      html += '<p class="media-detail-link"><a class="btn-solid" href="' + esc(item.url) + '" target="_blank" rel="noopener">查看原文 ↗</a></p>';
    }

    html += '<p class="media-credit">' + esc(data.credit || '') + '</p>';

    wrap.innerHTML = html;

    var copyBtn = wrap.querySelector('.media-copy');
    if (copyBtn && item.body) {
      copyBtn.addEventListener('click', function () {
        var text = item.body.join('\n\n');
        copyText(text).then(function () {
          copyBtn.textContent = '已复制';
          setTimeout(function () { copyBtn.textContent = '复制全文'; }, 1800);
        }).catch(function () {
          copyBtn.textContent = '复制失败，请手动选择';
        });
      });
    }

    lightboxItems = item.images || [];
    var shots = wrap.querySelectorAll('.media-shot-btn');
    for (var i = 0; i < shots.length; i++) {
      shots[i].addEventListener('click', function () {
        openLightbox(parseInt(this.getAttribute('data-index'), 10) || 0);
      });
    }
  }

  function copyText(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.top = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    if (ok) return Promise.resolve();
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return Promise.reject(new Error('copy failed'));
  }

  function fileIco(name, meta) {
    var s = String(meta || name || '').toUpperCase();
    if (s.indexOf('PDF') > -1) return 'PDF';
    if (s.indexOf('DOC') > -1) return 'DOC';
    if (s.indexOf('PPT') > -1) return 'PPT';
    if (s.indexOf('ZIP') > -1 || s.indexOf('压缩') > -1) return 'ZIP';
    if (s.indexOf('JPG') > -1 || s.indexOf('JPEG') > -1) return 'JPG';
    if (s.indexOf('PNG') > -1) return 'PNG';
    return '文件';
  }

  /* ---------- 图片灯箱 ---------- */
  function ensureLightbox() {
    if (lightbox) return;
    lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.hidden = true;
    lightbox.innerHTML =
      '<button class="lightbox-close" type="button" aria-label="关闭">×</button>' +
      '<button class="lightbox-nav lightbox-prev" type="button" aria-label="上一张">‹</button>' +
      '<figure class="lightbox-figure">' +
        '<img alt="">' +
        '<figcaption><span></span><a class="lightbox-dl" href="#" download>下载原图</a></figcaption>' +
      '</figure>' +
      '<button class="lightbox-nav lightbox-next" type="button" aria-label="下一张">›</button>';
    document.body.appendChild(lightbox);

    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox || e.target.classList.contains('lightbox-close')) closeLightbox();
      if (e.target.classList.contains('lightbox-prev')) stepLightbox(-1);
      if (e.target.classList.contains('lightbox-next')) stepLightbox(1);
    });

    document.addEventListener('keydown', function (e) {
      if (lightbox.hidden) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') stepLightbox(-1);
      if (e.key === 'ArrowRight') stepLightbox(1);
    });
  }

  function openLightbox(index) {
    ensureLightbox();
    lightboxIndex = index || 0;
    updateLightbox();
    lightbox.hidden = false;
    document.body.style.overflow = 'hidden';
    lightbox.querySelector('.lightbox-close').focus();
  }

  function closeLightbox() {
    if (!lightbox) return;
    lightbox.hidden = true;
    document.body.style.overflow = '';
  }

  function stepLightbox(dir) {
    if (lightboxItems.length < 2) return;
    lightboxIndex = (lightboxIndex + dir + lightboxItems.length) % lightboxItems.length;
    updateLightbox();
  }

  function updateLightbox() {
    var img = lightboxItems[lightboxIndex];
    if (!img) return;
    var pic = lightbox.querySelector('img');
    pic.src = img.src;
    pic.alt = img.cap || '';
    lightbox.querySelector('figcaption span').textContent = img.cap || '';
    var dl = lightbox.querySelector('.lightbox-dl');
    if (img.file) { dl.href = img.file; dl.style.display = ''; }
    else { dl.style.display = 'none'; }
    var multi = lightboxItems.length > 1;
    lightbox.querySelector('.lightbox-prev').style.display = multi ? '' : 'none';
    lightbox.querySelector('.lightbox-next').style.display = multi ? '' : 'none';
  }

  /* ---------- 启动 ---------- */
  function boot() {
    loadData().then(function (data) {
      if ($('mediaSections')) renderIndex(data);
      else if ($('mediaList')) renderList(data);
      else if ($('mediaDetail')) renderDetail(data);
    }).catch(function (err) {
      var target = $('mediaSections') || $('mediaList') || $('mediaDetail');
      if (target) target.innerHTML = errorBlock('素材暂时无法加载', '请稍后刷新页面，或联系论坛组委会获取素材。');
      if (window.console && console.error) console.error('[media] 数据加载失败：', err);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
