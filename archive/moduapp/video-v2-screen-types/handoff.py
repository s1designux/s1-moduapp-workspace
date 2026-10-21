# 다른 세션이 가져다 쓸 수 있게 영상 탭 NVR 분석을 넘겨주기 꾸러미로 정리한다
import json, collections, os, re
OUT = '/Users/designgroup_02/s1-moduapp-workspace/outputs/moduapp/service-video/'
TODAY = '2026-10-21'

comp = json.load(open(OUT + 'video-v2-components.json'))
ana = json.load(open(OUT + 'video-v2-screen-analysis.json'))
typ = json.load(open(OUT + 'video-v2-screen-type-components.json'))
ctx = json.load(open(OUT + 'video-v2-context-components.json'))
geo = json.load(open('inst_geo.json'))
ngeo = json.load(open('node_geo.json'))
SCR = {x['id']: x for x in typ['screens']}
CID = {x['copy_node']: x for x in typ['screens']}

# ---------- 1. 부품표 바로잡기 ----------
C = {c['key']: c for c in comp['components']}
if 'os_nav' not in C:
    t = C['tabbar']
    t['figma_names'] = [n for n in t['figma_names'] if n != 'phone_navi']
    t['usage_screens'].pop('phone_navi', None)
    v = C['video_state']
    v['figma_names'] = [n for n in v['figma_names'] if n != 'state_emoji']
    v['usage_screens'].pop('state_emoji', None)
    cl = C['camera_list']
    cl['figma_names'] += ['state_emoji']
    cl['usage_screens']['state_emoji'] = 8
    cl['variants'] = cl['variants']  # '감지 없음(빈 화면)'이 이미 있음
    d = C['datetime_picker']
    d['figma_names'] = [n for n in d['figma_names'] if n != 'ok']
    d['usage_screens'].pop('ok', None)
    comp['components'].append({
        'key': 'os_nav', 'name': '기기 시스템 내비게이션 바', 'scope': '기기(안드로이드)',
        'role': '화면 맨 아래 안드로이드 시스템 버튼 줄(최근 앱 · 홈 · 뒤로). 앱 부품이 아니라 기기 화면 틀',
        'figma_names': ['phone_navi'], 'usage_screens': {'phone_navi': 141},
        'used_in': ['세로 화면 전체(141)'], 'variants': [], 'figma_local_component': []})
    comp['meta']['corrections'] = [
        {'at': TODAY, 'what': "'phone_navi'는 하단 탭바가 아니라 기기 내비게이션 바 → os_nav로 옮김", 'evidence': '사본 2805:16516 스크린샷'},
        {'at': TODAY, 'what': "'state_emoji'는 영상 상태 표시가 아니라 빈 목록 그림(감지된 움직임/이벤트가 없어요) → camera_list로 옮김", 'evidence': '사본 2805:17656 스크린샷'},
        {'at': TODAY, 'what': "'ok'는 날짜 고르기의 확인 버튼이 아니라 목록의 체크(✓) 아이콘 → 날짜 고르기에서 뺌", 'evidence': '사본 2805:17232 스크린샷'},
    ]
    comp['meta']['needs_review_added'] = [
        {'at': TODAY, 'what': "'Component 13'은 layout_picker로 적혀 있지만 가로 화면 아래 780×80·780×120 띠 자리에 있음 — 딤 아래쪽 받침일 가능성", 'evidence': '사본 메타데이터 자리값'},
        {'at': TODAY, 'what': "'Frame 2087327575'(16채널 화면 등 23곳, 780×360 전체)는 영상 칸 격자, 'Frame 2087327567'(가로 아래 780×39·431×39)는 가로 시간바로 보임 — 이름 미정", 'evidence': '사본 메타데이터 자리값'},
    ]
    json.dump(comp, open(OUT + 'video-v2-components.json', 'w'), ensure_ascii=False, indent=1)
C = {c['key']: c for c in comp['components']}
KEYS = [c['key'] for c in comp['components']]

