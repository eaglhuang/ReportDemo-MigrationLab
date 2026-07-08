# Daily AI Dispatch - 2026-07-31

## Scope

- stage: Pilot
- roster_source: `drills/每日任務卡排程.md` W4D4
- dispatch_format_owner: `runbooks/RB-06-ai-dispatch-cycle.md`
- active_tasks: `TASK-RPT-0016`
- today_goal: 補 report generation job 設計、重跑、錯誤碼與測試草稿。
- out_of_scope:
  - 不建完整排程平台。
  - 不導入正式 job scheduler。
- forbidden_actions:
  - generation job 不得跳過 audit / status。
  - 失敗重跑策略不明不得 closure。

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain | Captain / Coordinator | `TASK-RPT-0016`：審查 generation job 是否過度設計。 | [AI->HUMAN] | scope cut list。 | `evidence/Pilot/TASK-RPT-0016/scope-cut-list.md` | QA / Security / DevOps |
| Backend / DBA | Backend / DBA Agent | `TASK-RPT-0016`：補批次 job 設計、重跑、錯誤碼。 | [AI->HUMAN] | design-spec。 | `evidence/Pilot/TASK-RPT-0016/design-spec.md` | Tech Lead / Captain |
| QA / Security / DevOps | QA / Security / DevOps Agent | `TASK-RPT-0016`：補成功 / 失敗 / 重跑測試。 | [AI->HUMAN] | validator 草稿。 | `evidence/Pilot/TASK-RPT-0016/validation-result.md` | Backend / DBA |

## Human Gate Watchlist

- ADR needed: 正式 scheduler / worker 技術選型需 ADR。
- Security / audit risk: job retry 不得重複寫錯誤 audit。
- Formal data boundary: 不跑正式批次。
- Go / No-Go or rollback concern: 無 rollback / retry evidence 不得通過。

## Required Reading

- `docs/keep.summary.md`
- `tasks/TASK-RPT-0016-m3-02-report-generation-job.task.md`
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

- 今日成果需支援 W4D5 state machine review。

