# 모두앱 현재 화면(영상 탭)에서 뽑은 부품 기준 세트
# 근거: Figma 사본 cysG5U1udpQqVagYY1hWHW · 페이지 80:16699 의 get_variable_defs / get_design_context (2026-10-21)
import json, html

ROOT = '/Users/designgroup_02/s1-moduapp-workspace/'
SRC = '2026-10-21 Figma 사본(SW-UX-GUIDE-V3.0-TEST · cysG5U1udpQqVagYY1hWHW · 80:16699)'

# ---------- 기초 값 ----------
# token: Figma에 묶여 있는 변수 이름(없으면 None = 값만 직접 들어감)
COLORS = [
    # key, 쓰임, 값, Figma 변수, 근거 노드
    ('accent', '강조 파랑 — 선택 칩·기본 버튼·탭 선택·활성 탭바 글자·선택 테두리', '#1D6CEB', 'color/button/bg/primary--default · color/text/state/accent · Primary/normal(옛 이름)', '2805:19343 · 2805:19302'),
    ('title', '제목 글자 — 시트 제목·목록 제목', '#000000', 'color/text/title/primary · Font/Title(옛 이름)', '2805:19302 · 2805:17082'),
    ('text-strong', '현장명 글자', '#202020', 'color/text/body/primary', '2805:19335'),
    ('text-body', '본문·보조 버튼 글자·진한 아이콘', '#353535', 'color/button/label/secondary--default · color/icon/gray-dark', '2805:18592'),
    ('text-sub', '보조 글자 — PTZ 이름·탭 기본 글자', '#555555', 'color/text/body/secondary · color/navigation/label/default', '2805:19667 · 2805:18597'),
    ('text-caption', '설명 글자 — 고르지 않은 분할 이름', '#757575', 'color/text/state/caption', '2805:29774'),
    ('text-inactive', '꺼진 글자 — 미선택 칩·탭바 글자·기록 일시', '#7F7F7F', 'Font/Tabmenu(옛 이름) · 대부분 값만 직접', '2805:19344 · 2805:19381 · 2805:17256'),
    ('text-helper', '시간바 눈금 글자 · 영상 없는 칸 바탕', '#9D9D9D', 'color/text/state/helper · gray/400', '2805:28943 · 2805:16746'),
    ('text-faint', '현장 아래 줄(지점·고객번호)', '#BFBFBF', None, '2805:19335'),
    ('disabled', '흐린 글자·밝은 아이콘·휠 위아래 값·움직임 감지 꺼진 탭', '#C4C4C4', 'color/icon/gray-light · color/chip/solid/label/disabled · gray/300', '2805:19302 · 2805:34335'),
    ('border', '보조 버튼·분할 카드 테두리·탭 기본 밑줄', '#D9D9D9', 'color/button/border/secondary--default', '2805:28943'),
    ('border-legacy', '체크박스 테두리', '#DCDCDC', 'box/Border_normal(옛 이름)', '2805:17522'),
    ('line', '구분선·목록 제목 윗줄·분할 카드 빈 칸·슬라이더 바탕', '#E9E9E9', 'color/table/border/default · color/control/bg/disabled · gray/100', '2805:19350 · 2805:29888'),
    ('fill-soft', '미선택 칩 바탕·PTZ 확대 막대 바탕', '#F2F2F2', 'box/BG_disabled(옛 이름) · 값만 직접', '2805:19344 · 2805:19667'),
    ('fill-disabled', '꺼진 버튼 바탕', '#F5F5F5', 'color/button/bg/disabled', '페이지 변수'),
    ('range', '달력 — 녹화 있는 날 바탕', '#E2F1FF', 'color/date-picker/cell/bg/range', '2805:18592'),
    ('live', '실시간 배지 빨간 점', '#E50533', 'red/400', '2805:19348'),
    ('warning-band', '수신 불량 띠(투명도 50%)', '#F22544', 'red/350', '2805:16650'),
    ('event-dot', '시간바 이벤트 점', '#FF954E', 'orange/250', '2805:28943'),
    ('white', '바탕·영상 위 글자·아이콘', '#FFFFFF', 'base/white · surface/neutral/bg/base · etc/White(옛 이름)', '-'),
    ('overlay', '영상 위 알약·원형 버튼·이름표 바탕, 시트 뒤 덮개', 'rgba(0,0,0,0.5)', 'color/overlay', '2805:19349 · 2805:17082'),
    ('dim-gradient', '딤 위·아래 그라데이션', 'rgba(0,0,0,0.8) → 0', None, '2805:19348'),
    ('toast', '토스트 바탕', 'rgba(34,34,34,0.9)', None, '2805:18181'),
]
TYPE = [
    # key, 쓰임, 크기/굵기/줄높이/자간, Figma 스타일
    ('display-24B', '달력 년·월(2025.01)', '24 · Bold · 1.3 · 0', 'title/24B'),
    ('sheet-title-20B', '시트·팝업 제목', '20 · Bold · 1.3 · 0 (옛 시트는 줄높이 1.0)', 'title/20B'),
    ('wheel-20M', '시·분 휠 값', '20 · Medium · 1.3', '값만 직접'),
    ('site-18B', '현장명', '18 · Bold · 1.3 · -0.36', '값만 직접'),
    ('picked-18B', '고른 날짜·시각 한 줄', '18 · Bold · 1.3 · -0.36', '값만 직접'),
    ('section-16B', '목록 제목(카메라 목록)·선택 탭', '16 · Bold · 1.3 · 0', 'title/16B'),
    ('label-16M', '버튼 글자·기본 탭·토스트', '16 · Medium · 1.3 · -0.32', 'component/button/label/16M · title/16M · body/16M'),
    ('list-16R', '목록 줄(더보기·PTZ 속도·이벤트 종류)', '16 · Regular · normal', '값만 직접'),
    ('chip-14M', '칩·시각 알약·모드 배지·분할 이름·PTZ 이름', '14 · Medium · 1.3 · -0.28', 'body/14M'),
    ('chip-14B', '고른 슬라이더 값', '14 · Bold · 1.3', 'title/14B'),
    ('meta-14R', '기록 일시', '14 · Regular · 1.3', '값만 직접'),
    ('tab-12M', '하단 탭바 글자', '12 · Medium · normal · -0.5', '값만 직접'),
    ('notice-12M', '수신 불량 띠 글자', '12 · Medium · 1.3 · 0', 'body/12M'),
    ('badge-12B', '이벤트 종류 칩(움직임)', '12 · Bold · 1.0', '값만 직접'),
    ('sub-12R', '현장 아래 줄', '12 · Regular · 1.3 · 0', 'body/12R'),
    ('cam-10M', '카메라 이름표', '10 · Medium · 1.4 · +0.2', 'body/10M'),
    ('tick-10R', '시간바 눈금', '10 · Regular · 1.4 · +0.2', 'body/10R'),
]
RADIUS = [
    ('2', '체크박스'), ('3', '카메라 이름표'), ('4', '버튼·썸네일·가로 분할 카드'), ('5.5', '세로 분할 카드'),
    ('8', '입력형 시트 위 모서리·슬라이더 막대'), ('10', '목록형(옛) 시트 위 모서리·이벤트 칩'),
    ('28', '시각 알약·모드 배지·토스트'), ('40', '영상 위·재생 원형 버튼·가로 시각 칩·PTZ 막대'), ('999', '실시간/녹화 칩(옛 칩은 100)'),
]
SPACING = [
    ('20', '화면 좌우 여백 · 시트 안 좌우 · 시트 위아래 · 시트 안 덩어리 간격', 'spacing/padding/inline/md · spacing/padding/block/md · spacing/section/sm'),
    ('24', '날짜/시간 탭 줄 좌우 · 옛 시트 제목 줄 위아래', 'spacing/padding/inline/lg'),
    ('16', '버튼 안 좌우 · 토스트 좌우', 'spacing/padding/inline/sm'),
    ('18', '옛 목록 줄 위아래(줄 높이 약 55)', '값만 직접'),
    ('12', '칩·알약 안 좌우 · 딤 위 아이콘 간격', '값만 직접'),
    ('8', '시각 줄·목록 제목 줄 위아래 · 원형 버튼 간격', '값만 직접'),
    ('4', '칩 사이 · 썸네일 안 여백', 'spacing/4'),
]
EFFECTS = [
    ('딤 위 아이콘 그림자', 'drop-shadow 0 0 2 rgba(0,0,0,0.5)', '2805:19348'),
    ('가로 재생 버튼 아이콘 그림자', 'drop-shadow 0 0 5 rgba(0,0,0,0.5)', '2805:23709'),
    ('가로 시각 칩 글자 그림자', 'text-shadow 0 0 4 rgba(0,0,0,0.5)', '2805:23714'),
    ('선택된 썸네일 덮개', '영상 위 rgba(0,0,0,0.5) + 가운데 재생 중 아이콘 24', '2805:19256'),
]
ICONS = [('24', '일반 UI 아이콘(닫기·체크·화살표·세로 재생 버튼)'), ('28', '딤 위 툴바·원형 버튼 아이콘'), ('30', '가로 재생 버튼 아이콘'),
         ('32', '하단 탭바'), ('36', '신호 없음 아이콘'), ('64', '빈 목록 그림'), ('156', 'PTZ 방향 패드')]

