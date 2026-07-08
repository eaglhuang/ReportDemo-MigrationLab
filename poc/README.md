# ReportDemo PoC Workspace

本目錄是 ReportDemo 演練專用 PoC 程式碼落點，依 ADR-015 管理。

> 2026-07-08 更新（ADR-018）：新平台功能（下載閘道、浮水印、hash、查詢、移植模組）改以 C# 直接在 `src/` 實作，不再先做 Python PoC 再重寫。本目錄降為輔助工具落點：合成資料、validator、比對腳本、migration CSV 管線。

## 邊界

- 僅用於演練下載閘道、動態浮水印、MariaDB metadata migration 與 validator。
- 不修改 Qutora submodule。
- 不代表正式系統最終架構或正式 SDK 採購決策。

## 建議結構

```text
poc/
├─ README.md
├─ download-gateway/
├─ watermark/
├─ migration/
└─ validators/
```

## 技術棧

- 語言：Python 3。
- PDF PoC：優先使用標準函式庫產生測試 PDF；若 MVP2 需要更完整浮水印，可在 ADR-015 記錄演練限定 library。
- MariaDB client：先以 `docker exec mariadb` 與 SQL 檔完成；若需要 Python client，需在 ADR-015 補充套件與安裝方式。

## 資料抽取建議路線

SQL Server 到 MariaDB 的抽取，預設不安裝 Python 的 SQL Server driver（pyodbc / ODBC 在 Windows 上安裝成本高且非演練重點），改走檔案交換：

1. 用 RB-01 的 sqlcmd 命令從 `QutoraDB` 匯出 CSV（`docker exec qutora-sqlserver ... sqlcmd -s "," -W`）。
2. Python 腳本只負責 CSV 清洗與轉換。
3. 用 `docker exec reportdemo-mariadb mariadb ...` 或 `LOAD DATA LOCAL INFILE` 匯入 MariaDB。

每一步的命令與輸出都需記入 `evidence/MVP2/TASK-RPT-0008/`，reviewer 需可用同一批 CSV 重跑。若此路線不足以支撐 MVP2 驗證，改用 Python client 前需先更新 ADR-015。
