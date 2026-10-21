import json, html
ROOT = '/Users/designgroup_02/s1-moduapp-workspace/'
d = json.load(open(ROOT + 'registry/services/moduapp/component-baseline.json'))
e = html.escape
F = d['foundation']

sw = ''.join(f'''<div class="sw"><div class="chip-c" style="background:{c['value'].split(' ')[0] if not c['value'].startswith('rgba(0,0,0,0.8)') else 'linear-gradient(#000c,#0000)'}"></div>
<div><b>{e(c['key'])}</b> <code>{e(c['value'])}</code><br><small>{e(c['use'])}</small></div></div>''' for c in F['colors'])


def tstyle(spec):
    p = [x.strip() for x in spec.split('·')]
    size = p[0]; w = {'Bold': 700, 'Medium': 500, 'Regular': 400}[p[1]]
    lh = p[2].split(' ')[0] if len(p) > 2 else 'normal'
    ls = p[3].split(' ')[0] if len(p) > 3 else '0'
    return f'font-size:{size}px;font-weight:{w};line-height:{lh};letter-spacing:{ls}px'


ty = ''.join(f'''<tr><td><span style="{tstyle(t['spec'])}">모두앱 영상 8층 사무실</span></td><td><b>{e(t['key'])}</b><br><small>{e(t['spec'])}</small></td><td><small>{e(t['use'])}</small></td></tr>''' for t in F['type'])

# 부품 견본: 값 그대로 CSS로 그린 것
spec = '''
<div class="phone">
  <div class="m-header"><div><div class="m-site">8층 사무실 <span class="caret">⌄</span></div><div class="m-sub">에스원 본사ㆍN1234567</div></div>
  <div class="m-chips"><span class="m-chip on">실시간</span><span class="m-chip off">녹화영상</span></div></div>
  <div class="m-video"><span class="m-label">카메라 01</span>
    <div class="m-dimtop"><span class="m-badge"><i></i>실시간</span><span class="m-dots">⋯</span></div>
    <span class="m-toast">기본 속도로 재생</span>
    <div class="m-band">영상 수신 상태가 좋지 않음</div></div>
  <div class="m-timerow"><span class="m-round"></span><span class="m-pill">2026.09.09. 15:53:20</span><span class="m-round">◎</span></div>
  <div class="m-listhead">카메라 목록</div>
  <div class="m-thumbs"><div class="m-thumb sel"><span class="m-label">카메라 01</span></div><div class="m-thumb"><span class="m-label">카메라 02</span></div></div>
  <div class="m-tabbar"><span>홈</span><span>경비</span><span class="on">영상</span><span>전체</span></div>
</div>'''
sheets = '''
<div class="pair">
 <div><div class="cap">입력형 시트(새) — 모서리 8 · 제목 줄 26 · 버튼 48</div>
  <div class="sheet new"><div class="s-title">화면 구성 <span>✕</span></div>
   <div class="cards"><div class="card on"><i></i><i></i></div><div class="card"><i></i><i></i><i></i></div><div class="card g"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
   <div class="cardlab"><b>1x2</b><span>1x3</span><span>2x4</span></div>
   <div class="btn new">적용</div></div></div>
 <div><div class="cap">목록형 시트(옛) — 모서리 10 · 제목 줄 위아래 24 · 버튼 50</div>
  <div class="sheet old"><div class="s-title old">이벤트 종류 <span>✕</span></div>
   <div class="row"><i class="cb"></i>전체 이벤트</div><div class="row"><i class="cb on"></i>침입</div><div class="row sel">4 <span>✓</span></div>
   <div class="btn old">적용</div></div></div>
</div>
<div class="pair">
 <div><div class="cap">탭 · 달력 칸 · 슬라이더</div>
  <div class="sheet new"><div class="tabs"><span class="on">날짜</span><span>시간</span></div>
   <div class="cal"><span class="o">31</span><span class="r">1</span><span class="r">2</span><span class="sel">10</span><span class="today">18</span><span>19</span></div>
   <div class="slider"><i style="width:50%"></i><b style="left:50%"></b></div><div class="cardlab"><span>4채널</span><b>9채널</b><span>16채널</span></div></div></div>
 <div><div class="cap">버튼 두 버전 나란히</div>
  <div class="sheet new" style="gap:12px"><div class="btn new">새 버튼 48</div><div class="btn old">옛 버튼 50</div>
   <div class="btns"><div class="btn sec">취소</div><div class="btn new">시간 선택</div></div>
   <div class="ev"><span class="evchip">움직임</span><span class="evtime">08.24 18:20:00</span></div></div></div>
</div>'''