# ---------- 부품 ----------
# parts: (이름, 값 설명) / versions: 같은 부품의 두 모양
COMP = [
 {'key': 'button', 'name': '버튼', 'component': 'bottom_sheet', 'parts': [
    ('기본(채움)', '높이 48 · 모서리 4 · 바탕 강조 파랑 · 테두리 1 같은 색 · 글자 label-16M 흰색 · 좌우 16 · 최소 폭 80'),
    ('보조(테두리)', '높이 48 · 바탕 흰색 · 테두리 1 #D9D9D9 · 글자 #353535'),
    ('꺼짐', '바탕 #F5F5F5 · 테두리 #D9D9D9'),
    ('두 개일 때', '[취소(보조)] [확인·시간 선택(기본)] 반씩'),
  ], 'versions': [('새 버튼 mobile_button', '높이 48 · 글자 줄높이 1.3 · 변수로 묶임', '2805:19330'), ('옛 버튼 m_button', '높이 50 · 글자 줄높이 1.0 · 값만 직접', '2805:17556')], 'evidence': '2805:19302 · 2805:17522'},
 {'key': 'chip', 'name': '실시간/녹화영상 칩', 'component': 'mode_chip', 'parts': [
    ('선택', '높이 30 · 좌우 12 · 모서리 999 · 바탕·테두리 강조 파랑 · 글자 chip-14M 흰색'),
    ('미선택', '위아래 8 · 좌우 16 · 모서리 100 · 바탕 #F2F2F2 · 글자 14 Medium #7F7F7F 줄높이 1.0'),
    ('배치', '헤더 줄 오른쪽, 칩 사이 4'),
  ], 'versions': [('선택 칩 Chip', '새 칩 변수(color/chip/solid/...)', '2805:19343'), ('미선택 칩 m_chips', '옛 이름(box/BG_disabled · Font/Tabmenu)', '2805:19344')], 'evidence': '2805:19335'},
 {'key': 'header', 'name': '상단 현장 헤더', 'component': 'app_header', 'parts': [
    ('줄', '높이 56 · 좌우 20 · 위 StatusBar 27 + 여백 16'),
    ('현장명', 'site-18B #202020 + 아래 화살표(More 24, 90도 돌림)'),
    ('아래 줄', 'sub-12R #BFBFBF "지점ㆍ고객번호"'),
  ], 'versions': [], 'evidence': '2805:19335'},
 {'key': 'tabbar', 'name': '하단 탭바', 'component': 'tabbar', 'parts': [
    ('줄', '높이 60 · 흰 바탕 · 4칸 균등'), ('아이콘', '32 · 꺼짐 #C4C4C4 / 켜짐 강조 파랑'),
    ('글자', 'tab-12M · 꺼짐 #7F7F7F / 켜짐 강조 파랑'), ('아래', '안드로이드 내비게이션 바 48'),
  ], 'versions': [], 'evidence': '2805:19381'},
 {'key': 'time_row', 'name': '시각 줄 · 시각 알약', 'component': 'time_pill', 'parts': [
    ('줄', '높이 44 · 좌우 20 · 위아래 8 · 흰 바탕'),
    ('알약', '높이 28 · 좌우 12 · 위아래 4 · 모서리 28 · 바탕 overlay · 글자 chip-14M 흰색'),
    ('양옆 버튼', '28 원 · 흰 바탕 · 테두리 0.875 #C4C4C4 · 아이콘 24(캡쳐 / 녹화는 왼쪽 달력)'),
    ('가로 시각 칩', '모서리 40 · 좌우 12 · 위아래 5 · 글자 그림자'),
  ], 'versions': [], 'evidence': '2805:19349 · 2805:23714'},
 {'key': 'badge', 'name': '모드 배지(딤 위)', 'component': 'mode_badge', 'parts': [
    ('알약', '높이 28 · 좌우 12 · 위아래 5 · 모서리 28 · 바탕 overlay'),
    ('점', '6 · 실시간은 빨강 #E50533'), ('글자', 'chip-14M 흰색 "실시간"/"녹화영상", 점과 간격 4'),
    ('오른쪽 아이콘 줄', '아이콘 28 · 간격 12 · 그림자'),
  ], 'versions': [], 'evidence': '2805:19348'},
 {'key': 'dim', 'name': '딤(조작 버튼 덮개)', 'component': 'dim_overlay', 'parts': [
    ('위 띠', '높이 80 · 위 12 · 아래 32 · 좌우 20 · 그라데이션 0.8 → 0'),
    ('아래 띠', '위 28 · 아래 12 · 좌우 20 · 그라데이션 0 → 0.8 (가로는 높이 120)'),
    ('원형 버튼', '40 원 · 바탕 overlay · 아이콘 28 그림자 · 간격 8'),
    ('가로 아래 줄', '왼쪽 메뉴·움직임 감지·달력·캡쳐 / 가운데 시각 칩 / 오른쪽 축소'),
  ], 'versions': [], 'evidence': '2805:19348 · 2805:23713'},
 {'key': 'tile', 'name': '영상 칸 · 썸네일', 'component': 'video_tile', 'parts': [
    ('이름표', '왼쪽 위 · 바탕 overlay · 모서리 3 · 좌우 4 · 위아래 1 · 글자 cam-10M 흰색'),
    ('썸네일', '156×87 · 모서리 4 · 안 여백 4 · 2열 간격 8 · 줄 간격 8'),
    ('선택 썸네일', '테두리 2 강조 파랑 + 영상 위 overlay + 가운데 재생 중 아이콘 24'),
    ('영상 없는 칸', '바탕 #9D9D9D'),
  ], 'versions': [], 'evidence': '2805:19256 · 2805:16746'},
 {'key': 'video_state', 'name': '영상 상태 표시', 'component': 'video_state', 'parts': [
    ('수신 불량', '칸 아래 띠 높이 20 · #F22544 투명도 50% · 글자 notice-12M 흰색'),
    ('신호 없음', '회색 칸 + 아이콘 36 + "신호없음" 16 Medium 흰색 투명도 50%'),
    ('카메라 없음', '회색 칸 + 가운데 "에스원" 로고(56×21)'),
  ], 'versions': [], 'evidence': '2805:16650 · 2805:16746 · 2805:16667'},
 {'key': 'toast', 'name': '토스트', 'component': 'toast', 'parts': [
    ('모양', '모서리 28 · 좌우 16 · 위아래 4 · 바탕 rgba(34,34,34,0.9) · 글자 label-16M 흰색'),
    ('자리', '영상 아래 가운데'),
  ], 'versions': [], 'evidence': '2805:18181 · 2805:20244'},
 {'key': 'playback', 'name': '재생 컨트롤 · 시간바', 'component': 'playback_panel', 'parts': [
    ('세로 줄', '높이 56 · 버튼 간격 20 · 위아래 구분선 1 #E9E9E9'),
    ('세로 버튼', '40 원 · 흰 바탕 · 테두리 1 #D9D9D9 · 아이콘 24'),
    ('가로 버튼', '50 원 · 바탕 overlay · 아이콘 30 그림자'),
    ('시간바', '눈금 칸 70 · 눈금 글자 tick-10R #9D9D9D · 눈금 막대 #C4C4C4 · 지금 위치선 2×24 검정 모서리 2 · 이벤트 점 3 #FF954E · 양 끝 흰색 흐림 100'),
  ], 'versions': [], 'evidence': '2805:28943 · 2805:23709'},
 {'key': 'sheet', 'name': '바텀시트 · 가로 팝업', 'component': 'bottom_sheet', 'parts': [
    ('뒤 덮개', 'overlay(rgba 0,0,0,0.5)'),
    ('가로', '폭 480 · 화면 아래에 붙음(위 두 모서리만 둥금) · 가운데 정렬'),
    ('닫기', '오른쪽 위 X 24'),
  ], 'versions': [
    ('입력형 시트(새) mobile_*_bottomsheet', '위 모서리 8 · 위아래 20 · 덩어리 간격 20 · 제목 줄 높이 26 · 제목 줄높이 1.3 · 아래 버튼 48 — 날짜·시간, 화면 구성', '2805:19302 · 2805:29774'),
    ('목록형 시트(옛) ptn_m_bottom sheet', '위 모서리 10(이벤트 종류는 8) · 제목 줄 위아래 24 · 제목 줄높이 1.0 · 목록 줄 위아래 18 · 글자 list-16R 검정 · 고른 줄 강조 파랑 + 체크 24 · 아래 16 — 더보기, PTZ 속도, 레이아웃 리스트, 이벤트 종류', '2805:17082 · 2805:19883 · 2805:17522'),
  ], 'evidence': '2805:19302 · 2805:17082'},
 {'key': 'tabs', 'name': '탭(날짜/시간)', 'component': 'datetime_picker', 'parts': [
    ('줄', '좌우 24 · 두 칸 균등 · 칸 높이 30 + 밑줄 2'),
    ('선택', 'section-16B 강조 파랑 + 밑줄 2 강조 파랑'), ('기본', 'label-16M #555555 + 밑줄 1 #D9D9D9'),
  ], 'versions': [], 'evidence': '2805:18597'},
 {'key': 'calendar', 'name': '달력 · 시간 휠', 'component': 'datetime_picker', 'parts': [
    ('년·월', 'display-24B + 좌우 화살표 20'), ('날짜 칸', '44 · 동그라미(999)'),
    ('상태', '고른 날 강조 파랑 채움·흰 글자 / 오늘 파랑 테두리·파랑 글자 / 녹화 있는 날 #E2F1FF / 지난 달·다음 달 #C4C4C4'),
    ('휠', 'wheel-20M · 고른 줄 강조 파랑 · 위아래 #C4C4C4 · 고른 줄 위아래 구분선 · 위아래 흰색 흐림'),
  ], 'versions': [], 'evidence': '2805:18592 · 2805:19302'},
 {'key': 'layout_picker', 'name': '분할 고르기', 'component': 'layout_picker', 'parts': [
    ('그림 카드(세로)', '약 52×71 · 테두리 1.8 · 모서리 5.5 · 카드 간격 40 · 이름 chip-14M'),
    ('그림 카드(가로)', '52×40 · 테두리 1.33 · 모서리 4'),
    ('상태', '고른 카드 테두리·칸 강조 파랑, 이름 파랑 / 나머지 테두리 #D9D9D9·칸 #E9E9E9, 이름 #757575'),
    ('슬라이더', '막대 높이 6 · 모서리 8 · 바탕 #E9E9E9 · 채움 강조 파랑 · 손잡이 20 흰색 테두리 #C4C4C4 · 값 이름 chip-14B 파랑 / 14M #757575'),
  ], 'versions': [], 'evidence': '2805:29774 · 2805:29888 · 2805:22577'},
 {'key': 'list_header', 'name': '목록 제목줄', 'component': 'camera_list', 'parts': [
    ('세로', '좌우 20 · 위아래 8 · 위 테두리 1 #E9E9E9 · 글자 section-16B 검정'),
    ('탭형(가로 패널)', '"카메라 목록" 16B 검정 + "움직임 감지" 16M #C4C4C4 · 간격 12 · 오른쪽 X 24'),
  ], 'versions': [], 'evidence': '2805:19350 · 2805:34335'},
 {'key': 'event_row', 'name': '감지·이벤트 기록 줄', 'component': 'camera_list', 'parts': [
    ('종류 칩', '바탕 #1D6CEB · 모서리 10 · 좌우 7 · 위아래 4 · 글자 badge-12B 흰색'),
    ('일시', 'meta-14R #7F7F7F · 칩과 간격 3'), ('고른 줄', '오른쪽 체크 24'),
  ], 'versions': [], 'evidence': '2805:17256'},
 {'key': 'checkbox', 'name': '체크박스', 'component': 'svms_panel', 'parts': [
    ('모양', '18 · 모서리 2 · 테두리 1 #DCDCDC · 흰 바탕 / 체크 켜짐은 파랑 그림'), ('줄', '높이 55 · 좌우 20 · 글자와 간격 8 · list-16R'),
  ], 'versions': [], 'evidence': '2805:17522'},
 {'key': 'ptz', 'name': 'PTZ 조종판', 'component': 'ptz_pad', 'parts': [
    ('방향 패드', '156 원 그림 · 아래 이름 chip-14M #555555'), ('확대/축소 막대', '52×156 · 모서리 40 · 바탕 #F2F2F2 · +/− 24'),
    ('배치', '두 덩어리 간격 70 · 흰 바탕'),
  ], 'versions': [], 'evidence': '2805:19667'},
]

