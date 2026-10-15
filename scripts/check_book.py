#!/usr/bin/env python3
"""Check a lecture build against the Cengel 9e knowledge base (tables, examples, equations, sections).

Usage: python3 scripts/check_book.py <03_Lecture-Stage folder> [report.md] [label] [log-key]
With log-key (e.g. mech230-lecture-2) the open findings are written to validation/discrepancies.md,
in a section between <!-- auto:KEY --> markers that each run replaces; validation/known-book-issues.json
holds explanations for differences that are understood (8e vs 9e, book misprints).

1. Table values. Every solves.json step field that cites a table ("Table A-5, 15 kPa: h_f = 225.94 ...")
   is split per table; the state is read from the text (P in kPa or MPa, T in °C); every other number
   in that part must equal a cell of a matching row of tables/A-*.csv to the book's printed digits.
   "interpolated" values are checked with KB().interp; a value with fewer digits than the book is
   accepted when it is the book value rounded. A miss is checked against the CSV flag column and
   KB().misprints() before it is reported.
2. Citations. Every "Ex n-m" / "Example n-m", "Eq. n-m", "§n-m" in content.json and solves.json (text
   inside [10e ...] brackets is skipped) must resolve in manifest.json. For a solve block that cites an
   example, the block's results are looked up in that example's text: low overlap suggests the wrong
   example number.
Exit code 0; the report is the deliverable. Prints a one-line summary.
"""
import datetime, json, os, re, sys
from decimal import Decimal, InvalidOperation

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cengel  # noqa: E402

NUM = re.compile(r'(?<![\w.^_])[-−]?\d+(?:\.\d+)?(?![\w])')
TABLE = re.compile(r'(?:Table\s+)?\bA-(\d+)\b')
SAT_TABLES_T = {'A-4', 'A-11'}          # keyed by T_C
SAT_TABLES_P = {'A-5', 'A-12'}          # keyed by P_kPa
SH_TABLES = {'A-6', 'A-7', 'A-13'}      # keyed by P_MPa and T_C (plus sat rows)


def dec(s):
    try:
        return Decimal(str(s).replace('−', '-').replace(',', ''))
    except InvalidOperation:
        return None


def same_printed(page, book):
    """page value vs CSV string: exact, or the book value rounded to the page's digits."""
    a, b = dec(page), dec(book)
    if a is None or b is None:
        return None
    if a == b:
        return 'exact'
    exp = a.as_tuple().exponent
    if exp < 0 and abs(b.as_tuple().exponent) > abs(exp) and b.quantize(Decimal(1).scaleb(exp)) == a:
        return 'rounded'
    if exp >= 0 and b.quantize(Decimal(1)) == a and abs(b) >= 10:
        return 'rounded'
    return None


def states(text):
    """Pressures (kPa) and temperatures (°C) named in a text."""
    P, T = set(), set()
    for v, u in re.findall(r'([-−]?\d+(?:\.\d+)?)\s*(kPa|MPa)\b', text):
        d = dec(v)
        P.add(d * 1000 if u == 'MPa' else d)
    for v in re.findall(r'([-−]?\d+(?:\.\d+)?)\s*°\s*C', text):
        T.add(dec(v))
    for a, b, u in re.findall(r'(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)\s*(°\s*C|kPa|MPa)', text):
        if 'C' in u:
            T.update({dec(a), dec(b)})
        else:
            P.update({dec(a) * (1000 if u == 'MPa' else 1), dec(b) * (1000 if u == 'MPa' else 1)})
    return P, T


def rows_for(k, tid, P, T):
    rows = k.table(tid)
    if tid in SAT_TABLES_T:
        return [r for r in rows if dec(r['T_C']) in T]
    if tid in SAT_TABLES_P:
        return [r for r in rows if dec(r['P_kPa']) in P]
    if tid in SH_TABLES:
        Pm = {p / 1000 for p in P}
        return [r for r in rows if dec(r['P_MPa']) in Pm and (dec(r['T_C']) in T or r.get('state') == 'sat')]
    return []


SYM = re.compile(r'\b(T_?sat|P_?sat|[hHuUvVsS])\s*(?:_?\{?\s*(fg|f|g)\b\}?)?[₀-₉]*\s*(?:@[^=,;()]*)?\s*[=≈]?\s*$')


def columns_for(prefix, row):
    """Columns a value may come from, from the symbol written just before it ("h_f = ", "s_g 6.52", "h₁ = ")."""
    m = SYM.search(prefix[-40:])
    if not m:
        return None
    base, suf = m.group(1).lower().replace('_', ''), (m.group(2) or '')
    if base == 'tsat':
        return [c for c in row if c in ('Tsat_C', 'T_C')]
    if base == 'psat':
        return [c for c in row if c == 'Psat_kPa']
    cols = [c for c in row if c.startswith(base + suf + '_')]
    return cols or None