# ---------- 꼬리표 ----------
REUSE = {
    'app_header': '공통 뼈대', 'mode_chip': '공통 뼈대', 'tabbar': '공통 뼈대', 'os_nav': '기기 틀',
    'video_tile': '공통 뼈대', 'video_state': '공통 뼈대', 'mode_badge': '공통 뼈대(아이콘 줄의 PTZ 아이콘은 PTZ 카메라 전용, 레이아웃(별 폴더) 아이콘은 SVMS 고객 전용)',
    'dim_overlay': '공통 뼈대', 'round_button': '공통 뼈대', 'page_dots': '공통 뼈대', 'time_pill': '공통 뼈대',
    'playback_panel': '공통 뼈대(녹화)', 'timeline': '공통 뼈대(녹화)', 'datetime_picker': '공통 뼈대(녹화)',
    'bottom_sheet': '공통 뼈대', 'layout_picker': '공통 뼈대(다채널)', 'camera_list': '공통 뼈대(움직임 감지 탭은 NVR 기준 기능)',
    'toast': '공통 뼈대', 'ptz_pad': 'PTZ 카메라 전용', 'svms_panel': 'SVMS 고객 전용',
}
CTX_SCOPE = {
    'watch': '공통 뼈대', 'controls': '공통 뼈대', 'trouble': '공통 뼈대(상태 종류는 NVR 기준)', 'zoom': '공통 뼈대',
    'layout': '공통 뼈대', 'ratio': '공통 뼈대', 'page': '공통 뼈대', 'camera': '공통 뼈대', 'group': 'SVMS 고객 전용',
    'datetime': '공통 뼈대(녹화)', 'playback': '공통 뼈대(녹화)', 'event': 'NVR 기준 기능(움직임 감지) + SVMS 고객 전용(이벤트 목록)',
    'capture': '공통 뼈대', 'ptz': 'PTZ 카메라 전용', 'more': '틀은 공통, 메뉴 내용은 NVR 기준(상세 설정 = NVR 웹뷰어 설정)',
}
NVR_ONLY = [
    {'what': 'NVR 2차 로그인(통합계정 + NVR 계정, NVR 비밀번호를 바꾸면 앱 재로그인)', 'where': '영상 탭 들어가기 전', 'evidence': '모두앱 사양 비교표(클라우드 프로젝트)'},
    {'what': '더보기 › 상세 설정 = NVR 웹뷰어 설정 화면', 'where': '기타 메뉴(더보기)', 'evidence': '11:14553'},
    {'what': '움직임 감지 탭(NVR이 보내는 움직임 이벤트 목록)', 'where': '녹화 · 카메라 목록 옆 탭 / 가로 오른쪽 패널', 'evidence': '11:14771 · 11:31689'},
    {'what': 'PTZ 조종판·제어 속도(PTZ 카메라가 붙은 경우)', 'where': '실시간 단일채널', 'evidence': '11:17164 · 11:17356'},
    {'what': 'SVMS 레이아웃 리스트·이벤트 목록·이벤트 종류(기업용 SVMS 고객)', 'where': '딤 위 별 폴더 버튼 / 녹화 탭', 'evidence': '11:17006 · 11:14983'},
    {'what': '영상 칸 상태 4가지(수신 불량·카메라 없음·신호 없음·빈 칸)는 NVR 연결 기준으로 정의됨', 'where': '영상 칸', 'evidence': '11:14122 · 11:14192 · 11:14271'},
]

# ---------- 2. 작은 사양표 ----------
FIGNAME_FOR = collections.defaultdict(list)
for c in comp['components']:
    for n in c['figma_names']:
        FIGNAME_FOR[c['key']].append(n)
SHAPE_OF = {'360x780': '세로', '476x752': '폴드 세로', '780x360': '가로', '874x402': 'iOS 가로'}


def measured(names):
    out = []
    for n in names:
        rows = geo.get(n, [])
        rows = [r for r in rows if r[0] in CID]
        if not rows:
            continue
        cnt = collections.Counter((SHAPE_OF.get(f'{r[1]}x{r[2]}', f'{r[1]}x{r[2]}'), f'{r[5]}×{r[6]}', f'x{r[3]} · y{r[4]}') for r in rows)
        out.append({'figma_name': n, 'screens': len({r[0] for r in rows}),
                    'common': [{'screen': a, 'size': b, 'pos': p, 'count': k} for (a, b, p), k in cnt.most_common(3)]})
    return out


