#!/usr/bin/env python3
"""Publish one finished Lecture-Stage build to the site: copy, check, index, commit, push.

Usage:
  python3 scripts/publish_lecture.py <course> <lecture-N> [options]
  python3 scripts/publish_lecture.py mech230 lecture-3
  python3 scripts/publish_lecture.py mech330 lecture-2 --pdf "../../courses/.../PRINT_x.pdf:Problem pack"

Options:
  --title "..."        lecture title (default: the title already published, else the first slide
                       title of content.json with "Lecture N:" removed)
  --pdf FILE[:Label]   add a printable PDF to the lecture (repeatable; kept on later republishes)
  --rebuild            always rebuild stage.html with the engine, even if index.html is current
  --no-push            commit but do not push
  --dry-run            copy and index only, no git

Source:  <project_root>/courses/<COURSE>/lectures/Lecture-N/our-work/03_Lecture-Stage/
  content.json, solves.json   required (solves may be {})
  index.html                  the built Stage; rebuilt into a temp folder with the engine when missing
                              or older than content.json, solves.json or the engine template
  study.html                  the Study Desk (optional)
  img/p-NN.jpg                slide renders; fallbacks: img/ inside a *.zip in the folder, then
                              Lecture-N/au-slide-images/
Target:  <unlisted>/<course>/lecture-N/{stage.html, study.html, img/, pdf/, lecture.json}
The source folders are never written to.
"""
import argparse, datetime, json, os, re, shutil, subprocess, sys, tempfile, zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import build_site  # noqa: E402

NOINDEX = '<meta name="robots" content="noindex,nofollow">'
MATHJAX = 'cdnjs.cloudflare.com/ajax/libs/mathjax/'


def die(msg):
    sys.exit('ERROR: ' + msg)


def run(cmd, **kw):
    print('  $', ' '.join(cmd))
    return subprocess.run(cmd, check=True, **kw)


def stage_html(src, engine, code, n, title, force):
    """Return the Stage HTML: the folder's index.html when current, else a fresh engine build."""
    idx = os.path.join(src, 'index.html')
    deps = [os.path.join(src, f) for f in ('content.json', 'solves.json')] + [os.path.join(engine, 'stage_template.html')]
    newest = max(os.path.getmtime(p) for p in deps if os.path.exists(p))
    if not force and os.path.exists(idx) and os.path.getmtime(idx) >= newest:
        print('  stage: using built index.html')
        with open(idx, encoding='utf-8') as f:
            return f.read()
    print('  stage: index.html ' + ('missing' if not os.path.exists(idx) else 'older than its sources')
          + ', building with the engine')
    with tempfile.TemporaryDirectory() as tmp:
        for f in ('content.json', 'solves.json'):
            if os.path.exists(os.path.join(src, f)):
                shutil.copy2(os.path.join(src, f), tmp)
        run([sys.executable, os.path.join(engine, 'build_stage.py'), tmp, code,
             f'Lecture {n} · {title}', f'{code} Lecture {n} Stage'])
        with open(os.path.join(tmp, 'index.html'), encoding='utf-8') as f:
            return f.read()


def image_source(src, lecdir):
    """Return (kind, reader) where reader(name) -> bytes or None."""
    d = os.path.join(src, 'img')
    if os.path.isdir(d):
        return 'img/', lambda name: open(os.path.join(d, name), 'rb').read() if os.path.exists(os.path.join(d, name)) else None
    for z in sorted(f for f in os.listdir(src) if f.endswith('.zip')):
        zf = zipfile.ZipFile(os.path.join(src, z))
        members = {os.path.basename(m): m for m in zf.namelist() if re.search(r'(^|/)img/[^/]+\.jpe?g$', m)}
        if members:
            return f'{z} (img/)', lambda name, zf=zf, mm=members: zf.read(mm[name]) if name in mm else None
    d = os.path.join(lecdir, 'au-slide-images')
    if os.path.isdir(d):
        return 'au-slide-images/', lambda name: open(os.path.join(d, name), 'rb').read() if os.path.exists(os.path.join(d, name)) else None
    die('no slide images found (img/, *.zip, au-slide-images/)')