comp = ''
for c in d['components']:
    parts = ''.join(f"<li><b>{e(p['part'])}</b> — {e(p['spec'])}</li>" for p in c['parts'])
    ver = ''.join(f"<li class='v'><b>{e(v['name'])}</b> — {e(v['spec'])} <small>({e(v['evidence'])})</small></li>" for v in c['versions'])
    comp += f"<details><summary><b>{e(c['name'])}</b> <code>{e(c['key'])}</code>{' <span class=warn>두 모양</span>' if c['versions'] else ''}</summary><ul>{parts}{ver}</ul><p class='note'>근거 노드 {e(c['evidence'])}</p></details>"
mixed = ''.join(f"<tr><th>{e(m['what'])}</th><td>{e(m['detail'])}</td><td><small>{e(m['note'])}</small></td></tr>" for m in d['mixed_versions'])
refs = ''.join(f'<figure><img src="../service-video/images/{p}" alt="{e(c)}"><figcaption>{e(c)}</figcaption></figure>' for p, c in [
    ('screen-types/11-14055.jpg', '세로 기본'), ('screen-types/11-16870.jpg', '딤'), ('screen-types/11-15653.jpg', '재생·토스트'),
    ('contexts/11-27272.jpg', '입력형 시트(카드)'), ('contexts/11-16064.jpg', '달력 시트'), ('contexts/11-14983.jpg', '목록형 시트(옛)'), ('contexts/11-14553.jpg', '더보기 시트(옛)')])

