# outputs/moduapp — 다층 메타데이터 저장 구조

모두앱은 다중 서비스를 묶는 허브 앱이므로, 결과를 평면이 아닌 **레이어별**로 저장합니다.

실제 서비스맵(Figma 보드 node 19338:3437)에서 확인한 섹션 기준입니다.

| 폴더 | 레이어 | 담는 내용 |
|---|---|---|
| `service-map/` | Phase 0 | 서비스맵 / 전체 IA / 앱 구조 (board-overview.png 포함) |
| `app-shell/` | Layer 0 (공통) | 홈 · 통합계정(로그인/계정) · 공통 · 설정 |
| `service-guard/` | Layer 1 | 시스템경비 |
| `service-video/` | Layer 1 | 영상 |
| `service-card/` | Layer 1 | 카드(출입카드 추정) |
| `service-mys1/` | Layer 1 | 마이에스원(계약/청구/입금) |
| `service-cs/` | Layer 1 | 고객센터 |
| `cross-service/` | Layer 2 (횡단) | 역할·권한 매트릭스, 서비스 간 연계 흐름 |

> 서비스가 더 있으면 `service-{이름}/` 폴더를 추가합니다.

## 파일 이름 규칙

각 폴더 안에서는 단계를 파일명 접미사로 구분합니다.
- 화면 분석: `{화면}-screen-analysis.json`
- DS 매핑: `{화면}-component-mapping.json`
- UX 검수: `{화면}-ux-validation.md`
- 화면 초안: `{화면}-screen-composition.json`