SPEC_RULE = {r['topic']: r for r in ana['spec_rules']}
FIXED = {  # 지난 분석의 치수 기록(spec_rules · local_component_detail)과 스크린샷에서 옮긴 것
    'app_header': ['세로 위 StatusBar 27 아래 헤더 줄(높이 56, 좌우 여백 20)', '현장명 + ▾(24×24) / 아래 줄 지점·고객번호'],
    'mode_chip': ['헤더 줄 오른쪽 두 칸 칩, 높이 30 (실시간 60~72 · 녹화영상 69~81 폭)', '선택된 칩 파랑 채움'],
    'tabbar': ['아이콘 32×32 네 개(x 58·148·238·328), 글자 홈·경비·영상·전체'],
    'os_nav': ['360×48, 화면 맨 아래(y 732)'],
    'video_tile': ['세로 단일 360×202(16:9) · 썸네일 156×87', '세로 2채널 360×234~262 · 3채널 360×155~174 · 8채널 179×116~130(2열)',
                   '가로 4채널 319×179 · 9채널 212×119 · 16채널 158×88 · 가로 단일은 좌우 검은 여백', '칸 왼쪽 위 카메라 이름표, 선택 칸 파란 테두리'],
    'video_state': [SPEC_RULE['신호없음/카메라없음']['values'], '수신 불량: 칸 아래 빨간 띠 + 흰 글자'],
    'mode_badge': ['가로 상단 줄 395×36(iOS 405×36)', '왼쪽 "● 실시간"(빨간 점) / "녹화영상" 배지, 오른쪽 흰 아이콘(28×28) 줄', '변형 24가지: 영상 유형 2 × 비율 2 × PTZ 3 × 카메라목록 2'],
    'dim_overlay': [SPEC_RULE['딤']['values'], '세로 덮개 360×470~528(영상 칸 위), 가로 780×360 전체'],
    'round_button': ['원형 40×40 회색 버튼', '가로 아래 줄 395×40 — 왼쪽 메뉴·움직임 감지·달력·캡쳐, 오른쪽 축소', '날짜·시간 칩 147~151×28'],
    'page_dots': ['딤 아래 가운데, 42×28 자리', '점 규칙: 1페이지 없음 · 2~5개 모두 · 6개 이상 5개 + 끝 작게 · 7개 이상 넘길 때 양 끝 작게'],
    'time_pill': ['세로 날짜시간 줄 360×44(영상 바로 아래)', '가운데 회색 알약 + 오른쪽 캡쳐(세로 단일채널만. 다채널은 캡쳐 없음) · 녹화는 왼쪽 달력 추가'],
    'playback_panel': ['세로 360×102(녹화 영상 아래, 재생 버튼 + 날짜시간 줄) · 실시간은 같은 부품의 날짜시간 줄만(360×45)',
                       '가로 가운데 재생 버튼 묶음 360×56', '배속 버튼 "2x" 자리 = 빨리감기 자리, 배속 중 30초 버튼 흐림'],
    'timeline': ['10초 눈금 + 가운데 현재 위치선 + 주황 이벤트 점', '가로 아래 780×39(단일 iOS 431×39) — 이름 확인 필요'],
    'datetime_picker': ['달력 칸 44×44, 월 이동 화살표 20×20', '날짜/시간 탭 156×32 두 칸', '녹화 있는 날 하늘색 동그라미 · 오늘 파란 테두리 · 고른 날 파랑 채움'],
    'bottom_sheet': [SPEC_RULE['바텀시트']['values'], '버튼: 세로 한 개 320×48 / 둘이면 반씩, 가로 440×48', '닫기 X 24×24 오른쪽 위'],
    'layout_picker': ['그림 카드 안: 카드 3개 가로 줄 + 아래 이름(1×2 등)', '슬라이더 안: 3단 눈금 + 이름, 고른 값 파랑'],
    'camera_list': ['제목줄 360×38("카메라 목록" + 오른쪽 탭/버튼)', '2열 썸네일 156×87, 선택 칸 파란 테두리 + 재생 중 막대', '빈 목록 그림 64×64 + 한 줄 글'],
    'toast': [SPEC_RULE['토스트']['values'], '자리: 세로·가로 모두 영상 아래 가운데(스크린샷 확인)'],
    'ptz_pad': ['"PTZ 모드" 제목 + 원형 방향 패드(가운데 빈 원, 8방향 화살표) + 확대/축소 세로 막대(+/− 24×24)'],
    'svms_panel': ['목록 줄: 고른 줄 파란 글씨 + 오른쪽 체크, 결정 버튼 없음', '이벤트 목록: 파란 종류 칩 + 일시, 거르기 "이벤트 전체 ▾"'],
}
CTX_OF = collections.defaultdict(list)
for c_ in ctx['contexts']:
    for k in c_['core_components']:
        CTX_OF[k['key']].append(c_['name'])
    for b in c_['bundles']:
        pass
