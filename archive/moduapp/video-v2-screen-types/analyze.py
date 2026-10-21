import json, re, collections, itertools, sys

BASE = '/Users/designgroup_02/s1-moduapp-workspace/outputs/moduapp/service-video/'
d = json.load(open(BASE + 'video-v2-screen-analysis.json'))
comp = json.load(open(BASE + 'video-v2-components.json'))
NAMES = {c['key']: c['name'] for c in comp['components']}
NAMES['os_nav'] = '기기 시스템 내비게이션 바'

# 눈으로 적은 부품 글 → 부품 키(여러 개 가능). 위에서부터 차례로 검사, 걸리는 것 모두 붙임.
RULES = [
    (r'헤더', ['app_header']),
    (r'전환 (칩|버튼)', ['mode_chip']),
    (r'탭바', ['tabbar']),
    (r'시스템 내비게이션', ['os_nav']),
    (r'토스트', ['toast']),
    (r'배율 표시', ['toast']),
    (r'바텀시트|가운데 팝업|가운데 시트|화면 구성 팝업|더보기 팝업|레이아웃 리스트 팝업|오른쪽 패널|측면 패널|^닫기|취소|확인 버튼|적용 버튼|메뉴 목록', ['bottom_sheet']),
    (r'화면 구성|분할 그림|슬라이더|배치 그림|격자 (그림|아이콘) 선택지', ['layout_picker']),
    (r'레이아웃 리스트|레이아웃 목록|이벤트 (목록|기록|칩|종류)|SVMS', ['svms_panel']),
    (r'PTZ 제어 속도|제어 속도|PTZ 모드 영역|방향 조종판|방향 조작|확대/축소 세로', ['ptz_pad']),
    (r'달력\b(?! 버튼)|달력\(|날짜 달력$|휠|날짜/시간 탭|월 이동|녹화 있는 날|오늘 표시|시간 선택 버튼|날짜 탭|시간 탭', ['datetime_picker']),
    (r'카메라 (목록|썸네일)|움직임 감지|감지 (시각|기록)|체크박스 목록|빈 화면 (그림|안내)', ['camera_list']),
    (r'타임라인|재생 시각 말풍선', ['timeline']),
    (r'재생 (컨트롤|조작)|30초 버튼|배속 표시', ['playback_panel']),
    (r'알약|날짜·시간 표시|날짜 달력 버튼|^날짜 버튼', ['time_pill']),
    (r'딤|덮개', ['dim_overlay']),
    (r'배지|모드 표시|화면 구성\(격자\) 버튼|화면 구성 버튼|비율 버튼|화면 비율|PTZ 버튼|레이아웃\(|더보기|레이아웃 리스트 버튼', ['mode_badge']),
    (r'페이지 점', ['page_dots']),
    (r'캡쳐 버튼|전체화면|축소|하단 (컨트롤 바|도구 버튼|메뉴)|카메라 목록\(메뉴\) 버튼', ['round_button']),
    (r'경고 띠|신호 ?없음|에스원|카메라 없음 칸|영상 없음', ['video_state']),
    (r'영상 칸|격자|자리표시|이름표|이름 꼬리표|숨[긴김] 칸|빈 칸|레터박스|선택 칸 파란', ['video_tile']),
]
# 앞 규칙이 내용 부품을 이미 잡은 경우에도 겹쳐 붙지 않게 할 예외
EXCLUDE = {
    'mode_badge': [r'기록 목록', r'^바텀시트', r'팝업', r'토스트', r'^더보기 버튼$', r'^더보기\(…\) 버튼$'],
    'layout_picker': [r'화면 구성\(격자\) 버튼', r'화면 구성 버튼', r'덮개', r'딤'],
    'camera_list': [r'SVMS', r'카메라 목록\(메뉴\) 버튼', r'하단 도구 버튼', r'이벤트 목록 탭'],
    'video_tile': [r'카메라 (목록|썸네일)', r'경고 띠', r'에스원', r'미리보기 격자\(회색 칸', r'격자 (그림|아이콘) 선택지', r'화면 구성\(격자\)', r'격자·', r'신호 없음 영상 칸'],
    'svms_panel': [],
    'dim_overlay': [r'화면 뒤 8채널 격자'],
    'datetime_picker': [r'날짜 달력 버튼', r'카메라 목록'],
    'time_pill': [r'배율'],
    'round_button': [r'세로 (막대|바)'],
}
# 선택 표시·체크는 화면에 있는 목록에 붙임
GENERIC_SELECT = r'^선택(된|됨)? ?(체크|표시|목록)|선택 체크|선택된 기록|선택 결과 표시 줄'


