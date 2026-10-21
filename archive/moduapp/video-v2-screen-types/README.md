# 영상 화면 유형별 부품 — 다시 돌리는 법 (2026-10-21)

1. Figma 앱에서 사본 파일(SW-UX-GUIDE-V3.0-TEST, 페이지 `80:16699`)을 열고 그 페이지 메타데이터를 받아 `meta.xml`로 저장한다(약 2MB, 저장소에 넣지 않음).
2. `python3 parse_copy.py` → `copy_frames.json`(화면별 Figma 부품 이름)
3. `python3 build.py` → `outputs/moduapp/service-video/video-v2-screen-type-components.json/html`

- 사본 노드 번호 = 원본 번호 + 2461 (270화면 모두 확인).
- 대표 화면 그림은 `outputs/moduapp/service-video/images/screen-types/`에 있다(사본에서 찍은 스크린샷).

## 맥락별 부품 조합 (2026-10-21)
4. `python3 context_build.py` → `outputs/moduapp/service-video/video-v2-context-components.json/html`
- 맥락 나누기·자리·다른 곳 글은 `context_spec.py`에 직접 적어 둠(스크린샷 대조 근거). 흐름 그림은 `images/contexts/`(없으면 `images/screen-types/`)에서 찾는다.

## 넘겨주기 꾸러미 (2026-10-21)
5. `python3 inst_geo.py` · `python3 node_geo.py` → Figma 사본에서 부품·영상 칸 크기와 자리를 잰다(`meta.xml` 필요).
6. `python3 handoff.py` → 용어 사전 · 작은 사양표 · 미정 목록 · 그림 목록을 만들고, 기존 결과에 `scope`·`confidence` 꼬리표를 붙인다. **build.py · context_build.py를 다시 돌렸으면 handoff.py를 맨 마지막에 다시 돌린다**(꼬리표가 지워지므로).
