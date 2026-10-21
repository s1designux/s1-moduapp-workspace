import json, collections, html, os, re
from contexts import S, CONTEXTS
from context_spec import SPEC, RULES
from analyze import NAMES
import build

OUT = build.OUT
SHAPES = build.SHAPES
BUN = {b['key']: b for b in build.bundles_out}
BY_ID = {x['id']: x for x in S}
IMG_DIRS = ['images/screen-types', 'images/contexts']


def img(oid):
    for dr in IMG_DIRS:
        p = f"{dr}/{oid.replace(':', '-')}.jpg"
        if os.path.exists(OUT + p):
            return p
    return None


def container(x):
    st = x['state_flags']
    if '바텀시트 열림' in st: return '바텀시트'
    if '가운데 팝업' in st: return '가운데 팝업'
    if '오른쪽 패널' in st: return '오른쪽 패널'
    if '토스트' in st: return '토스트'
    return None


def buttons(x):
    r = ' / '.join(x['components_raw'])
    out = []
    for lab in ['확인', '적용', '시간 선택', '취소']:
        if re.search(lab + r"( 버튼|'|\b|·)", r) and lab not in out:
            out.append(lab)
    if re.search(r'닫기', r):
        out.append('닫기 X')
    return out


ctx_out = []
for key, name, f in CONTEXTS:
    sub = [x for x in S if f(x)]
    sp = SPEC[key]
    c = collections.Counter(k for x in sub for k in x['keys'])
    core = [{'key': k, 'name': NAMES[k], 'screens': n, 'rate': round(n / len(sub), 2)} for k, n in c.most_common() if n / len(sub) >= 0.5]
    cont = collections.defaultdict(collections.Counter)
    btn = collections.defaultdict(collections.Counter)
    for x in sub:
        o = x['orientation']
        cn = container(x)
        if cn: cont[o][cn] += 1
        for b in buttons(x): btn[o][b] += 1
    ctx_out.append({
        'key': key, 'name': name, 'goal': sp['goal'], 'screens': len(sub),
        'by_shape': dict(collections.Counter(x['shape'] for x in sub)),
        'by_mode': dict(collections.Counter(x['mode'] for x in sub)),
        'platform_extra': dict(collections.Counter(x['platform'] for x in sub if x['platform'] != 'common')),
        'entry': sp['entry'], 'exit': sp['exit'],
        'bundles': [{'key': b, 'name': BUN[b]['name']} for b in sp['combo']],
        'core_components': core,
        'containers': {o: dict(v) for o, v in cont.items()},
        'decision_buttons': {o: dict(v) for o, v in btn.items()},
        'placement': sp['zones'],
        'flow': [{'id': i, 'caption': BY_ID[i]['caption'], 'view': BY_ID[i]['view'], 'image': img(i), 'copy_node': build.copy_id(i)} for i in sp['flow']],
        'differences': [{'what': a, 'evidence': b} for a, b in sp['diffs']],
        'screen_ids': [x['id'] for x in sub],
    })

missing = [fl['id'] for c_ in ctx_out for fl in c_['flow'] if not fl['image']]
result = {
    'meta': {'service': 'video', 'layer': 'service', 'title': '모두앱 영상 — 맥락별 부품 조합',
             'analyzed_at': '2026-10-21', 'basis': 'NVR(녹화기) 연동 신규 기준만',
             'source': 'video-v2-screen-type-components.json(화면별 부품, 두 기록 합침) + video-v2-screen-analysis.json(흐름·누르는 곳) + Figma 스크린샷',
             'method': '맥락 = 사용자가 하려는 일. 화면 묶음(기능)과 상태로 270화면을 15개 맥락에 하나씩 나눔. 맥락마다 들어오고 나가는 법, 부품 묶음, 자리, 겹쳐 뜨는 창·결정 버튼을 세고, 같은 일인데 다르게 만든 곳을 적음',
             'images_missing': missing},
    'rules': [{'rule': a, 'detail': b} for a, b in RULES],
    'contexts': ctx_out,
}
json.dump(result, open(OUT + 'video-v2-context-components.json', 'w'), ensure_ascii=False, indent=1)

# ---------- HTML ----------
e = html.escape
TOC = ''.join(f'<a href="#{c_["key"]}">{e(c_["name"])}</a>' for c_ in ctx_out)