css = '''
:root{--bg:#f4f6f9;--card:#fff;--ink:#1b2130;--sub:#5d6678;--line:#e3e7ee;--acc:#1d6ceb;--warnbg:#fff3d6;--warn:#8a5a00}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#11141b;--card:#1a1e28;--ink:#e6e9f0;--sub:#9aa3b5;--line:#2c3240;--acc:#6b9bf5;--warnbg:#3a3218;--warn:#f0c060;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#11141b;--card:#1a1e28;--ink:#e6e9f0;--sub:#9aa3b5;--line:#2c3240;--acc:#6b9bf5;--warnbg:#3a3218;--warn:#f0c060;color-scheme:dark}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.6 Pretendard,-apple-system,"Apple SD Gothic Neo",sans-serif}
main{max-width:1120px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:22px;margin:0} h2{font-size:17px;margin:0 0 8px} .meta{color:var(--sub);font-size:12px}
section{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px;margin:16px 0}
.rule{background:var(--warnbg);color:var(--warn);border-radius:8px;padding:8px 12px;margin:10px 0 0;font-size:13px}
.sws{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.sw{display:flex;gap:10px;align-items:flex-start} .chip-c{flex:none;width:40px;height:40px;border-radius:8px;border:1px solid var(--line)}
.sw small,.note,td small{color:var(--sub)} code{font-size:12px}
table{border-collapse:collapse;width:100%} td,th{border-top:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
.scroll{overflow-x:auto}
.stage{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start}
.specimen{background:#fff;color:#000;border-radius:10px;padding:12px}
.phone{width:360px;background:#fff;color:#000;font-family:Pretendard,-apple-system,sans-serif;border:1px solid #ddd;border-radius:6px;overflow:hidden}
.m-header{height:56px;padding:0 20px;display:flex;align-items:center;justify-content:space-between}
.m-site{font-size:18px;font-weight:700;letter-spacing:-.36px;color:#202020;line-height:1.3} .caret{font-size:14px}
.m-sub{font-size:12px;color:#bfbfbf;line-height:1.3}
.m-chips{display:flex;gap:4px}.m-chip{font-size:14px;font-weight:500}
.m-chip.on{height:30px;padding:0 12px;border-radius:999px;background:#1d6ceb;color:#fff;display:flex;align-items:center;letter-spacing:-.28px}
.m-chip.off{padding:8px 16px;border-radius:100px;background:#f2f2f2;color:#7f7f7f;line-height:1}
.m-video{position:relative;height:202px;background:linear-gradient(135deg,#6b5a4a,#2d2a28)}
.m-label{position:absolute;left:4px;top:4px;background:rgba(0,0,0,.5);border-radius:3px;padding:1px 4px;font-size:10px;font-weight:500;letter-spacing:.2px;line-height:1.4;color:#fff}
.m-dimtop{position:absolute;inset:0 0 auto;height:80px;padding:12px 20px 32px;box-sizing:border-box;background:linear-gradient(rgba(0,0,0,.8),rgba(0,0,0,0));display:flex;justify-content:space-between}
.m-badge{height:28px;padding:5px 12px;box-sizing:border-box;border-radius:28px;background:rgba(0,0,0,.5);color:#fff;font-size:14px;font-weight:500;display:flex;align-items:center;gap:4px}
.m-badge i{width:6px;height:6px;border-radius:50%;background:#e50533}.m-dots{color:#fff;font-size:20px;line-height:28px}
.m-toast{position:absolute;left:50%;bottom:28px;transform:translateX(-50%);background:rgba(34,34,34,.9);border-radius:28px;padding:4px 16px;color:#fff;font-size:16px;font-weight:500;letter-spacing:-.32px;white-space:nowrap}
.m-band{position:absolute;left:0;right:0;bottom:0;height:20px;background:rgba(242,37,68,.5);color:#fff;font-size:12px;font-weight:500;text-align:center;line-height:20px}
.m-timerow{height:44px;padding:8px 20px;box-sizing:border-box;display:flex;align-items:center;justify-content:space-between}
.m-pill{height:28px;padding:4px 12px;box-sizing:border-box;border-radius:28px;background:rgba(0,0,0,.5);color:#fff;font-size:14px;font-weight:500;letter-spacing:-.28px}
.m-round{width:28px;height:28px;border-radius:28px;box-sizing:border-box;display:flex;align-items:center;justify-content:center;font-size:13px}
.m-round:last-child{border:.875px solid #c4c4c4}
.m-listhead{padding:8px 20px;border-top:1px solid #e9e9e9;font-size:16px;font-weight:700;line-height:1.3}
.m-thumbs{display:flex;gap:8px;padding:0 20px 8px}.m-thumb{position:relative;width:156px;height:87px;border-radius:4px;background:linear-gradient(135deg,#888,#444)}
.m-thumb.sel{outline:2px solid #1d6ceb;outline-offset:-2px;filter:brightness(.6)}
.m-tabbar{height:60px;display:flex;border-top:1px solid #f0f0f0}.m-tabbar span{flex:1;display:flex;align-items:flex-end;justify-content:center;padding-bottom:8px;font-size:12px;font-weight:500;letter-spacing:-.5px;color:#7f7f7f}
.m-tabbar span.on{color:#1d6ceb}
.pair{display:flex;flex-wrap:wrap;gap:24px;margin-top:16px}.cap{font-size:12px;color:var(--sub);margin-bottom:6px}
.sheet{width:360px;background:#fff;color:#000;border:1px solid #ddd;display:flex;flex-direction:column;box-sizing:border-box}
.sheet.new{border-radius:8px 8px 0 0;padding:20px 0;gap:20px}.sheet.old{border-radius:10px 10px 0 0;padding-bottom:16px}
.s-title{height:26px;padding:0 20px;display:flex;justify-content:space-between;align-items:center;font-size:20px;font-weight:700;line-height:1.3}
.s-title.old{height:auto;padding:24px 20px;line-height:1}
.cards{display:flex;gap:40px;justify-content:center}.card{width:52px;height:71px;border:1.8px solid #d9d9d9;border-radius:5.5px;padding:3.6px;box-sizing:border-box;display:flex;flex-direction:column;gap:2.7px}
.card i{flex:1;background:#e9e9e9}.card.on{border-color:#1d6ceb}.card.on i{background:#1d6ceb}.card.g{display:grid;grid-template-columns:1fr 1fr}
.cardlab{display:flex;justify-content:space-around;font-size:14px;font-weight:500;color:#757575;padding:0 20px}.cardlab b{color:#1d6ceb}
.btn{margin:0 20px;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:500;color:#fff;background:#1d6ceb}
.btn.new{height:48px;letter-spacing:-.32px}.btn.old{height:50px;line-height:1;margin-top:20px}.btn.sec{background:#fff;color:#353535;border:1px solid #d9d9d9;height:48px;margin:0}
.btns{display:flex;gap:8px;padding:0 20px}.btns .btn{flex:1;margin:0}
.row{height:55px;padding:0 20px;display:flex;align-items:center;gap:8px;font-size:16px}.row.sel{color:#1d6ceb;justify-content:space-between}
.cb{width:18px;height:18px;border:1px solid #dcdcdc;border-radius:2px;box-sizing:border-box}.cb.on{background:#1d6ceb;border-color:#1d6ceb}
.tabs{display:flex;padding:0 24px}.tabs span{flex:1;text-align:center;height:30px;line-height:30px;font-size:16px;font-weight:500;color:#555;border-bottom:1px solid #d9d9d9}
.tabs span.on{font-weight:700;color:#1d6ceb;border-bottom:2px solid #1d6ceb}
.cal{display:flex;gap:4px;padding:0 20px}.cal span{width:44px;height:44px;border-radius:999px;display:flex;align-items:center;justify-content:center;font-size:16px}
.cal .o{color:#c4c4c4}.cal .r{background:#e2f1ff}.cal .sel{background:#1d6ceb;color:#fff}.cal .today{border:1px solid #1d6ceb;color:#1d6ceb}
.slider{position:relative;margin:0 20px;height:6px;border-radius:8px;background:#e9e9e9}.slider i{position:absolute;inset:0 auto 0 0;background:#1d6ceb;border-radius:8px}
.slider b{position:absolute;top:-7px;width:20px;height:20px;margin-left:-10px;border-radius:50%;background:#fff;border:1px solid #c4c4c4;box-sizing:border-box}
.ev{display:flex;flex-direction:column;gap:3px;padding:0 20px}.evchip{align-self:flex-start;background:#1d6ceb;color:#fff;border-radius:10px;padding:4px 7px;font-size:12px;font-weight:700;line-height:1}.evtime{font-size:14px;color:#7f7f7f}
details{border-top:1px solid var(--line);padding:8px 0}summary{cursor:pointer}details ul{margin:6px 0 0;padding-left:18px}details li{margin:3px 0}li.v{color:var(--warn)}
.warn{font-size:11px;background:var(--warnbg);color:var(--warn);padding:1px 6px;border-radius:999px;margin-left:4px}
.refs{display:flex;gap:10px;overflow-x:auto}.refs figure{margin:0;flex:none;text-align:center;font-size:12px}.refs img{width:150px;border:1px solid var(--line);border-radius:6px}
'''
page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>모두앱 부품 기준 세트</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css"><style>{css}</style></head><body><main>
<h1>모두앱 부품 기준 세트 — 현재 화면 추출본</h1>
<p class="meta">{e(d['meta']['made_at'])} · {e(d['meta']['scope'])} · {e(d['meta']['source'])}</p>
<p class="rule">{e(d['meta']['rule'])}<br>{e(d['meta']['caution'])}</p>
<section><h2>부품 견본 — 뽑은 값으로 다시 그린 것</h2><p class="meta">아래 실제 화면 그림과 나란히 보며 맞는지 대조하세요. 영상은 색 덩어리로 대신했습니다.</p>
<div class="stage">{spec}</div>{sheets}
<h2 style="margin-top:20px">실제 화면(대조용)</h2><div class="refs">{refs}</div></section>
<section><h2>한 화면 안에 섞여 있는 두 버전</h2><div class="scroll"><table>{mixed}</table></div></section>
<section><h2>색 {len(F['colors'])}가지</h2><div class="sws">{sw}</div></section>
<section><h2>글자 {len(F['type'])}단계</h2><p class="meta">글꼴 {e(F['font'])}</p><div class="scroll"><table>{ty}</table></div></section>
<section><h2>모서리 · 간격 · 그림자 · 아이콘</h2><div class="scroll"><table>
<tr><th>모서리</th><td>{'<br>'.join(f"<b>{r['value']}</b> {e(r['use'])}" for r in F['radius'])}</td></tr>
<tr><th>간격</th><td>{'<br>'.join(f"<b>{s['value']}</b> {e(s['use'])}" for s in F['spacing'])}</td></tr>
<tr><th>그림자·덮개</th><td>{'<br>'.join(f"{e(x['name'])}: {e(x['spec'])}" for x in F['effects'])}</td></tr>
<tr><th>아이콘</th><td>{'<br>'.join(f"<b>{x['size']}</b> {e(x['use'])}" for x in F['icon_sizes'])}</td></tr></table></div></section>
<section><h2>부품 {len(d['components'])}개 상세</h2>{comp}</section>
</main></body></html>'''
open(ROOT + 'outputs/moduapp/design-baseline/component-baseline.html', 'w').write(page)
print('ok')
