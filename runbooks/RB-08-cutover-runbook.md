# RB-08 Cutover Runbook

目的：定義 Production Candidate 階段的切換 rehearsal 腳本，包含凍結點、最終同步、checksum、切換動作、煙霧測試、回退決策點與 hypercare 觀察期。

適用階段：W12-W14、`TASK-RPT-0040`、`TASK-RPT-0043`、`TASK-RPT-0044`。

## 1. 前置條件

| 條件 | 必要證據 |
| --- | --- |
| Pilot Gate 通過 | `evidence/Pilot/parallel-run-summary.md` 或等效 Gate package。 |
| RB-07 連續 N=3 通過 | parallel run summary。 |
| RB-09 備份與回復政策確認 | backup manifest、restore evidence。 |
| RB-04 rollback dry run 通過 | rollback run result、RTO / RPO。 |
| Go / No-Go package 草稿完成 | `evidence/ProductionCandidate/TASK-RPT-0040/`。 |
| 人類簽核 | 業務、稽核、資安、維運代理簽核。 |

## 2. Cutover 時間軸

| 時點 | 動作 | Owner | 繼續 / 回退判斷 |
| --- | --- | --- | --- |
| T-2d | 發布 cutover rehearsal scope、凍結功能變更。 | Captain | 未完成不得進 T-1d。 |
| T-1d | 執行完整備份、產生 restore point、確認 rollback path。 | Backend / DBA + QA | restore point 不存在則停止。 |
| T-4h | 凍結 Pilot 資料範圍，停止新增演練資料。 | Captain | 若有未完成批次，延後切換。 |
| T-3h | 最終 Qutora export 與 MariaDB sync。 | Backend / DBA | 筆數 / hash 不一致且無解釋則回退。 |
| T-2h | 執行 checksum、metadata、PDF hash、audit sample 檢查。 | QA / Security / DevOps | 任一 P0 / P1 未解則回退。 |
| T-1h | 切換 rehearsal：將使用者路徑指向新下載閘道或模擬 routing。 | Captain + Backend | gateway / auth / audit 失敗則回退。 |
| T+30m | Smoke test：登入、查詢、下載、浮水印、hash、audit、alert。 | QA / Security / DevOps | 任一核心 smoke test 失敗則回退。 |
| T+2h | Hypercare 第一次觀察：錯誤率、延遲、audit、alert。 | 三人小隊 | 指標超標則回退或 freeze。 |
| T+1d | Hypercare 結束判斷。 | Captain + Human Gate | 未達穩定門檻不得宣告通過。 |

## 3. Smoke Test 清單

| ID | 測試 | 通過條件 | 回退條件 |
| --- | --- | --- | --- |
| SMK-01 | 使用者登入 / token | 可登入且權限正確。 | 無法登入或權限錯誤。 |
| SMK-02 | 報表查詢 | 只看得到 Data Scope 內資料。 | 越權可見。 |
| SMK-03 | PDF 下載 | 必經 gateway、watermark、hash、audit。 | 可繞過任一關卡。 |
| SMK-04 | 浮水印 | 下載人、時間、序號、查核碼可見。 | 缺欄位或無水印。 |
| SMK-05 | Audit | 下載與失敗事件皆可查。 | audit 遺失。 |
| SMK-06 | Alert | P0/P1 事件依嚴重度通知。 | 無通知或通知錯人。 |
| SMK-07 | Rollback | 可切回 Qutora 路徑。 | 回退路徑不可用。 |

## 4. Hypercare 觀察指標

| 指標 | 門檻 | 觸發動作 |
| --- | --- | --- |
| P0 事件 | 0 | 立即回退或 freeze。 |
| P1 事件 | 0 未解 | freeze，2 小時內裁決。 |
| 下載錯誤率 | 小於 1% | 超標則停新路徑。 |
| audit 寫入失敗 | 0 | fail-closed 並回退。 |
| 平均下載延遲 | 需低於 Pilot baseline 2 倍 | 超標則降載或回退。 |
| rollback readiness | 必須可執行 | 不可執行則不得切換。 |

## 5. 回退判斷

任一情境發生時回退：

- 權限越權、audit 遺失、未浮水印 PDF 輸出。
- checksum / hash 不一致且無解釋。
- 下載閘道或登入不可用。
- RTO / RPO 無法量測或超過 RB-09 政策。
- 人類 Gate 未簽核。

回退後需產出：

- `cutover-abort-report.md`
- `rollback-started-at` / `rollback-ended-at`
- `impact-summary.md`
- `postmortem-draft.md`