REP = {}
for t in typ['type_matrix']:
    r = t['representative']
    if r:
        for k in t['components']:
            REP.setdefault(k, r['id'])

sheet = []
for k in KEYS:
    c = C[k]
    sheet.append({
        'key': k, 'name': c['name'], 'reuse_scope': REUSE[k], 'role': c['role'], 'variants': c['variants'],
        'figma_names': c['figma_names'], 'spec': FIXED.get(k, []),
        'measured_in_figma': measured(c['figma_names']),
        'contexts': CTX_OF.get(k, []), 'evidence_screen': REP.get(k),
        'confidence': '그림 확인 + Figma 치수' if measured(c['figma_names']) else '그림 확인(치수는 Figma 확인 필요)',
    })
json.dump({'meta': {'title': '모두앱 영상(NVR) — 부품별 작은 사양표', 'made_at': TODAY,
                    'how': 'spec = 지난 분석 치수 기록과 스크린샷에서 옮긴 값. measured_in_figma = 사본 파일(cysG5U1udpQqVagYY1hWHW · 80:16699) 메타데이터에서 잰 크기·자리(화면 왼쪽 위 기준, 가장 많은 3가지)',
                    'not_covered': '색 · 글자 크기 · 모서리 · 그림자 같은 디자인 시스템 값은 재지 않음'},
           'components': sheet}, open(OUT + 'video-v2-spec-sheet.json', 'w'), ensure_ascii=False, indent=1)

# ---------- 3. 용어 사전 ----------
ALIAS = collections.defaultdict(collections.Counter)
import sys
sys.path.insert(0, '.')
from analyze import map_component
for v in ana['views']:
    for g in v['groups']:
        for s in g['screens']:
            for t in s['components']:
                for k in map_component(t):
                    ALIAS[k][re.sub(r'\(.*', '', t).strip()] += 1
ONSCREEN = {
    'app_header': ['8층 사무실 ▾', '에스원 본사 · N1234567'], 'mode_chip': ['실시간', '녹화영상'], 'tabbar': ['홈', '경비', '영상', '전체'],
    'mode_badge': ['● 실시간', '● 녹화영상'], 'time_pill': ['2026.09.09. 15:53:20'], 'bottom_sheet': ['더보기', '화면 구성', '레이아웃 리스트', '날짜, 시간 선택', 'PTZ 제어 속도', '이벤트 종류'],
    'layout_picker': ['화면 구성', '1×2 · 1×3 · 2×4', '2채널 · 3채널 · 8채널', '확인', '적용'], 'camera_list': ['카메라 목록', '움직임 감지', '감지된 움직임이 없어요.'],
    'datetime_picker': ['날짜', '시간', '시간 선택', '취소', '확인', '적용'], 'toast': ['기본 속도로 재생', '일시 정지', '2배속으로 빨리감기', '30초 뒤로', '현재 화면이 캡쳐되었어요', '원본 비율 유지', '화면 채우기', '1.5X', '원본'],
    'video_state': ['영상 수신 상태가 좋지 않음', '신호없음', '에스원'], 'ptz_pad': ['PTZ 모드', '카메라 방향', '확대/축소', '제어 속도 보통(4) ▾'],
    'svms_panel': ['레이아웃 리스트', '기본 카메라 목록', '이벤트 목록', '이벤트 전체 ▾'], 'playback_panel': ['2x', '-2x'], 'page_dots': [],
}
gl_parts = [{'key': k, 'name': C[k]['name'], 'also_called': [a for a, _ in ALIAS[k].most_common(6) if a != C[k]['name']],
             'figma_names': C[k]['figma_names'], 'on_screen_text': ONSCREEN.get(k, [])} for k in KEYS]
