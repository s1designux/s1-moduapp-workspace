import json, collections, html
import os, re
from analyze import screens as S, NAMES, STATE_ORDER, comp

# Figma 부품 기록: 사본 페이지(SW-UX-GUIDE-V3.0-TEST › modu app (준비중), 80:16699)는 원본 페이지를 통째로 복제한 것.
# 사본 노드 번호 = 원본 번호 + 2461 (270화면 모두 크기·캡션 일치 확인)
COPY_FILE = 'cysG5U1udpQqVagYY1hWHW'
CF = {f['id']: f for f in json.load(open('copy_frames.json'))}
FIG = {
    'StatusBar': ['app_header'], 'More': ['app_header'], 'Chip': ['mode_chip'], 'm_chips': ['mode_chip'],
    'home': ['tabbar'], 'under security': ['tabbar'], 'dome camera': ['tabbar'], 'menu(hamburger)': ['tabbar'],
    'phone_navi': ['os_nav'], 'dome camera trouble': ['video_state'], 'Component 5': ['mode_badge'],
    'Component 53': ['dim_overlay'], 'Component 54': ['dim_overlay'], 'Component 11': ['dim_overlay'], 'Component 12': ['dim_overlay'],
    'Component 10/Frame 2087327495': ['dim_overlay', 'round_button'], 'Component 10/Frame 2087327496': ['round_button', 'time_pill'],
    'Component 7': ['round_button'], 'Component 8': ['round_button'], 'Component 9': ['round_button'], 'Component 10': ['round_button'],
    'ic_화살표, 더보기': ['round_button'], 'time': ['time_pill'], 'Frame 2087327570': ['playback_panel'],
    'DatePicker/Calendar Cell': ['datetime_picker'], 'calendar_arrow': ['datetime_picker'], 'tab': ['datetime_picker'],
    'ic_닫기': ['bottom_sheet'], 'close': ['bottom_sheet'], 'mobile_button': ['bottom_sheet'], 'm_button': ['bottom_sheet'],
    'Component 13': ['layout_picker'], 'Component 45': ['camera_list'], 'm_checkbox': ['camera_list'],
    'plus': ['ptz_pad'], 'minus': ['ptz_pad'],
}
UNKNOWN_FIG = collections.Counter()


def copy_id(oid):
    return f"2805:{int(oid.split(':')[1]) + 2461}"


def figma_keys(x):
    ks = []
    for n in CF[copy_id(x['id'])]['inst']:
        if n == 'Component 44':
            got = ['playback_panel', 'timeline', 'time_pill'] if x['mode'] == '녹화영상' else ['time_pill']
        elif n == 'state_emoji':
            got = ['camera_list'] if '움직임' in x['caption'] else ['svms_panel']
        else:
            got = FIG.get(n)
            if got is None:
                UNKNOWN_FIG[n] += 1
                got = []
        for k in got:
            if k not in ks:
                ks.append(k)
    # 부품이 아닌 글자 레이어로 확인되는 것
    texts = CF[copy_id(x['id'])]['texts']
    if any(re.match(r'^카메라 ?\d+$', t) for t in texts) and 'video_tile' not in ks:
        ks.append('video_tile')
    if any(re.search(r'배속으로|^일시 정지$|기본 속도로 재생|^30초 (앞|뒤)|캡쳐되었어요|원본 비율 유지|^화면 채우기$', t) for t in texts) and 'toast' not in ks:
        ks.append('toast')
    return ks


NO_FIGMA = {'video_tile', 'toast', 'svms_panel', 'page_dots'}  # Figma에 부품으로 잡히지 않는 것(그림·글자 레이어)
for x in S:
    x['visual_keys'] = list(x['keys'])
    x['figma_keys'] = figma_keys(x)
    x['keys'] = list(dict.fromkeys(x['visual_keys'] + x['figma_keys']))

OUT = '/Users/designgroup_02/s1-moduapp-workspace/outputs/moduapp/service-video/'
SHAPES = ['세로 기본 · 단일채널', '세로 기본 · 다채널', '가로 확대 · 단일채널', '가로 확대 · 다채널']
KEY_ORDER = [c['key'] for c in comp['components']] + ['os_nav']

