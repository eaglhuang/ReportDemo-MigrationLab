# Daily AI Dispatch - 2026-07-16

## Scope

- stage: MVP2
- roster_source: `drills/每日任務卡排程.md` W2D3
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0007`, `TASK-RPT-0010`
- today_goal: 補 batch retry / rollback 與 audit write fail-closed 基礎。
- out_of_scope:
  - 不進入下載閘道實作。
  - 不接受 audit fail-open。
- forbidden_actions:
  - audit writer unavailable 時不得標示通過。
  - AI 不得降級 audit finding。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer | hands_on_tc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0010`：定義 audit 必寫事件與 fail-closed 邊界。 | [AI->HUMAN] | audit event checklist。 | `evidence/MVP2/TASK-RPT-0010/audit-event-checklist.md` | QA / Security / DevOps | pending |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0007`：補 batch retry / rollback / error code。 | [AI->HUMAN] | batch state machine。 | `evidence/MVP2/TASK-RPT-0007/batch-state-machine.md` | Tech Lead / Captain | pending |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0010`：驗證 audit 寫入失敗不得靜默通過。 | [AI->HUMAN] | fail-closed evidence。 | `evidence/MVP2/TASK-RPT-0010/audit-fail-closed-evidence.md` | Backend / DBA | pending |

## Human Gate Watchlist

- ADR needed: audit 保存落點或 fail-closed 原則變更需 ADR。
- Security / audit risk: audit payload 不得含未遮罩敏感資料。
- Formal data boundary: 禁用正式資料。
- Go / No-Go or rollback concern: audit fail-open 是 P0。

## Required Reading

- `docs/keep.summary.md`
- `runbooks/RB-03-evidence-standard.md`
- `tasks/TASK-RPT-0007-m1-01-import-batch-management.task.md`
- `tasks/TASK-RPT-0010-m1-04-audit-write-foundation.task.md`

## End-of-day Gate

- passed:
  - pending
- blocked:
  - pending
- carry_over:
  - pending
- reviewer_conflict:
  - pending
- hands_on_tc_complete:
  - pending
- velocity:
  - ai_outputs: pending
  - human_closures: pending
  - diff_decisions: pending

## Captain Notes

- 今日若有 P0/P1 finding，需入 `evidence/MVP2/risk-blocker-log.md`。

