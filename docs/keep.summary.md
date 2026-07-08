# ReportDemo Migration Lab Keep Summary

## Preflight 補充：先補既有文件

文件治理採「必要性優先」：先判斷既有文件能不能承載缺口；能承載就原地補強，不能承載才新增文件。本次不新增閱讀總包、不新增 ownership map。

| 類型 | 職責 | 開工時是否必讀 |
| --- | --- | --- |
| `README.md` | repo 入口、閱讀路線、文件邊界 | 是 |
| `docs/keep.summary.md` | preflight 摘要、最高共識索引 | 是 |
| `drills/分階段演練與驗收計畫.md` | MVP 範圍、12+2 計畫、人力、Gate、風險總覽 | 需要理解整體時讀 |
| `drills/每日任務卡排程.md` | 每日 WHAT / WHEN roster；+2 只作 buffer，不是開發期 | 每日開工讀 |
| `runbooks/RB-*.md` | HOW：可執行步驟、命令、證據格式 | 依任務讀 |
| `tasks/TASK-RPT-*.task.md` | 單一 Owner 的 scope、deliverables、validators、reviewer | 依任務 ID 讀 |
| `evidence/` | dispatch、測試、review、Gate package 證據 | 寫入與驗收時讀 |
| `archive/` | 已被取代的歷史文件 | 平常不讀 |

## 核心共識

本 repo 的工作方式是：先讀摘要，再依任務讀最小必要文件；規格、ADR、任務卡、runbook、evidence 各司其職，不用多份文件重複同一段流程。

- Qutora 是參考平台，鎖定 `open-source-sandbox/qutora-api` 的既定 commit。
- 目標資料庫採 MariaDB，決策依 ADR-013。
- PoC 只落在 `poc/` 與 `tools/`，決策依 ADR-015。
- Evidence 標準依 `runbooks/RB-03-evidence-standard.md`。
- 任務卡入口依 `tasks/README.md`。
- 每日 WHAT/WHEN 依 `drills/每日任務卡排程.md`。
- 每日 HOW 依 `runbooks/RB-06-ai-dispatch-cycle.md`。

## 文件權威順序

1. `README.md`
2. `docs/keep.summary.md`
3. `內部人員交易報表轉媒體儲存系統_系統架構與治理計畫書.md`
4. `內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md`
5. `決策紀錄樣板ADR.md`
6. `內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md`
7. `tasks/README.md`
8. `tasks/TASK-RPT-*.task.md`
9. `runbooks/RB-*.md`
10. `drills/分階段演練與驗收計畫.md`
11. `drills/每日任務卡排程.md`
12. `evidence/`
13. `archive/`，僅供歷史查考，不作為現行規則

## 30 分鐘上手路線

1. 讀 `README.md` 的文件權威順序、每日閱讀路線、角色新人地圖。
2. 讀本摘要，確認最新共識與 preflight。
3. 讀 `內部人員交易報表轉媒體儲存系統_系統架構與治理計畫書.md`，只抓 Qutora、MariaDB、PDF、storage、security 的邊界。
4. 讀 `內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md`，理解 M0 到 M10 的順序。
5. 讀 `tasks/README.md`，理解任務卡、DRI、closure reviewer、evidence path。
6. 若今天要開工，照 `drills/每日任務卡排程.md` -> RB-06 -> 任務卡。

## 深讀分流

- 要做架構或資料庫：讀系統架構與治理計畫書、ADR-012/013/015、相關 RB 與任務卡。
- 要指揮每日協作：讀 Agent Team 計畫書、`drills/每日任務卡排程.md`、RB-06、今日任務卡。
- 要做驗證或安全：讀 `tasks/README.md`、RB-03、RB-04、相關 validator / evidence 任務卡。
- 要處理 Gate：讀 ADR、分階段演練與驗收計畫、對應 evidence package。

## 任務卡閱讀規則

不要從 TASK-RPT-0001 一路讀到 TASK-RPT-0045。先讀 `tasks/README.md` 判斷 stage，再只讀今天 dispatch 指到的任務卡與其 dependencies。

- MVP1：Qutora 盤點、資料源盤點、Golden Dataset、第三方 PoC。
- MVP2：MariaDB、staging、audit、Data Scope、PDF metadata、download / watermark / hash。
- Pilot：平行驗證、PDF 完整性、查詢、安全、audit、role/data scope。
- Production Candidate：break-glass、Go / No-Go、rollback、UAT、release acceptance。
- Backlog：只在被 dispatch 或 Gate 指定時讀。

## AI 協作邊界

AI 可以起草、實作、產生 evidence、整理 validator 結果，但不可擔任 DRI、closure reviewer、human-only gate 或 ADR 決策者。

所有不可逆決策、正式資料邊界、權限模型、Go / No-Go、release gate 都必須有人類 sign-off。

## Preflight Checklist

1. 讀本摘要。
2. 執行 `git status --short`，辨識既有變更。
3. 確認本次任務 ID、stage、evidence path。
4. 讀相關任務卡與 runbook。
5. 修改文件後檢查 UTF-8 no BOM、U+FFFD、mojibake。