# 부품 묶음 후보: core = 이 묶음을 대표하는 부품. 비율 = core가 나온 화면 중 묶음 전체가 함께 나온 비율
BUNDLES = [
    {'key': 'portrait_frame', 'name': '세로 기본 뼈대', 'members': ['app_header', 'mode_chip', 'video_tile', 'time_pill', 'tabbar'], 'core': 'app_header',
     'desc': '맨 위 현장 헤더 → 실시간/녹화 칩 → 영상 칸 → 시각 알약 → 맨 아래 탭바. 세로 화면의 바탕 틀'},
    {'key': 'single_list', 'name': '단일채널 영상 + 카메라 목록', 'members': ['video_tile', 'round_button', 'camera_list'], 'core': 'camera_list',
     'desc': '큰 영상 칸 아래 캡쳐 버튼, 그 아래 카메라 썸네일 2열 목록'},
    {'key': 'dim_controls', 'name': '딤 조작 세트', 'members': ['dim_overlay', 'mode_badge', 'round_button'], 'core': 'dim_overlay',
     'desc': '영상을 탭하면 어두운 덮개 위로 모드 배지·상단 아이콘 줄·원형 버튼이 한꺼번에 뜸'},
    {'key': 'dim_controls_paged', 'name': '딤 조작 세트 + 페이지 점', 'members': ['dim_overlay', 'mode_badge', 'round_button', 'page_dots'], 'core': 'page_dots',
     'desc': '다채널에서 카메라가 분할 수보다 많을 때 딤 아래에 페이지 점이 붙음'},
    {'key': 'toolbar_buttons', 'name': '상단 툴바 + 원형 버튼', 'members': ['mode_badge', 'round_button'], 'core': 'mode_badge',
     'desc': '가로 확대에서 딤 덮개를 따로 적지 않았어도 배지 줄과 아래 버튼 줄은 늘 같이 나옴'},
    {'key': 'playback', 'name': '녹화 재생 세트', 'members': ['playback_panel', 'timeline'], 'core': 'timeline',
     'desc': '재생 컨트롤 줄 + 시간바. 녹화영상 화면 아래쪽'},
    {'key': 'speed_toast', 'name': '재생 컨트롤 + 안내 토스트', 'members': ['playback_panel', 'toast'], 'core': 'toast',
     'desc': '배속·일시정지·30초 이동을 누르면 영상 가운데 토스트가 뜸'},
    {'key': 'sheet_datetime', 'name': '시트 + 날짜·시간 고르기', 'members': ['bottom_sheet', 'datetime_picker'], 'core': 'datetime_picker',
     'desc': '세로는 바텀시트, 가로는 오른쪽 패널·가운데 팝업 안에 달력과 시·분 휠'},
    {'key': 'sheet_layout', 'name': '시트 + 분할 수 고르기', 'members': ['bottom_sheet', 'layout_picker'], 'core': 'layout_picker',
     'desc': '"화면 구성" 시트·팝업 안에 그림 카드 또는 슬라이더 + 확인/적용'},
    {'key': 'panel_camera_list', 'name': '오른쪽 패널 + 카메라 목록', 'members': ['bottom_sheet', 'camera_list'], 'core': 'camera_list', 'shape_filter': '가로',
     'desc': '가로 확대에서 카메라 목록·움직임 감지는 오른쪽 패널로 열림'},
    {'key': 'sheet_svms', 'name': '시트 + 레이아웃 리스트·이벤트 목록', 'members': ['bottom_sheet', 'svms_panel'], 'core': 'svms_panel',
     'desc': 'SVMS 카메라 묶음 고르기와 이벤트 목록'},
    {'key': 'tile_state', 'name': '영상 칸 + 영상 상태 표시', 'members': ['video_tile', 'video_state'], 'core': 'video_state',
     'desc': '수신 불량 빨간 띠·카메라 없음 로고·신호 없음 표시가 영상 칸 안에 들어감'},
]

