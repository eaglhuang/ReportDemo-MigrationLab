# ReportDemo Migration Lab

本 repo 是「內部人員交易報表轉媒體儲存系統」的遷移演練場，目標是用 Qutora、MariaDB、任務卡、runbook 與 evidence，把舊報表流程逐步驗證到可上線的節奏。

## 文件邊界

本 repo 不新增新的 MVP 總包文件；缺口優先補回既有 source of truth，避免文件越補越肥。

| 問題 | 主要閱讀文件 | 邊界 |
| --- | --- | --- |
| MVP v1 範圍、12+2 計畫、人力、Gate | `drills/分階段演練與驗收計畫.md` | 12 週是 baseline；+2 是 buffer，不是開發期 |
| 每天誰做什麼、何時交 evidence | `drills/每日任務卡排程.md` | 只管 WHAT / WHEN，不重貼設計細節 |
| M5-01 下載閘道 API / DB / 狀態 / fail-closed | `tasks/TASK-RPT-0023-m5-01-download-gateway.task.md` | 任務卡是實作契約 |
| M5-02 動態浮水印欄位 / 主副本流程 / Hash 時點 | `tasks/TASK-RPT-0024-m5-02-dynamic-watermark.task.md` 與 `TASK-RPT-0025` | 0024 管浮水印，0025 管下載副本 Hash |
| MariaDB 環境、MSSQL -> MariaDB 改造與回復 | `runbooks/RB-05-mariadb-environment.md` | runbook 管 HOW |
| Qutora 代碼轉換軌（新平台 HTML5 + ASP.NET Core C#） | ADR-018、`tasks/TASK-RPT-0005`、`0009`、`src/README.md` | **全功能轉換**：19 controllers / 173 endpoints 全部要有下落（移植或 documented exception，0045 對帳）；轉換來源唯讀；`src/` 是新平台落點；`poc/` 降為輔助工具 |
| PoC 輔助工具與 smoke path | `poc/README.md`、`evidence/MVP2/poc-smoke/validation-result.json` | 不取代 `src/` C# 實作；用來快速產生合成資料、metadata projection、download decision、watermark payload 與 validator evidence |
| 每日 hands-on TC 與每週五 Demo Day（結果制雙層驗收） | `runbooks/RB-06-ai-dispatch-cycle.md`、ADR-016 | 每人每日親手跑 1 條 test case；週五目視 4 種最終結果；格式唯一出處是 RB-06 |
| 單一 Owner、reviewer、validators、evidence path | `tasks/README.md` 與各任務卡 | 不另建 ownership map |

簡單分工：`docs` 是長期共識與入口，`drills` 是演練節奏，`runbooks` 是怎麼做，`tasks` 是單一 Owner 的交付契約，`evidence` 是證據，`archive` 是歷史。

## 文件權威順序

| 順位 | 文件 | 用途 |
| ---: | --- | --- |
| 1 | `README.md` | 全 repo 入口、閱讀路線、角色地圖。 |
| 2 | `docs/keep.summary.md` | 每次開工 preflight 摘要；共識變更需同步 ADR 或 ChangeLog。 |
| 3 | `內部人員交易報表轉媒體儲存系統_系統架構與治理計畫書.md` | 系統範圍、Qutora/MariaDB/PDF/storage/security 規格。 |
| 4 | `內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md` | M0 到 M10 里程碑與功能分期。 |
| 5 | `決策紀錄樣板ADR.md` | 架構決策、AI 協作、人類 Gate 與不可逆決策。 |
| 6 | `內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md` | 三人角色、review、validator、human / ADR gate。 |
| 7 | `tasks/README.md` + `tasks/TASK-RPT-*.task.md` | 任務卡契約、單一 DRI、closure reviewer、實際交付邊界。 |
| 8 | `drills/分階段演練與驗收計畫.md` | MVP1 / MVP2 / Pilot / Production Candidate 的 Gate 範圍。 |
| 9 | `drills/每日任務卡排程.md` | 每日 WHAT/WHEN roster；今天誰做哪張卡。 |
| 10 | `runbooks/RB-06-ai-dispatch-cycle.md` | 每日 HOW；派工單、六步驟、AI 回報、review、EOD。 |
| 11 | `runbooks/` | 各主題操作手冊。 |
| 12 | `evidence/` | 每日派工單、任務證據、Gate package。 |
| 13 | `archive/` | 歷史分析與過渡文件；不能作為現行規則。 |

## 每日閱讀路線

每天開工只走這條：

1. 讀 `docs/keep.summary.md`，確認最高共識與 preflight。
2. 讀 `drills/每日任務卡排程.md`，找今天的 WHAT/WHEN。
3. 讀 `runbooks/RB-06-ai-dispatch-cycle.md`，照 HOW 產生或更新 `evidence/<Stage>/daily-dispatch-YYYY-MM-DD.md`。
4. 讀當天涉及的 `tasks/TASK-RPT-*.task.md`，只讀任務卡內的 scope、deliverables、validators、evidence path。
5. 每人每日從主責卡挑 1 條 test case **親手執行**，記入派工單 `hands_on_tc` 欄（優先挑負向 / fail-closed 類；fail 即 blocker 入簿）。
6. 收工時把 evidence 與 review 結果回填到派工單與任務卡指定位置。
7. 每週五加開 Demo Day：目視 4 種最終結果（功能畫面與浮水印 PDF、親手越權被拒、稽核查詢可反查、173 endpoints 差異儀表板 P0=0），格式依 RB-06。

## 角色新人地圖

第一天不用讀完整 repo。每個角色先用約 90 分鐘讀到可開工，再依任務卡補讀。

