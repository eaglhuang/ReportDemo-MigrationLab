---
task_id: TASK-RPT-0004
source_milestone: M0-04
title: "建立第三方與跨平台 PoC"
status: planned
owner: project-captain
priority: P0
milestone: M0
drill_stage: "MVP1"
execution_mode: "ai-with-human-review"
primary_role: "Tech Lead / Captain"
support_roles:
  - "Backend / DBA"
  - "QA / Security / DevOps"
depends_on:
  - "TASK-RPT-0001"
  - "TASK-RPT-0002"
related_plan: "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
drill_plan: "drills/分階段演練與驗收計畫.md"
runbooks:
  - "runbooks/RB-01-qutora-startup.md"
  - "runbooks/RB-03-evidence-standard.md"
evidence_path: "evidence/MVP1/TASK-RPT-0004/"
scopePaths:
  - "tasks/TASK-RPT-0004-m0-04-third-party-cross-platform-poc.task.md"
  - "evidence/MVP1/TASK-RPT-0004/**"
  - "open-source-sandbox/qutora-api/samples/docker-compose.sqlserver.yml"
  - "open-source-sandbox/qutora-api/Qutora.Database.SqlServer/**"
  - "open-source-sandbox/qutora-api/Qutora.Database.MySQL/**"
  - "open-source-sandbox/qutora-api/Qutora.Database.PostgreSQL/**"
deliverables:
  - "evidence/MVP1/TASK-RPT-0004/qutora-startup-poc.md"
  - "evidence/MVP1/TASK-RPT-0004/db-provider-compatibility.md"
  - "evidence/MVP1/TASK-RPT-0004/pdf-library-risk.md"
  - "evidence/MVP1/TASK-RPT-0004/storage-auth-poc.md"
  - "evidence/MVP1/TASK-RPT-0004/poc-decision-summary.md"
validators:
  - "V-0004-01"
  - "V-0004-02"
  - "V-0004-03"
  - "V-0004-04"
  - "V-0004-05"
  - "V-0004-06"
  - "V-0004-07"
  - "V-0004-08"
  - "V-0004-09"
  - "V-0004-10"
evidence:
  required: command-backed
rollback:
  strategy: stop-poc-and-clean-local-containers
  notes: "本卡只做 PoC 與決策摘要；若 PoC 失敗，停止該技術路線並記錄不可用原因，不修改 Qutora 原始碼。"
outOfScope:
  - "採購或正式選定 PDF library"
  - "取代 ADR-001 的正式 DB 選型"
  - "導入 Kubernetes 或正式 CI/CD"
  - "修改 Qutora 原始碼"
nonGoals:
  - "完成正式跨平台部署"
  - "完成 MariaDB migration 實作"
---
# TASK-RPT-0004 - M0-04 建立第三方與跨平台 PoC

## 任務目標

建立 MVP1 所需的最小 PoC 判斷：Qutora 是否能在演練環境啟動、Qutora 既有 DB provider 是否能支撐後續 SQL Server 到 MariaDB 的演練、PDF / storage / auth 風險是否需要在 MVP2 前升級為 blocking issue。

## 真實功能帶入場景

Tech Lead / Captain 協調 Backend / DBA 與 QA / Security / DevOps，依 `RB-01` 驗證 Qutora Docker Compose、SQL Server provider 與既有 MySQL / PostgreSQL provider 原始碼。此卡不完成正式選型，只輸出可否進入 MVP2 的 PoC decision summary。

## 舊系統覆蓋

| PoC 類型 | Qutora 對應 | 目的 |
| --- | --- | --- |
| 啟動基準 | `samples/docker-compose.sqlserver.yml` | 確認舊系統可跑。 |
| SQL Server provider | `Qutora.Database.SqlServer` | 確認舊系統來源 DB。 |
| MariaDB / MySQL 參考 | `Qutora.Database.MySQL` | 供 ADR-013 演練目標 DB 參考。 |
| PostgreSQL provider | `Qutora.Database.PostgreSQL` | 作為技術比較，不取代演練決策。 |
| PDF / storage 風險 | Documents / Storage provider | 確認 MVP2 下載與浮水印風險。 |

## 落地設計

| 項目 | 定義 |
| --- | --- |
| API | 不新增 API；只驗證 Qutora 既有 API 與 provider。 |
| 資料表 | 不新增資料表；記錄 SQL Server schema 與 MySQL / PostgreSQL provider 差異。 |
| 狀態機 | `candidate`、`usable-for-drill`、`needs-follow-up`、`blocked`。 |
| 錯誤碼 | PoC 文件需記錄 docker / DB / auth / storage / PDF 風險錯誤與阻擋條件。 |
| 權限檢查 | 僅確認 admin 初始化、一般使用者與下載權限是否能被演練。 |
| 稽核欄位 | 記錄 Qutora 是否能產生上傳 / 下載 / 登入相關 audit 或替代 log。 |
| fail-closed | 若 Qutora 無法啟動、DB provider 不可判讀或 PDF baseline 不可建立，不得進入 MVP2。 |