MIXED = [
    ('버튼 높이', '새 버튼 48 / 옛 버튼 50', '이벤트 종류 시트만 옛 버튼'),
    ('시트 모양', '입력형 시트 모서리 8·제목 줄 26 / 목록형 시트 모서리 10·제목 줄 위아래 24', '같은 화면 안에서 시트를 열 때마다 모양이 다름'),
    ('실시간/녹화 칩', '선택 칩은 새 칩(높이 30, 999) / 미선택 칩은 옛 칩(위아래 8, 100)', '한 쌍의 칩이 서로 다른 부품'),
    ('변수 이름 두 벌', '새 이름(color/button/... · spacing/...) / 옛 이름(Primary/normal · Font/Title · box/... · etc/White)', '값은 같은 것이 많음(#1D6CEB 등)'),
    ('같은 이름 다른 값', "'color/text/body/primary' = #202020(헤더) / #353535(달력·패널), 'color/text/body/secondary' = #353535 / #555555(PTZ)", '같은 변수 이름이 두 값을 가짐 — 변수 모음이 둘일 가능성'),
    ('직접 넣은 값', '현장명 18B, 현장 아래 줄 #BFBFBF, 탭바 글자 #7F7F7F, 토스트 바탕, 딤 그라데이션', '변수로 묶이지 않음'),
]

