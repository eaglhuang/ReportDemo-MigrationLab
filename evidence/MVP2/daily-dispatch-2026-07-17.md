# Daily AI Dispatch - 2026-07-17

## Scope

- stage: MVP2
- roster_source: `drills/每日任務卡排程.md` W2D4
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0014`
- today_goal: 建立 Role / Data Scope foundation 與越權負向測試草稿。
- out_of_scope:
  - 不建立正式 IAM / SSO。
  - 不接受 Admin 自動取得報表內容權限。
- forbidden_actions:
  - 權限不明時不得 fail-open。
  - 未經 QA / Security review 不得 closure。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer | hands_on_tc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0014`：審查 Role 與 Data Scope 分離；確認最小權限。 | [HUMAN] | scope decision notes。 | `evidence/MVP2/TASK-RPT-0014/scope-decision-notes.md` | QA / Security / DevOps | pending |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0014`：建立 Data Scope matrix 與資料表草案。 | [AI->HUMAN] | `data_scope` model。 | `evidence/MVP2/TASK-RPT-0014/data-scope-model.md` | Tech Lead / Captain | pending |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0014`：執行越權查詢 / 下載負向測試草稿。 | [AI->HUMAN] | deny-case evidence。 | `evidence/MVP2/TASK-RPT-0014/deny-case-evidence.md` | Backend / DBA | pending |

## Human Gate Watchlist

- ADR needed: 權限模型邊界改變需 ADR。
- Security / audit risk: Data Scope 測試不得洩漏跨部門資料。
- Formal data boundary: 使用合成 metadata。
- Go / No-Go or rollback concern: 越權成功即 blocking。

## Required Reading

- `docs/keep.summary.md`
- `tasks/TASK-RPT-0014-m2-04-data-scope-foundation.task.md`
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
- hands_on_tc_complete:
  - pending
- velocity:
  - ai_outputs: pending
  - human_closures: pending
  - diff_decisions: pending

## Captain Notes

- 權限 / Data Scope finding 由 QA / Security / DevOps 具 blocking 權限。

