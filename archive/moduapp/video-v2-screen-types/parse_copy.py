import re, collections, json
L = open('meta.xml').read().split('\n')
pat = re.compile(r'^(\s*)<(\w+) id="([^"]+)" name="(.*?)" x="([-\d.e]+)" y="([-\d.e]+)" width="([-\d.e]+)" height="([-\d.e]+)"')
frames = []; cur = None; hide_at = None; hidden_skipped = 0
for l in L:
    m = pat.match(l)
    if not m:
        continue
    ind = len(m.group(1))
    if hide_at is not None and ind > hide_at:
        hidden_skipped += 1
        continue
    hide_at = None
    if ind == 2:
        cur = None
        if m.group(2) == 'frame' and m.group(4).startswith('A-4'):
            cur = {'id': m.group(3), 'x': float(m.group(5)), 'y': float(m.group(6)), 'w': round(float(m.group(7))), 'h': round(float(m.group(8))), 'inst': collections.Counter(), 'texts': []}
            frames.append(cur)
        continue
    if 'hidden="true"' in l:
        hide_at = ind
        hidden_skipped += 1
        continue
    if cur is not None:
        if m.group(2) == 'instance': cur['inst'][m.group(4)] += 1
        if m.group(2) == 'text': cur['texts'].append(m.group(4))
print('frames', len(frames), 'hidden nodes skipped', hidden_skipped)
json.dump([{**f, 'inst': dict(f['inst'])} for f in frames], open('copy_frames.json', 'w'), ensure_ascii=False)
