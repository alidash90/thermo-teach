#!/usr/bin/env python3
"""Trace every number in a lecture's content.json + solves.json to the Çengel knowledge base.

Usage: python3 scripts/validate_numbers.py <03_Lecture-Stage folder> [report.md] [label]

Corpus (read-only, from the project root in site.json):
  courses/MECH330/resources/cengel/digest/*.md, text/*.txt      Çengel 9e digest + appendix CSVs
  courses/MECH230/mcgraw-hill-connect/**/md/*.md                 10e solutions manual + lecture PPTs
A number counts as traced when the same value (trailing zeros and thousands separators ignored)
appears anywhere in the corpus. Numbers with fewer than 3 significant digits are skipped (too common).
Untraced numbers are listed by priority: table lookups (the "tbl" field) first, then other solve
steps, then notes. Untraced does not mean wrong: most are results computed in the step; check them.
Exit code is 0; the report is the deliverable.
"""
import glob, json, os, re, sys
from decimal import Decimal, InvalidOperation

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = re.compile(r'(?<![\w.^_])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+|\d{3,})(?![\w])')


def norm(tok):
    try:
        d = Decimal(tok.replace(',', ''))
    except InvalidOperation:
        return None
    return format(d.normalize(), 'f')


def sig_digits(tok):
    digits = tok.replace(',', '').replace('.', '').lstrip('0')
    return len(digits.rstrip('0')) if '.' not in tok else len(digits)


def corpus_numbers(root):
    files = (glob.glob(os.path.join(root, 'courses/MECH330/resources/cengel/digest/*.md'))
             + glob.glob(os.path.join(root, 'courses/MECH330/resources/cengel/text/*.txt'))
             + glob.glob(os.path.join(root, 'courses/MECH230/mcgraw-hill-connect/**/md/*.md'), recursive=True))
    seen = set()
    for p in files:
        with open(p, encoding='utf-8', errors='ignore') as f:
            for tok in NUM.findall(f.read()):
                n = norm(tok)
                if n:
                    seen.add(n)
    return seen, len(files)


def items(folder):
    """Yield (priority, where, field, text) for every text field that can hold numbers."""
    with open(os.path.join(folder, 'content.json'), encoding='utf-8') as f:
        content = json.load(f)
    for s in content:
        for i, line in enumerate(s.get('lines', [])):
            yield 3, f'slide {s["n"]}', f'line {i + 1}', line
        for i, a in enumerate(s.get('ask', [])):
            yield 3, f'slide {s["n"]}', f'ask {i + 1}', a.get('q', '') + ' | ' + a.get('a', '')
    sp = os.path.join(folder, 'solves.json')
    if os.path.exists(sp):
        with open(sp, encoding='utf-8') as f:
            solves = json.load(f)
        for key, blk in solves.items():
            for i, st in enumerate(blk.get('steps', [])):
                for fld in ('tbl', 'num', 'res', 'eq', 'note', 't'):
                    if st.get(fld):
                        yield (1 if fld == 'tbl' else 2), f'{key} step {i + 1}', fld, st[fld]


def main():
    folder = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    with open(os.path.join(REPO, 'site.json'), encoding='utf-8') as f:
        root = os.path.normpath(os.path.join(REPO, json.load(f)['project_root']))
    corpus, nfiles = corpus_numbers(root)
    total, traced, misses = 0, 0, []
    for prio, where, fld, text in items(folder):
        for tok in NUM.findall(text):
            if sig_digits(tok) < 3:
                continue
            total += 1
            if norm(tok) in corpus:
                traced += 1
            else:
                ctx = text[max(0, text.find(tok) - 50): text.find(tok) + len(tok) + 30].replace('\n', ' ').replace('|', '/')
                misses.append((prio, where, fld, tok, ctx))
    misses.sort(key=lambda m: m[0])
    label = {1: 'Table lookups (check first)', 2: 'Solve steps (mostly computed results)', 3: 'Notes and ask answers'}
    rel = sys.argv[3] if len(sys.argv) > 3 else os.path.relpath(folder, root)
    lines = [f'# Number trace: {rel}', '',
             f'- Corpus: {nfiles} files from the Çengel 9e digest and the 10e Connect markdown.',
             f'- Numbers checked (3+ significant digits): {total}; traced to the corpus: {traced}; untraced: {len(misses)}.',
             '- Untraced is not an error by itself: computed results rarely appear verbatim. Review the table lookups first.', '']
    for p in (1, 2, 3):
        group = [m for m in misses if m[0] == p]
        lines.append(f'## {label[p]}: {len(group)}')
        if group:
            lines += ['', '| Where | Field | Value | Context |', '|---|---|---|---|']
            lines += [f'| {w} | {fl} | {t} | `{c}` |' for _, w, fl, t, c in group]
        lines.append('')
    report = '\n'.join(lines)
    if out:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(report)
    print(f'numbers: {total} checked, {traced} traced, {len(misses)} untraced '
          f'({sum(1 for m in misses if m[0] == 1)} table lookups)' + (f' -> {out}' if out else ''))
    return misses


if __name__ == '__main__':
    main()
