# RB-06 AI Dispatch Cycle

目的：定義三人皆具 AI 開發環境時，每日如何派工、執行、回報、review、升級 blocker 與保存 evidence。本 runbook 依 ADR-016 與 `drills/AI主導三人併行排程與缺口分析.md` 執行。

## 1. 基本規則

- 每人每日最多 8 小時，每週 5 個工作日，週末不排正式工作。
- AI 可主開發，但不得取代 human / ADR gate。
- AI 產出的程式、文件、validator、evidence 草稿，需由人類 reviewer 或指定人類代理驗收。
- producer 不得自審；產出該 evidence 的 AI session、Agent 或人類，不得單獨擔任 reviewer。
- 每人每日最多 review 3 張任務卡或 3 組 evidence package；超過即排入下一工作日。
- 任何資安、稽核、資料一致性、權限、rollback、Go / No-Go 相關 blocker，優先於新增功能。

## 2. 每日派工單格式

每天 09:00 前由 Tech Lead / Captain 建立或更新當日派工單，可放在 `evidence/<Stage>/daily-dispatch-YYYY-MM-DD.md`。

```markdown
# Daily AI Dispatch - YYYY-MM-DD

## Scope

- stage:
- active_tasks:
- today_goal:
- out_of_scope:
- forbidden_actions:

## Assignments

| Person | AI role/session | Task | execution_mode | Expected artifact | Reviewer |
| --- | --- | --- | --- | --- | --- |
| Tech Lead / Captain |  |  | [AI] / [AI->HUMAN] / [HUMAN] / [GATE] |  |  |
| Backend / DBA |  |  |  |  |  |
| QA / Security / DevOps |  |  |  |  |  |

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

## 3. AI 回報格式

AI 每次完成一個工作單元，需回報下列內容，不得只寫「已完成」：

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

## 4. Review Checklist

### 4.1 程式碼 / PoC Review

| 檢查項 | 必要條件 |
| --- | --- |
| Scope | 只修改任務卡 `scopePaths` 或派工單允許範圍。 |
| Qutora | 不修改 `open-source-sandbox/qutora-api`，除非另有 ADR 或人類簽核。 |
| Secret | 無硬編碼密碼、token、連線字串或正式資料。 |
| Fail-closed | 權限、稽核、浮水印、hash、metadata 失敗時不得靜默成功。 |
| Evidence | 有可重跑命令、輸出、hash 或 log。 |
| Rollback | 說明停用、回復或丟棄 PoC 的方式。 |

### 4.2 Evidence Review

| 檢查項 | 必要條件 |
| --- | --- |
| 路徑 | 符合 `evidence/<Stage>/<TASK-ID>/`。 |
| Producer | 可填 AI agent / session / person。 |
| Reviewer | 必須是人類 reviewer 或指定人類代理。 |
| Reproducible | reviewer 能重跑命令或追溯手動步驟。 |
| Masking | token、密碼、連線字串、IP 如需遮罩應已遮罩。 |
| Gap | Qutora 能力不足需標 `qutora_capability_gap=true`。 |

### 4.3 負向測試 Review

| 檢查項 | 必要條件 |
| --- | --- |
| Unauthorized | 未授權 / 跨 scope / 過期 token 不得成功。 |
| Audit failure | 關鍵稽核寫入失敗時需 fail-closed。 |
| Watermark failure | 浮水印失敗不得輸出未浮水印 PDF。 |
| Hash mismatch | hash 不一致需標記 mismatch 或 failed_closed。 |
| Data mismatch | 新舊資料差異需分類、owner、處理建議。 |

## 5. Blocker 升級規則

| 類型 | 升級對象 | 規則 |
| --- | --- | --- |
| 資安 / 權限 | QA / Security / DevOps + Tech Lead | 立即停止 closure，不得由 AI 放行。 |
| 稽核 / evidence | Audit / Evidence reviewer + Tech Lead | 補證據或列 Gate blocking。 |
| 正式資料 | Tech Lead + 人類資料 owner | 未核准正式資料不得進 repo 或一般測試。 |
| ADR | Tech Lead / Captain | 建 ADR 草稿，但決策需人類接受。 |
| Qutora 限制 | Tech Lead + Backend / DBA + QA | 標 `qutora_capability_gap=true`，決定 fallback 是否可接受。 |
| Go / No-Go | 人類代理簽核人 | AI 只能彙整 package，不得建議自動放行。 |

## 6. 週末規則

週末不排正式工作。若 AI 在週末被動或自動產出草稿：

- 不得直接納入 evidence。
- 不得標記任務卡 closure。
- 不得觸發 Go / No-Go 或 ADR 狀態變更。
- 必須在下一個工作日由人類 reviewer 檢查後，才可作為正式產出。

## 7. End-of-day Checklist

每天收工前需完成：

- 今日 AI 產出均有 `AI Work Report`。
- 今日正式 evidence 均有 producer / reviewer。
- reviewer_conflict 已標記並排第二層 review。
- blocking finding 已列 owner 與下一步。
- 未 review 的 AI 產出未被標記 closure。
- 明日派工不超過 review WIP 上限。