# Figma 부품 기록(파일 전체 합계, 기존 부품표에 저장된 숫자)과 눈으로 적은 기록 비교
FIGMA_TOTAL = {}
for c in comp['components']:
    if c['usage_screens']:
        FIGMA_TOTAL[c['key']] = max(c['usage_screens'].values())

total = collections.Counter(k for x in S for k in x['keys'])


def counts_of(sub, field):
    c = collections.Counter(k for x in sub for k in x[field])
    return {k: c[k] for k in KEY_ORDER if c[k]}


def cell(shape=None, state=None):
    return [x for x in S if (shape is None or x['shape'] == shape) and (state is None or x['state_type'] == state)]


def counts(sub):
    c = collections.Counter(k for x in sub for k in x['keys'])
    return {k: c[k] for k in KEY_ORDER if c[k]}


def bundle_stats(b, sub):
    if b.get('shape_filter'):
        sub = [x for x in sub if x['orientation'] == b['shape_filter']]
    core = [x for x in sub if b['core'] in x['keys']]
    full = [x for x in sub if all(m in x['keys'] for m in b['members'])]
    return len(full), len(core), full


# 유형별 대표 화면: 그 칸에서 가장 흔한 부품 조합에 가까운 화면
def representative(sub):
    if not sub:
        return None
    c = collections.Counter(k for x in sub for k in x['keys'])
    common = {k for k, n in c.items() if n / len(sub) >= 0.5}
    best = max(sub, key=lambda x: (len(common & set(x['keys'])) - len(set(x['keys']) - common), x['platform'] == 'common'))
    return best


types = []
for sh in SHAPES:
    for st in STATE_ORDER:
        sub = cell(sh, st)
        rep = representative(sub)
        types.append({
            'shape': sh, 'state': st, 'screen_count': len(sub),
            'platform_extra': dict(collections.Counter(x['platform'] for x in sub if x['platform'] != 'common')),
            'components': counts(sub),
            'components_visual': counts_of(sub, 'visual_keys'),
            'components_figma': counts_of(sub, 'figma_keys'),
            'bundles': [b['key'] for b in BUNDLES if bundle_stats(b, sub)[0] > 0],
            'representative': {'id': rep['id'], 'caption': rep['caption'], 'view': rep['view'], 'feature': rep['feature'], 'figma_link': rep['figma_link'],
                               'image': f"images/screen-types/{rep['id'].replace(':', '-')}.jpg", 'checked_copy_node': copy_id(rep['id'])} if rep else None,
            'screen_ids': [x['id'] for x in sub],
        })

bundles_out = []
for b in BUNDLES:
    full, core, fs = bundle_stats(b, S)
    by_shape = {}
    for sh in SHAPES:
        f, c, _ = bundle_stats(b, cell(sh))
        if c or f:
            by_shape[sh] = {'together': f, 'core_screens': c}
    by_state = collections.Counter(x['state_type'] for x in fs)
    bundles_out.append({**{k: b[k] for k in ['key', 'name', 'desc', 'members', 'core']},
                        'member_names': [NAMES[m] for m in b['members']],
                        'together_screens': full, 'core_screens': core,
                        'together_rate': round(full / core, 2) if core else None,
                        'by_shape': by_shape, 'by_state': dict(by_state)})

