# RB-07 Parallel Run Operations

目的：定義 Pilot 期間 Qutora 舊系統與新系統平行作業的比對節奏、差異分類、accept / reject 判準、SLA、evidence 與退出條件。本 runbook 依 ADR-017 執行。

適用階段：Pilot W6-W9、`TASK-RPT-0013`、`TASK-RPT-0018`、`TASK-RPT-0022`、`TASK-RPT-0043`。

## 1. 基準方與原則

| 項目 | 規則 |
| --- | --- |
| 基準方 | 本演練並行期間以 Qutora 為 legacy authority。 |
| 退出條件 | 連續 N=3 批次或 N=3 工作日通過平行作業驗證。 |
| 正式資料 | 不得使用未脫敏正式資料。 |
| 裁決權 | AI 可產生差異報告；accept / reject / downgrade 必須由 `[HUMAN]` 或 ADR gate 決定。 |
| evidence | 每次平行作業需寫入 `evidence/Pilot/parallel-run/YYYY-MM-DD/`。 |

## 2. 每日運轉節奏

| 時間 | 動作 | Owner | Evidence |
| --- | --- | --- | --- |
| 09:00 | 確認今日批次範圍、資料日期、報表代號、PDF 清單。 | Captain | `parallel-run-plan.md` |
| 10:00 | 從 Qutora 匯出 metadata、PDF hash、audit sample。 | Backend / DBA | `qutora-export.csv`、`qutora-hash.csv` |
| 11:00 | 從新系統 / MariaDB 匯出同批資料。 | Backend / DBA | `new-system-export.csv`、`new-system-hash.csv` |
| 13:00 | 執行差異比對與分類。 | AI + Backend / DBA | `diff-report.csv` |
| 15:00 | 執行權限、下載、audit、alert 抽測。 | QA / Security / DevOps | `validation-result.md` |
| 16:30 | 差異 review、accept / reject / owner 指派。 | Captain + Reviewer | `accept-reject-list.md` |
| 17:30 | 更新連續通過次數與 blocker。 | Captain | `parallel-run-summary.md` |

## 3. 差異分類字典

P0-P3 的全域定義以 `runbooks/RB-03-evidence-standard.md` 為準；本節只提供平行作業差異的特化判讀例子。若本節與 RB-03 衝突，以 RB-03 為準。

| 等級 | 類型 | 範例 | 處理方式 | Gate 影響 |
| --- | --- | --- | --- | --- |
| P0 | 資安 / 權限 / 稽核重大差異 | 越權下載成功、audit 遺失、繞過 gateway、未浮水印 PDF 輸出。 | 立即停止 Gate，修復後重跑。 | 阻擋進 Production Candidate。 |
| P0 | 資料完整性重大差異 | PDF 主檔 hash 不一致、資料筆數遺失、legacy reference 重複。 | 立即停止 Gate，需 root cause。 | 阻擋。 |
| P1 | 業務結果差異 | metadata 重要欄位不同、狀態機結果不同、報表版本錯誤。 | 24 小時內修復或人類簽核降級。 | 未關閉則阻擋。 |
| P2 | 可解釋格式差異 | 排序不同、時間格式不同、大小寫或空白差異、非關鍵欄位 null / empty 表示不同。 | 3 個工作日內關閉或登記轉換規則。 | 可不阻擋，但需 owner。 |
| P3 | 文件 / evidence 差異 | 檔名、路徑、報表描述文字不一致但不影響驗證。 | 5 個工作日內修正。 | 不阻擋。 |

## 4. 可接受差異判準

| 差異 | 可接受條件 | 不可接受條件 |
| --- | --- | --- |
| 時間戳差異 | 時區轉換可解釋，差距小於 1 秒或符合批次產生時間規則。 | 影響資料日期、報表版本、audit 時序或追責。 |
| 排序差異 | 排序欄位未定義，重新排序後結果一致。 | 排序影響報表頁碼、hash、審核結果或下載結果。 |
| 編碼差異 | UTF-8 / Big5 轉換可逆且欄位內容一致。 | 產生亂碼、欄位截斷或無法搜尋。 |
| 空值差異 | 舊系統空字串與新系統 null 已登記 mapping。 | 權限、機密等級、報表代號、資料日期等關鍵欄位缺值。 |
| PDF hash 差異 | 只限動態浮水印後的下載副本，且 master hash 一致。 | 主檔 hash 不一致或無法解釋。 |

## 5. 平行作業輸入與輸出

輸入：

- Qutora document id / legacy reference 清單。
- Qutora metadata export。
- Qutora PDF master hash。
- MariaDB metadata export。
- 新系統 PDF hash / download copy hash。
- audit event export。
- 權限與 Data Scope matrix。

輸出：

- `parallel-run-plan.md`
- `diff-report.csv`
- `diff-classification.md`
- `accept-reject-list.md`
- `parallel-run-summary.md`
- `review-and-signoff.md`

## 6. 退出條件

需同時滿足：

1. 連續 3 批次或 3 個工作日 P0 差異為 0。
2. P1 差異為 0，或已修復並重跑通過，或經 human gate 簽核降級。
3. P2 / P3 差異皆有 owner、期限與追蹤紀錄。
4. rollback dry run 已可用，至少可回到 Qutora 路徑。
5. evidence 可重跑，reviewer 與 producer 不為同一人。

## 7. 阻擋條件

- 任一 P0 差異。
- 未解釋 P1 差異。
- audit / hash / 權限 evidence 不可重跑。
- 差異分類沒有 owner。
- Qutora 與新系統任一側資料來源不明。
- 連續通過次數未達 ADR-017 的 N=3。
