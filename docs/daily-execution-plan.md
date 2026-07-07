# Daily Execution Plan

## 文件定位

本文件是每日開工的靜態作戰手冊。它不取代 `runbooks/RB-06-ai-dispatch-cycle.md` 的派工單格式，也不取代 `drills/每日任務卡排程.md` 的 14 週 roster。

每日實例不得寫回本文件；請依 RB-06 建立在 `evidence/<Stage>/daily-dispatch-YYYY-MM-DD.md`。

## 每日 6 步流程

1. 讀 `docs/keep.summary.md`，確認文件權威順序、AI 決策邊界與開工 preflight。
2. 依 `drills/每日任務卡排程.md` 找出今天的 week / day / stage 與三人主責任務卡。
3. 依 `runbooks/RB-06-ai-dispatch-cycle.md` 建立或更新今日派工單。
4. 每人每日只掛 1 張主責任務卡；團隊 active cards 不超過 3 張。
5. 17:00 依 RB-06 做 evidence / blocker / reviewer conflict 檢查，未 review 的 AI 產出不得 closure。
6. 收工前更新今日派工單的 End-of-day Gate，列出 passed、blocked、carry_over 與 reviewer_conflict。

## 格式唯一 owner

每日派工單、AI 回報格式、review checklist、blocker 升級規則與 end-of-day checklist 的唯一格式 owner 是 `runbooks/RB-06-ai-dispatch-cycle.md`。

本文件只描述每日使用順序，不另定義派工模板。若每日派工欄位不足，應補 RB-06，而不是在本文件另開格式。

## 今日實例落點

每日正式派工單放在：

```text
evidence/<Stage>/daily-dispatch-YYYY-MM-DD.md
```

其中 `<Stage>` 應使用 `MVP1`、`MVP2`、`Pilot` 或 `ProductionCandidate`。若當日是跨階段補洞，仍以主要 Gate 或主要 evidence package 所屬 stage 為準，並在派工單 `Scope` 標明跨階段任務。

## 每日紅線速查

- WIP：每人每日主責最多 1 張任務卡，團隊每日最多 3 張 active cards。
- Review：producer 不得自審；若三人限制導致 reviewer 重疊，需標記 `reviewer_conflict` 並補第二層 review。
- Gate：`[GATE]`、human-only、ADR、人類簽核、Go / No-Go、rollback、舊系統下線不得由 AI 代決。
- Evidence：正式 evidence 必須有 producer、reviewer、可重跑命令或可追溯手動步驟。
- 範圍外任務：W12 / W14 驗收時需對照 `drills/每日任務卡排程.md` §8 的演練範圍外任務卡與例外處理。
- 週末：週末 AI 產出只能作草稿，下一工作日 review 後才可納入 evidence。