data = {
    'meta': {'title': '모두앱 부품 기준 세트(현재 화면 추출본)', 'made_at': '2026-10-21', 'source': SRC,
             'scope': '모두앱 영상 탭 화면에서 쓰인 값. 다른 탭(홈 등)은 아직 보지 않음',
             'rule': '모두앱 새 화면은 이 기준을 따른다. 최신 디자인 기준(S-1 디자인가이드·SW-UX-GUIDE-V3.0)을 적용하지 않는다 (river 2026-10-21)',
             'method': '부품별 대표 노드 약 40곳에서 Figma 변수(get_variable_defs)와 실제 스타일(get_design_context)을 읽음. 값은 그 노드의 값 그대로',
             'caution': '추출한 파일은 새 가이드 시험용 사본이다. 구조·크기는 원본과 같음을 확인했지만, 색이 원본과 같은지는 원본 파일로 대조하지 않았다'},
    'foundation': {
        'font': 'Pretendard (Regular 400 · Medium 500 · Bold 700)',
        'colors': [dict(key=k, use=u, value=v, figma_variable=t, evidence=e) for k, u, v, t, e in COLORS],
        'type': [dict(key=k, use=u, spec=s, figma_style=f) for k, u, s, f in TYPE],
        'radius': [dict(value=v, use=u) for v, u in RADIUS],
        'spacing': [dict(value=v, use=u, figma_variable=t) for v, u, t in SPACING],
        'effects': [dict(name=n, spec=s, evidence=e) for n, s, e in EFFECTS],
        'icon_sizes': [dict(size=s, use=u) for s, u in ICONS],
    },
    'components': [dict(key=c['key'], name=c['name'], maps_to=c['component'], parts=[dict(part=p, spec=s) for p, s in c['parts']],
                        versions=[dict(name=n, spec=s, evidence=e) for n, s, e in c['versions']], evidence=c['evidence']) for c in COMP],
    'mixed_versions': [dict(what=a, detail=b, note=c) for a, b, c in MIXED],
}
json.dump(data, open(ROOT + 'registry/services/moduapp/component-baseline.json', 'w'), ensure_ascii=False, indent=1)

