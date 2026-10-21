# 모두앱 부품 기준 세트 — 다시 만드는 법 (2026-10-21)

- 값은 Figma 사본(SW-UX-GUIDE-V3.0-TEST, 페이지 `80:16699`)에서 부품별 대표 노드 약 40곳을 골라 Figma 변수와 실제 스타일을 읽어 `baseline.py`에 직접 적었다(노드 번호는 각 항목의 근거 칸).
- `python3 baseline.py` → `registry/services/moduapp/component-baseline.json` + `outputs/moduapp/design-baseline/component-baseline.md`
- `python3 baseline_html.py` → `outputs/moduapp/design-baseline/component-baseline.html`
