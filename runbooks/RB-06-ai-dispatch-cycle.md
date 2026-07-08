# RB-06 AI Dispatch Cycle

目的：定義三人皆具 AI 開發環境時，每日如何派工、執行、回報、review、升級 blocker 與保存 evidence。本 runbook 是每日 HOW；每日 WHAT/WHEN 由 `drills/每日任務卡排程.md` 維護，AI / HUMAN / GATE 邊界由 ADR-016 維護。

## 1. 基本規則

- 每人每日最多 8 小時，週末不排正式工作。
- AI 可以主開發、整理 evidence、起草 review notes，但不可擔任 DRI、closure reviewer、human-only gate 或 ADR 決策者。
- 任務卡 `primary_role` 是單一 DRI；`closure_reviewer` 必須是另一個人類角色。
- Producer 不可自我驗收；reviewer conflict 必須記在 dispatch 與 EOD。
- 每日正式 closure 建議最多 3 張任務卡，避免 review WIP 爆量。
- 權限、正式資料、audit、rollback、Go / No-Go、ADR 都是 blocker 類型，不能用 AI 結論直接關閉。

## 2. 每日六步驟

1. **Preflight**：讀 `docs/keep.summary.md`、`git status --short`、今日 roster、相關任務卡。
2. **選卡**：從 `drills/每日任務卡排程.md` 找今天 WHAT/WHEN，不從 backlog 隨機抓卡。
3. **派工**：09:00 前由 Tech Lead / Captain 建立或更新 `evidence/<Stage>/daily-dispatch-YYYY-MM-DD.md`。
4. **執行**：每位角色只負責自己是 `primary_role` 的卡；支援其他卡時在 Main task 標成 contributor。
5. **Review**：依任務卡 `closure_reviewer` 指派，不可 producer 自審，不可 AI review closure。
6. **EOD**：回填 passed / blocked / carry_over / reviewer_conflict，並把 evidence path 保持可追溯。

## 3. 每日派工單格式

每天 09:00 前由 Tech Lead / Captain 建立或更新，可放在 `evidence/<Stage>/daily-dispatch-YYYY-MM-DD.md`。

`Main task` 可填正式任務卡，也可標註卡內 workstream，例如：`TASK-RPT-0004 / 0004b contributor`。workstream 不是獨立任務卡，除非已可獨立排程、獨立 gate、獨立 closure，且已寫入 ChangeLog。

```markdown
# Daily AI Dispatch - YYYY-MM-DD

## Scope

- stage:
- active_tasks:
- today_goal:
- out_of_scope:
- forbidden_actions:

## Assignments

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer |
| --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain |  |  | [AI] / [AI->HUMAN] / [HUMAN] / [GATE] |  |  |  |
| Backend / DBA |  |  |  |  |  |  |
| QA / Security / DevOps |  |  |  |  |  |  |

## Human Gate Watchlist

- ADR needed:
- Security / audit risk:
- Formal data boundary:
- Go / No-Go or rollback concern:

## End-of-day Gate

- passed:
- blocked:
- carry_over:
- reviewer_conflict:
```

## 4. AI Work Report

```markdown
## AI Work Report

- task_id:
- execution_mode:
- files_changed:
- commands_run:
- evidence_path:
- validators_run:
- test_cases_run:
- assumptions:
- blockers:
- human_decision_needed:
- rollback_or_recovery_note:
```

## 5. Review Checklist

| 類型 | 檢查重點 |
| --- | --- |
| Scope | 是否只改任務卡與 dispatch 允許的範圍。 |
| Qutora | 是否未修改 Qutora 原始碼；若需改，是否已有 ADR 或明確授權。 |
| Secret | 是否沒有 token、密碼、正式個資或未遮罩資料。 |
| Fail-closed | 權限、audit、hash、metadata、rollback 是否有失敗路徑。 |
| Evidence | 是否可重現、可追溯、含 producer / reviewer。 |
| Rollback | PoC 或資料變更是否能回復。 |

## 6. Blocker 升級規則

| 類型 | 升級對象 | 規則 |
| --- | --- | --- |
| 權限 / 正式資料 | QA / Security / DevOps + Tech Lead | 必須 human gate，不可 AI closure。 |
| Evidence | closure reviewer + Tech Lead | 缺 evidence 時不可關卡。 |
| 架構決策 | Tech Lead / Captain | 需要 ADR 或明確 deferred decision。 |
| Qutora capability gap | Tech Lead + Backend / DBA + QA | 記錄 gap 與 fallback，不直接改上游。 |
| Go / No-Go | 三角色共同 review | AI 只能準備 package，人類決策。 |

## 7. 週末規則

週末不排正式工作；只能做非阻塞整理，不得新增正式 closure、Go / No-Go 或 ADR 決策。

## 8. End-of-day Checklist

每日 EOD 必須把風險從 daily dispatch 收斂到 stage-level risk log；daily dispatch 不是長期風險登錄簿。

新增檢查項：

- 今日 P0/P1 finding 或 `[GATE]` blocker 已寫入 `evidence/<Stage>/risk-blocker-log.md`。
- 若任務卡標為 `blocked`，已在 blocker 欄位或 Notes 引用 risk-blocker-log id。
- 若同一 blocker 連續三個工作日未關閉，隔日 dispatch 必須排入 Tech Lead / Captain triage。

## 9. Weekly Gate Risk Sweep

每週五 Gate day 由 Tech Lead / Captain 彙整：

- `evidence/<Stage>/risk-blocker-log.md` 的 open / investigating 項。
- 本週 daily dispatch 的 blocked / carry_over / reviewer_conflict。
- 任務卡 `status: blocked` 且缺少 risk id 的違規項。
- 累積三天以上未關閉的同一 blocker。

若存在 P0/P1 open finding，該 Gate 不得標記 pass；若要降級，必須有 human sign-off、原因、owner、target close date 與 evidence reference。

- 收齊 AI Work Report。
- 確認 evidence path 存在且可追溯。
- 確認 reviewer 不等於 producer / DRI。
- 確認 blocker 有 owner 與 next action。
- 確認沒有 AI 擔任 DRI、closure reviewer 或 human gate。
- 更新隔日 carry_over。
