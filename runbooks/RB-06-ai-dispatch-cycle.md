# RB-06 AI Dispatch Cycle

目的：定義三人皆具 AI 開發環境時，每日如何派工、執行、回報、review、升級 blocker 與保存 evidence。本 runbook 是每日 HOW；每日 WHAT/WHEN 由 `drills/每日任務卡排程.md` 維護，AI / HUMAN / GATE 邊界由 ADR-016 維護。

## 1. 基本規則

- 每人每日最多 8 小時，週末不排正式工作。
- AI 可以主開發、整理 evidence、起草 review notes，但不可擔任 DRI、closure reviewer、human-only gate 或 ADR 決策者。
- 任務卡 `primary_role` 是單一 DRI；`closure_reviewer` 必須是另一個人類角色。
- Producer 不可自我驗收；reviewer conflict 必須記在 dispatch 與 EOD。
- 每日正式 closure 建議最多 3 張任務卡，避免 review WIP 爆量。
- 權限、正式資料、audit、rollback、Go / No-Go、ADR 都是 blocker 類型，不能用 AI 結論直接關閉。
- 結果制驗收採雙層人類動作：每日每人 1 條 hands-on test case；週五 Demo Day 目視 4 種最終結果。格式與最低要求以本 runbook 為準。

## 2. 每日六步驟

1. **Preflight**：讀 `docs/keep.summary.md`、`git status --short`、今日 roster、相關任務卡。
2. **選卡**：從 `drills/每日任務卡排程.md` 找今天 WHAT/WHEN，不從 backlog 隨機抓卡。
3. **派工**：09:00 前由 Tech Lead / Captain 建立或更新 `evidence/<Stage>/daily-dispatch-YYYY-MM-DD.md`。
4. **執行**：每位角色只負責自己是 `primary_role` 的卡；支援其他卡時在 Main task 標成 contributor。
5. **Review**：依任務卡 `closure_reviewer` 指派，不可 producer 自審；AI reviewer 只能驗證中間 evidence，不能取代 closure reviewer。
6. **Hands-on**：每位角色親手執行 1 條當日主責卡 test case，回填 `hands_on_tc`。
7. **EOD**：回填 passed / blocked / carry_over / reviewer_conflict、hands_on_tc 與 velocity，並把 evidence path 保持可追溯。

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

| Person | AI role/session | Main task | execution_mode | Today outcome | Evidence path | Reviewer | hands_on_tc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain |  |  | [AI] / [AI->HUMAN] / [HUMAN] / [GATE] |  |  |  | TC-ID / pass-fail / finding / <=30m |
| Backend / DBA |  |  |  |  |  |  |  |
| QA / Security / DevOps |  |  |  |  |  |  |  |

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
- hands_on_tc_complete:
- velocity:
  - ai_outputs:
  - human_closures:
  - diff_decisions:
```

`hands_on_tc` 必填規則：

- 每人每日從當日主責任務卡的 Test Cases 表挑 1 條親手執行，記錄 TC 編號、pass / fail、發現與耗時；每人每日上限 30 分鐘。
- 優先挑負向、fail-closed、權限、audit、hash mismatch、rollback 類 test case。
- 若 hands-on TC fail，當日比照 blocker 寫入 `evidence/<Stage>/risk-blocker-log.md`；該卡當日不得由 AI reviewer close。
- hands-on TC 不取代任務卡 validators，也不取代 closure reviewer；它是防止橡皮圖章的最低人類動作。

## 4. AI 輔助驗收模式

AI reviewer 可協助驗證中間 evidence，但必須遵守：

- 使用獨立 session；不得與 producer 同一 session。
- 只讀任務卡驗收條件、validators、test cases、evidence path 與必要輸入；不得讀 producer 的實作理由來替 producer 辯護。
- 輸出決策包採三段格式：`結論建議`、`異常清單`、`可重跑命令`。
- AI reviewer 的 review note 可供 closure reviewer 參考，但不能取代人類 closure reviewer、human-only gate 或 ADR 決策。
- 安全關鍵例外不得由 AI reviewer 加速 closure：`TASK-RPT-0023` / `0024` 的 fail-closed 負向測試、`TASK-RPT-0038` break-glass、所有 `[GATE]` 與 human-only 卡（0040 / 0041 / 0043 / 0044 / 0045）。

```markdown
## AI Reviewer Decision Pack

