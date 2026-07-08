# Daily AI Dispatch - 2026-09-08

## Scope

- stage: ProductionCandidate
- roster_source: `drills/每日任務卡排程.md` W10D1
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0041`
- today_goal: 建立 rollback / restore 演練門檻、restore point 與 dry-run checklist。
- out_of_scope:
  - 不宣告正式上線。
  - 不下線 Qutora。
- forbidden_actions:
  - rollback 未驗證不得進 Go / No-Go。
  - AI 不得決定 RTO / RPO 接受。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0041`：決定 RTO / RPO 演練門檻。 | [HUMAN] | rollback acceptance。 | `evidence/ProductionCandidate/TASK-RPT-0041/rollback-acceptance.md` | QA / Security / DevOps |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0041`：建立 restore point 與 rollback plan。 | [AI->HUMAN] | restore point record。 | `evidence/ProductionCandidate/TASK-RPT-0041/restore-point-record.md` | Tech Lead / Captain |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0041`：依 RB-04 準備 rollback dry run。 | [AI->HUMAN] | dry-run checklist。 | `evidence/ProductionCandidate/TASK-RPT-0041/dry-run-checklist.md` | Backend / DBA |

## Human Gate Watchlist

- ADR needed: RTO / RPO 例外接受需 ADR / human sign-off。
- Security / audit risk: restore evidence 不得含敏感資料。
- Formal data boundary: 不使用正式資料。
- Go / No-Go or rollback concern: rollback 不可用即 No-Go。

## Required Reading

- `docs/keep.summary.md`
- `runbooks/RB-04-rollback-rehearsal.md`
- `tasks/TASK-RPT-0041-m9-03-rollback-runbook.task.md`

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

- ProductionCandidate 階段所有 Gate 均需 human review。

