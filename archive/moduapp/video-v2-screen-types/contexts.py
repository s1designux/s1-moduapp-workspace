import json, collections, re
import build  # noqa: 부품 합친 기록(keys)을 만든다
from analyze import NAMES

S = build.S
d = json.load(open(build.OUT + 'video-v2-screen-analysis.json'))
GROUP = {}
for v in d['views']:
    for g in v['groups']:
        for i, s in enumerate(g['screens']):
            GROUP[s['id']] = {'feature_key': g['feature_key'], 'group_id': g['group_id'], 'order': i, 'flow': g['flow'],
                              'purpose': g['purpose'], 'trigger': s['trigger'], 'summary': s['summary'], 'notes': s['notes'],
                              'components_raw': s['components'], 'label': g['label_actual']}
for x in S:
    x.update(GROUP[x['id']])

# 맥락 = 사용자가 하려는 일. 화면 묶음(feature_key)과 상태로 고른다
CONTEXTS = [
    ('watch', '영상 보기', lambda x: x['feature_key'] == 'state' and x['state_type'] == '기본'),
    ('controls', '조작 버튼 꺼내기', lambda x: x['feature_key'] == 'state' and x['state_type'] == '버튼 뜬 상태(딤)'),
    ('trouble', '영상이 안 나올 때', lambda x: x['feature_key'] == 'state' and x['state_type'] in ('영상 안 나옴', '빈 화면')),
    ('zoom', '크게 보기(핀치 확대)', lambda x: x['feature_key'] == 'zoom'),
    ('layout', '화면 나누기(분할 수)', lambda x: x['feature_key'] == 'layout'),
    ('ratio', '화면 비율 바꾸기', lambda x: x['feature_key'] == 'ratio'),
    ('page', '다음 카메라 묶음 넘기기', lambda x: x['feature_key'] == 'page'),
    ('camera', '다른 카메라 고르기', lambda x: x['feature_key'] in ('camlist',) or (x['feature_key'] == 'motion' and '카메라 목록' in x['caption'])),
    ('group', '카메라 묶음 고르기(SVMS)', lambda x: x['feature_key'] == 'svms' or (x['feature_key'] == 'svms_event' and re.search('레이아웃|카메라 목록 버튼|버튼 선택', x['caption']))),
    ('datetime', '지난 영상 날짜·시간 찾기', lambda x: x['feature_key'] == 'datetime'),
    ('playback', '재생·배속 조절', lambda x: x['feature_key'] == 'control'),
    ('event', '움직임·이벤트 찾아보기', lambda x: (x['feature_key'] == 'motion' and '카메라 목록' not in x['caption']) or (x['feature_key'] == 'svms_event' and not re.search('레이아웃|카메라 목록 버튼|버튼 선택', x['caption']))),
    ('capture', '화면 저장(캡쳐)', lambda x: x['feature_key'] == 'capture'),
    ('ptz', '카메라 방향 돌리기(PTZ)', lambda x: x['feature_key'] == 'ptz'),
    ('more', '기타 메뉴(더보기)', lambda x: x['feature_key'] == 'more'),
]

if __name__ == '__main__':
    assigned = collections.Counter()
    for key, name, f in CONTEXTS:
        sub = [x for x in S if f(x)]
        for x in sub:
            assigned[x['id']] += 1
        print('=====', name, len(sub), dict(collections.Counter(x['shape'] for x in sub)), dict(collections.Counter(x['platform'] for x in sub if x['platform'] != 'common')))
        c = collections.Counter(k for x in sub for k in x['keys'])
        print('  부품:', ', '.join(f'{NAMES[k]} {n}' for k, n in c.most_common()))
        print('  상태:', dict(collections.Counter(x['state_type'] for x in sub)))
        print('  누르기:', collections.Counter(x['trigger'] for x in sub).most_common(5))
        btn = collections.Counter(t for x in sub for t in x['components_raw'] if re.search('확인|적용|취소|닫기|시간 선택 버튼|토스트', t))
        print('  버튼·알림:', btn.most_common(8))
    print('맥락 없음', [x['id'] + ' ' + x['feature_key'] + ' ' + x['state_type'] + ' ' + x['caption'] for x in S if not assigned[x['id']]])
    print('두 맥락', [k for k, v in assigned.items() if v > 1])