gl_terms = [
    {'term': '딤', 'means': '영상을 한 번 누르면 위·아래가 검게 깔리며 조작 버튼이 뜨는 상태', 'also_called': ['영상 뷰 딤', '조작 버튼 덮개', '컨트롤 표시']},
    {'term': '세로 기본 / 가로 확대', 'means': '화면 방향. 가로 확대는 전체화면 버튼 또는 기기 회전으로 들어감', 'also_called': ['기본', '확대', '전체화면']},
    {'term': '단일채널 / 다채널', 'means': '카메라 1대를 크게 / 여러 대를 격자로', 'also_called': ['1채널', 'N채널', '분할']},
    {'term': '분할 표기', 'means': '세로 1×2·1×3·2×4(2·3·8채널), 가로 2×2·3×3·4×4(4·9·16채널)', 'also_called': ['화면 구성']},
    {'term': '화면 구성 ≠ 레이아웃 리스트', 'means': '화면 구성 = 한 화면에 몇 칸으로 볼지(분할 수, layout_picker). 레이아웃 리스트 = SVMS 고객이 미리 묶은 카메라 묶음 고르기(svms_panel). 이름이 비슷하지만 다른 기능', 'also_called': ['분할 수', '카메라 묶음']},
    {'term': '바텀시트', 'means': '세로에서 아래에서 올라오는 창(제목 + 닫기 X)', 'also_called': ['시트']},
    {'term': '가운데 팝업', 'means': '가로에서 가운데 뜨는 창(폭 최대 480, 높이 화면의 80%)', 'also_called': ['가운데 시트', '팝업']},
    {'term': '오른쪽 패널', 'means': '가로에서 오른쪽에 붙는 창, 영상은 왼쪽으로 작아짐', 'also_called': ['측면 패널']},
    {'term': '토스트', 'means': '영상 아래 가운데 잠깐 뜨는 알림 알약', 'also_called': ['안내 토스트', '배율 표시']},
    {'term': '맥락', 'means': '사용자가 하려는 일 15가지(맥락 파일의 contexts)', 'also_called': ['기능 묶음']},
    {'term': '부품 묶음', 'means': '거의 늘 함께 나오는 부품 조합 12개(유형 파일의 bundles)', 'also_called': []},
    {'term': '대표 상태', 'means': '화면 하나에 붙인 상태 8가지 중 하나(덮는 쪽 우선)', 'also_called': ['state_type']},
    {'term': '원본 번호 / 사본 번호', 'means': '원본 Figma 화면 번호 11:NNNNN, 사본 파일 번호 2805:(NNNNN+2461)', 'also_called': []},
]
gl_states = [{'term': s, 'means': m} for s, m in [
    ('기본', '아무것도 안 덮인 화면'), ('버튼 뜬 상태(딤)', '딤이 떠 있음'), ('바텀시트 열림', '세로 시트'), ('가운데 팝업', '가로 팝업'),
    ('오른쪽 패널', '가로 패널'), ('토스트', '토스트가 뜬 순간'), ('영상 안 나옴', '수신 불량·카메라 없음·신호 없음'), ('빈 화면', '목록에 기록이 없음')]]
