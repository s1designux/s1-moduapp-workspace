# 업무 흐름 개요 — S1 모두앱 UX Subagent Workflow

## 모두앱은 Top-down (구조 먼저)

모두앱은 다중 서비스를 묶는 허브 앱이라, 화면을 바로 보지 않고 **전체 구조를 먼저** 파악합니다.

```
Phase 0  서비스맵 / IA 파악         → moduapp-ia-mapper
Phase 1  앱 셸·공통(로그인·네비·홈)  → moduapp-reader (layer=app-shell)
Phase 2  서비스별(출입/영상/권한)    → moduapp-reader (layer=service, 병렬 가능)
Phase 3  횡단(역할·권한 매트릭스)    → moduapp-permission-mapper
Phase 4  UX 검수(서비스 내부+전환)   → ux-checker
   ↳ 이후: 신규 화면 구성 → 아카이브
```

각 화면 메타데이터에는 `layer` / `service` / `required_role`을 함께 기록합니다.

## 전체 흐름 (단계 처리)

```
입력 → 서비스맵 → 화면 분석 → 메타데이터 정리 → 디자인 시스템 매핑 → UX 검수
     → 신규 화면 구성 → 아카이브
```

---

## 입력 종류

| 입력 유형 | 경로 | 설명 |
|---|---|---|
| Figma 링크 | — (URL + node-id) | Figma MCP로 직접 메타데이터·스크린샷 조회 |
| Figma 익스포트 | `samples/moduapp/figma-export/` | Figma에서 내보낸 화면 파일 |
| 스크린샷 / 캡처 이미지 | `samples/moduapp/screenshots/` | 화면 캡처 이미지 (Figma 링크와 함께 사용 시 검수 기준) |
| 기획서 / 사양서 | `samples/moduapp/spec-docs/` | 서비스 기획서, UI 사양서 (PDF·문서) |
| HTML/CSS | — | 개발 환경에서 추출한 화면 |

---

## 단계별 처리

### 1단계 — 화면 분석 (A1)
- **담당자**: `moduapp-reader` 또는 `ui-reader`
- **입력**: Figma 링크 또는 샘플 화면 파일 (캡처 이미지 병행 사용 권장)
- **출력**: `screen-analysis.json`

#### Figma 링크 + 캡처 이미지 기반 화면 분석 워크플로우

Figma 링크가 제공된 경우 아래 4단계 순서로 분석합니다.
**프레임명 / 레이어명 / 섹션명은 참고 정보**이며, 최종 판단 기준이 아닙니다.

**Step 1. Figma 링크 분석** — `get_metadata(nodeId)`로 프레임 목록·컴포넌트·텍스트 수집. 프레임명은 참고 정보로만 기록.

**Step 2. 캡처 이미지 검수** — `get_screenshot(nodeId)`로 실제 시각 결과 확인. 화면 제목·탭바 활성 탭명·버튼 레이블로 실제 화면 명칭 식별.

**Step 3. 불일치 확인** — 프레임명과 실제 UI가 다른 경우 차이를 명시. 불확실한 항목은 `needs-review`.

**Step 4. 최종 화면 맥락 판단**

| 순위 | 기준 | 신뢰도 |
|---|---|---|
| 1 | 캡처 이미지에서 실제로 보이는 UI | 최상 |
| 2 | Figma 화면 안 텍스트·컴포넌트 (탭명, 화면 제목, 버튼 레이블) | 높음 |
| 3 | 사용자 플로우상 앞뒤 화면과의 관계 | 중간 |
| 4 | 프레임명 / 레이어명 / 섹션명 | 낮음 |

### 2단계 — 메타데이터 정리 (A1 포함)
- **담당자**: `moduapp-reader`
- **입력**: 분석 결과
- **출력**: `component-list.json`, `user-flow-notes.md`

### 3단계 — 디자인 시스템 매핑 (A2)
- **담당자**: `ds-mapper`
- **입력**: `screen-analysis.json` + `registry/shared/component-role-map.json`
- **출력**: `component-mapping.json`, `token-mapping.json`

### 4단계 — UX 검수 (A3)
- **담당자**: `ux-checker`
- **입력**: `screen-analysis.json`
- **출력**: `ux-validation-report.md`, `must-fix-list.md`

### 5단계 — 신규 화면 구성 (A5)
- **담당자**: `moduapp-screen-maker`
- **입력**: 요구사항 + 매핑 결과
- **출력**: `screen-composition.json`, `figma-ready-layout-schema.json`

### 6단계 — 아카이브 (A6)
- **담당자**: 없음 (수동 또는 Claude 보조)
- **입력**: 각 단계 산출물
- **출력**: `archive/moduapp/` 업데이트, 대시보드 반영

---

## 산출물 저장 위치 (레이어별)

결과는 단계 폴더가 아니라 **레이어 폴더**에 저장하고, 단계는 파일명 접미사로 구분합니다.

| 레이어 | 저장 위치 | 예시 파일 |
|---|---|---|
| 서비스맵/IA | `outputs/moduapp/service-map/` | `service-map.json` (= registry 반영) |
| 앱 셸·공통 | `outputs/moduapp/app-shell/` | `login-screen-analysis.json` |
| 출입관리 | `outputs/moduapp/service-access/` | `access-list-screen-analysis.json` |
| 영상관리 | `outputs/moduapp/service-video/` | `video-live-ux-validation.md` |
| 사용자 권한관리 | `outputs/moduapp/service-permission/` | `role-edit-screen-analysis.json` |
| 횡단(권한·연계) | `outputs/moduapp/cross-service/` | `permission-matrix.md`, `cross-flow.json` |
| 대시보드 업데이트 | `dashboard/index.html` | — |

자세한 규칙: `outputs/moduapp/README.md`

---

## 처음 시작하는 방법 (비개발자 가이드)

**Step 1.** 분석할 화면 자료를 `samples/moduapp/` 하위 폴더에 넣거나, Figma 링크를 채팅으로 전달합니다.

**Step 2.** Claude에게 다음처럼 요청합니다.
> "moduapp-reader를 사용해서 이 화면을 분석해줘."

**Step 3.** 분석 결과를 `outputs/moduapp/screen-analysis/`에 저장해달라고 합니다.
> "분석 결과를 outputs/moduapp/screen-analysis/screen-001.json으로 저장해줘."

**Step 4.** 디자인 시스템 매핑을 요청합니다.
> "ds-mapper를 사용해서 이 분석 결과를 디자인 시스템으로 매핑해줘."

**Step 5.** UX 검수를 요청합니다.
> "ux-checker를 사용해서 앱 UX 관점으로 이 화면을 검수해줘."

**Step 6.** 중요한 결과는 `archive/moduapp/`와 `dashboard/index.html`에 반영합니다.

---

## 순서 요약

```
samples/에 화면/자료 넣기 (또는 Figma 링크 전달)
    ↓
moduapp-reader → screen-analysis.json
    ↓
ds-mapper → component-mapping.json
    ↓
ux-checker → ux-validation-report.md
    ↓
moduapp-screen-maker → screen-composition.json
    ↓
archive/ 및 dashboard 업데이트
```
