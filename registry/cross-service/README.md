# Cross-Service Registry — 안내

Cross-service(여러 서비스 통합) 레지스트리의 단일 source of truth는 아래 위치입니다.

## 위치 (Single Source of Truth)

```
s1-service-intelligence/registry/cross-service/
```

## 주요 파일

| 파일 | 경로 |
|---|---|
| `service-agent-index.json` | `../../s1-service-intelligence/registry/cross-service/service-agent-index.json` |
| `service-context-map.json` | `../../s1-service-intelligence/registry/cross-service/service-context-map.json` |

## 원칙

- Cross-service 데이터는 단일 서비스가 아닌 **S1 전체 레벨**의 데이터입니다.
- `s1-service-intelligence`가 S1 통합 Admin의 single source of truth 역할을 담당합니다.
- 모두앱 전용 데이터(`registry/services/moduapp/`, `outputs/moduapp/`)는 이 워크스페이스에 유지됩니다.

## 모두앱 전용 데이터 (유지 위치)

- `registry/services/moduapp/` — 모두앱 서비스 전용 registry
- `outputs/moduapp/` — 모두앱 분석 결과물
