# Daily AI Dispatch - 2026-09-11

## Scope

- stage: ProductionCandidate
- roster_source: `drills/每日任務卡排程.md` W10D4
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0042`
- today_goal: 定義 UAT / operations manual 範圍，補 DB / storage / config 維運命令與 UAT checklist。
- out_of_scope:
  - 不進行正式 UAT 簽核。
  - 不承諾正式 SLA。
- forbidden_actions:
  - 操作手冊缺 rollback 步驟不得 closure。
  - UAT checklist 不得使用正式資料。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0042`：定義 UAT / ops manual 範圍。 | [AI->HUMAN] | manual outline。 | `evidence/ProductionCandidate/TASK-RPT-0042/manual-outline.md` | QA / Security / DevOps |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0042`：補 DB / storage / config 維運命令。 | [AI->HUMAN] | ops steps。 | `evidence/ProductionCandidate/TASK-RPT-0042/ops-steps.md` | Tech Lead / Captain |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0042`：補 UAT checklist 與 evidence standard。 | [AI->HUMAN] | UAT checklist。 | `evidence/ProductionCandidate/TASK-RPT-0042/uat-checklist.md` | Backend / DBA |

## Human Gate Watchlist

- ADR needed: 正式維運責任或 SLA 承諾需 ADR / human sign-off。
- Security / audit risk: 操作步驟不得包含未遮罩 secret。
- Formal data boundary: UAT 仍用演練資料。
- Go / No-Go or rollback concern: 操作手冊缺 rollback 為 blocking。

## Required Reading

- `tasks/TASK-RPT-0042-m9-04-uat-training-operations-manual.task.md`
- `runbooks/RB-03-evidence-standard.md`
- `runbooks/RB-04-rollback-rehearsal.md`

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

- 今日產出供 W10D5 rollback readiness review 使用。