- task_id:
- conclusion: pass / fail / blocked / needs-human
- anomalies:
- rerun_commands:
- evidence_checked:
- reviewer_session_id:
- human_decision_needed:
```

## 5. AI Work Report

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

## 6. Review Checklist

| 類型 | 檢查重點 |
| --- | --- |
| Scope | 是否只改任務卡與 dispatch 允許的範圍。 |
| Qutora | 是否未修改 Qutora 原始碼；若需改，是否已有 ADR 或明確授權。 |
| Secret | 是否沒有 token、密碼、正式個資或未遮罩資料。 |
| Fail-closed | 權限、audit、hash、metadata、rollback 是否有失敗路徑。 |
| Evidence | 是否可重現、可追溯、含 producer / reviewer。 |
| Rollback | PoC 或資料變更是否能回復。 |

## 7. Blocker 升級規則

| 類型 | 升級對象 | 規則 |
| --- | --- | --- |
| 權限 / 正式資料 | QA / Security / DevOps + Tech Lead | 必須 human gate，不可 AI closure。 |
| Evidence | closure reviewer + Tech Lead | 缺 evidence 時不可關卡。 |
| 架構決策 | Tech Lead / Captain | 需要 ADR 或明確 deferred decision。 |
| Qutora capability gap | Tech Lead + Backend / DBA + QA | 記錄 gap 與 fallback，不直接改上游。 |
| Go / No-Go | 三角色共同 review | AI 只能準備 package，人類決策。 |

## 8. Demo Day 結果制驗收

每週五 Gate day 需做 Demo Day，定位為整週畫面級驗收；它與每日 hands-on TC 互補，不互相取代。紀錄落點：

```text
evidence/<Stage>/demo-day-W<N>.md
```

| # | 人類目視的最終結果 | 驗到什麼 | 硬規則 | 預估時間 |
| --- | --- | --- | --- | ---: |
| 1 | 功能畫面 + 浮水印 PDF 目視 | 功能正確 | 需看到實際畫面與 PDF，不只看文字摘要 | 20m |
| 2 | 親手用無權限帳號操作一次，看到拒絕畫面 | 越權防護 | 必須本人操作，不得看 AI 截圖代替 | 15m |
| 3 | 稽核查詢畫面：1 / 2 操作可查到，查核碼可反查下載紀錄 | 稽核完整性 | 查核碼與下載紀錄需可追溯 | 20m |
| 4 | 差異儀表板：173 endpoints 雙製比對彙總頁 | 轉換等價性 | P0=0 才算綠燈 | 30m；W8 前端 19 域走查可放大為半天 |

Demo Day evidence 欄位：

| 欄位 | 說明 |
| --- | --- |
| result_item | 1 / 2 / 3 / 4 |
| operator | 實際操作人 |
| decision | pass / fail / blocked |
| finding | 發現與嚴重度 |
| artifact_ref | 截圖、PDF、hash、查核碼、儀表板連結或檔案指標 |
| follow_up | 需要回填的任務卡、risk id 或 ADR |

## 9. 週末規則

週末不排正式工作；只能做非阻塞整理，不得新增正式 closure、Go / No-Go 或 ADR 決策。

## 10. End-of-day Checklist

每日 EOD 必須把風險從 daily dispatch 收斂到 stage-level risk log；daily dispatch 不是長期風險登錄簿。

新增檢查項：

- 今日 P0/P1 finding 或 `[GATE]` blocker 已寫入 `evidence/<Stage>/risk-blocker-log.md`。
- 若任務卡標為 `blocked`，已在 blocker 欄位或 Notes 引用 risk-blocker-log id。
- 若同一 blocker 連續三個工作日未關閉，隔日 dispatch 必須排入 Tech Lead / Captain triage。
- 今日三人的 `hands_on_tc` 已填；fail 已入 risk-blocker-log，且該卡未由 AI reviewer close。
- velocity 已記錄：當日 AI 產出數、人類 close 數、差異裁決筆數；供 W5 檢查點與未來估算使用。

## 11. Weekly Gate Risk Sweep

每週五 Gate day 由 Tech Lead / Captain 彙整：

- `evidence/<Stage>/risk-blocker-log.md` 的 open / investigating 項。
- 本週 daily dispatch 的 blocked / carry_over / reviewer_conflict。
- 任務卡 `status: blocked` 且缺少 risk id 的違規項。
- 累積三天以上未關閉的同一 blocker。

若存在 P0/P1 open finding，該 Gate 不得標記 pass；若要降級，必須有 human sign-off、原因、owner、target close date 與 evidence reference。

- 收齊 AI Work Report。
- 確認 evidence path 存在且可追溯。
- 確認 reviewer 不等於 producer / DRI。
- 確認 AI reviewer 不等於 producer session，且沒有取代人類 closure reviewer。
- 確認 Demo Day 4 種結果已執行；若缺漏，該週 Gate 不得標記 pass。
- 確認 blocker 有 owner 與 next action。
- 確認沒有 AI 擔任 DRI、closure reviewer 或 human gate。
- 更新隔日 carry_over。
