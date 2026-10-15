#!/bin/bash
# Auto-publish for thermo-teach: runs on the Mac every 3 minutes (launchd).
# If the lecture agent has committed in this repo and the branch is ahead of origin, push it.
# Also: if any lecture source (content.json / solves.json / engine template) is newer than its published stage.html, re-import it and commit first.
set -e
REPO="$HOME/Documents/Claude/Projects/AU Professorship agent/code/thermodynamics"
cd "$REPO"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
LOG="$REPO/launchd/autopush.log"
log(){ echo "$(date '+%F %T') $*" >> "$LOG"; }
# 0. never run on top of a live git process
[ -e .git/index.lock ] && { log "index.lock present, skipping"; exit 0; }
# 1. re-import any lecture whose sources are newer than the published page
python3 - <<'PY' >> "$LOG" 2>&1
import json,os,subprocess,sys
repo=os.getcwd(); site=json.load(open('site.json'))
root=os.path.expanduser(site.get('project_root','../..'))
if not os.path.isabs(root): root=os.path.normpath(os.path.join(repo,root))
unl=site.get('unlisted','teach-1383d49e09')
tpl=os.path.join(root,'courses/_engine/lecture-stage/stage_template.html')
cs=site.get('courses',{}); items=cs.items() if isinstance(cs,dict) else [(c.lower() if isinstance(c,str) else c['code'].lower(),c) for c in cs]
for slug,c in items:
    code=c.get('folder',c.get('code',slug.upper())) if isinstance(c,dict) else c.upper()
    lec=os.path.join(root,'courses',code,'lectures')
    if not os.path.isdir(lec): continue
    for d in sorted(os.listdir(lec)):
        if not d.startswith('Lecture-'): continue
        n=d.split('-',1)[1]; src=os.path.join(lec,d,'our-work/03_Lecture-Stage'); pub=os.path.join(repo,unl,slug,'lecture-'+n,'stage.html')
        if not os.path.exists(os.path.join(src,'content.json')) or not os.path.exists(pub): continue
        newest=max(os.path.getmtime(os.path.join(src,f)) for f in ('content.json','solves.json','index.html') if os.path.exists(os.path.join(src,f)))
        newest=max(newest,os.path.getmtime(tpl)) if os.path.exists(tpl) else newest
        if newest>os.path.getmtime(pub)+5:
            print('re-import',slug,'lecture-'+n)
            subprocess.run([sys.executable,'scripts/publish_lecture.py',slug,'lecture-'+n,'--no-push'],check=False)
PY
# 2. commit anything the import left uncommitted, then push if ahead
if [ -n "$(git status --porcelain)" ]; then git add -A && git commit -q -m "Auto-publish: $(date '+%F %H:%M')" && log "committed"; fi
if [ "$(git rev-list --count @{u}..HEAD 2>/dev/null)" != "0" ]; then git push -q && log "pushed $(git rev-parse --short HEAD)"; fi