# ---------- 사람용 MD ----------
md = [f"# 모두앱 부품 기준 세트 — 현재 화면 추출본\n\n{data['meta']['made_at']} · 범위: {data['meta']['scope']}\n",
      f"- **{data['meta']['rule']}**", f"- 근거: {SRC}", f"- 주의: {data['meta']['caution']}", '- 기계용: `registry/services/moduapp/component-baseline.json` · 눈으로 보기: `outputs/moduapp/design-baseline/component-baseline.html`\n',
      f"## 1. 기초 값\n\n글꼴: {data['foundation']['font']}\n", '### 색\n', '| 이름 | 값 | 쓰임 | Figma 변수 |', '|---|---|---|---|']
md += [f"| {k} | `{v}` | {u} | {t or '값만 직접'} |" for k, u, v, t, e in COLORS]
md += ['\n### 글자\n', '| 이름 | 크기 · 굵기 · 줄높이 · 자간 | 쓰임 | Figma 스타일 |', '|---|---|---|---|'] + [f'| {k} | {s} | {u} | {f} |' for k, u, s, f in TYPE]
md += ['\n### 모서리\n'] + [f'- **{v}** — {u}' for v, u in RADIUS]
md += ['\n### 간격\n'] + [f'- **{v}** — {u}' for v, u, t in SPACING]
md += ['\n### 그림자·덮개\n'] + [f'- {n}: {s}' for n, s, e in EFFECTS]
md += ['\n### 아이콘 크기\n'] + [f'- **{s}** — {u}' for s, u in ICONS]
md += ['\n## 2. 부품\n']
for c in COMP:
    md.append(f"### {c['name']} `{c['key']}`\n")
    md += [f'- **{p}**: {s}' for p, s in c['parts']]
    if c['versions']:
        md.append('- 같은 부품 두 모양:')
        md += [f'  - {n} — {s} ({e})' for n, s, e in c['versions']]
    md.append(f"- 근거 노드: {c['evidence']}\n")
md += ['## 3. 한 화면 안에 섞여 있는 두 버전\n', '| 무엇 | 차이 | 메모 |', '|---|---|---|'] + [f'| {a} | {b} | {c} |' for a, b, c in MIXED]
open(ROOT + 'outputs/moduapp/design-baseline/component-baseline.md', 'w').write('\n'.join(md) + '\n')
print('ok', len(COLORS), len(TYPE), len(COMP))
