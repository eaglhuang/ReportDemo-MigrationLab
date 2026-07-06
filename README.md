# ReportDemo Migration Lab

本 repo 是「內部人員交易報表轉媒體儲存系統」的獨立模擬搬移實驗室，用來保存計畫書、任務卡、ADR、演練 runbook、驗收 evidence，以及以 Qutora 作為本演練舊系統的執行紀錄。

## 固定事實

| 項目 | 內容 |
| --- | --- |
| 本演練舊系統 | Qutora |
| 舊系統位置 | `open-source-sandbox/qutora-api` |
| 固定 commit | `de156e0eb72d58772a76e570eb711db344bedfc0` |
| 舊系統 DB | Qutora SQL Server / `QutoraDB` |
| 本演練目標 DB | MariaDB，依 ADR-013，僅限本演練路線 |
| 正式資料原則 | 不得使用未脫敏正式資料 |

Qutora 代表本次演練舊系統，用於驗證搬移流程、PDF 移轉、metadata、下載、權限、稽核與平行驗證；不宣稱涵蓋真實券商舊系統的全部業務規則、正式資料、法遵規則或報表計算邏輯。

## 文件權威順序

| 順序 | 文件 | 說了算的範圍 |
| ---: | --- | --- |
| 1 | `README.md` | 先讀什麼、什麼文件說了算、三人小隊如何開始。 |
| 2 | `內部人員交易報表轉媒體儲存系統_系統架構與治理計畫書.md` | 架構、安全、權限、PDF、浮水印、稽核、告警、NFR 與治理邊界。 |
| 3 | `內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md` | 功能範圍、M0 到 M10 里程碑與驗收條件。 |
| 4 | `決策紀錄樣板ADR.md` | 人類決策、ADR 狀態、Qutora、MariaDB、MVP 節奏與任務卡 gate。 |
| 5 | `內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md` | Agent Team 派工、review、validator、human / ADR gate 與違規阻擋。 |
| 6 | `drills/分階段演練與驗收計畫.md` | 三人小隊分階段執行、驗收、Gate 與 evidence package。 |
| 7 | `runbooks/` | 可照做的操作手冊。 |
| 8 | `tasks/` | 可派工任務卡與任務卡開工標準。 |

若文件衝突，先依架構治理與已簽核 ADR 判定邊界，再更新演練計畫、runbook 與任務卡。

## 三人小隊首讀清單

| 角色 | 先讀 | 第二步 |
| --- | --- | --- |
| Tech Lead / Captain | 本 README、架構與治理計畫書、ADR | 讀 `drills/分階段演練與驗收計畫.md` 第 1 到 3 章，確認 Gate 與責任矩陣。 |
| Backend / DBA | 功能里程碑計畫、ADR-012、ADR-013 | 讀 MVP1 / MVP2 階段與 `RB-02-seed-data-synthetic-pdf.md`。 |
| QA / Security / DevOps | Agent Team 計畫書、`tasks/README.md` | 讀 `RB-01-qutora-startup.md`、`RB-03-evidence-standard.md`、`RB-04-rollback-rehearsal.md`。 |

## 12 步執行路線

1. 讀本 README，確認固定事實與文件權威順序。
2. 執行 `git submodule update --init --recursive`，確認 Qutora commit。
3. 依 `runbooks/RB-01-qutora-startup.md` 啟動 Qutora 與 SQL Server。
4. 依 `runbooks/RB-02-seed-data-synthetic-pdf.md` 建立合成 PDF 與 metadata。
5. 依 `runbooks/RB-03-evidence-standard.md` 建立 evidence index。
6. 執行 `drills/分階段演練與驗收計畫.md` 的 MVP1。
7. MVP1 Gate 通過後，執行 MVP2。
8. MVP2 Gate 通過後，升級 Pilot 核心任務卡並執行 Pilot。
9. Pilot Gate 通過後，準備 Production Candidate evidence package。
10. 依 `runbooks/RB-04-rollback-rehearsal.md` 執行 rollback dry run。
11. 依 ADR 與 Gate 總表完成 human sign-off。
12. 若要正式上線或下線舊路徑，必須另行取得 Go / No-Go 簽核。

## 第一個命令

```powershell
git submodule update --init --recursive
```

完成後請依 `runbooks/RB-01-qutora-startup.md` 繼續。
