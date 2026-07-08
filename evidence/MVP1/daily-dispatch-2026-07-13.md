# Daily AI Dispatch - 2026-07-13

## Scope

- stage: MVP1
- roster_source: `drills/每日任務卡排程.md` W1D5
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0002`, `TASK-RPT-0003`, `TASK-RPT-0004`
- today_goal: 主持 MVP1 Gate 準備與 evidence 收斂，重看 `TASK-RPT-0001` 到 `TASK-RPT-0004` evidence，判斷是否具備進入 MVP2 的建議條件。
- weekend_skip: 2026-07-11 and 2026-07-12 are skipped; no formal weekend dispatch files are created.
- out_of_scope:
  - 不由 AI 自動宣告 MVP1 Gate pass。
  - 不把缺 evidence 的任務標示 closure。
  - 不使用未脫敏正式資料。
  - 不修改 Qutora 原始碼。
- forbidden_actions:
  - AI 不得代簽 Gate、human sign-off 或 ADR。
  - Gate evidence 缺漏時，不得以進度壓力進入 MVP2。
  - producer 不得單獨 review 自己產出的 evidence。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer | hands_on_tc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0004`：主持 MVP1 Gate；重看 `0001-0004` evidence，決定是否進 MVP2。 | [GATE] | MVP1 Gate summary 草稿，含 pass / blocked / carry_over 建議、限制與 human decision needed。 | `evidence/MVP1/TASK-RPT-0004/mvp1-gate-summary.md` | QA / Security / DevOps | pending |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0002`：補 DB 風險與差異說明；確認 migration 前置輸入完整。 | [AI->HUMAN] | DB inventory final，含 source table map、migration risk、前置輸入完整性與待決項。 | `evidence/MVP1/TASK-RPT-0002/db-inventory-final.md` | Tech Lead / Captain | pending |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0003`：重跑至少 2 個 validator，打包 MVP1 evidence index。 | [AI->HUMAN] | reviewer 可追溯 evidence package，含 validator rerun、evidence index 與缺漏清單。 | `evidence/MVP1/TASK-RPT-0003/mvp1-evidence-index.md` | Backend / DBA | pending |

## Human Gate Watchlist

- ADR needed: 若 MVP1 Gate 建議涉及正式資料、正式技術選型、修改 Qutora、放寬 evidence 或進入 MVP2 條件變更，需 human / ADR gate。
- Security / audit risk: Gate package 必須檢查 token、密碼、連線字串、IP、log 與 PDF / metadata 是否有敏感資訊未遮罩。
- Formal data boundary: 今日只允許 Qutora demo / 合成 / 非正式資料。
- Go / No-Go or rollback concern: 今日可提出 MVP1 Gate 建議，但不得由 AI 自動放行；未通過項需進 blocked 或 carry_over。

## Required Reading

- `docs/keep.summary.md`
- `drills/每日任務卡排程.md` W1D5
- `runbooks/RB-06-ai-dispatch-cycle.md`
- `runbooks/RB-03-evidence-standard.md`
- `tasks/TASK-RPT-0001-m0-01-legacy-report-inventory.task.md`
- `tasks/TASK-RPT-0002-m0-02-legacy-data-source-inventory.task.md`
- `tasks/TASK-RPT-0003-m0-03-legacy-result-baseline.task.md`
- `tasks/TASK-RPT-0004-m0-04-third-party-cross-platform-poc.task.md`

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

- 本派工單只把 W1D5 roster 轉成 RB-06 格式，不新增任務卡規格。
- W1D5 接在 2026-07-10 之後的下一個工作日；2026-07-11 與 2026-07-12 不排正式工作。
- 若本派工單與任務卡、ADR 或 runbook 衝突，以任務卡、ADR 或 runbook 為準，並在本檔 End-of-day Gate 記錄修正。
- 17:00 前需完成 evidence / blocker / reviewer conflict 檢查；未 review 的 AI 產出不得標記 closure。
