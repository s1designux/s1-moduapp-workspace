# S1 모두앱 UX Subagent Workspace

## 목적

Claude Subagent 기반으로 모두앱 UX 분석 담당자 팀을 만들고, 단계별 산출물을 아카이브하는 워크스페이스입니다.

- 기존 모두앱 UI를 분석하고 메타데이터화합니다.
- 기존 모두앱 디자인 가이드 기준으로 컴포넌트와 토큰을 매핑합니다. (최신 디자인 기준은 모두앱에 적용하지 않음 — `docs/context/moduapp-design-guide-basis.md`)
- 분석 결과를 바탕으로 추가 분석과 신규 화면 UI 제안을 수행합니다.
- 각 단계의 산출물과 의사결정을 HTML 대시보드에 아카이브합니다.

> 이 워크스페이스는 `s1-mobility-uvis-workspace`와 동일한 방법론을 **모두앱(B2C/B2B 일반 사용자용 모바일 앱)**에 적용한 형제 프로젝트입니다.

---

## 현재 범위

**모두앱(moduapp)**만 진행합니다.

---

## 운영 원칙

| 폴더 | 역할 |
|---|---|
| `.claude/agents/shared/` | 모든 서비스에서 공통으로 쓰는 담당자 정의 |
| `.claude/agents/services/` | 서비스별 전용 담당자 정의 |
| `schemas/` | 결과물 형식(양식)을 맞추기 위한 초안 |
| `registry/` | 여러 담당자가 함께 참조하는 기준표 |
| `samples/` | 분석할 원본 화면/자료 파일 |
| `outputs/` | 실제 분석 결과 저장 |
| `archive/` | 단계별 의사결정 기록 |
| `dashboard/` | 현재 진행 상황 확인용 HTML |

---

## 담당자(Subagent) 목록

### 공통 담당자

| 이름 | 역할 |
|---|---|
| `ui-reader` | 기존 화면을 읽고 화면 구조와 구성요소를 정리해주는 담당자 |
| `ds-mapper` | 예전 UI를 우리 최신 디자인 시스템 기준으로 바꿔주는 담당자 |
| `ux-checker` | 사용자가 실제로 쓰기 좋은 화면인지 점검해주는 담당자 |

### 모두앱 전용 담당자

| 이름 | 역할 |
|---|---|
| `moduapp-reader` | 네비게이션, 화면 유형, 핵심 task 흐름을 중심으로 화면을 읽어주는 담당자 |
| `moduapp-screen-maker` | 새 모두앱 화면의 구조 초안을 만들어주는 담당자 |

---

## 비개발자용 사용 방법

1. 분석할 화면/자료를 `samples/moduapp/` 하위 폴더에 넣습니다.
   - Figma 익스포트 → `samples/moduapp/figma-export/`
   - 스크린샷 → `samples/moduapp/screenshots/`
   - 기획서/사양서 → `samples/moduapp/spec-docs/`
   - (또는 Figma 링크를 채팅으로 바로 전달해도 됩니다.)
2. Claude에게 적절한 담당자를 사용해 분석해달라고 요청합니다.
3. **처음에는 `moduapp-reader → ds-mapper → ux-checker` 순서**로 진행합니다.
4. 분석 결과는 `outputs/moduapp/` 폴더에 저장합니다.
5. 중요한 결정은 `archive/moduapp/`와 `dashboard/index.html`에 반영합니다.

---

## 현황 대시보드

`dashboard/index.html` 파일을 브라우저로 열면 현재 진행 상황을 한눈에 볼 수 있습니다.
