# ReportDemo Migration Lab

本 repo 是「內部人員交易報表轉媒體儲存系統」的遷移演練場，目標是用 Qutora、MariaDB、任務卡、runbook 與 evidence，把舊報表流程逐步驗證到可上線的節奏。

## 文件權威順序

| 順位 | 文件 | 用途 |
| ---: | --- | --- |
| 1 | `README.md` | 全 repo 入口、閱讀路線、角色地圖。 |
| 2 | `docs/keep.summary.md` | 每次開工 preflight 摘要；只有要改共識才讀 `docs/keep.md` 全文。 |
| 3 | `內部人員交易報表轉媒體儲存系統_架構暨功能規格書.md` | 系統範圍、Qutora/MariaDB/PDF/storage/security 規格。 |
| 4 | `內部人員交易報表轉媒體儲存系統_功能階段計畫書.md` | M0 到 M10 里程碑與功能分期。 |
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
5. 收工時把 evidence 與 review 結果回填到派工單與任務卡指定位置。

## 角色新人地圖

| 情境 | Tech Lead / Captain | Backend / DBA | QA / Security / DevOps |
| --- | --- | --- | --- |
| 第一天理解全貌 | `README.md` -> `docs/keep.summary.md` -> 架構規格書 -> 功能階段計畫書 -> ADR | `README.md` -> `docs/keep.summary.md` -> 架構規格書的 DB / migration / PDF metadata 段落 -> ADR-012/013/015 | `README.md` -> `docs/keep.summary.md` -> Agent Team 計畫書 -> `tasks/README.md` -> RB-03/RB-04 |
| 每日開工 | `drills/每日任務卡排程.md` -> RB-06 -> 今日 dispatch -> 任務卡 | 今日 dispatch -> 任務卡 -> 對應 DB / migration / storage runbook | 今日 dispatch -> 任務卡 -> RB-03 evidence -> 對應 validation/security runbook |
| 建立派工單 | RB-06 -> 每日 roster -> 任務卡 `primary_role` / `closure_reviewer` | 只確認自己是 DRI 或 contributor，不自行改責任歸屬 | 確認 reviewer 不等於 producer，並檢查 evidence 可重現 |
| 任務卡責任 | `primary_role` 是單一 DRI；Captain 只在卡片標示自己時負責 closure | 只對 `primary_role: Backend / DBA` 的卡負 closure | 只對 `primary_role: QA / Security / DevOps` 的卡負 closure |
| Gate / ADR | ADR、Go / No-Go、scope cut、人類決策 | 提供技術證據與風險摘要 | 提供 validator、security、audit、rollback 證據 |
| 找不到方向 | 回到 `docs/keep.summary.md` 與 RB-06 | 回到任務卡 `scopePaths` / `deliverables` | 回到 RB-03 與任務卡 `validators` |

## 12 步啟動流程

1. 讀本 README 與 `docs/keep.summary.md`。
2. 執行 `git submodule update --init --recursive`，確認 Qutora commit。
3. 依 `runbooks/RB-01-qutora-startup.md` 啟動 Qutora 與 SQL Server。
4. 依 `runbooks/RB-02-seed-data-synthetic-pdf.md` 建立測試 PDF 與 metadata。
5. 依 `runbooks/RB-03-evidence-standard.md` 建 evidence index。
6. 依 `drills/分階段演練與驗收計畫.md` 執行 MVP1。
7. 每日依 `drills/每日任務卡排程.md`、RB-06 與任務卡開工。
8. MVP1 Gate 通過後，依 `runbooks/RB-05-mariadb-environment.md` 建 MariaDB 環境。
9. 依 ADR-015 在 `poc/` 與 `tools/` 做 MVP2 PoC，不改 Qutora 原始碼。
10. Gate 通過後進 Pilot，再收斂 Production Candidate evidence package。
11. 依 RB-04 與 RB-09 驗證 backup / restore / rollback dry run。
12. 最終 Go / No-Go 只能由人類依 ADR 與 Gate evidence 決策。

## 常用命令

```powershell
git submodule update --init --recursive
```