DIFF_MIN = 3  # 한 유형 안에서 두 기록이 이만큼 이상 다르면 차이로 표시
needs_review = [
    {'item': 'Figma 사본 파일을 기록으로 쓴 것', 'reason': f'원본 파일(PYnxdzOnjfmLV69sgQPseQ)이 아니라 river가 준 사본(SW-UX-GUIDE-V3.0-TEST {COPY_FILE}, 80:16699)에서 부품 이름을 받음. 270화면이 번호(+2461)·크기·캡션까지 모두 맞고 부품 수도 10-14 저장값과 같아 같은 화면으로 판단. 사본에서 화면을 고쳤다면 차이가 날 수 있음'},
    {'item': 'Figma 이름을 알 수 없는 부품', 'reason': "'Frame 2087327567'(녹화 가로 단일 22화면), 'Frame 2087327575'(16채널 화면 등 22화면)은 이름만으로 무엇인지 모름. 셈에서 뺌"},
    {'item': "'Component 9'의 정체", 'reason': '지난 분석은 페이지 점일 수 있다고 적었지만 세로 화면 18곳에 원형 버튼과 짝으로 나와 원형 버튼으로 셈'},
    {'item': "'state_emoji'의 소속", 'reason': '부품표에는 영상 상태 표시로 적혀 있지만 실제로는 "감지된 움직임/이벤트가 없어요" 빈 목록 그림. 목록 부품으로 옮겨 셈'},
    {'item': 'Figma에 부품으로 없는 것', 'reason': '영상 칸·토스트는 Figma에서 글자(카메라 이름표, 안내 문구)로만 확인. 페이지 점·SVMS 목록은 Figma 기록이 없어 눈으로 적은 기록만 씀'},
    {'item': 'Figma 기록은 덮인 부품도 셈', 'reason': '바텀시트·팝업 아래 깔린 탭바·헤더도 Figma에는 있음(스크린샷 2805:16433 확인). 그래서 "화면에 들어 있는 부품" 기준으로 셈. 눈에 보이는 것만 세려면 components_visual을 쓴다'},
    {'item': "'ok' 이름 부품", 'reason': '부품표에는 날짜 고르기로 적혀 있지만 스크린샷(2805:17232)으로 보니 목록의 체크(✓) 아이콘. 셈에서 뺌'},
    {'item': '녹화 다채널 "재생" 화면의 칩', 'reason': '11:24841(사본 2805:27302)은 녹화영상 화면인데 위 칩은 "실시간"이 눌려 있고 영상 배지는 "녹화영상". 디자인 확인 필요'},
    {'item': '대표 상태 하나로 나누기', 'reason': '한 화면에 여러 상태가 겹치면(예: 패널 안 빈 화면) 덮는 쪽을 대표로 잡음. 겹친 상태는 state_flags에 모두 남김'},
]

figma_compare = []
for k in KEY_ORDER:
    v = sum(1 for x in S if k in x['visual_keys']); f = sum(1 for x in S if k in x['figma_keys'])
    both = sum(1 for x in S if k in x['visual_keys'] and k in x['figma_keys'])
    figma_compare.append({'key': k, 'name': NAMES[k], 'visual_screens': v, 'figma_screens': f, 'both': both,
                          'visual_only': v - both, 'figma_only': f - both, 'combined': sum(1 for x in S if k in x['keys'])})

type_diffs = []
for t in types:
    for k in KEY_ORDER:
        v = t['components_visual'].get(k, 0); f = t['components_figma'].get(k, 0)
        if k in NO_FIGMA and k not in ('video_tile', 'toast'):
            continue
        if abs(v - f) >= DIFF_MIN:
            type_diffs.append({'shape': t['shape'], 'state': t['state'], 'key': k, 'name': NAMES[k], 'visual': v, 'figma': f, 'screens': t['screen_count']})