def check_part(k, tid, part, context, misprints):
    """Return list of (status, value, detail) for the numbers in one table's part of a citation.
    The state comes from the clause itself, else from the whole part ("0.5 MPa block: 200 °C -> ...; 250 °C -> ...")."""
    out = []
    Pc, Tc = states(part)
    Pp, Tp = states(context)
    P, T = (Pc or Pp), (Tc or Tp)
    keys = {str(x.normalize()) for x in P} | {str((x / 1000).normalize()) for x in P} | {str(x.normalize()) for x in T}
    try:
        rows = rows_for(k, tid, P, T)
    except FileNotFoundError:
        return [('no-csv', tid, f'{tid} has no CSV in the knowledge base')]
    interp = 'interpolat' in part.lower()
    for mt in NUM.finditer(part):
        tok = mt.group(0)
        if re.match(r'\s*m³(?!/)', part[mt.end():]):
            continue  # a volume worked out in the text, not a table cell
        if re.search(r'(\bour\s+\w*\s*=?\s*|\bx\s*=\s*|\bstate\s+|\(\s*x\s*=\s*)$', part[:mt.start()], re.I):
            continue  # the problem's own value ("our s = 6.6796", "x = 0.996", "state 13")
        d = dec(tok)
        if d is None or str(d.normalize()) in keys or abs(d) < Decimal('0.0001'):
            continue
        if re.fullmatch(r'\d', tok.strip('-−')):
            continue  # state labels, step numbers
        hit = None
        want = columns_for(re.sub(r'([hHuUvVsS])_?g\s*[−-]\s*\1_?f\s*=\s*$', r'\1_fg = ', part[:mt.start()]), rows[0]) if rows else None
        for r in rows:
            for col, val in r.items():
                if col in ('state', 'flag') or val in (None, '') or (want and col not in want):
                    continue
                how = same_printed(tok, val)
                if how:
                    hit = (how, f'{tid} {col} = {val}')
                    break
            if hit:
                break
        pre = re.sub(r'([hHuUvVsS])_?g\s*[−-]\s*\1_?f\s*=\s*$', r'\1_fg = ', part[:mt.start()])  # "v_g − v_f =" means v_fg
        m_fg = SYM.search(pre[-40:])
        if not hit and m_fg and m_fg.group(2) == 'fg' and rows:
            base = m_fg.group(1).lower()
            for r in rows:
                f_ = next((c for c in r if c.startswith(base + 'f_')), None)
                g_ = next((c for c in r if c.startswith(base + 'g_')), None)
                if f_ and g_ and f'{base}fg_' not in ''.join(r):
                    diff = dec(r[g_]) - dec(r[f_])
                    if same_printed(tok, str(diff)):
                        hit = ('derived', f'{tid} {g_} - {f_} = {r[g_]} - {r[f_]} = {diff}')
                        break
        if not hit and interp and tid in SAT_TABLES_P | SAT_TABLES_T:
            key = 'P_kPa' if tid in SAT_TABLES_P else 'T_C'
            for x in (P if key == 'P_kPa' else T):
                for col in k.table(tid)[0]:
                    if col == key:
                        continue
                    try:
                        v = k.interp(tid, col, **{key: float(x)})
                    except Exception:
                        continue
                    if same_printed(tok, f'{v:.6f}'):
                        hit = ('interpolated', f'{tid} {col} at {key}={x}: {v:.6g}')
                        break
                if hit:
                    break
        if hit:
            out.append(('ok', tok, hit[1] + (' (rounded)' if hit[0] == 'rounded' else '')))
            continue
        if not rows:
            out.append(('no-row', tok, f'{tid}: state not recognised in "{context[:80]}"'))
            continue
        flagged = [r for r in rows if r.get('flag')]
        cells = {v for r in rows for c, v in r.items() if c not in ('state', 'flag') and v}
        mp = [m for m in misprints if tid in m and (tok in m or any(v in m for v in cells if len(v) > 3))]
        note = ('; flagged cell(s) in this row: ' + ', '.join(r['flag'] for r in flagged)) if flagged else ''
        note += ('; book misprint list: ' + mp[0][:120]) if mp else ''
        nearest = nearest_cell(tok, rows, want)
        out.append(('miss', tok, f'{tid} {nearest}{note}'))
    return out


def nearest_cell(tok, rows, want=None):
    d = dec(tok)
    best = None
    for r in rows:
        for col, val in r.items():
            v = dec(val)
            if v is None or col in ('state', 'flag') or (want and col not in want):
                continue
            rel = abs(v - d) / max(abs(v), Decimal('1e-9'))
            if best is None or rel < best[0]:
                key = ', '.join(f'{c}={r[c]}' for c in ('P_kPa', 'P_MPa', 'T_C') if c in r)
                best = (rel, f'nearest: {col} = {val} at {key}')
    return best[1] if best else 'no numeric cell'