json.dump({'meta': {'title': '모두앱 영상(NVR) — 용어 사전', 'made_at': TODAY},
           'components': gl_parts, 'terms': gl_terms, 'states': gl_states, 'contexts': [{'key': c_['key'], 'name': c_['name'], 'goal': c_['goal']} for c_ in ctx['contexts']]},
          open(OUT + 'video-v2-glossary.json', 'w'), ensure_ascii=False, indent=1)

# ---------- 4. 꼬리표를 기존 결과에 붙이기 ----------
IMG_IDS = set()
for dr in ['images/screen-types', 'images/contexts']:
    for f in os.listdir(OUT + dr):
        IMG_IDS.add('11:' + f.split('-')[1].split('.')[0])
for c_ in ctx['contexts']:
    c_['scope'] = CTX_SCOPE[c_['key']]
    c_['confidence'] = {'placement': '그림 확인', 'flow': '그림 확인', 'counts': '데이터로 셈'}
    for d in c_['differences']:
        ids = re.findall(r'11:\d+', d['evidence'])
        d['confidence'] = '그림 확인' if ids and all(i in IMG_IDS for i in ids) else ('데이터로 셈' if ids else '추정')
for r in ctx['rules']:
    r['confidence'] = '추정(여러 맥락을 견주어 찾은 규칙 — 확정 사양 아님)'
json.dump(ctx, open(OUT + 'video-v2-context-components.json', 'w'), ensure_ascii=False, indent=1)
for b in typ['bundles']:
    b['confidence'] = '데이터로 셈'
    b['scope'] = 'SVMS 고객 전용' if b['key'] == 'sheet_svms' else '공통 뼈대'
json.dump(typ, open(OUT + 'video-v2-screen-type-components.json', 'w'), ensure_ascii=False, indent=1)

# ---------- 5. 그림 목록 ----------
CTX_BY_ID = {}
for c_ in ctx['contexts']:
    for i in c_['screen_ids']:
        CTX_BY_ID[i] = c_['name']
imgs = []
for dr in ['images/screen-types', 'images/contexts']:
    for f in sorted(os.listdir(OUT + dr)):
        oid = '11:' + f.split('-')[1].split('.')[0]
        s = SCR[oid]
        imgs.append({'file': f'{dr}/{f}', 'screen': oid, 'copy_node': s['copy_node'], 'caption': s['caption'], 'view': s['view'],
                     'shape': s['shape'], 'platform': s['platform'], 'state_type': s['state_type'], 'context': CTX_BY_ID.get(oid),
                     'used_as': '유형 대표 화면' if dr.endswith('screen-types') else '맥락 흐름 그림'})
json.dump({'meta': {'made_at': TODAY, 'source': 'Figma 사본(SW-UX-GUIDE-V3.0-TEST · cysG5U1udpQqVagYY1hWHW · 페이지 80:16699)에서 찍음. 사본 번호 = 원본 번호 + 2461', 'count': len(imgs)},
           'images': imgs}, open(OUT + 'images/INDEX.json', 'w'), ensure_ascii=False, indent=1)

# ---------- 6. 미정 시안 · 다르게 만든 곳 ----------
ALTS = [
    ('화면 나누기', '그림 카드 3개 + 확인 / 슬라이더 + 적용', '11:27272 · 11:27386 (세로) · 11:20105 · 11:20435 (가로)'),
    ('날짜·시간 고르기', '날짜/시간 탭 + 달력 + 시·분 휠 / 휠 하나(날짜·시·분) + 적용', '11:16064 · 11:16773 (세로) · 11:21551 · 11:17726 (가로)'),
    ('이벤트 종류 거르기 자리', '시안 01: 탭 아래 줄 / 시안 02: 탭 줄 오른쪽', '11:14838 · 11:14908'),
    ('시간바', '현재 위치선 버전 / 양 끝 흐림 버전 (Figma 부품 두 개, 최종 미정)', 'Frame 2116933726 · Frame 2087327574'),
    ('녹화 가로 확대 날짜시간 자리', '시안 A: 시간바 위 / 시안 B: 아래 버튼 줄 가운데 (캔버스에 떠 있는 시안)', '11:32308 · 11:32325'),
]
md = [f'# 모두앱 영상(NVR) — 정해지지 않은 것\n\n{TODAY} 정리. 다른 세션은 아래 항목을 **확정 사양으로 쓰지 않는다.** 근거 번호는 원본 Figma 화면 번호다(그림은 `images/INDEX.json`에서 찾는다).\n',
      '## 1. 시안이 두 가지인 것\n', '| 기능 | 두 안 | 근거 |', '|---|---|---|']
