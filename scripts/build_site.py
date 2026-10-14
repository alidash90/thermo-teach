#!/usr/bin/env python3
"""Regenerate the landing page and every course index from the lecture folders present.

Usage: python3 scripts/build_site.py

Reads site.json. A lecture exists when <unlisted>/<course>/lecture-N/lecture.json exists
(written by publish_lecture.py). Writes:
  index.html                      public landing page (course cards)
  <course>/index.html             public course page (lecture titles, no links to solutions)
  <unlisted>/index.html           instructor home (noindex)
  <unlisted>/<course>/index.html  instructor course page: Stage, Study Desk, PDFs per lecture
"""
import html, json, os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,600'
         '&family=IBM+Plex+Sans:wght@400;600;700&display=swap" rel="stylesheet">')
esc = html.escape


def load_site():
    with open(os.path.join(REPO, 'site.json'), encoding='utf-8') as f:
        return json.load(f)


def lectures(site, key):
    """Lecture records for one course, sorted by lecture number."""
    base = os.path.join(REPO, site['unlisted'], key)
    out = []
    if os.path.isdir(base):
        for d in os.listdir(base):
            m = re.fullmatch(r'lecture-(\d+)', d)
            meta = os.path.join(base, d, 'lecture.json')
            if m and os.path.exists(meta):
                with open(meta, encoding='utf-8') as f:
                    rec = json.load(f)
                rec['dir'] = d
                rec['n'] = int(m.group(1))
                out.append(rec)
    return sorted(out, key=lambda r: r['n'])


def page(site, title, body, depth, private=False):
    up = '../' * depth
    robots = '<meta name="robots" content="noindex,nofollow">' if private else ''
    home = up + (site['unlisted'] + '/' if private else '')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
{robots}<title>{esc(title)}</title>{FONTS}
<link rel="stylesheet" href="{up}assets/site.css"></head>
<body><header class="top"><div class="wrap"><a class="site" href="{home}">{esc(site['site_title'])}</a>
<span class="who">{esc(site['instructor'])} · {esc(site['department'])}</span></div></header>
<main><div class="wrap">
{body}
</div></main>
<footer><div class="wrap">{esc(site['instructor'])} · {esc(site['department'])}</div></footer>
</body></html>
'''


def write(rel, text):
    path = os.path.join(REPO, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def course_cards(site, with_counts):
    cards = []
    for key, c in site['courses'].items():
        n = len(lectures(site, key))
        count = f'<p style="margin-top:8px"><b>{n}</b> lecture{"" if n == 1 else "s"} online</p>' if with_counts else ''
        cards.append(f'<a class="card" href="{key}/"><div class="code">{esc(c["code"])}</div>'
                     f'<div class="name">{esc(c["name"])}</div><p>{esc(c["blurb"])}</p>{count}</a>')
    return '<div class="grid">' + ''.join(cards) + '</div>'


def lecture_row(rec, private):
    title = f'<div class="t"><div class="n">Lecture {rec["n"]}</div><div class="title">{esc(rec["title"])}</div>'
    if not private:
        return '<div class="lec">' + title + '</div></div>'
    meta = f'{rec.get("slides", "?")} slides · {rec.get("solves", 0)} worked problems · published {esc(rec.get("published", ""))}'
    btns = [f'<a class="btn primary" href="{rec["dir"]}/stage.html">Stage</a>']
    if rec.get('study'):
        btns.append(f'<a class="btn" href="{rec["dir"]}/study.html">Study Desk</a>')
    else:
        btns.append('<span class="btn off" title="No study.html in the build folder yet">Study Desk: not built</span>')
    for p in rec.get('pdfs', []):
        btns.append(f'<a class="btn" href="{rec["dir"]}/pdf/{esc(p["file"])}">{esc(p["label"])}</a>')
    return (f'<div class="lec">{title}<div class="meta">{meta}</div></div>'
            f'<div class="btns">{"".join(btns)}</div></div>')


def course_page(site, key, private):
    c = site['courses'][key]
    recs = lectures(site, key)
    rows = ''.join(lecture_row(r, private) for r in recs) or '<p class="empty">No lectures online yet.</p>'
    note = ('' if private else
            '<p class="lead">Lecture materials are presented in class. Course announcements, '
            'assessments and grades are on AU EduLearn.</p>')
    crumb = '<div class="crumb"><a href="../">All courses</a></div>'
    body = (f'{crumb}<h1>{esc(c["code"])} · {esc(c["name"])}</h1>'
            f'<p class="lead">{esc(c["blurb"])} Textbook: {esc(c["book"])}.</p>{note}'
            f'<h2>Lectures</h2>{rows}')
    title = f'{c["code"]} {c["name"]}' + (' · Instructor' if private else '')
    return page(site, title, body, 2 if private else 1, private)


def main():
    site = load_site()
    u = site['unlisted']
    write('index.html', page(site, site['site_title'],
          '<h1>Thermodynamics</h1><p class="lead">Course pages for Thermodynamics I and II, '
          f'{esc(site["department"])}.</p>' + course_cards(site, False), 0))
    write(f'{u}/index.html', page(site, 'Instructor home',
          '<h1>Instructor home</h1><p class="lead">Unlisted page: Lecture Stage and Study Desk for every '
          'published lecture. Bookmark it; it is not linked from the public pages.</p>'
          + course_cards(site, True), 1, True))
    for key in site['courses']:
        write(f'{key}/index.html', course_page(site, key, False))
        write(f'{u}/{key}/index.html', course_page(site, key, True))
    print('site indexes rebuilt:', ', '.join(f'{k} ({len(lectures(site, k))} lectures)' for k in site['courses']))


if __name__ == '__main__':
    main()