def for_web(page):
    """Make a page safe to serve as a file: full document, UTF-8, noindex.
    The Stage engine emits a fragment (claude.ai artifacts add the skeleton); add it here the same way."""
    if not page.lstrip().lower().startswith('<!doctype'):
        return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                f'{NOINDEX}\n{page}\n</html>\n')
    if NOINDEX in page:
        return page
    return re.sub(r'(<head[^>]*>)', r'\1' + NOINDEX, page, count=1, flags=re.I)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('course')
    ap.add_argument('lecture')
    ap.add_argument('--title')
    ap.add_argument('--pdf', action='append', default=[])
    ap.add_argument('--rebuild', action='store_true')
    ap.add_argument('--no-push', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)

    site = build_site.load_site()
    key = a.course.lower()
    if key not in site['courses']:
        die(f'unknown course {a.course}; known: {", ".join(site["courses"])}')
    m = re.search(r'(\d+)$', a.lecture)
    if not m:
        die('lecture must look like lecture-N')
    n = int(m.group(1))
    c = site['courses'][key]
    root = os.path.normpath(os.path.join(REPO, site['project_root']))
    lecdir = os.path.join(root, 'courses', c['folder'], 'lectures', f'Lecture-{n}')
    src = os.path.join(lecdir, 'our-work', '03_Lecture-Stage')
    engine = os.path.join(root, 'courses', '_engine', 'lecture-stage')
    if not os.path.exists(os.path.join(src, 'content.json')):
        die(f'no content.json in {src}')
    print(f'Publishing {c["code"]} lecture {n}\n  source: {os.path.relpath(src, root)}')

    with open(os.path.join(src, 'content.json'), encoding='utf-8') as f:
        content = json.load(f)
    solves = {}
    if os.path.exists(os.path.join(src, 'solves.json')):
        with open(os.path.join(src, 'solves.json'), encoding='utf-8') as f:
            solves = json.load(f)

    dest = os.path.join(REPO, site['unlisted'], key, f'lecture-{n}')
    old = {}
    if os.path.exists(os.path.join(dest, 'lecture.json')):
        with open(os.path.join(dest, 'lecture.json'), encoding='utf-8') as f:
            old = json.load(f)
    title = (a.title or old.get('title')
             or re.sub(r'^\s*Lecture\s*\d+\s*[:·.-]\s*', '', content[0].get('title', f'Lecture {n}')))
    if os.path.isdir(dest):
        for e in os.listdir(dest):
            if e != 'pdf':
                p = os.path.join(dest, e)
                shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(os.path.join(dest, 'img'), exist_ok=True)

    pages = {'stage.html': stage_html(src, engine, c['code'], n, title, a.rebuild)}
    if os.path.exists(os.path.join(src, 'study.html')):
        with open(os.path.join(src, 'study.html'), encoding='utf-8') as f:
            pages['study.html'] = f.read()
    else:
        print('  study: no study.html in the build folder; course page will show "not built"')

    warnings = []
    for f in ('content.json', 'solves.json', 'study.html'):
        p = os.path.join(src, f)
        dashes = open(p, encoding='utf-8').read().count(chr(0x2014)) if os.path.exists(p) else 0
        if dashes:
            warnings.append(f'{f}: {dashes} em dash(es); fix in the source folder, then republish')
    for name, html in pages.items():
        if MATHJAX not in html:
            warnings.append(f'{name}: MathJax from cdnjs not found')
        with open(os.path.join(dest, name), 'w', encoding='utf-8') as f:
            f.write(for_web(html))

    wanted = sorted({os.path.basename(s['img']) for s in content if s.get('img')}
                    | {mm for h in pages.values() for mm in re.findall(r'img/(p-\d+\.jpe?g)', h)})
    kind, read = image_source(src, lecdir)
    missing = []
    for name in wanted:
        data = read(name)
        if data is None:
            missing.append(name)
            continue
        with open(os.path.join(dest, 'img', name), 'wb') as f:
            f.write(data)
    if missing:
        die(f'images missing from {kind}: {", ".join(missing)}')
    print(f'  images: {len(wanted)} from {kind}')

    pdfs = list(old.get('pdfs', []))
    for spec in a.pdf:
        path, _, label = spec.partition(':')
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            die(f'pdf not found: {path}')
        os.makedirs(os.path.join(dest, 'pdf'), exist_ok=True)
        fname = os.path.basename(path)
        shutil.copy2(path, os.path.join(dest, 'pdf', fname))
        pdfs = [p for p in pdfs if p['file'] != fname] + [{'file': fname, 'label': label or 'PDF'}]
        print(f'  pdf: {fname}')

    vreport = os.path.join(REPO, 'validation', f'{key}-lecture-{n}.md')
    subprocess.run([sys.executable, os.path.join(REPO, 'scripts', 'validate_numbers.py'), src, vreport], check=True)

    meta = {'n': n, 'title': title, 'slides': len(content), 'solves': len(solves),
            'study': 'study.html' in pages, 'pdfs': pdfs,
            'published': datetime.date.today().isoformat(),
            'source': os.path.relpath(src, root)}
    with open(os.path.join(dest, 'lecture.json'), 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    build_site.main()

    for w in warnings:
        print('  WARNING:', w)
    rel = os.path.relpath(dest, REPO)
    if a.dry_run:
        print(f'dry run: files in {rel}, nothing committed')
        return
    run(['git', 'add', '-A'], cwd=REPO)
    if subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=REPO).returncode == 0:
        print('nothing changed; no commit')
    else:
        run(['git', 'commit', '-q', '-m', f'Publish {c["code"]} lecture {n}: {title}'], cwd=REPO)
    if not a.no_push:
        run(['git', 'push', '-q'], cwd=REPO)
    print(f'done: {rel}/stage.html')


if __name__ == '__main__':
    main()
