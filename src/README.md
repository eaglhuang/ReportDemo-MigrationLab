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
├─ ReportDemo.Documents/           # TASK-RPT-0009 移植模組（Documents / Approval / Shares / Admin）
├─ ReportDemo.Web/                 # TASK-RPT-0028 HTML5 19 功能域 UI
└─ ReportDemo.Shared/              # audit / auth / storage 共用元件
```

## Engineering Start Contract

所有涉及 `src/` 的任務卡，都以本節作為最低工程契約。

| 項目 | 定義 |
| --- | --- |
| Solution | `src/ReportDemo.sln` |
| Target framework | .NET 10 / ASP.NET Core 10 |
| Restore command | `dotnet restore src/ReportDemo.sln` |
| Build command | `dotnet build src/ReportDemo.sln --no-restore` |
| Test command | `dotnet test src/ReportDemo.sln --no-build` |
| Warnings | `src/Directory.Build.props` 設定 `TreatWarningsAsErrors=true` |

## Project Map

| Project | 任務卡 | 責任 |
| --- | --- | --- |
| `ReportDemo.Shared` | shared | audit、operation result、共用 value object |
| `ReportDemo.DownloadGateway` | `TASK-RPT-0023` | 下載閘道狀態、錯誤碼、fail-closed decision |
| `ReportDemo.Watermark` | `TASK-RPT-0024` / `0025` | 浮水印 payload、render policy、hash handoff |
| `ReportDemo.Documents` | `TASK-RPT-0005` / `0009` | Qutora conversion map、0009 workstreams 移植 |
| `ReportDemo.Web` | `TASK-RPT-0028` | HTML5 19 功能域 UI 與 API facade |
| `ReportDemo.Tests` | all `src/` cards | task-level unit tests and regression tests |

## AI Code Change Checklist

AI 或人類修改 `src/` 時，closure 前至少要留下：

1. 對應任務卡 ID。
2. 修改的 project / module。
3. `dotnet build src/ReportDemo.sln --no-restore` 結果。
4. `dotnet test src/ReportDemo.sln --no-build` 結果。
5. 任務卡指定的 evidence path。
6. reviewer 非 producer 的 review note。

## Module Done Definition

卡片層 closure 依 ADR-016 結果制雙層驗收：AI reviewer（獨立 session）驗中間 evidence，人類以每日 hands-on TC 與週五 Demo Day 驗最終結果；安全關鍵模組（DownloadGateway fail-closed、break-glass 相關）維持人類逐卡 closure，不得由 AI reviewer 加速。

一個 `src/` 模組只有在下列條件都滿足時，才可回報 done：

- 對應任務卡的 `scopePaths`、deliverables、validators 已更新或引用。
- 至少一個正向測試與一個 blocking / fail-closed 測試已存在，若任務性質不適用需在 evidence 說明。
- `ReportDemo.Tests` 可重跑。
- 若模組是 Qutora 移植項，必須能連回 `TASK-RPT-0005` conversion map；若屬 `TASK-RPT-0009`，還要連回 module porting comparison report。
- 未完成或未移植項不得偽裝完成，必須交給 `TASK-RPT-0045` 的 `unported-qutora-api-list.md` 收口。