rows = ''
for c_ in ctx_out:
    tds = ''.join(f'<td>{c_["by_shape"].get(s, "") or "·"}</td>' for s in SHAPES)
    def cs(o):
        v = c_['containers'].get(o, {})
        return ' · '.join(k for k, _ in sorted(v.items(), key=lambda a: -a[1])) or '-'
    def bs(o):
        v = c_['decision_buttons'].get(o, {})
        return ' · '.join(k for k in ['확인', '적용', '시간 선택', '취소', '닫기 X'] if k in v) or '-'
    rows += f'<tr><th class="l"><a href="#{c_["key"]}">{e(c_["name"])}</a></th>{tds}<td>{e(cs("세로"))}</td><td>{e(cs("가로"))}</td><td>{e(bs("세로"))} / {e(bs("가로"))}</td><td class="num">{len(c_["differences"])}</td></tr>'

overview = f'''<section><h2>한눈에 보기</h2>
<p class="lead">영상 탭 화면 270개를 사용자가 하려는 일 15가지로 나눴습니다. 칸의 숫자는 화면 수입니다.</p>
<div class="scroll"><table class="grid"><tr><th class="l">맥락</th>{''.join(f'<th>{e(s)}</th>' for s in SHAPES)}<th>세로에서 뜨는 창</th><th>가로에서 뜨는 창</th><th>결정 버튼(세로 / 가로)</th><th>다른 곳</th></tr>{rows}</table></div></section>'''

rules = ''.join(f'<li><b>{e(a)}</b><br>{e(b)}</li>' for a, b in RULES)
rules_sec = f'<section><h2>맥락을 가로질러 보이는 규칙</h2><ol class="rules">{rules}</ol></section>'

secs = ''
for c_ in ctx_out:
    flow = ''
    for i, fl in enumerate(c_['flow']):
        if i: flow += '<span class="arr">→</span>'
        pt = BY_ID[fl['id']]['orientation'] == '세로'
        pic = f'<a href="{e(fl["image"])}" target="_blank"><img class="{"pt" if pt else "ls"}" src="{e(fl["image"])}" alt="{e(fl["caption"])}" loading="lazy"></a>' if fl['image'] else f'<div class="ph {"pt" if pt else "ls"}">그림 대기</div>'
        flow += f'<figure>{pic}<figcaption>{e(fl["caption"])}<br><small>{e(fl["view"])}</small></figcaption></figure>'
    bun = ''.join(f'<span class="chip b">{e(b["name"])}</span>' for b in c_['bundles'])
    core = ''.join(f'<span class="chip">{e(k["name"])} <small>{int(k["rate"] * 100)}%</small></span>' for k in c_['core_components'])
    place = ''.join(f'<div class="col"><h4>{e(o)}</h4><ul>{"".join(f"<li>{e(z)}</li>" for z in zs)}</ul></div>' for o, zs in c_['placement'].items())
    diff = ''.join(f'<li>{e(d["what"])} <small>({e(d["evidence"])})</small></li>' for d in c_['differences']) or '<li class="none">다르게 만든 곳 없음</li>'
    shp = ' · '.join(f'{e(k)} {v}' for k, v in c_['by_shape'].items())
    plat = (' · ' + ' · '.join(f'{k} {v}' for k, v in c_['platform_extra'].items())) if c_['platform_extra'] else ''
    secs += f'''<section id="{c_['key']}"><h2>{e(c_['name'])}</h2>
<p class="goal">{e(c_['goal'])}</p><p class="meta">{c_['screens']}화면 · {shp}{e(plat)}</p>
<div class="flow">{flow}</div>
<div class="io"><div><h4>들어오기</h4><ul>{''.join(f'<li>{e(t)}</li>' for t in c_['entry'])}</ul></div><div><h4>나가기</h4><ul>{''.join(f'<li>{e(t)}</li>' for t in c_['exit'])}</ul></div></div>
<h4>쓰는 부품</h4><div class="chips">{bun}{core}</div>
<p class="note">파란 칩 = 부품 묶음, 회색 칩 = 이 맥락 화면의 절반 이상에 나오는 부품(비율)</p>
<h4>어디에 어떻게 놓이나</h4><div class="cols">{place}</div>
<h4>같은 일인데 다르게 만든 곳</h4><ul class="diff">{diff}</ul></section>'''

