# Daily AI Dispatch - 2026-07-09

## Scope

- stage: MVP1
- roster_source: `drills/每日任務卡排程.md` W1D3
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0002`, `TASK-RPT-0003`
- today_goal: 建立 Golden Dataset 邊界、metadata 欄位對照與合成 PDF baseline，確保後續 MVP1 Gate 有可重跑資料證據。
- out_of_scope:
  - 不使用未脫敏正式資料。
  - 不宣告 Golden Dataset 可代表正式業務完整樣貌。
  - 不修改 `open-source-sandbox/qutora-api`。
  - 不宣告 MVP1 Gate 通過。
- forbidden_actions:
  - AI 不得代簽正式資料或 Golden Dataset 使用邊界。
  - 缺少 hash 或 metadata export 時，不得將 PDF baseline 標示完成。
  - producer 不得單獨 review 自己產出的 evidence。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer | hands_on_tc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0003`：確認 Golden Dataset 邊界；審核合成 PDF 欄位與正式資料禁用聲明。 | [AI->HUMAN] | `golden-dataset-definition.md`，含資料邊界、正式資料禁用聲明、欄位與限制。 | `evidence/MVP1/TASK-RPT-0003/golden-dataset-definition.md` | QA / Security / DevOps | pending |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0002`：支援 metadata 欄位對照；把 Qutora 欄位對應到新系統初版欄位。 | [AI->HUMAN] | metadata mapping 草稿，含 Qutora 欄位、新系統候選欄位、轉換風險與未知項。 | `evidence/MVP1/TASK-RPT-0002/metadata-mapping-draft.md` | Tech Lead / Captain | pending |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0003`：產生、上傳、下載合成 PDF；依 RB-02 執行並計算 hash。 | [AI->HUMAN] | `metadata-export.json` 與 `pdf-baseline-hash.csv`，含可重跑命令、輸出與遮罩說明。 | `evidence/MVP1/TASK-RPT-0003/metadata-export.json` | Backend / DBA | pending |

## Human Gate Watchlist

- ADR needed: 若需使用正式資料、擴大 Golden Dataset 邊界或改變正式資料禁用原則，需 human / ADR gate。
- Security / audit risk: PDF、metadata、hash 與 log 不得含正式個資、密碼、token 或未遮罩連線資訊。
- Formal data boundary: 今日只允許合成資料與 Qutora demo 資料。
- Go / No-Go or rollback concern: 今日不是 Gate day；不得宣告 MVP1 Gate pass。

## Required Reading

- `docs/keep.summary.md`
- `drills/每日任務卡排程.md` W1D3
- `runbooks/RB-06-ai-dispatch-cycle.md`
- `runbooks/RB-02-seed-data-synthetic-pdf.md`
- `tasks/TASK-RPT-0002-m0-02-legacy-data-source-inventory.task.md`
- `tasks/TASK-RPT-0003-m0-03-legacy-result-baseline.task.md`

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

- 本派工單只把 W1D3 roster 轉成 RB-06 格式，不新增任務卡規格。
- 若本派工單與任務卡、ADR 或 runbook 衝突，以任務卡、ADR 或 runbook 為準，並在本檔 End-of-day Gate 記錄修正。
- 17:00 前需完成 evidence / blocker / reviewer conflict 檢查；未 review 的 AI 產出不得標記 closure。