result = {
    'meta': {
        'service': 'video', 'layer': 'service', 'title': '모두앱 영상 — 화면 유형별 부품·부품 묶음',
        'source': 'video-v2-screen-analysis.json(눈으로 적은 부품 기록) + Figma 부품 기록(사본 파일 cysG5U1udpQqVagYY1hWHW · 80:16699, 원본 번호+2461) + video-v2-components.json(부품 19개)',
        'analyzed_at': '2026-10-21', 'basis': 'NVR(녹화기) 연동 신규 기준만. 레거시·클라우드영상 대응 제외',
        'screens': len(S),
        'status': 'done',
        'method': '화면 모양(세로/가로 × 단일/다채널)과 대표 상태(8가지)로 나눈 뒤, 두 기록(눈으로 적은 부품 글 → 부품 19개+기기 내비게이션 바 / Figma 부품 이름 → 같은 부품)을 화면마다 합쳐 셈. 한쪽이라도 있으면 있는 것으로 봄(components), 기록별 숫자는 components_visual·components_figma. 묶음 비율 = 대표 부품이 나온 화면 중 묶음 전체가 함께 나온 비율. 유형마다 대표 화면 1개(23개)를 스크린샷으로 대조함',
    },
    'axes': {'shape': SHAPES, 'state': STATE_ORDER,
             'platform_note': 'iOS 가로(874×402) 16화면, 안드로이드 가로 16화면, 폴드 세로(476×752) 3화면은 platform_extra로 따로 표시'},
    'type_matrix': types,
    'bundles': bundles_out,
    'figma_compare': figma_compare,
    'type_diffs': type_diffs,
    'figma_unknown_instances': dict(UNKNOWN_FIG),
    'screens': [{k: x[k] for k in ['id', 'view', 'shape', 'platform', 'feature', 'caption', 'state_raw', 'state_type', 'state_flags', 'keys', 'visual_keys', 'figma_keys', 'figma_link']} | {'copy_node': copy_id(x['id'])} for x in S],
    'needs_review': needs_review,
    'screenshot_check': {'checked': 25, 'nodes': 'type_matrix[].representative.checked_copy_node 23개 + 2805:17232·2805:16433',
                         'result': '23개 대표 화면 모두 유형(모양·상태)과 부품 표가 맞음. 2개 의심 화면에서 Figma 이름 오해 1건(ok)과 덮인 부품 셈 방식을 확인'},
}
json.dump(result, open(OUT + 'video-v2-screen-type-components.json', 'w'), ensure_ascii=False, indent=1)

# ---------- HTML ----------
e = html.escape


def heat(n, d, v=None, f=None):
    if not d or not n:
        return '<td class="z">·</td>'
    r = n / d
    lv = 4 if r >= .9 else 3 if r >= .6 else 2 if r >= .3 else 1
    mark, tip = '', f'{n}/{d}화면'
    if v is not None:
        tip += f' · 눈 {v} / Figma {f}'
        if abs(v - f) >= DIFF_MIN:
            mark = '<i class="dot"></i>'
    return f'<td class="h{lv}" title="{tip}">{n}{mark}</td>'


parts = []
# 1. 유형 지도
rows = ''
for sh in SHAPES:
    tds = ''.join(f'<td>{len(cell(sh, st)) or "·"}</td>' for st in STATE_ORDER)
    rows += f'<tr><th>{e(sh)}</th>{tds}<td><b>{len(cell(sh))}</b></td></tr>'
parts.append(f'''<section><h2>1. 화면 유형 지도</h2>
<p class="lead">세로/가로 × 단일/다채널 4가지 모양과 8가지 상태로 270개 화면을 나눈 결과입니다. 칸의 숫자는 화면 수입니다.</p>
<div class="scroll"><table class="grid"><tr><th></th>{''.join(f'<th>{e(s)}</th>' for s in STATE_ORDER)}<th>합계</th></tr>{rows}</table></div>
<p class="note">사본 파일에서 스크린샷을 찍었습니다(원본과 같은 화면). 기기별: iOS 가로 16 · 안드로이드 가로 16 · 폴드 세로 3. PTZ를 켜면 세로로 바뀌는 화면 1개는 세로에 넣었습니다.</p></section>''')

# 2. 모양별 부품 표
for si, sh in enumerate(SHAPES, 1):
    sts = [st for st in STATE_ORDER if cell(sh, st)]
    allc = counts(cell(sh))
    head = ''.join(f'<th>{e(st)}<br><small>{len(cell(sh, st))}화면</small></th>' for st in sts)
    body = ''
    for k in KEY_ORDER:
        if k not in allc:
            continue
        def hv(sub):
            return heat(counts(sub).get(k, 0), len(sub), counts_of(sub, 'visual_keys').get(k, 0), counts_of(sub, 'figma_keys').get(k, 0)) if k not in NO_FIGMA or k in ('video_tile', 'toast') else heat(counts(sub).get(k, 0), len(sub))
        body += f'<tr><th class="l">{e(NAMES[k])}</th>' + ''.join(hv(cell(sh, st)) for st in sts) + hv(cell(sh)) + '</tr>'
    reps = ''
    for st in sts:
        t = next(x for x in types if x['shape'] == sh and x['state'] == st)
        r = t['representative']
        reps += f'''<div class="rep"><a href="{e(r['image'])}" target="_blank"><img class="{'pt' if sh.startswith('세로') else 'ls'}" src="{e(r['image'])}" alt="{e(r['caption'])}" loading="lazy"></a>
<div><b>{e(st)}</b><br>{e(r['caption'])}<br><small>{e(r['feature'])}</small><br><a href="{e(r['figma_link'])}" target="_blank">Figma에서 보기</a></div></div>'''
    parts.append(f'''<section><h2>2-{si}. {e(sh)} — 상태별 부품</h2>
<p class="lead">칸의 숫자 = 그 상태 화면 중 이 부품이 있는 화면 수(두 기록 중 한쪽이라도 있으면 셈). 진할수록 거의 항상 나옵니다. 주황 점 = 두 기록이 3화면 이상 다른 칸(마우스를 올리면 숫자).</p>
<div class="scroll"><table class="grid heat"><tr><th class="l">부품</th>{head}<th>전체<br><small>{len(cell(sh))}화면</small></th></tr>{body}</table></div>
<h3>대표 화면 (Figma 스크린샷으로 대조)</h3><div class="reps">{reps}</div></section>''')

