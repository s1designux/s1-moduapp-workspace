import re, collections, json
L = open('meta.xml').read().split('\n')
pat = re.compile(r'^(\s*)<(\w+) id="([^"]+)" name="(.*?)" x="([-\d.e]+)" y="([-\d.e]+)" width="([-\d.e]+)" height="([-\d.e]+)"')
geo = collections.defaultdict(list)  # name -> [(frame_id, fw, fh, ax, ay, w, h)]
stack = []; frame = None; hide_at = None
for l in L:
    m = pat.match(l)
    if not m: continue
    ind = len(m.group(1)); typ, nid, name = m.group(2), m.group(3), m.group(4)
    x, y, w, h = map(float, m.groups()[4:8])
    if hide_at is not None and ind > hide_at: continue
    hide_at = None
    if 'hidden="true"' in l: hide_at = ind; continue
    while stack and stack[-1][0] >= ind: stack.pop()
    if ind == 2:
        frame = (nid, round(w), round(h)) if typ == 'frame' and name.startswith('A-4') else None
        stack = [(ind, 0.0, 0.0)]; continue
    if frame is None: continue
    px, py = stack[-1][1], stack[-1][2]
    ax, ay = px + x, py + y
    if typ == 'instance' or re.match(r'^(tile \d+|카메라 \d+|time pill)$', name):
        geo[name].append((frame[0], frame[1], frame[2], round(ax), round(ay), round(w), round(h)))
    if not l.rstrip().endswith('/>'):
        stack.append((ind, ax, ay))
json.dump(geo, open('node_geo.json', 'w'))
for n, v in sorted(geo.items(), key=lambda a: -len(a[1]))[:0]:
    sz = collections.Counter((f'{a[1]}x{a[2]}', f'{a[5]}x{a[6]}', a[3], a[4]) for a in v).most_common(3)
    print(len(v), n, sz)