alld = ''.join(f'<li><b>{e(c_["name"])}</b> — {e(d["what"])}</li>' for c_ in ctx_out for d in c_['differences'])
diff_sec = f'<section><h2>다르게 만든 곳 모아 보기</h2><p class="lead">디자인을 하나로 맞출지 정해야 하는 곳입니다.</p><ul class="diff">{alld}</ul></section>'

page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>영상 맥락별 부품 조합</title>
<style>
:root{{--bg:#f6f7f9;--card:#fff;--ink:#1d2230;--sub:#5b6475;--line:#e2e6ee;--acc:#2f6be6;--accbg:#e8effd;--chip:#eef0f4;--warn:#b35c00}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#12151c;--card:#1b1f29;--ink:#e6e9f0;--sub:#9aa3b5;--line:#2c3240;--acc:#6b9bf5;--accbg:#1f2a44;--chip:#262b37;--warn:#f0a050}}}}
:root[data-theme="dark"]{{--bg:#12151c;--card:#1b1f29;--ink:#e6e9f0;--sub:#9aa3b5;--line:#2c3240;--acc:#6b9bf5;--accbg:#1f2a44;--chip:#262b37;--warn:#f0a050}}
body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.6 -apple-system,"Apple SD Gothic Neo","Pretendard",sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:24px 16px 64px}}
h1{{font-size:22px;margin:0 0 4px}} h2{{font-size:18px;margin:0 0 4px}} h4{{font-size:13px;margin:16px 0 6px;color:var(--sub)}}
section{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px;margin:16px 0;scroll-margin-top:60px}}
.lead,.meta,.note{{color:var(--sub)}} .note{{font-size:12px;margin:4px 0 0}} .meta{{margin:0;font-size:12px}} .goal{{margin:0 0 2px;font-size:15px}}
nav.toc{{position:sticky;top:0;z-index:2;background:var(--bg);padding:8px 0;display:flex;gap:6px;overflow-x:auto;white-space:nowrap}}
nav.toc a{{font-size:12px;padding:4px 10px;border:1px solid var(--line);border-radius:999px;color:var(--ink);text-decoration:none;background:var(--card)}}
.scroll{{overflow-x:auto}} table.grid{{border-collapse:collapse;width:100%;font-size:13px}}
.grid th,.grid td{{border:1px solid var(--line);padding:6px 8px;text-align:center}} .grid th.l{{text-align:left}} .num{{font-variant-numeric:tabular-nums}}
a{{color:var(--acc)}}
.flow{{display:flex;align-items:center;gap:8px;overflow-x:auto;padding:12px 0 4px}}
.flow figure{{margin:0;flex:none;text-align:center}} .flow figcaption{{font-size:12px;margin-top:4px;max-width:220px}} .flow small{{color:var(--sub)}}
.flow img,.ph{{display:block;border:1px solid var(--line);border-radius:8px;margin:0 auto}} img.pt,.ph.pt{{width:150px}} img.ls,.ph.ls{{width:300px}}
.ph{{display:flex;align-items:center;justify-content:center;color:var(--sub);font-size:12px;border-style:dashed}} .ph.pt{{height:325px}} .ph.ls{{height:139px}}
.arr{{flex:none;color:var(--sub);font-size:20px}}
.io{{display:grid;grid-template-columns:1fr 1fr;gap:16px}} .io ul,.cols ul{{margin:0;padding-left:18px}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:16px}} .col{{background:var(--bg);border-radius:8px;padding:8px 12px}} .col h4{{margin:4px 0}}
.chips{{display:flex;flex-wrap:wrap;gap:6px}} .chip{{background:var(--chip);border-radius:999px;padding:3px 10px;font-size:12px}} .chip.b{{background:var(--accbg);color:var(--acc);font-weight:600}}
.diff li{{margin:3px 0}} .diff small{{color:var(--sub)}} .diff .none{{color:var(--sub);list-style:none}}
.rules li{{margin:8px 0}}
@media (max-width:640px){{.io,.cols{{grid-template-columns:1fr}}}}
</style></head><body><main>
<h1>모두앱 영상 — 맥락별 부품 조합</h1>
<p class="meta">신규 기준(2026-10 Figma, NVR) 화면 270개 · 2026-10-21 · 사용자가 하려는 일 15가지</p>
<nav class="toc">{TOC}</nav>
{overview}{rules_sec}{secs}{diff_sec}
</main></body></html>'''
open(OUT + 'video-v2-context-components.html', 'w').write(page)
print('missing images', len(missing), missing)