md += [f'| {a} | {b} | {c} |' for a, b, c in ALTS]
md += ['\n## 2. 같은 일인데 다르게 만든 곳\n', '| 맥락 | 무엇이 다른가 | 근거 | 확신 |', '|---|---|---|---|']
nd = 0
for c_ in ctx['contexts']:
    for d in c_['differences']:
        md.append(f"| {c_['name']} | {d['what']} | {d['evidence']} | {d['confidence']} |"); nd += 1
md += ['\n## 3. 부품 이름이 확인 안 된 것\n'] + [f"- {x['what']}" for x in comp['meta']['needs_review_added']]
md += [f"\n## 4. 지난 분석의 확인 필요 항목\n\n화면 분석 파일의 `needs_review`에 {len(ana['needs_review'])}건, `mismatches`(Figma 이름과 실제 화면이 다른 곳)에 {len(ana['mismatches'])}건이 있다. 화면 이름은 Figma 프레임명이 아니라 `label_actual`·`caption`을 쓴다.\n"]
open(OUT + 'video-v2-open-decisions.md', 'w').write('\n'.join(md))

# ---------- 사람용 MD: 사양표 · 용어 사전 ----------
sm = [f'# 모두앱 영상(NVR) — 부품별 작은 사양표\n\n{TODAY} 정리. 기계용은 `video-v2-spec-sheet.json`(Figma에서 잰 크기·자리 포함). 색·글자 크기·모서리는 재지 않았다.\n']
for s in sheet:
    sm.append(f"## {s['name']} `{s['key']}`\n")
    sm.append(f"- 쓰임 범위: **{s['reuse_scope']}**")
    sm.append(f"- 역할: {s['role']}")
    if s['variants']: sm.append(f"- 변형: {' · '.join(s['variants'])}")
    for x in s['spec']: sm.append(f'- 사양: {x}')
    if s['contexts']: sm.append(f"- 화면 절반 이상에 나오는 맥락: {' · '.join(s['contexts'])}")
    sm.append(f"- Figma 이름: {', '.join(s['figma_names']) or '없음(그림·글자 레이어)'}")
    sm.append(f"- 근거 화면: {s['evidence_screen']}\n")
open(OUT + 'video-v2-spec-sheet.md', 'w').write('\n'.join(sm))
gm = [f'# 모두앱 영상(NVR) — 용어 사전\n\n{TODAY} 정리. 기계용은 `video-v2-glossary.json`. 다른 세션은 아래 **쉬운 이름**으로 부른다.\n',
      '## 부품\n', '| 쉬운 이름 | 키 | 다른 이름(분석 글에서) | Figma 이름 | 화면 글자 |', '|---|---|---|---|---|']
gm += [f"| {g['name']} | `{g['key']}` | {' · '.join(g['also_called'][:4])} | {', '.join(g['figma_names'])} | {' · '.join(g['on_screen_text'])} |" for g in gl_parts]
gm += ['\n## 말\n', '| 말 | 뜻 | 다른 이름 |', '|---|---|---|'] + [f"| {t['term']} | {t['means']} | {' · '.join(t['also_called'])} |" for t in gl_terms]
gm += ['\n## 대표 상태 8가지\n'] + [f"- **{s['term']}** — {s['means']}" for s in gl_states]
gm += ['\n## 맥락 15가지\n'] + [f"- **{c_['name']}** — {c_['goal']}" for c_ in ctx['contexts']]
open(OUT + 'video-v2-glossary.md', 'w').write('\n'.join(gm))
print('components', len(KEYS), 'contexts', len(ctx['contexts']), 'bundles', len(typ['bundles']), 'images', len(imgs), 'diffs', nd)
