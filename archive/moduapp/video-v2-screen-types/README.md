# 영상 화면 유형별 부품 — 다시 돌리는 법 (2026-10-21)

1. Figma 앱에서 사본 파일(SW-UX-GUIDE-V3.0-TEST, 페이지 `80:16699`)을 열고 그 페이지 메타데이터를 받아 `meta.xml`로 저장한다(약 2MB, 저장소에 넣지 않음).
2. `python3 parse_copy.py` → `copy_frames.json`(화면별 Figma 부품 이름)
3. `python3 build.py` → `outputs/moduapp/service-video/video-v2-screen-type-components.json/html`

- 사본 노드 번호 = 원본 번호 + 2461 (270화면 모두 확인).
- 대표 화면 그림은 `outputs/moduapp/service-video/images/screen-types/`에 있다(사본에서 찍은 스크린샷).
