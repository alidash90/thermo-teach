#!/usr/bin/env python3
"""Book figures and book examples for Lecture Stage slides (used by publish_lecture.py).

A slide in content.json may carry
  "book_figure": "3-17"                                   or {"id": "3-17", "crop": [x, y, w, h]}  or a list
  "book_example": "5-7"                                   or a list
crop is a fraction of the page (0..1) from the top-left corner, e.g. [0.05, 0.10, 0.55, 0.40].

build(content, lecture_dir) writes <lecture_dir>/book/fig-N-M.jpg (when the page image exists in the
knowledge base: figures/pages/p-NNNN.jpg, made by tools/render_figures.py once the book PDF is supplied)
and returns the data for book.json: {slide n: {"figures": [...], "examples": [...]}}. Without the image a
figure falls back to its caption and page number. Examples are rendered in the Cengel solution layout
(CENGEL-BRAIN.md section 4). Nothing is written into the knowledge base.

Try one:  python3 scripts/book_assets.py example 5-7   (prints the rendered HTML)
"""
import html, os, re, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cengel  # noqa: E402

LABELS = r'Problem|Statement|Assumptions?|Properties|Solution|Route|Analysis|Discussion'
SIGN_NOTE = ('Sign convention: the book writes Q − W = ΔE with work out positive (Eq. 4-17); in class we write '
             'every term with in = +, out = −. The two forms are equivalent.')


def _list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def caption(k, fid, page):
    """Caption text of a figure from the book page text ("FIGURE 3–17 / Property diagrams ...")."""
    n = fid.replace('-', '[–-]')
    for p in (page, page - 1, page + 1):
        try:
            t = k.page_text(p)
        except KeyError:
            continue
        m = re.search(rf'FIGURE\s*{n}\b\s*\n?(.*?)(?:\n\s*\n|$)', t, re.S)
        if m:
            cap = re.sub(r'\s+', ' ', m.group(1)).strip()
            if cap[:1].islower() and '. ' in cap:  # body text interleaved before the caption
                cap = cap.split('. ', 1)[1]
            return cap
    return ''


def crop_jpeg(src, dst, box):
    """Crop with macOS sips (no Python dependencies). box = [x, y, w, h] as fractions of the page."""
    out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', src], capture_output=True, text=True).stdout
    W = int(re.search(r'pixelWidth:\s*(\d+)', out).group(1))
    H = int(re.search(r'pixelHeight:\s*(\d+)', out).group(1))
    x, y, w, h = box
    shutil.copy2(src, dst)
    subprocess.run(['sips', '-c', str(round(h * H)), str(round(w * W)), '--cropOffset', str(round(y * H)), str(round(x * W)),
                    dst], check=True, capture_output=True)


def figure_entry(k, spec, lecture_dir):
    fid = spec['id'] if isinstance(spec, dict) else spec
    crop = spec.get('crop') if isinstance(spec, dict) else None
    f = k.figure(fid)
    rec = {'id': fid, 'page': f['book_page'], 'caption': caption(k, fid, f['book_page']), 'image': None}
    if f['image_exists']:
        os.makedirs(os.path.join(lecture_dir, 'book'), exist_ok=True)
        name = f'fig-{fid}.jpg'
        dst = os.path.join(lecture_dir, 'book', name)
        if crop:
            crop_jpeg(f['image_abs'], dst, crop)
        else:
            shutil.copy2(f['image_abs'], dst)
        rec['image'] = 'book/' + name
    return rec


