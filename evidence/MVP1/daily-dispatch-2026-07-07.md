# Daily AI Dispatch - 2026-07-07

## Scope

- stage: MVP1
- roster_source: `drills/每日任務卡排程.md` W1D1
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0001`, `TASK-RPT-0002`
- today_goal: 建立 Qutora 舊系統可用性與盤點基準，產出第一批可 review 的 inventory / DB / startup evidence 草稿。
- out_of_scope:
  - 不修改 `open-source-sandbox/qutora-api`。
  - 不使用未脫敏正式資料。
  - 不宣告 MVP1 Gate 通過。
  - 不新增正式架構決策或 ADR 狀態。
- forbidden_actions:
  - AI 不得代簽 human gate 或 ADR gate。
  - producer 不得單獨 review 自己產出的 evidence。
  - 缺少 Qutora 啟動或 DB evidence 時，不得將任務標示 closure。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0001`：建立 Qutora 功能盤點框架；讀 README / RB-01 / Qutora docs，列 Documents API、metadata、download、audit 初表。 | [AI->HUMAN] | `report-inventory.md` 草稿，含功能清單、未知項、Qutora capability gap 初判。 | `evidence/MVP1/TASK-RPT-0001/report-inventory.md` | QA / Security / DevOps |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0002`：盤點 Qutora DB；讀 entity / migration / compose，列主要 table 與欄位。 | [AI->HUMAN] | `qutora-db-inventory.md` 草稿，含主要資料表、欄位、migration risk 初表。 | `evidence/MVP1/TASK-RPT-0002/qutora-db-inventory.md` | Tech Lead / Captain |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0001`：證明 Qutora 可作為舊系統來源；依 RB-01 啟動 API / DB，保存 health evidence。 | [AI->HUMAN] | `qutora-startup.md`，含啟動命令、health / API / DB 檢查結果與敏感資訊遮罩說明。 | `evidence/MVP1/TASK-RPT-0001/qutora-startup.md` | Backend / DBA |

## Human Gate Watchlist

- ADR needed: none for today;若需修改 Qutora、改 DB 目標、使用正式資料或變更 Gate 條件，立即停下並提出 ADR / human decision。
- Security / audit risk: token、密碼、連線字串、IP 與 log 需遮罩；startup evidence 不得含正式資料。
- Formal data boundary: 今日只允許 Qutora demo / 合成 / 非正式資料。
- Go / No-Go or rollback concern: 今日不是 Gate day；不得宣告 MVP1 Gate pass。

## Required Reading

- `docs/keep.summary.md`
- `drills/每日任務卡排程.md` W1D1
- `runbooks/RB-06-ai-dispatch-cycle.md`
- `runbooks/RB-01-qutora-startup.md`
- `tasks/TASK-RPT-0001-m0-01-legacy-report-inventory.task.md`
- `tasks/TASK-RPT-0002-m0-02-legacy-data-source-inventory.task.md`

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

- 本派工單只把 W1D1 roster 轉成 RB-06 格式，不新增任務卡規格。
- 若本派工單與任務卡、ADR 或 runbook 衝突，以任務卡、ADR 或 runbook 為準，並在本檔 End-of-day Gate 記錄修正。
- 17:00 前需完成 evidence / blocker / reviewer conflict 檢查；未 review 的 AI 產出不得標記 closure。
