# Daily AI Dispatch - 2026-07-28

## Scope

- stage: Pilot
- roster_source: `drills/每日任務卡排程.md` W4D1
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0011`
- today_goal: 補齊 validation rule 規格與 10 validators / 10 test cases 草稿。
- out_of_scope:
  - 不新增正式 DSL。
  - 不改變 MVP scope。
- forbidden_actions:
  - 未定義阻擋條件不得 closure。
  - AI 不得裁決 validation rule MVP 邊界。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0011`：決定 validation rule MVP 範圍。 | [HUMAN] | rule scope decision。 | `evidence/Pilot/TASK-RPT-0011/rule-scope-decision.md` | QA / Security / DevOps |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0011`：補完整設計規格與最小 PoC。 | [AI->HUMAN] | design-spec。 | `evidence/Pilot/TASK-RPT-0011/design-spec.md` | Tech Lead / Captain |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0011`：補 10 validators / 10 test cases。 | [AI->HUMAN] | validation-result 草稿。 | `evidence/Pilot/TASK-RPT-0011/validation-result.md` | Backend / DBA |

## Human Gate Watchlist

- ADR needed: 若 validation expression 技術棧成正式選型，需 ADR。
- Security / audit risk: validation 不得跳過 audit evidence。
- Formal data boundary: 只用合成資料。
- Go / No-Go or rollback concern: 無阻擋條件不得進 W4D2。

## Required Reading

- `docs/keep.summary.md`
- `tasks/TASK-RPT-0011-m2-01-validation-rule-versioning.task.md`
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

## Captain Notes

- Pilot 補洞期以任務卡完整規格化為主，不開新功能。

