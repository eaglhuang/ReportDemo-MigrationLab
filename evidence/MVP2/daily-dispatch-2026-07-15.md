# Daily AI Dispatch - 2026-07-15

## Scope

- stage: MVP2
- roster_source: `drills/每日任務卡排程.md` W2D2
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0008`
- today_goal: 建立 staging schema / mapping，完成第一批可重跑 metadata import evidence。
- out_of_scope:
  - 不碰正式資料。
  - 不修改 Qutora 原始碼。
  - 不把 schema 草案宣告為正式 DB 設計。
- forbidden_actions:
  - 未有 reviewer notes 不得 closure。
  - schema mismatch 不得以口頭接受。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0008`：審查 staging 欄位是否足以支援後續比對；確認不過度設計。 | [AI->HUMAN] | staging review notes。 | `evidence/MVP2/TASK-RPT-0008/staging-review-notes.md` | QA / Security / DevOps |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0008`：建立 staging tables 與 Qutora metadata mapping。 | [AI->HUMAN] | schema / mapping SQL。 | `evidence/MVP2/TASK-RPT-0008/staging-schema-mapping.sql` | Tech Lead / Captain |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0008`：匯入 MVP1 metadata sample 並重跑。 | [AI->HUMAN] | staging import validator。 | `evidence/MVP2/TASK-RPT-0008/staging-import-validator.md` | Backend / DBA |

## Human Gate Watchlist

- ADR needed: 欄位型別策略若偏離 ADR-013 需升級。
- Security / audit risk: sample import 不得含正式個資。
- Formal data boundary: 只用 MVP1 合成 metadata。
- Go / No-Go or rollback concern: mapping mismatch 需列 blocker。

## Required Reading

- `docs/keep.summary.md`
- `drills/每日任務卡排程.md` W2D2
- `runbooks/RB-05-mariadb-environment.md`
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

- 今日目標是可重跑 staging evidence；不追求完整資料模型。