def map_component(text):
    keys = []
    for pat, ks in RULES:
        if re.search(pat, text):
            for k in ks:
                if any(re.search(x, text) for x in EXCLUDE.get(k, [])):
                    continue
                if k not in keys:
                    keys.append(k)
    # 더보기 단독 버튼은 상단 툴바 아이콘
    if re.match(r'^더보기', text) and not keys:
        keys.append('mode_badge')
    if re.search(r'^더보기( 버튼|\(…\) 버튼|\(⋯\)( 버튼)?)$', text):
        keys = ['mode_badge']
    if re.search(r'미리보기 격자|화면 뒤 8채널 격자', text):
        keys = ['video_tile']
    return keys


SHAPE_LABEL = {
    ('세로', '단일채널'): '세로 기본 · 단일채널',
    ('세로', '다채널'): '세로 기본 · 다채널',
    ('가로', '단일채널'): '가로 확대 · 단일채널',
    ('가로', '다채널'): '가로 확대 · 다채널',
}
STATE_ORDER = ['기본', '버튼 뜬 상태(딤)', '바텀시트 열림', '가운데 팝업', '오른쪽 패널', '토스트', '영상 안 나옴', '빈 화면']


def classify_state(s, keys_texts):
    st = s['state']
    comps = ' / '.join(s['components'])
    flags = []
    if re.search(r'바텀시트', comps) or re.search(r'바텀시트', st):
        flags.append('바텀시트 열림')
    if re.search(r'가운데 팝업|가운데 시트|화면 구성 팝업|더보기 팝업|레이아웃 리스트 팝업', comps) or (re.search(r'팝업', st) and '바텀시트 열림' not in flags):
        flags.append('가운데 팝업')
    if re.search(r'오른쪽 패널|측면 패널', comps) or re.search(r'패널', st):
        flags.append('오른쪽 패널')
    if re.search(r'토스트', comps) or re.search(r'토스트', st):
        flags.append('토스트')
    if re.search(r'수신 불량|경고 띠|신호 ?없음|카메라 없음|에스원|영상 없음|칸별 상태|여러 상태', st + ' / ' + comps) or st in ('에러', '경고', '상태값'):
        flags.append('영상 안 나옴')
    if re.search(r'빈 화면 (그림|안내)', comps) or (re.search(r'빈 화면', st) and '영상 안 나옴' not in flags):
        flags.append('빈 화면')
    if re.search(r'딤|덮개|조작 버튼|컨트롤 표시|버튼 표시', st + ' / ' + comps):
        flags.append('버튼 뜬 상태(딤)')
    # 대표 상태 하나: 위에 덮는 것이 우선
    for p in ['바텀시트 열림', '가운데 팝업', '오른쪽 패널', '토스트', '빈 화면', '영상 안 나옴', '버튼 뜬 상태(딤)']:
        if p in flags:
            return p, flags
    return '기본', flags


screens = []
unmapped = collections.Counter()
for v in d['views']:
    for g in v['groups']:
        for s in g['screens']:
            keys = []
            generic = []
            for t in s['components']:
                ks = map_component(t)
                if re.search(GENERIC_SELECT, t):
                    generic.append(t)
                    continue
                if not ks:
                    unmapped[t] += 1
                for k in ks:
                    if k not in keys:
                        keys.append(k)
            for t in generic:
                for k in ['svms_panel', 'camera_list', 'layout_picker', 'ptz_pad', 'bottom_sheet']:
                    if k in keys:
                        break
                else:
                    unmapped[t] += 1
            orient = '세로' if s['orientation'] == 'portrait' else '가로'
            primary, flags = classify_state(s, keys)
            screens.append({
                'id': s['id'], 'view': v['view'], 'mode': v['mode'], 'channel': v['channel'],
                'view_orientation': v['orientation'], 'orientation': orient,
                'shape': SHAPE_LABEL[(orient, v['channel'])],
                'platform': s['platform'], 'feature': g['feature'], 'group_label': g['label_actual'],
                'caption': s['caption'], 'state_raw': s['state'], 'state_type': primary, 'state_flags': flags,
                'keys': keys, 'components_raw': s['components'], 'figma_link': s['figma_link'],
                'summary': s['summary'],
            })

if __name__ == '__main__':
    print('unmapped:', unmapped)
    print(collections.Counter(x['state_type'] for x in screens))
    print(collections.Counter(x['shape'] for x in screens))
    tot = collections.Counter(k for x in screens for k in x['keys'])
    for k, n in tot.most_common():
        print(n, k, NAMES[k])
    json.dump(screens, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1) if len(sys.argv) > 1 else None
