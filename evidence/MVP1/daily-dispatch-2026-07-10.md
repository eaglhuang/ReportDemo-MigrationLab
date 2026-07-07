# Daily AI Dispatch - 2026-07-10

## Scope

- stage: MVP1
- roster_source: `drills/每日任務卡排程.md` W1D4
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0003`, `TASK-RPT-0004`
- today_goal: 建立第三方 / 跨平台 PoC 風險判斷，補齊 DB provider、PDF、storage、auth 與無權限下載 / audit 追蹤測試。
- task_ownership:
  - `TASK-RPT-0004 / 0004c` DRI: Tech Lead / Captain; Backend / DBA is contributor; QA / Security / DevOps is closure reviewer.
  - `TASK-RPT-0003` DRI: QA / Security / DevOps; Backend / DBA is technical reviewer for baseline evidence.
- out_of_scope:
  - 不做正式技術選型。
  - 不修改 Qutora 原始碼補齊缺口。
  - 不使用未脫敏正式資料。
  - 不宣告 MVP1 Gate 通過。
- forbidden_actions:
  - AI 不得接受資安例外或正式選型風險。
  - 無權限下載若成功，必須列為 blocker，不得視為可接受差異。
  - producer 不得單獨 review 自己產出的 evidence。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0004 / 0004c` DRI：建立第三方 / 跨平台 PoC 風險判斷；整理 DB provider、PDF、storage、auth 風險。 | [AI->HUMAN] | `0004c-decision-summary.md` 草稿，含 DB provider、PDF、storage、auth 風險與待決項；負責本卡當日 closure 建議。 | `evidence/MVP1/TASK-RPT-0004/0004c-decision-summary.md` | QA / Security / DevOps |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0004 / 0004b` contributor：檢查 DB provider 與 storage compatibility；列出 MariaDB / SQL Server 差異風險，交給本卡 DRI 彙整。 | [AI->HUMAN] | `0004b-db-provider-compat.md`，含 provider 差異、storage 風險、migration 注意事項；不單獨宣告本卡完成。 | `evidence/MVP1/TASK-RPT-0004/0004b-db-provider-compat.md` | Tech Lead / Captain + QA / Security / DevOps |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0003`：執行無權限下載與 audit / log 追蹤測試；保存失敗與成功路徑。 | [AI->HUMAN] | `expected-result.md` 與 `baseline-review.md`，含成功 / 失敗路徑、audit / log 追蹤與 blocker 判斷。 | `evidence/MVP1/TASK-RPT-0003/expected-result.md` | Backend / DBA |

## Human Gate Watchlist

- ADR needed: 若今日風險判斷推導出正式 DB、PDF library、storage、auth 或資安例外選型，需 ADR / human decision。
- Security / audit risk: 無權限下載、audit 缺漏、log 含敏感資料都應列 blocker 或 rework。
- Formal data boundary: 今日只允許 Qutora demo / 合成 / 非正式資料。
- Go / No-Go or rollback concern: 今日不是 Gate day；只準備 MVP1 Gate input。

## Required Reading

- `docs/keep.summary.md`
- `drills/每日任務卡排程.md` W1D4
- `runbooks/RB-06-ai-dispatch-cycle.md`
- `runbooks/RB-02-seed-data-synthetic-pdf.md`
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

## Captain Notes

- 本派工單只把 W1D4 roster 轉成 RB-06 格式，不新增任務卡規格。
- 同一任務卡若同日有多人參與，只能有一位 DRI；其他人是 contributor 或 reviewer，不得共同宣告 closure。
- 2026-07-11 與 2026-07-12 為週末，不建立正式每日派工單；週末 AI 產出只能作草稿，需 2026-07-13 review 後才可納入 evidence。
- 若本派工單與任務卡、ADR 或 runbook 衝突，以任務卡、ADR 或 runbook 為準，並在本檔 End-of-day Gate 記錄修正。
- 17:00 前需完成 evidence / blocker / reviewer conflict 檢查；未 review 的 AI 產出不得標記 closure。
