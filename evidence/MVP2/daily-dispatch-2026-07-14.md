# Daily AI Dispatch - 2026-07-14

## Scope

- stage: MVP2
- roster_source: `drills/每日任務卡排程.md` W2D1
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0007`, `TASK-RPT-0008`
- today_goal: 啟動 MariaDB / staging / import batch 基礎，確認 MVP1 baseline 可帶入 MVP2。
- out_of_scope:
  - 不使用未脫敏正式資料。
  - 不修改 `open-source-sandbox/qutora-api`。
  - 不宣告 MVP2 Gate 通過。
- forbidden_actions:
  - AI 不得擔任 DRI、closure reviewer 或 human gate。
  - 缺 MariaDB evidence 時不得標示 DB 任務 closure。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0007`：定義 import batch 範圍與成功條件；確認來源只用 MVP1 合成資料。 | [HUMAN] | batch source scope 與成功條件。 | `evidence/MVP2/TASK-RPT-0007/batch-source-scope.md` | QA / Security / DevOps |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0007`：設計 batch 狀態、筆數、hash、錯誤與重跑欄位。 | [AI->HUMAN] | import batch design 草稿。 | `evidence/MVP2/TASK-RPT-0007/import-batch-design.md` | Tech Lead / Captain |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0008`：依 RB-05 建 MariaDB 並驗證連線。 | [AI->HUMAN] | MariaDB environment evidence。 | `evidence/MVP2/TASK-RPT-0008/mariadb-environment-evidence.md` | Backend / DBA |

## Human Gate Watchlist

- ADR needed: DB 邊界改變、正式資料使用或 migration 策略改變才需要。
- Security / audit risk: DB 連線字串、帳密、host / port 需遮罩。
- Formal data boundary: 只允許 MVP1 合成 / demo baseline。
- Go / No-Go or rollback concern: 今日只建立環境，不做 Gate pass。

## Required Reading

- `docs/keep.summary.md`
- `drills/每日任務卡排程.md` W2D1
- `runbooks/RB-06-ai-dispatch-cycle.md`
- `runbooks/RB-05-mariadb-environment.md`
- `tasks/TASK-RPT-0007-m1-01-import-batch-management.task.md`
- `tasks/TASK-RPT-0008-m1-02-staging-tables.task.md`

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

- 本派工單只把 W2D1 roster 轉成 RB-06 格式，不新增任務卡規格。
- 若出現 DB blocker，需寫入 `evidence/MVP2/risk-blocker-log.md`。

