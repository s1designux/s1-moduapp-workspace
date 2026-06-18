# S1 모두앱 Workspace — Status

_마지막 업데이트: 2026-05-26_

> **주의:** Cross-service registry의 단일 source of truth는 `../s1-service-intelligence/registry/cross-service/`입니다.
> 이 파일은 모두앱 워크스페이스 내 요약 참조 파일입니다.

---

## 서비스 현황

| Service | Status | 현재 단계 | 에이전트 팀 |
|---|---|---|---|
| moduapp | active | S0 완료 — Phase 0(서비스맵) 대기 | moduapp (다중 서비스 허브) |

---

## 에이전트 레이어별 현황

### Leadership
| Agent | Status | 비고 |
|---|---|---|
| s1-service-intelligence-lead | standby | 서비스 2개 이상 metadata 축적 후 활성화 |

### Orchestration
| Agent | Status | 비고 |
|---|---|---|
| main-orchestrator | active | 모든 작업의 기본 진입점 |

### Shared Capabilities
| Agent | Status | 비고 |
|---|---|---|
| ui-reader | active | |
| ux-checker | active | |
| ds-mapper | standby | 화면 분석 후 매핑 단계에서 활성화 |
| research-synthesizer | standby | |

### Service Team (moduapp) — Top-down 진행
| Agent | Status | 비고 |
|---|---|---|
| moduapp-ia-mapper | active | Phase 0 — 서비스맵·IA 먼저 파악 (자료 입수 대기) |
| moduapp-reader | standby | 서비스맵 확정 후 서비스별 화면 분석 |
| moduapp-permission-mapper | standby | 권한 매트릭스 정리 (서비스 분석과 병행) |
| moduapp-screen-maker | standby | 매핑 축적 후 |

---

## 현재 상태 (moduapp)

- **서비스:** 모두앱 (출입관리·영상관리·사용자 권한관리 등 다중 서비스 통합 허브 앱)
- **수집 모델:** 다층(앱 셸 / 서비스별 / 횡단) + Top-down — 사용자 승인됨 (2026-05-26)
- **완료 단계:** S0(워크스페이스 세팅, 다층 구조 반영, 담당자 5종 정의, 기준표 스켈레톤)
- **다음 단계:** Phase 0(서비스맵/IA) — Figma Dev Mode MCP 연결 후 사양서 확인 대기
- **DS 매핑 / 신규 화면 제안:** 미시작

---

## 다음 활성화 트리거

| 조건 | 다음 변화 |
|---|---|
| Figma 연결 또는 사양서 입수 | moduapp-ia-mapper 서비스맵 파악 시작 (Phase 0) |
| 서비스맵 확정 | moduapp-reader / moduapp-permission-mapper standby → active |
| 화면 분석 + 매핑 축적 | ds-mapper / moduapp-screen-maker 활성화 검토 |
