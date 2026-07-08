# Daily AI Dispatch - 2026-07-08

## Scope

- stage: MVP1
- roster_source: `drills/每日任務卡排程.md` W1D2
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0001`, `TASK-RPT-0002`, `TASK-RPT-0004`
- today_goal: 收斂 Qutora 文件 / 報表功能覆蓋、DB inventory 與 admin / token / API 可用性，補上 gap、風險與可 review 的 PoC evidence。
- out_of_scope:
  - 不修改 `open-source-sandbox/qutora-api`。
  - 不使用未脫敏正式資料。
  - 不宣告 MVP1 Gate 通過。
  - 不把 Qutora limitation 偽裝成已完成能力。
- forbidden_actions:
  - AI 不得代簽 human gate 或 ADR gate。
  - producer 不得單獨 review 自己產出的 evidence。
  - 未完成 admin / token / API 可用性 evidence 前，不得進入後續下載或正式資料情境。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer | hands_on_tc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0001`：完成文件 / 報表功能覆蓋盤點；補 gap 與不做項。 | [AI->HUMAN] | `qutora-document-feature-map.md`，含覆蓋清單、gap、不做項與下一步建議。 | `evidence/MVP1/TASK-RPT-0001/qutora-document-feature-map.md` | QA / Security / DevOps | pending |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0002`：完成 DB inventory 與 migration risk register；匯出 schema sample。 | [AI->HUMAN] | `source-table-map.csv` 與 migration risk register 草稿，含主要 table、欄位與風險註記。 | `evidence/MVP1/TASK-RPT-0002/source-table-map.csv` | Tech Lead / Captain | pending |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0004`：驗證 admin / token / API 可用性；執行登入與 Swagger / endpoint 探查。 | [AI->HUMAN] | `0004a-qutora-startup-poc.md`，含登入、token、Swagger / endpoint 探查、遮罩與失敗案例紀錄。 | `evidence/MVP1/TASK-RPT-0004/0004a-qutora-startup-poc.md` | Backend / DBA | pending |

## Human Gate Watchlist

- ADR needed: none for today;若需修改 Qutora、改 DB 目標、使用正式資料或接受安全例外，立即停下並提出 ADR / human decision。
- Security / audit risk: token、密碼、連線字串、IP 與 Swagger / endpoint response 需遮罩。
- Formal data boundary: 今日只允許 Qutora demo / 合成 / 非正式資料。
- Go / No-Go or rollback concern: 今日不是 Gate day；不得宣告 MVP1 Gate pass。

## Required Reading

- `docs/keep.summary.md`
- `drills/每日任務卡排程.md` W1D2
- `runbooks/RB-06-ai-dispatch-cycle.md`
- `runbooks/RB-01-qutora-startup.md`
- `tasks/TASK-RPT-0001-m0-01-legacy-report-inventory.task.md`
- `tasks/TASK-RPT-0002-m0-02-legacy-data-source-inventory.task.md`
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

- 本派工單只把 W1D2 roster 轉成 RB-06 格式，不新增任務卡規格。
- 若本派工單與任務卡、ADR 或 runbook 衝突，以任務卡、ADR 或 runbook 為準，並在本檔 End-of-day Gate 記錄修正。
- 17:00 前需完成 evidence / blocker / reviewer conflict 檢查；未 review 的 AI 產出不得標記 closure。