## 影響範圍

- 影響 MVP1 是否可進入 MVP2。
- 影響 ADR-013 的 MariaDB 演練落地方式，但不取代正式專案 DB 選型。
- 影響 M5-01 / M5-02 是否需要提前處理 PDF library 或下載風險。
- 不修改 Qutora 原始碼、不建立正式部署、不採購商用 library。

## 輸入與輸出

| 類型 | 內容 |
| --- | --- |
| 輸入 | `TASK-RPT-0001` 功能盤點、`TASK-RPT-0002` DB 盤點、Qutora samples、DB provider 原始碼。 |
| 輸出 | Qutora startup PoC、DB provider compatibility、PDF library risk、storage/auth PoC、decision summary。 |

## 完成定義

- Qutora 啟動與 DB provider 風險有明確 pass / fail / blocked 結論。
- MariaDB 演練路線的可行性、缺口與 MVP2 前置條件已列出。
- PDF、storage、auth、audit 的高風險項目已標記 owner 與後續任務。
- reviewer 可依 evidence 判斷是否進入 MVP2。

## Validators

| ID | 輸入條件 | 執行方式 / Evidence | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| V-0004-01 | Docker 可用 | `docker compose ... config --quiet` | Compose 可解析 | Compose 失敗 |
| V-0004-02 | Qutora 可啟動 | 記錄 startup evidence | API / DB 可用或明確記錄 blocked | 啟動失敗無 evidence |
| V-0004-03 | SQL Server provider 可讀 | 檢查 provider / migration | 舊系統 DB 來源明確 | provider 不明 |
| V-0004-04 | MySQL provider 可讀 | 檢查 provider / migration | 可供 MariaDB 演練參考 | provider 不明且無替代 |
| V-0004-05 | PostgreSQL provider 可讀 | 記錄比較結果 | 比較項存在 | 比較完全缺失 |
| V-0004-06 | PDF 路徑可判讀 | 記錄文件上傳 / 下載風險 | MVP2 PDF PoC 風險明確 | 風險不明 |
| V-0004-07 | Storage provider 可判讀 | 記錄 bucket/provider 能力 | 儲存風險明確 | 儲存來源不明 |
| V-0004-08 | Auth / permission 可判讀 | 記錄登入與權限風險 | 權限 PoC 可規劃 | 權限來源不明 |
| V-0004-09 | decision summary 完成 | 檢查 pass/fail/blocked | 每項 PoC 有結論 | 結論缺失 |
| V-0004-10 | evidence 路徑正確 | 檢查 `evidence/MVP1/TASK-RPT-0004/` | 符合 RB-03 | 使用舊 `M0-04` 路徑 |

## Test Cases

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| TC-0004-01 | Docker 可用 | 檢查 Qutora compose config | config pass | config fail |
| TC-0004-02 | Compose 可用 | 啟動或 dry-run 記錄 | 可取得啟動 evidence | 無法啟動且無處理 |
| TC-0004-03 | SQL Server provider 存在 | 盤點 provider 能力 | SQL Server 來源明確 | 來源不明 |
| TC-0004-04 | MySQL provider 存在 | 比對 migration / provider | MariaDB 演練可初步評估 | 風險無法評估 |
| TC-0004-05 | PostgreSQL provider 存在 | 記錄比較差異 | 比較依據存在 | 比較無資料 |
| TC-0004-06 | PDF baseline 需求存在 | 檢查 Qutora 文件流程 | 可規劃 MVP2 PDF PoC | PDF 流程不明 |
| TC-0004-07 | storage 元件存在 | 檢查 provider / bucket | 可規劃 storage PoC | 儲存風險不明 |
| TC-0004-08 | auth 元件存在 | 檢查 auth / role / permission | 可規劃權限測試 | 權限風險不明 |
| TC-0004-09 | PoC 結論完成 | reviewer 檢查 decision summary | 可判斷 Go to MVP2 / 調整 / blocked | 結論不可決策 |
| TC-0004-10 | MVP1 Gate review | Tech Lead 彙整 V-0004 evidence | Gate 狀態明確 | Gate 無證據 |

## Reviewer / Human Gate / ADR

| 項目 | 規則 |
| --- | --- |
| Reviewer | Tech Lead / Captain 彙整，Backend / DBA 複核 DB provider，QA / Security / DevOps 複核 runtime / auth / evidence。 |
| Human Gate | 若 Qutora 啟動或 provider PoC 失敗，需人類決定是否延長 MVP1、縮 MVP2 或更換演練舊系統。 |
| ADR | 若要改變 MariaDB 演練目標、修改 Qutora 原始碼或採購 PDF library，需更新 ADR-013 或新增 ADR。 |

## Notes

- 2026-07-06 | upgraded | MVP1 核心卡已補齊完整任務卡格式，evidence 改為 `evidence/MVP1/TASK-RPT-0004/`。
