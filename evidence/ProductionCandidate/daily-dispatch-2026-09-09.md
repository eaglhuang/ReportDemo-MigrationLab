# Daily AI Dispatch - 2026-09-09

## Scope

- stage: ProductionCandidate
- roster_source: `drills/每日任務卡排程.md` W10D2
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0041`
- today_goal: 執行 MariaDB restore 到隔離環境，初測 RTO / RPO 與 PDF / config restore。
- out_of_scope:
  - 不覆蓋現有環境。
  - 不使用正式備份。
- forbidden_actions:
  - restore 未驗證不得標示 readiness。
  - 不得在非隔離環境做破壞性還原。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0041`：審查 backup / restore evidence。 | [AI->HUMAN] | review notes。 | `evidence/ProductionCandidate/TASK-RPT-0041/backup-restore-review-notes.md` | QA / Security / DevOps |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0041`：執行 MariaDB restore 到隔離環境。 | [AI->HUMAN] | restore evidence。 | `evidence/ProductionCandidate/TASK-RPT-0041/mariadb-restore-evidence.md` | Tech Lead / Captain |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0041`：驗證 PDF / config restore。 | [AI->HUMAN] | RTO / RPO 初測。 | `evidence/ProductionCandidate/TASK-RPT-0041/rto-rpo-initial-test.md` | Backend / DBA |

## Human Gate Watchlist

- ADR needed: RTO / RPO 未達標但要接受，需 ADR。
- Security / audit risk: restore log 需遮罩。
- Formal data boundary: 不使用正式備份。
- Go / No-Go or rollback concern: restore fail 是 blocking。

## Required Reading

- `runbooks/RB-04-rollback-rehearsal.md`
- `runbooks/RB-05-mariadb-environment.md`
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

- 所有 restore 命令需可重跑並保存輸出摘要。

