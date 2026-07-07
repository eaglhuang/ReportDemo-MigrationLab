# ReportDemo Migration Lab Keep Summary

## 文件定位

本文件是本 repo 的 preflight 入口。每次開工前先讀本檔，再依任務 ID、里程碑或操作目的讀對應文件。

本 repo 是「內部人員交易報表轉媒體儲存系統」的遷移演練與治理文件包。它不是一般單一程式碼專案，而是把系統架構、里程碑、任務卡、runbook、evidence 與演練排程集中管理。

## 固定事實

- 舊系統範本：Qutora。
- 舊系統程式碼位置：`open-source-sandbox/qutora-api`。
- 目標資料庫：MariaDB，依 ADR-013。
- PoC 與工具落點：`poc/`、`tools/`，依 ADR-015。
- Evidence 標準：`runbooks/RB-03-evidence-standard.md`。
- 任務卡入口：`tasks/README.md`。

## 文件權威順序

1. `README.md`
2. `docs/keep.summary.md`
3. `docs/daily-execution-plan.md`
4. `內部人員交易報表轉媒體儲存系統_系統架構與治理計畫書.md`
5. `內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md`
6. `決策紀錄樣板ADR.md`
7. `內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md`
8. `tasks/README.md`
9. 對應的 `tasks/TASK-RPT-*.task.md`
10. 對應的 `runbooks/RB-*.md`
11. 對應的 `drills/*.md`
12. `evidence/`
13. `archive/`

`archive/` 只作為歷史背景，不作為目前決策依據。若 archive 與現行文件衝突，以現行文件與 ADR 為準。

## 首讀路線

### 30 分鐘建立地圖

1. 讀 `README.md` 的固定事實、文件權威順序、首讀清單與 12 步執行路線。
2. 讀 `docs/daily-execution-plan.md`，理解每日開工只用靜態手冊，實例落在 evidence，派工格式由 RB-06 維護。
3. 掃讀系統架構與治理計畫書，只抓系統定位、主要模組、資料流程、權限、PDF、稽核、資料模型、風險與驗收。
4. 掃讀功能里程碑計畫，只抓 M0 到 M10 的順序與依賴。
5. 讀 `tasks/README.md`，理解 MVP1、MVP2、Pilot、Production Candidate 四批任務卡。

### 深讀時機

- 要理解整體系統：讀系統架構與治理計畫書。
- 要知道接下來做什麼：讀功能里程碑計畫與 `tasks/README.md`。
- 要開工某張任務卡：讀對應 `TASK-RPT-*`、相關 runbook、相關 evidence 目錄。
- 要指揮 AI 或三人小隊：讀 Agent Team 計畫書、`docs/daily-execution-plan.md`、`drills/AI主導三人併行排程與缺口分析.md`、`runbooks/RB-06-ai-dispatch-cycle.md`。
- 要驗收或交付：讀 `runbooks/RB-03-evidence-standard.md`、`drills/分階段演練與驗收計畫.md`、`drills/每日任務卡排程.md`。

## 任務卡閱讀規則

不要逐張從 TASK-RPT-0001 讀到 TASK-RPT-0045。先從 `tasks/README.md` 判斷任務屬於哪一批：

- MVP1：舊系統盤點、基準、PoC 起點。
- MVP2：MariaDB、Staging、Audit、Data Scope、PDF metadata、下載閘道與浮水印。
- Pilot：新舊驗證、雙製比對、PDF integrity、查詢、稽核、角色與資料範圍。
- Production Candidate：break-glass、Go / No-Go、rollback、UAT、release acceptance、舊系統覆蓋確認。
- Backlog：尚未進入核心演練批次，需確認完整規格與依賴後再開工。

## 隊長決策邊界

AI 可以協助整理、比對、產生候選方案、檢查任務卡、準備 evidence 與 runbook 草稿。

以下事項需要人類或 ADR 簽核：

- 資料庫最終選型或遷移路線變更。
- 舊系統下線與正式 cutover。
- 權限治理、Admin 職責分離與 break-glass 原則變更。
- 稽核保存、PDF 保存、WORM 或 retention policy 變更。
- Golden Dataset 與正式資料使用邊界。
- AI 自動決策範圍擴大。
- MVP 節奏、release gate 或 Go / No-Go 條件變更。

## 開工 Preflight Checklist

1. 讀本檔。
2. 確認 `git status --short`，不可覆蓋既有未歸屬修改。
3. 確認任務 ID、stage、依賴與 evidence path。
4. 讀對應任務卡與 `tasks/README.md`。
5. 讀對應 runbook。
6. 若涉及決策邊界，查 ADR 並停止自動決策。
7. 若涉及文字檔修改，完成後檢查 UTF-8、BOM、U+FFFD 與 mojibake。
