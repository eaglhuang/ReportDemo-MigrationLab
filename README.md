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
| 7 | `drills/AI主導三人併行排程與缺口分析.md` | 三人皆具 AI 環境時的壓縮排程、AI / HUMAN 標籤、review WIP 與缺口清單。 |
| 8 | `drills/每日任務卡排程.md` | 14 週每日三人任務卡 roster；每人每天至少 1 張主責卡，含目標、步驟與下班驗收。 |
| 9 | `runbooks/` | 可照做的操作手冊。 |
| 10 | `tasks/` | 可派工任務卡與任務卡開工標準。 |

若文件衝突，先依架構治理與已簽核 ADR 判定邊界，再更新演練計畫、runbook 與任務卡。

## 三人小隊首讀清單

| 角色 | 先讀 | 第二步 |
| --- | --- | --- |
| Tech Lead / Captain | 本 README、架構與治理計畫書、ADR | 讀 `drills/分階段演練與驗收計畫.md` 第 1 到 3 章，再讀 `drills/AI主導三人併行排程與缺口分析.md` 與 `drills/每日任務卡排程.md` 確認 AI 主導排程、每日領卡、WIP 與 Gate。 |
| Backend / DBA | 功能里程碑計畫、ADR-012、ADR-013、ADR-015 | 讀 MVP1 / MVP2 階段、`RB-02-seed-data-synthetic-pdf.md` 與 `RB-05-mariadb-environment.md`。 |
| QA / Security / DevOps | Agent Team 計畫書、`tasks/README.md` | 讀 `RB-01-qutora-startup.md`、`RB-03-evidence-standard.md`、`RB-04-rollback-rehearsal.md`、`RB-07-parallel-run-operations.md`、`RB-09-backup-recovery-policy.md`。 |

## 12 步執行路線

1. 讀本 README，確認固定事實與文件權威順序。
2. 執行 `git submodule update --init --recursive`，確認 Qutora commit。
3. 依 `runbooks/RB-01-qutora-startup.md` 啟動 Qutora 與 SQL Server。
4. 依 `runbooks/RB-02-seed-data-synthetic-pdf.md` 建立合成 PDF 與 metadata。
5. 依 `runbooks/RB-03-evidence-standard.md` 建立 evidence index。
6. 執行 `drills/分階段演練與驗收計畫.md` 的 MVP1；若三人皆具 AI 環境，依 `drills/AI主導三人併行排程與缺口分析.md` 採 Base Plan 12 到 14 週排程，並依 `drills/每日任務卡排程.md` 與 `runbooks/RB-06-ai-dispatch-cycle.md` 進行每日領卡、派工與 review。
7. MVP1 Gate 通過後，依 `runbooks/RB-05-mariadb-environment.md` 建立 MariaDB 演練環境。
8. 依 ADR-015 在 `poc/` 與 `tools/` 內執行 MVP2 PoC，不修改 Qutora 原始碼。
9. MVP2 Gate 通過後，升級 Pilot 核心任務卡並執行 Pilot。
10. Pilot Gate 通過後，準備 Production Candidate evidence package。
11. 依 `runbooks/RB-04-rollback-rehearsal.md` 與 `runbooks/RB-09-backup-recovery-policy.md` 執行 backup / restore / rollback dry run，並依 ADR 與 Gate 總表完成 human sign-off。
12. 若要正式上線或下線舊路徑，必須依 `runbooks/RB-08-cutover-runbook.md` 執行切換 rehearsal，並另行取得 Go / No-Go 簽核。

## 第一個命令

```powershell
git submodule update --init --recursive
```

完成後請依 `runbooks/RB-01-qutora-startup.md` 繼續。
