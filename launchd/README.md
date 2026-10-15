# Auto-publish (launchd)
Install once on the Mac:
```
cp "launchd/kw.au.thermo-autopush.plist" ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/kw.au.thermo-autopush.plist
```
Every 3 minutes `scripts/autopush.sh` re-imports any lecture whose sources in `courses/` are newer than its published page, commits, and pushes if the branch is ahead of origin. Log: `launchd/autopush.log`. Uninstall: `launchctl unload ~/Library/LaunchAgents/kw.au.thermo-autopush.plist`.
