# ReportDemo 新平台程式碼落點

本目錄是演練新平台（HTML5 + ASP.NET Core, C#）的程式碼落點，依 ADR-018 管理。

## 邊界

- 轉換來源為 `open-source-sandbox/qutora-api` 固定 commit 的 ASP.NET 代碼；只讀取、不修改（ADR-012）。
- 新平台功能（下載閘道、浮水印、下載副本 hash、查詢、移植模組）以 C# 在本目錄實作；對應任務卡 `TASK-RPT-0023`、`0024`、`0025`、`0028`、`0009`。
- Python + shell / SQL 輔助工具（合成資料、validator、比對腳本、migration CSV 管線）仍放 `poc/` 與 `tools/`，依 ADR-015。
- 本目錄程式碼僅限演練；不代表正式系統最終架構或正式技術選型（ADR-001 / ADR-007 未決）。

## 建議結構

```text
src/
├─ README.md
├─ ReportDemo.DownloadGateway/     # TASK-RPT-0023
├─ ReportDemo.Watermark/           # TASK-RPT-0024 / 0025
├─ ReportDemo.Documents/           # TASK-RPT-0009 移植模組（document CRUD / categories）
├─ ReportDemo.Web/                 # TASK-RPT-0028 HTML5 最小查詢 / 下載頁
└─ ReportDemo.Shared/              # audit / auth / storage 共用元件
```

實際專案結構由各任務卡開工時定案；每個模組的 evidence 依 RB-03 落在對應任務卡 evidence path。