def table_checks(k, folder, misprints):
    with open(os.path.join(folder, 'solves.json'), encoding='utf-8') as f:
        solves = json.load(f)
    results = []
    for key, blk in solves.items():
        for i, st in enumerate(blk.get('steps', [])):
            for fld in ('tbl', 'note'):
                text = st.get(fld) or ''
                text = ' '.join(text) if isinstance(text, list) else text
                marks = list(TABLE.finditer(text))
                if not marks:
                    continue
                for j, m in enumerate(marks):
                    tid = 'A-' + m.group(1)
                    end = marks[j + 1].start() if j + 1 < len(marks) else len(text)
                    part = text[m.end():end]
                    # the state can sit in this part or, for "Table A-5: 10 kPa (...)" lists, in its own clauses
                    for clause in re.split(r';|\.\s', part) or [part]:
                        for status, tok, detail in check_part(k, tid, clause, part, misprints):
                            results.append((status, f'{key} step {i + 1} {fld}', tok, detail))
    return results


CITE = [('example', re.compile(r'\b(?:Ex(?:ample)?\.?)\s*(\d+)[-–](\d+)')),
        ('equation', re.compile(r'\bEqs?\.?\s*(\d+)[-–](\d+)')),
        ('section', re.compile(r'§\s*(\d+)[-–](\d+)'))]


def strings(obj, path=''):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, list):
        for i, x in enumerate(obj):
            yield from strings(x, f'{path}[{i}]')
    elif isinstance(obj, dict):
        for kk, v in obj.items():
            yield from strings(v, f'{path}.{kk}' if path else kk)


def citation_checks(k, folder):
    out, seen = [], {}
    docs = {}
    for f in ('content.json', 'solves.json'):
        p = os.path.join(folder, f)
        if os.path.exists(p):
            with open(p, encoding='utf-8') as fh:
                docs[f] = json.load(fh)
    for f, d in docs.items():
        for path, s in strings(d):
            s9 = re.sub(r'\[10e[^\]]*\]', '', s)
            s9 = re.sub(r'\b(8e|10e)\b[^.;,)]*', '', s9)
            for kind, rx in CITE:
                for m in rx.finditer(s9):
                    cid = f'{m.group(1)}-{m.group(2)}'
                    if (kind, cid) in seen:
                        seen[(kind, cid)].append(f'{f}:{path}')
                        continue
                    seen[(kind, cid)] = [f'{f}:{path}']
    for (kind, cid), where in sorted(seen.items(), key=lambda x: (x[0][0], [int(n) for n in x[0][1].split('-')])):
        try:
            rec = getattr(k, kind)(cid)
            label = rec.get('title') or (rec.get('text') or '')[:60]
            pages = rec.get('pages', '')
            out.append(('ok', kind, cid, f'{label} (pp. {pages})' if pages else label, where))
        except (StopIteration, KeyError, ValueError):
            hits = k.find(r'\(\s*' + cid.replace('-', '[–-]') + r'\s*\)') if kind == 'equation' else []
            if hits:
                out.append(('ok-text', kind, cid, f'in the book text p. {hits[0][0]}; not indexed in manifest.json', where))
            else:
                out.append(('missing', kind, cid, 'not in manifest or book text', where))
    return out


def example_fit(k, folder):
    """For solve blocks citing an example: share of their result numbers found in that example's text."""
    p = os.path.join(folder, 'solves.json')
    with open(p, encoding='utf-8') as fh:
        solves = json.load(fh)
    out = []
    for key, blk in solves.items():
        m = re.search(r'\b(?:Ex(?:ample)?\.?)\s*(\d+)[-–](\d+)', blk.get('title', ''))
        if not m:
            continue
        eid = f'{m.group(1)}-{m.group(2)}'
        try:
            ex = k.example(eid)
        except StopIteration:
            continue
        text = ex['text'].replace(',', '')
        nums = []
        for st in blk.get('steps', []):
            for fld in ('res', 'num'):
                nums += [t for t in NUM.findall(st.get(fld, '')) if len(t.replace('.', '').strip('0-−')) >= 3]
        nums = list(dict.fromkeys(nums))
        found = [t for t in nums if t in text or t.rstrip('0').rstrip('.') in text]
        out.append((key, eid, ex['title'], ex['pages'], len(found), len(nums)))
    return out