def parse_example(text):
    """Example file -> {'Problem', 'Assumptions', 'Discussion': str, 'steps': [str]} whatever its layout
    (bold labels, plain labels, or numbered lines)."""
    t = re.sub(r'^#+\s*', '', text.replace('**', ''), flags=re.M)
    lines = t.splitlines()[1:]  # first line is the title
    sec = {'Problem': '', 'Assumptions': '', 'Discussion': '', 'steps': []}
    analysis = ('Solution', 'Route', 'Analysis')
    split = lambda x: [re.sub(r'^\d+\.\s+', '', y).strip() for y in re.split(r'\s+(?=\d+\.\s)', ' ' + x) if y.strip()]
    cur = 'Problem'
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        numbered = re.match(r'^\d+\.\s+', raw)
        core = re.sub(r'^(?:-\s+|\d+\.\s+)', '', raw)
        m = re.match(rf'^({LABELS})\s*:\s*(.*)$', core, re.S)
        if m:
            lab = m.group(1).capitalize()
            lab = 'Assumptions' if lab.startswith('Assumption') else 'Problem' if lab == 'Statement' else lab
            if lab in analysis:
                sec['steps'] += split(m.group(2))
                cur = 'steps'
            elif lab == 'Properties':
                sec['steps'].append(m.group(2))
                cur = 'steps'
            else:
                sec[lab] = (sec[lab] + ' ' + m.group(2)).strip()
                cur = lab
        elif numbered or cur == 'steps':
            sec['steps'].append(core)
            cur = 'steps'
        else:
            sec[cur] = (sec[cur] + ' ' + core).strip()
    return sec


def render_example(k, eid):
    e = k.example(eid)
    sec = parse_example(e['text'])
    steps = [x for x in sec['steps'] if x]
    props = []
    for st in steps:
        for clause in re.split(r';\s+|\.\s+(?=[A-Z(])', st):
            if re.search(r'Table\s+A[–-]\d+', clause) and len(clause) < 220:
                props.append(clause.strip().rstrip('.'))
    E = lambda x: html.escape(x, quote=False)
    H = [f'<div class="bk-ex"><div class="bk-title"><b>EXAMPLE {E(e["id"])}</b> {E(e["title"])}</div>']
    if sec['Problem']:
        H.append(f'<p class="bk-stmt">{E(sec["Problem"])}</p>')
    H.append('<p class="bk-sol"><b>SOLUTION</b></p>')
    if sec['Assumptions']:
        a = [x.strip().rstrip('.') for x in re.split(r';\s*', sec['Assumptions']) if x.strip()]
        H.append('<p><b>Assumptions</b> ' + ' '.join(f'{i + 1} {E(x)}.' for i, x in enumerate(a)) + '</p>')
    if props:
        H.append('<p><b>Properties</b> ' + ' '.join(f'{E(x)}.' for x in dict.fromkeys(props)) + '</p>')
    if steps:
        H.append('<div><b>Analysis</b><ol class="bk-steps">' + ''.join(f'<li>{E(x)}</li>' for x in steps) + '</ol></div>')
    if sec['Discussion']:
        H.append(f'<p><b>Discussion</b> {E(sec["Discussion"])}</p>')
    H.append(f'<p class="bk-src">Çengel and Boles, 9e (SI), Example {E(e["id"])}, pp. {E(e["pages"])}. {E(SIGN_NOTE)}</p></div>')
    return {'id': e['id'], 'title': e['title'], 'pages': e['pages'], 'html': ''.join(H)}


def build(content, lecture_dir):
    k = cengel.kb()
    out, problems = {}, []
    for s in content:
        figs, exs = [], []
        for spec in _list(s.get('book_figure')):
            try:
                figs.append(figure_entry(k, spec, lecture_dir))
            except StopIteration:
                problems.append(f'slide {s["n"]}: book_figure {spec} not in the manifest')
        for eid in _list(s.get('book_example')):
            try:
                exs.append(render_example(k, eid))
            except StopIteration:
                problems.append(f'slide {s["n"]}: book_example {eid} not in the manifest')
        if figs or exs:
            out[str(s['n'])] = {'figures': figs, 'examples': exs}
    return out, problems


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == 'example':
        print(render_example(cengel.kb(), sys.argv[2])['html'])
    elif len(sys.argv) == 3 and sys.argv[1] == 'figure':
        k = cengel.kb()
        f = k.figure(sys.argv[2])
        print(f'Figure {sys.argv[2]}, p. {f["book_page"]}: {caption(k, sys.argv[2], f["book_page"])} (image: {"yes" if f["image_exists"] else "not rendered yet"})')
    else:
        print(__doc__)