# 3. 부품 묶음
brow = ''
for b in bundles_out:
    shp = ' · '.join(f'{e(k)} {v["together"]}' for k, v in b['by_shape'].items() if v['together'])
    stp = ' · '.join(f'{e(k)} {v}' for k, v in sorted(b['by_state'].items(), key=lambda a: -a[1]))
    rate = f'{int(b["together_rate"] * 100)}%' if b['together_rate'] is not None else '-'
    brow += f'''<tr><th class="l">{e(b['name'])}<br><small>{e(b['desc'])}</small></th>
<td>{' + '.join(e(n) for n in b['member_names'])}</td><td class="num">{b['together_screens']}</td><td class="num">{rate}</td><td>{shp}</td><td>{stp}</td></tr>'''
parts.append(f'''<section><h2>3. 부품 묶음</h2>
<p class="lead">늘 함께 나오는 부품 조합입니다. "함께 나온 비율"은 묶음의 대표 부품이 나온 화면 중 나머지도 다 같이 나온 비율입니다.</p>
<div class="scroll"><table class="grid"><tr><th class="l">묶음</th><th>들어가는 부품</th><th>화면 수</th><th>함께 나온 비율</th><th>모양별</th><th>상태별</th></tr>{brow}</table></div></section>''')

# 4. 두 기록 비교
frow = ''
for f in figma_compare:
    if f['key'] in NO_FIGMA and f['key'] not in ('video_tile', 'toast'):
        fig, only = '기록 없음', ''
    else:
        fig = f['figma_screens']; only = f"눈에만 {f['visual_only']} · Figma에만 {f['figma_only']}"
    warn = ' class="warn"' if f['key'] not in NO_FIGMA and (f['visual_only'] >= 10 or f['figma_only'] >= 10) else ''
    frow += f'<tr{warn}><th class="l">{e(f["name"])}</th><td class="num">{f["visual_screens"]}</td><td class="num">{fig}</td><td>{only}</td><td class="num"><b>{f["combined"]}</b></td></tr>'
drow = ''.join(f'<tr><td>{e(d["shape"])}</td><td>{e(d["state"])}</td><th class="l">{e(d["name"])}</th><td class="num">{d["visual"]}</td><td class="num">{d["figma"]}</td><td class="num">{d["screens"]}</td></tr>' for d in type_diffs)
parts.append(f'''<section><h2>4. 두 기록 비교</h2>
<p class="lead">화면을 눈으로 보고 적은 기록과 Figma 부품 이름 기록을 화면마다 맞대 본 결과입니다. 한쪽에만 10화면 이상 있는 줄은 노랗게 칠했습니다. 위 표는 두 기록을 합친 숫자(맨 오른쪽)를 씁니다.</p>
<div class="scroll"><table class="grid"><tr><th class="l">부품</th><th>눈으로 적은 기록</th><th>Figma 기록</th><th>한쪽에만 있음</th><th>합친 숫자</th></tr>{frow}</table></div>
<details><summary>유형 안에서 3화면 이상 다른 곳 ({len(type_diffs)}곳) 펼쳐 보기</summary>
<div class="scroll"><table class="grid"><tr><th>모양</th><th>상태</th><th class="l">부품</th><th>눈</th><th>Figma</th><th>유형 화면 수</th></tr>{drow}</table></div></details></section>''')

