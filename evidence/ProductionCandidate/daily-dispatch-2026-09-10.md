# Daily AI Dispatch - 2026-09-10

## Scope

- stage: ProductionCandidate
- roster_source: `drills/每日任務卡排程.md` W10D3
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0041`
- today_goal: 審查 rollback 是否足以阻擋上線，演練停用新路徑並回 Qutora dry run。
- out_of_scope:
  - 不執行正式切換。
  - 不修改 Qutora 原始碼。
- forbidden_actions:
  - rollback path 不可用時不得 conditional-go。
  - AI 不得決定接受 rollback 例外。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0041`：判斷 rollback 是否足以阻擋上線。 | [HUMAN] | blocking criteria。 | `evidence/ProductionCandidate/TASK-RPT-0041/blocking-criteria.md` | QA / Security / DevOps |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0041`：修正 restore / rollback 缺口。 | [AI->HUMAN] | rerun command。 | `evidence/ProductionCandidate/TASK-RPT-0041/rollback-rerun-command.md` | Tech Lead / Captain |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0041`：執行停用新路徑、回 Qutora dry run。 | [AI->HUMAN] | rollback result。 | `evidence/ProductionCandidate/TASK-RPT-0041/rollback-dry-run-result.md` | Backend / DBA |

## Human Gate Watchlist

- ADR needed: rollback exception、RTO/RPO 降級需 ADR。
- Security / audit risk: rollback 操作需 audit。
- Formal data boundary: 不碰正式流量。
- Go / No-Go or rollback concern: rollback 不可重跑即 blocking。

## Required Reading

- `runbooks/RB-04-rollback-rehearsal.md`
- `tasks/TASK-RPT-0041-m9-03-rollback-runbook.task.md`
- `tasks/TASK-RPT-0040-m9-02-go-no-go-gate.task.md`

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

- 今日所有結果會進 W10D5 rollback readiness review。