| 角色 | 必讀 | 明確不用先讀 |
| --- | --- | --- |
| Tech Lead / Captain | `README.md` 全文 -> `docs/keep.summary.md` -> `drills/分階段演練與驗收計畫.md` §0/§2/§4/§9 -> `內部人員交易報表轉媒體儲存系統_系統架構與治理計畫書.md` §1 -> `決策紀錄樣板ADR.md` §3、ADR-012 到 ADR-018 | 架構書附錄 B-H；功能里程碑全文，接任務卡時再查對應 M 節 |
| Backend / DBA | `README.md` 全文 -> `docs/keep.summary.md` -> `drills/分階段演練與驗收計畫.md` §0/§2.1 -> 架構書 §4/§6/§8 -> `runbooks/RB-05-mariadb-environment.md` -> ADR-013/015/017 | M6-M10、RB-07 到 RB-09，Pilot 前再讀 |
| QA / Security / DevOps | `README.md` 全文 -> `docs/keep.summary.md` -> `內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md` §3/§7/§8 -> 架構書 §5/§7 -> RB-01/RB-02/RB-03 -> `tasks/README.md` | 架構書 §8 資料模型、`poc/`，W3 前不用 |

| 情境 | Tech Lead / Captain | Backend / DBA | QA / Security / DevOps |
| --- | --- | --- | --- |
| 每日開工 | `drills/每日任務卡排程.md` -> RB-06 -> 今日 dispatch -> 任務卡 | 今日 dispatch -> 任務卡 -> 對應 DB / migration / storage runbook | 今日 dispatch -> 任務卡 -> RB-03 evidence -> 對應 validation/security runbook |
| 建立派工單 | RB-06 -> 每日 roster -> 任務卡 `primary_role` / `closure_reviewer` | 只確認自己是 DRI 或 contributor，不自行改責任歸屬 | 確認 reviewer 不等於 producer，並檢查 evidence 可重現 |
| 任務卡責任 | `primary_role` 是單一 DRI；Captain 只在卡片標示自己時負責 closure | 只對 `primary_role: Backend / DBA` 的卡負 closure | 只對 `primary_role: QA / Security / DevOps` 的卡負 closure |
| Gate / ADR | ADR、Go / No-Go、scope cut、人類決策 | 提供技術證據與風險摘要 | 提供 validator、security、audit、rollback 證據 |
| 找不到方向 | 回到 `docs/keep.summary.md` 與 RB-06 | 回到任務卡 `scopePaths` / `deliverables` | 回到 RB-03 與任務卡 `validators` |

## 情境觸發表

| 遇到的問題 | 先讀 |
| --- | --- |
| 權限、角色、資料範圍不清楚 | 架構書 §5、`TASK-RPT-0014`、`TASK-RPT-0036`、`TASK-RPT-0037` |
| 要動 DB、mapping、MSSQL -> MariaDB | RB-05、ADR-013、功能里程碑 M1、`TASK-RPT-0008` |
| 下載閘道或浮水印設計卡住 | `TASK-RPT-0023`、`TASK-RPT-0024`、`TASK-RPT-0025`、架構書 §6 |
| 想先確認 PoC 輔助流程能不能跑 | `poc/README.md` 的最小 smoke path；結果看 `evidence/MVP2/poc-smoke/validation-result.json` |
| 平行作業差異吵不出結論 | RB-07、ADR-017、`TASK-RPT-0013` |
| evidence 格式或 Gate package 不確定 | RB-03、`drills/分階段演練與驗收計畫.md` §9 |
| 要改共識、scope、ADR 或 Go / No-Go | `docs/keep.summary.md`、`決策紀錄樣板ADR.md`、ChangeLog |
| 每日派工與 AI 回報不知道怎麼寫 | RB-06、`drills/每日任務卡排程.md`、今日任務卡 |
| 風險或 blocker 要升級 | RB-03 risk-blocker-log、RB-06 Weekly Gate Risk Sweep、演練計畫 §0 top-10 風險 |

## 12 步啟動流程

1. 讀本 README 與 `docs/keep.summary.md`。
2. 執行 `git submodule update --init --recursive`，確認 Qutora commit。
3. 依 `runbooks/RB-01-qutora-startup.md` 啟動 Qutora 與 SQL Server。
4. 依 `runbooks/RB-02-seed-data-synthetic-pdf.md` 建立測試 PDF 與 metadata。
5. 依 `runbooks/RB-03-evidence-standard.md` 建 evidence index。
6. 依 `drills/分階段演練與驗收計畫.md` 執行 MVP1。
7. 每日依 `drills/每日任務卡排程.md`、RB-06 與任務卡開工；每人每日親手跑 1 條 hands-on TC，每週五依 RB-06 Demo Day 驗收 4 種最終結果。
8. MVP1 Gate 通過後，依 `runbooks/RB-05-mariadb-environment.md` 建 MariaDB 環境。
9. 依 ADR-018 在 `src/` 以 C# 實作新平台功能（閘道 / 浮水印 / 查詢 / 移植模組）；輔助腳本依 ADR-015 放 `poc/` 與 `tools/`；不改 Qutora 原始碼。
   - 若只想先跑輔助 PoC，依 `poc/README.md` 的最小 smoke path 產出 `evidence/MVP2/poc-smoke/validation-result.json`。
10. Gate 通過後進 Pilot，再收斂 Production Candidate evidence package。
11. 依 RB-04 與 RB-09 驗證 backup / restore / rollback dry run。
12. 最終 Go / No-Go 只能由人類依 ADR 與 Gate evidence 決策。

## 常用命令

```powershell
git submodule update --init --recursive
```
