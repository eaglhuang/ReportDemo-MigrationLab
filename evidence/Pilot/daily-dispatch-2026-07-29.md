# Daily AI Dispatch - 2026-07-29

## Scope

- stage: Pilot
- roster_source: `drills/每日任務卡排程.md` W4D2
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0012`, `TASK-RPT-0005`
- today_goal: 定義 validation severity，並產 Qutora 元件 conversion-map 草稿。
- out_of_scope:
  - 不開始 0009 實作。
  - 不修改 Qutora 原始碼。
- forbidden_actions:
  - 未完成 conversion map 草稿不得裁決移植工作量。
  - P0/P1 定義不得由 AI 單獨決定。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0012`：定義 severity 對 Gate 的阻擋規則。 | [AI->HUMAN] | severity policy。 | `evidence/Pilot/TASK-RPT-0012/severity-policy.md` | QA / Security / DevOps |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0012` + `TASK-RPT-0005` contributor：補設計規格並產 Qutora 元件分類草稿。 | [AI->HUMAN] | design-spec 與 conversion-map 草稿。 | `evidence/Pilot/TASK-RPT-0005/qutora-component-conversion-map.md` | Tech Lead / Captain |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0012`：補 P0/P1/P2 測試與 fail-closed。 | [AI->HUMAN] | validator 草稿。 | `evidence/Pilot/TASK-RPT-0012/validation-result.md` | Backend / DBA |

## Human Gate Watchlist

- ADR needed: P0/P1 對 Gate 的定義若改動 RB-03，需 ADR / ChangeLog。
- Security / audit risk: severity 降級需 human sign-off。
- Formal data boundary: 不使用正式資料。
- Go / No-Go or rollback concern: conversion-map 草稿不可當 final。

## Required Reading

- `docs/keep.summary.md`
- `tasks/TASK-RPT-0012-m2-02-validation-result-severity.task.md`
- `tasks/TASK-RPT-0005-m0-05-sp-sql-refactor-classification.task.md`
- `src/README.md`

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

- 0005 今日只產草稿；W4D5 / W5D5 才裁決。

