#!/usr/bin/env python3
"""Ask the Cengel & Boles 9e (SI) knowledge base from the site repo.

Usage:
  python3 scripts/cengel.py example 5-7        the book's full solution, with title and pages
  python3 scripts/cengel.py equation 5-38      an equation by number
  python3 scripts/cengel.py section 3-5        a section's digest notes
  python3 scripts/cengel.py lookup A-5 P_kPa=15             one table row
  python3 scripts/cengel.py interp A-6 h_kJ_per_kg T_C=216.3 P_MPa=0.5
  python3 scripts/cengel.py page 230           the full text of a book page
  python3 scripts/cengel.py find "Kelvin.Planck"
  python3 scripts/cengel.py misprints

The knowledge base lives at <project_root>/courses/MECH330/resources/cengel/ (read-only; nothing is
written there). Other scripts import kb() from here.
"""
import json, os, sys, textwrap

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def kb_root():
    with open(os.path.join(REPO, 'site.json'), encoding='utf-8') as f:
        root = os.path.normpath(os.path.join(REPO, json.load(f)['project_root']))
    return os.path.join(root, 'courses', 'MECH330', 'resources', 'cengel')


def kb():
    """The KB reader object from the knowledge base's own tools/cengel_kb.py."""
    tools = os.path.join(kb_root(), 'tools')
    if tools not in sys.path:
        sys.path.insert(0, tools)
    from cengel_kb import KB
    return KB()


def _kv(args):
    out = {}
    for a in args:
        k, _, v = a.partition('=')
        out[k] = v
    return out


def main(argv):
    if len(argv) < 2 or argv[1] in ('-h', '--help'):
        print(__doc__)
        return
    k, cmd, rest = kb(), argv[1], argv[2:]
    if cmd == 'example':
        e = k.example(rest[0])
        print(f"Example {e['id']}: {e['title']}  (Cengel 9e, Ch {e['chapter']}, pp. {e['pages']}; {e['file']})\n")
        print(e['text'].rstrip())
    elif cmd == 'equation':
        e = k.equation(rest[0])
        print(f"Eq. {e['id']} (Ch {e['chapter']}): {e['text']}")
    elif cmd == 'section':
        s = k.section(rest[0])
        print(f"Section {s['id']}: {s.get('title', '')}  (pp. {s.get('pages', '?')})\n")
        print(s['text'])
    elif cmd == 'lookup':
        row = k.lookup(rest[0], **_kv(rest[1:]))
        print('\n'.join(f'{c:>18}  {v}' for c, v in row.items()))
    elif cmd == 'interp':
        print(k.interp(rest[0], rest[1], **_kv(rest[2:])))
    elif cmd == 'page':
        print(k.page_text(int(rest[0])))
    elif cmd == 'find':
        for page, line in k.find(rest[0])[:60]:
            print(f'p. {page}: {line}')
    elif cmd == 'misprints':
        for m in k.misprints():
            print('- ' + textwrap.shorten(str(m), 220))
    else:
        sys.exit(f'unknown command {cmd}; see --help')


if __name__ == '__main__':
    main(sys.argv)
