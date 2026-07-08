# Daily AI Dispatch - 2026-07-20

## Scope

- stage: MVP2
- roster_source: `drills/每日任務卡排程.md` W2D5
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0010`, `TASK-RPT-0019`
- today_goal: W2 Gate 檢查 DB / audit / scope 是否可支援 W3 下載閘道，建立 PDF metadata 初版。
- out_of_scope:
  - 不宣告完整 MVP2 Gate 通過。
  - 不實作下載閘道。
- forbidden_actions:
  - 缺 audit / scope evidence 不得進入 W3。
  - Gate 判斷不得由 AI 單獨完成。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer | hands_on_tc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0019`：主持 W2 Gate，確認 DB / audit / scope 不阻擋 W3。 | [GATE] | W2 Gate summary。 | `evidence/MVP2/TASK-RPT-0019/w2-gate-summary.md` | QA / Security / DevOps | pending |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0019`：建立 PDF metadata 初版模型。 | [AI->HUMAN] | `pdf_metadata` 欄位草案。 | `evidence/MVP2/TASK-RPT-0019/pdf-metadata-model.md` | Tech Lead / Captain | pending |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0010`：重跑 audit / scope validators，打包 W2 evidence。 | [AI->HUMAN] | W2 evidence index。 | `evidence/MVP2/index.md` | Tech Lead / Captain | pending |

## Human Gate Watchlist

- ADR needed: PDF metadata 欄位若牽涉正式法遵或保存策略，開 ADR。
- Security / audit risk: audit / scope 未過不得進入下載閘道。
- Formal data boundary: 仍限合成資料。
- Go / No-Go or rollback concern: W3 開工條件需 human review。

## Required Reading

- `docs/keep.summary.md`
- `drills/每日任務卡排程.md` W2D5
- `tasks/TASK-RPT-0010-m1-04-audit-write-foundation.task.md`
- `tasks/TASK-RPT-0019-m4-01-pdf-metadata.task.md`

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

- 這是 W2 mid-gate，不是完整 MVP2 closure。