nr = ''.join(f'<li><b>{e(n["item"])}</b> — {e(n["reason"])}</li>' for n in needs_review)
parts.append(f'<section><h2>5. 아직 못 믿는 곳</h2><ul class="nr">{nr}</ul></section>')

page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>영상 화면 유형별 부품</title>
<style>
:root{{--bg:#f6f7f9;--card:#fff;--ink:#1d2230;--sub:#5b6475;--line:#e2e6ee;--h1:#e8effd;--h2:#c4d6fa;--h3:#7ea6f2;--h4:#2f6be6;--warn:#fff4d6}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#12151c;--card:#1b1f29;--ink:#e6e9f0;--sub:#9aa3b5;--line:#2c3240;--h1:#1f2a44;--h2:#24407a;--h3:#3561b8;--h4:#4f86f0;--warn:#3a3218}}}}
:root[data-theme="dark"]{{--bg:#12151c;--card:#1b1f29;--ink:#e6e9f0;--sub:#9aa3b5;--line:#2c3240;--h1:#1f2a44;--h2:#24407a;--h3:#3561b8;--h4:#4f86f0;--warn:#3a3218}}
body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.55 -apple-system,"Apple SD Gothic Neo","Pretendard",sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:24px 16px 64px}}
h1{{font-size:22px;margin:0 0 4px}} h2{{font-size:17px;margin:0 0 6px}} h3{{font-size:14px;margin:18px 0 8px}}
section{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px;margin:16px 0}}
.lead{{color:var(--sub);margin:0 0 12px}} .note{{color:var(--sub);font-size:12px;margin:10px 0 0}}
.scroll{{overflow-x:auto}} table.grid{{border-collapse:collapse;width:100%;font-size:13px}}
.grid th,.grid td{{border:1px solid var(--line);padding:6px 8px;text-align:center;vertical-align:middle}}
.grid th.l{{text-align:left;font-weight:600}} .grid small{{color:var(--sub);font-weight:400}} .num{{font-variant-numeric:tabular-nums}}
.heat td{{min-width:54px;font-variant-numeric:tabular-nums}} .z{{color:var(--line)}}
.h1{{background:var(--h1)}} .h2{{background:var(--h2)}} .h3{{background:var(--h3);color:#fff}} .h4{{background:var(--h4);color:#fff;font-weight:700}}
tr.warn td,tr.warn th{{background:var(--warn)}}
.reps{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:10px}}
.dot{{display:inline-block;width:6px;height:6px;border-radius:50%;background:#f08a24;margin-left:3px;vertical-align:super}}
.rep img{{display:block;border-radius:6px;border:1px solid var(--line)}} .rep img.pt{{width:96px}} .rep img.ls{{width:200px}}
.rep{{display:flex;gap:10px;border:1px solid var(--line);border-radius:10px;padding:10px;font-size:13px}}
.ph{{flex:none;width:72px;height:96px;border:1px dashed var(--sub);border-radius:6px;display:flex;align-items:center;justify-content:center;text-align:center;color:var(--sub);font-size:11px}}
a{{color:var(--h4)}} .nr li{{margin:4px 0}}
.top{{color:var(--sub)}} summary{{cursor:pointer;margin:14px 0 8px;font-weight:600}}
</style></head><body><main>
<h1>모두앱 영상 — 화면 유형별 부품</h1>
<p class="top">신규 기준(2026-10 Figma, NVR) 화면 270개 · 2026-10-21 · 눈으로 적은 기록 + Figma 부품 기록 · 대표 화면 23개 스크린샷 대조</p>
{''.join(parts)}
</main></body></html>'''
open(OUT + 'video-v2-screen-type-components.html', 'w').write(page)
print('ok')
for b in bundles_out:
    print(b['name'], b['together_screens'], b['core_screens'], b['together_rate'], b['by_shape'])