def log_discrepancies(key, label, bad, cit, fit, misprints):
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    known_p = os.path.join(repo, 'validation', 'known-book-issues.json')
    known = json.load(open(known_p, encoding='utf-8')).get(key, {}) if os.path.exists(known_p) else {}
    rows = []
    for _, where, tok, detail in bad:
        expl = known.get(f'table:{tok}')
        rows.append(('table value', where, tok, detail, expl or 'open'))
    for st, kind, cid, lab, where in cit:
        if st == 'missing':
            rows.append((kind, ', '.join(where[:2]), cid, lab, 'open'))
    for b, e, t, p, f, n in fit:
        if n and f / n < 0.5:
            expl = known.get(f'fit:{b}')
            rows.append(('example fit', b, f'Ex {e}', f'{f} of {n} results found in "{t}" (pp. {p})', expl or 'open: check the example number'))
    gaps = [f'{kind} {cid} ({lab})' for st, kind, cid, lab, where in cit if st == 'ok-text']
    L = [f'<!-- auto:{key} -->', f'## {label}: book check (automatic, {datetime.date.today().isoformat()})', '',
         '- Rewritten by `scripts/check_book.py` on every publish. Each finding was compared with `KB().misprints()` '
         'and the CSV `flag` column first; explained ones carry their explanation.', '']
    if rows:
        L += ['| Kind | Where | Value / id | Finding | Status |', '|---|---|---|---|---|']
        L += [f'| {a} | {b} | {c} | {d} | {e} |' for a, b, c, d, e in rows]
    else:
        L.append('No open findings.')
    if gaps:
        L += ['', '- Knowledge-base index gaps (cited correctly, found in the book text, missing from manifest.json): ' + '; '.join(gaps) + '.']
    L.append(f'<!-- /auto:{key} -->')
    block = '\n'.join(L)
    path = os.path.join(repo, 'validation', 'discrepancies.md')
    text = open(path, encoding='utf-8').read() if os.path.exists(path) else '# Discrepancy log\n'
    pat = re.compile(rf'<!-- auto:{re.escape(key)} -->.*?<!-- /auto:{re.escape(key)} -->', re.S)
    text = pat.sub(lambda m: block, text) if pat.search(text) else text.rstrip() + '\n\n' + block + '\n'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    return sum(1 for r in rows if r[4].startswith('open'))


def main():
    folder = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    label = sys.argv[3] if len(sys.argv) > 3 else folder
    k = cengel.kb()
    misprints = k.misprints()
    tab = table_checks(k, folder, misprints)
    cit = citation_checks(k, folder)
    fit = example_fit(k, folder)
    ok = [r for r in tab if r[0] == 'ok']
    bad = [r for r in tab if r[0] != 'ok']
    weak = [f for f in fit if f[5] and f[4] / f[5] < 0.5]
    L = [f'# Book check: {label}', '',
         'Against the Cengel 9e knowledge base (`courses/MECH330/resources/cengel/`, manifest + tables/A-*.csv). '
         'Made by `scripts/check_book.py`.', '',
         f'- Table values: {len(ok)} matched to the printed digits, {len(bad)} not matched.',
         f'- Citations: {sum(1 for c in cit if c[0] == "ok")} resolved in the manifest, {sum(1 for c in cit if c[0] == "ok-text")} found only in the book text (index gap), {sum(1 for c in cit if c[0] == "missing")} missing.',
         f'- Example fit: {len(fit) - len(weak)} of {len(fit)} solve blocks find most of their results in the cited example.', '']
    L += ['## Table values not matched', '']
    if bad:
        L += ['| Where | Value | Finding |', '|---|---|---|'] + [f'| {w} | {t} | {d} |' for _, w, t, d in bad]
    else:
        L.append('None.')
    L += ['', '## Citations', '', '| Kind | Id | Book | Status | Used in |', '|---|---|---|---|---|']
    L += [f'| {kind} | {cid} | {lab} | {st} | {len(where)} place(s) |' for st, kind, cid, lab, where in cit]
    L += ['', '## Example fit (results found in the cited example text)', '', '| Block | Cites | Book title | Pages | Found |', '|---|---|---|---|---|']
    L += [f'| {b} | Ex {e} | {t} | {p} | {f} of {n}{" (check the citation)" if n and f / n < 0.5 else ""} |' for b, e, t, p, f, n in fit]
    L += ['', '## Table values matched', '', '| Where | Value | Book cell |', '|---|---|---|'] + [f'| {w} | {t} | {d} |' for _, w, t, d in ok]
    rep = '\n'.join(L) + '\n'
    if out:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(rep)
    print(f'book: {len(ok)} table values matched, {len(bad)} not; {len(cit)} citations '
          f'({sum(1 for c in cit if c[0] == "missing")} missing, {sum(1 for c in cit if c[0] == "ok-text")} index gaps); example fit weak for {len(weak)}' + (f' -> {out}' if out else ''))
    if len(sys.argv) > 4:
        n_open = log_discrepancies(sys.argv[4], label, bad, cit, fit, misprints)
        print(f'  discrepancies.md: {n_open} open finding(s) for {sys.argv[4]}')
    return bad, cit, weak


if __name__ == '__main__':
    main()
