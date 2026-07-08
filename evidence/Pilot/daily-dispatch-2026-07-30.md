# Daily AI Dispatch - 2026-07-30

## Scope

- stage: Pilot
- roster_source: `drills/每日任務卡排程.md` W4D3
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0015`
- today_goal: 決定報表模板版本 MVP 邊界，補模板版本設計與 evidence skeleton。
- out_of_scope:
  - 不建立完整報表設計器。
  - 不導入正式模板維運流程。
- forbidden_actions:
  - 模板版本邊界未定不得 closure。
  - 不得用正式報表樣本。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0015`：決定報表模板版本 MVP 邊界。 | [HUMAN] | template scope。 | `evidence/Pilot/TASK-RPT-0015/template-scope.md` | QA / Security / DevOps |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0015`：補模板版本資料模型與狀態。 | [AI->HUMAN] | design-spec。 | `evidence/Pilot/TASK-RPT-0015/design-spec.md` | Tech Lead / Captain |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0015`：補模板版本 evidence skeleton。 | [AI->HUMAN] | test cases。 | `evidence/Pilot/TASK-RPT-0015/test-cases.md` | Backend / DBA |

## Human Gate Watchlist

- ADR needed: 模板保存政策若成正式承諾，需 ADR。
- Security / audit risk: 模板變更需可追溯。
- Formal data boundary: 不使用正式模板。
- Go / No-Go or rollback concern: 模板版本不可覆蓋舊版。

## Required Reading

- `docs/keep.summary.md`
- `tasks/TASK-RPT-0015-m3-01-report-template-versioning.task.md`
- `runbooks/RB-03-evidence-standard.md`

## End-of-day Gate

- passed:
  - pending
- blocked:
  - pending
- carry_over:
  - pending
- reviewer_conflict:
  - pending

## Captain Notes

- 本日只建立 Pilot 可驗證的模板版本邊界。

