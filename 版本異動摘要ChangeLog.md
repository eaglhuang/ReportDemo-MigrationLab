# 內部人員交易報表轉媒體儲存系統
## 版本異動摘要 Change Log

## 2026-07-08：新平台技術假設與 Qutora 代碼轉換軌（ADR-018）

範圍：因無法取得真實 ASP.NET 舊系統，以 Qutora 固定 commit 的 ASP.NET 代碼作為轉換來源標的；新平台假設為 HTML5 + .NET server（ASP.NET Core, C#）。已知真實系統進場後會返工，由 `TASK-RPT-0045` 的 `real-aspnet-intake-startup-pack.md` 承接。

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| 對齊 M5-01 下載閘道契約與程式骨架：`TASK-RPT-0023` 前段落地設計同步為 10 態狀態機與完整錯誤碼；`ReportDemo.DownloadGateway` 補 `DownloadStateMachine` 與 transition tests，避免文件 / 代碼漂移。 | `tasks/TASK-RPT-0023-m5-01-download-gateway.task.md`, `src/ReportDemo.DownloadGateway`, `src/ReportDemo.Tests` |
| 補齊 `src/` 工程開工骨架：新增 `ReportDemo.sln`、ASP.NET Core / class library / xUnit test projects、共用 build 設定、最小可測的下載閘道 fail-closed、浮水印 payload、conversion map validator 與 Web health endpoint；`dotnet build` / `dotnet test` 均通過。 | `src/`, `src/README.md`, `tasks/README.md`, `TASK-RPT-0009`, `TASK-RPT-0023`, `TASK-RPT-0024`, `TASK-RPT-0025`, `TASK-RPT-0028` |
| 補齊 ADR-018 收口缺口：keep.summary 同步 `src/` / ADR-018 口徑；每日排程 §6 摘要補入 W4-W9 轉換軌；0005 / 0009 evidence path 收斂到 Pilot 任務卡目錄；0045 升級為 Qutora API / module 全功能覆蓋矩陣、未移植項清單與 `real-aspnet-intake-startup-pack.md` 的收口卡；ADR-016 / 018 追蹤列修正 7 張裁減與具名啟動包。 | `docs/keep.summary.md`, `drills/每日任務卡排程.md`, `TASK-RPT-0005`, `TASK-RPT-0009`, `TASK-RPT-0045`, `決策紀錄樣板ADR.md` |
| 新增 ADR-018「演練新平台技術假設與 Qutora 代碼轉換軌」：HTML5 + ASP.NET Core (C#)、`src/` 落點、轉換深度（核心功能面）、W5 檢查點與 re-baseline 條件；ADR-015 的 Python 降為輔助工具。 | `決策紀錄樣板ADR.md` §21、追蹤表 |
| 新增 `src/` 新平台程式碼落點與模組結構建議（DownloadGateway / Watermark / Documents / Web / Shared）。 | `src/README.md` |
| `TASK-RPT-0005` 解除裁減：目標改為 Qutora 元件改造分類（四式），交付 conversion map；`drill_stage: Pilot`。 | `tasks/TASK-RPT-0005-*.task.md` |
| `TASK-RPT-0009` 解除裁減：承接 conversion map 殘餘模組的 C# 移植（document CRUD / categories），每模組附雙製比對 evidence；`drill_stage: Pilot`。 | `tasks/TASK-RPT-0009-*.task.md` |
| 每日排程 §8 範圍外清單由 9 張改為 7 張，0005 / 0009 移入轉換軌並註明落點；W4D2 / W4D5 / W5D5 / W7D2 / W8D4 / W9D1 插入轉換軌併行工作與 W5 檢查點。 | `drills/每日任務卡排程.md` §5、§8 |
| MVP v1 Must Do 加入轉換軌；Stage 對照表 Pilot 列加入 0005 / 0009。 | `drills/分階段演練與驗收計畫.md` §0、§3 |
| Pilot 核心卡批次加入 0005 / 0009；Drill Plan Contract 加 ADR-018 邊界。 | `tasks/README.md` |
| 0023 / 0024 / 0025 / 0028 scopePaths 加入 `src/**`（C# 實作計入轉換軌）。 | 對應任務卡 |
| README 文件邊界表加入轉換軌一列；12 步流程第 9 步改為 `src/` C# 實作。 | `README.md` |
| `poc/` 降為輔助工具落點聲明。 | `poc/README.md` |

本次未執行：不修改 Qutora 原始碼、不展延 12+2 baseline（由 W5 檢查點決定是否 re-baseline）、不取代 ADR-001 / ADR-007 正式選型、不宣稱 Qutora 轉換等價於真實券商系統轉換。

# 2026-07-08 - 文件必要性審查、12+2 定義與落地缺口原地補強

本次依馬斯克五步驟先做必要性審查：不新增 MVP 閱讀總包，也不新增 ownership map。可承載的缺口一律補回既有 source of truth。

| 缺口 | 處理方式 | 文件 |
| --- | --- | --- |
| README 入口品質硬傷 | 修正不存在檔名引用、去除日期化章節，補角色章節級閱讀路線與情境觸發表 | `README.md`, `docs/keep.summary.md` |
| docs / drills 分工不清 | 補 README、keep.summary、每日 roster 的邊界說明 | `README.md`, `docs/keep.summary.md`, `drills/每日任務卡排程.md` |
| 12 週與 14 週誤解 | 統一定義為 `12+2`：12 週 baseline，+2 是 buffer，不是開發期 | `README.md`, `docs/keep.summary.md`, `drills/分階段演練與驗收計畫.md`, `drills/每日任務卡排程.md` |
| 第一版 MVP 可落地範圍與 10 項剛需對照 | 補到階段演練文件，不另開總包 | `drills/分階段演練與驗收計畫.md` |
| M5-01 下載閘道 API / tables / state / error / fail-closed | 補回 M5-01 任務卡 | `tasks/TASK-RPT-0023-m5-01-download-gateway.task.md` |
| M5-02 浮水印欄位、主副本流程、Hash 時點、失敗與效能 | 補回 M5-02 任務卡 | `tasks/TASK-RPT-0024-m5-02-dynamic-watermark.task.md` |
| MSSQL -> MariaDB 改造點、風險、驗證、回復 | 補回 MariaDB runbook | `runbooks/RB-05-mariadb-environment.md` |
| P0-P3 風險語言不統一 | 補全域 finding 嚴重度字典與 risk-blocker-log 慣例 | `runbooks/RB-03-evidence-standard.md` |
| RB-07 平行作業差異分類需對齊全域字典 | 補註明 P0-P3 以 RB-03 為準，RB-07 只保留特化例子 | `runbooks/RB-07-parallel-run-operations.md` |
| 每日 blocker 缺少聚合落點 | 補 EOD 入簿規則與週五 Gate risk sweep | `runbooks/RB-06-ai-dispatch-cycle.md` |
| 任務卡狀態生命週期未定義 | 補 `planned -> in-progress -> blocked -> done / exception` 規則 | `tasks/README.md` |
| 三人小隊缺席替補未定義 | 補代理順序與 producer / reviewer 限制 | `drills/分階段演練與驗收計畫.md` |
| 一般性排程漂移未定義 | 補 >=3 天 re-baseline 與 >=5 天 fallback 評估規則 | `drills/每日任務卡排程.md` |
| 第 8 項風險與取捨缺少靜態 top-10 表 | 補前 10 大落地風險與取捨，並修正 §0 對照表指向 | `drills/分階段演練與驗收計畫.md` |
| ChangeLog 檔頭順序錯位 | 將文件主標題移回第 1 行 | `版本異動摘要ChangeLog.md` |

# 2026-07-07 - 文件瘦身、DRI 收斂與 TASK-RPT-0004 workstream

範圍：移除重複每日作戰手冊、封存過渡分析文件，將每日協作固定為 README / keep.summary / 每日 roster / RB-06 / 任務卡的單一路線。

| 變更 | 影響文件 |
| --- | --- |
| 刪除 `docs/daily-execution-plan.md`；每日六步驟、派工單格式、AI 回報、review 與 EOD 統一由 RB-06 維護。 | `runbooks/RB-06-ai-dispatch-cycle.md` |
| 封存 AI 主導三人併行排程分析；其有效規則已收斂到 ADR-016、RB-06 與每日任務卡排程。 | `archive/AI主導三人併行排程與缺口分析.md` |
| README 新增三角色新人地圖與每日閱讀路線，不另開 ownership map 文件。 | `README.md` |
| `primary_role` 正式定義為單一 DRI，新增 `closure_reviewer`；AI 不得擔任 DRI 或 closure reviewer。 | `tasks/README.md`、`tasks/TASK-RPT-*.task.md`、`tools/generate_reportdemo_task_cards.py` |
| `TASK-RPT-0004` 保留為母任務卡，新增 0004a/0004b/0004c 卡內 workstream 與 evidence 命名；不建立正式子任務卡。 | `tasks/TASK-RPT-0004-m0-04-third-party-cross-platform-poc.task.md`、`evidence/MVP1/daily-dispatch-*.md` |
## 2026-07-07：每日作戰手冊與 preflight 入口註冊

範圍：收斂每日開工入口，將 `docs/keep.summary.md` 與 `docs/daily-execution-plan.md` 納入文件權威順序；每日派工格式仍由 RB-06 單一維護，避免每日模板雙軌。

| 異動 | 併入文件 / 章節 |
| --- | --- |
| 新增 `docs/keep.summary.md` 作為 AI 與人類開工 preflight 入口，整理固定事實、閱讀順序、任務卡閱讀規則與隊長決策邊界。 | `docs/keep.summary.md` |
| 新增 `docs/daily-execution-plan.md` 作為每日開工靜態作戰手冊；每日實例規定落在 `evidence/<Stage>/daily-dispatch-YYYY-MM-DD.md`，不寫回計畫檔。 | `docs/daily-execution-plan.md` |
| RB-06 的每日派工單格式補上 Main task、Today outcome、Evidence path 欄位，維持每日派工格式唯一 owner。 | `runbooks/RB-06-ai-dispatch-cycle.md` |
| README 權威順序、三人首讀清單與 12 步路線註冊 docs 入口，明確區分新進入口、preflight 入口與每日開工入口。 | `README.md` |

本次未執行：不新增自動化抽取腳本；先手動跑每日格式，穩定後再自動化。

## 2026-07-07：AI 主導三人併行排程補充

範圍：加入「三人皆具 AI 開發環境、AI 主開發、人類監控決策與驗收、每日 8 小時、週末不工作」的排程前提，並將 Production Candidate 演練的 Base Plan 重估為 12 到 14 週。

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| 新增 ADR-017，將演練並行期間基準方定為 Qutora，退出條件定為連續 N=3 批次或 3 工作日通過，作為 RB-07 與 W9 Pilot Gate 前提。 | `決策紀錄樣板ADR.md` §20 |
| 新增 RB-07 平行作業運轉細則，定義每日平行作業節奏、差異分類字典、accept / reject 判準、SLA 與退出條件。 | `runbooks/RB-07-parallel-run-operations.md` |
| 新增 RB-08 cutover runbook，定義凍結點、最終同步、checksum、smoke test、hypercare 與回退判斷。 | `runbooks/RB-08-cutover-runbook.md` |
| 新增 RB-09 備份與回復政策，定義備份範圍、保留、驗證頻率、DR 情境分級與事故應變一頁決策樹。 | `runbooks/RB-09-backup-recovery-policy.md` |
| RB-01 / RB-05 補上 Teardown，避免 container、volume 或合成資料污染下一輪演練。 | `runbooks/RB-01-qutora-startup.md`、`runbooks/RB-05-mariadb-environment.md` |
| Pilot 測試補上大檔 PDF 效能測法，要求 streaming hash、下載閘道、耗時、記憶體與 fail-closed evidence。 | `drills/分階段演練與驗收計畫.md` TC-PILOT-08 |
| 任務卡 scopePaths 補上 RB-07 / RB-08 / RB-09，讓平行作業、Go / No-Go、Rollback、舊系統下線 Gate 開卡時能找到操作依據。 | `TASK-RPT-0013`、`0040`、`0041`、`0043` |
| 新增每日任務卡排程，將 14 週 Base Plan 拆成每週 5 天、每天 3 人各至少 1 張主責任務卡；每格包含任務卡 ID、當日目標、操作步驟與下班驗收。 | `drills/每日任務卡排程.md` |
| 每日排程明確標出新舊平行作業驗證、上線驗證、緊急備份回復措施、break-glass 與舊系統下線 Gate 的週次落點與不可壓縮條件。 | `drills/每日任務卡排程.md` §7 |
| README、分階段演練計畫與 AI 主導排程文件新增每日 roster 引用，避免只停留在週級排程。 | `README.md`、`drills/分階段演練與驗收計畫.md`、`drills/AI主導三人併行排程與缺口分析.md` |
| 新增 AI 主導三人併行排程與缺口分析，定義 `[AI]`、`[AI->HUMAN]`、`[HUMAN]`、`[GATE]` 標籤、Best/Base/Risk 三段時程、14 週排程、每日節奏與缺口清單。 | `drills/AI主導三人併行排程與缺口分析.md` |
| 新增 AI 派工循環 runbook，定義每日派工單、AI 回報格式、review checklist、blocker 升級、週末規則與 end-of-day checklist。 | `runbooks/RB-06-ai-dispatch-cycle.md` |
| README 補上新排程文件的權威順序、首讀清單與 12 步路線引用。 | `README.md` |
| 分階段演練計畫補上 AI 主導排程前提與 12-14 週 Base Plan / 16-18 週 fallback 說明。 | `drills/分階段演練與驗收計畫.md` §2、§2.0 |
| tasks README 補上 `execution_mode` 與 AI / HUMAN / GATE 標籤規則。 | `tasks/README.md` |
| 45 張任務卡新增 `execution_mode` frontmatter；核心卡標記 `ai-with-human-review` 或 `human-only`，Backlog 標記 `requires-full-spec-before-start`。 | `tasks/TASK-RPT-*.task.md` |
| 新增「演練範圍外任務卡與例外處理」：顯式列出 9 張不排入 14 週演練的任務卡（0005、0006、0009、0026、0027、0029-0032）與裁減理由；W14 驗收一律記為 documented exception 並彙整 next-phase recommendation；0027 高機密控制的裁減需於 W12 sign-off-record 的 conditions 欄顯式記載，缺此記載不得做出 conditional-go 以上結論。 | `drills/每日任務卡排程.md` §8、`TASK-RPT-0044`、`TASK-RPT-0045`、`決策紀錄樣板ADR.md` ADR-016 追蹤列 |
| Agent Team 計畫書補上 AI 主導三人模式與不可越界邊界。 | `內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md` §2.1 |
| 新增 ADR-016，接受本演練採 AI 主導三人併行模式，但 human / ADR gate 不得被 AI 取代。 | `決策紀錄樣板ADR.md` §19 |
| RB-03 / RB-04 補上 AI producer、人類 reviewer、不得自審、rollback / break-glass 不可委派邊界。 | `runbooks/RB-03-evidence-standard.md`、`runbooks/RB-04-rollback-rehearsal.md` |
| RB-01 / RB-02 / RB-05 補上 AI 可執行但需人類驗收的檔頭說明；MVP1 evidence index 範本補上 AI producer / human reviewer 規則。 | `runbooks/RB-01-qutora-startup.md`、`runbooks/RB-02-seed-data-synthetic-pdf.md`、`runbooks/RB-05-mariadb-environment.md`、`evidence/MVP1/.index-template.md` |
| 產卡模板同步新增 `execution_mode` 與 ADR-016 / RB-06 引用，避免未來重產卡遺失 AI 主導治理欄位。 | `tools/generate_reportdemo_task_cards.py` |

本次未執行：不把 Best Case 8 到 10 週作為正式承諾、不移除原穩健演練 Gate、不讓 AI 取代 human / ADR gate、不修改 Qutora submodule。

## 2026-07-07：執行層 Day 1 缺口補齊

範圍：補齊三人小隊 Day 1 可執行與 MVP2 可落地的缺口，包含 Qutora `.env` / `--env-file` 啟動方式、MariaDB 演練環境、PoC 程式碼落點、合成 PDF 工具、evidence index 範本、Qutora 能力 fallback、MVP 兩週節奏與任務卡 scopePaths。

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| Qutora 啟動 runbook 補上 sample `.env` 建立方式、`--env-file` compose 指令、API / Swagger / SQL Server 存取資訊與敏感資訊遮罩規則。 | `runbooks/RB-01-qutora-startup.md` |
| 新增 MariaDB 演練環境 runbook、compose 與 env 範本，定義 MariaDB 11.4、`utf8mb4`、dump / restore 與失敗處理。 | `runbooks/RB-05-mariadb-environment.md`、`runbooks/docker-compose.mariadb.yml`、`runbooks/env.mariadb.example` |
| 新增 ADR-015，固定本演練 PoC 技術棧與程式碼落點，明確限制不得修改 Qutora 原始碼。 | `決策紀錄樣板ADR.md` §18 |
| 新增 `poc/` 目錄與 MVP2 子目錄，作為下載閘道、浮水印、migration 與 validators PoC 落點。 | `poc/README.md`、`poc/download-gateway/`、`poc/watermark/`、`poc/migration/`、`poc/validators/` |
| 新增合成 PDF 產生工具，輸出 PDF、metadata export 與 baseline hash，支援 RB-02 與 MVP1 evidence。 | `tools/generate_synthetic_pdf.py`、`runbooks/RB-02-seed-data-synthetic-pdf.md` |
| Evidence 標準補上 MVP1 index template 引用；新增 MVP1 evidence index 範本。 | `runbooks/RB-03-evidence-standard.md`、`evidence/MVP1/.index-template.md` |
| 演練計畫補上 MVP1 / MVP2 週節奏、Qutora 能力限制 fallback 規則、CI 與命令型 evidence 定位、ADR-015 PoC 落點。 | `drills/分階段演練與驗收計畫.md` §2.1、§4.4、§5.1、§6 |
| README 的三人首讀清單與 12 步路線補上 RB-05 與 ADR-015。 | `README.md` |
| MVP2 核心任務卡 scopePaths 補上 RB-05、`poc/` 與 validators 落點。 | `tasks/TASK-RPT-0008`、`0019`、`0023`、`0024`、`0025` |
| 產卡模板補上 RB-05、ADR-015 與 `poc/`，避免未來重新產卡遺失演練落點規則。 | `tools/generate_reportdemo_task_cards.py` |

本次未執行：不修改 Qutora submodule、不啟動 migration、不重新產 PDF、不把 PoC 技術棧推論為正式上線技術棧。

## 2026-07-07：收斂落地複查缺口補齊

範圍：補齊複查列出的 5 個殘餘缺口，使 MVP1 kickoff 前需要的責任矩陣、簽核邊界、Phase↔M 權威、admin 初始化、Backlog 任務卡標記與 Production Candidate 簽核範本都有文件依據。

| 缺口 | 修正內容 | 併入文件 |
| --- | --- | --- |
| 三人每階段責任矩陣與代理簽核表未落表 | 新增每階段責任矩陣、代理簽核表與 Gate Review 規則，明確定義誰驗收、誰不得自審、哪些 Gate 只能建議不可代理正式簽核。 | `drills/分階段演練與驗收計畫.md` §4.1、§4.2、§4.3 |
| 架構書附錄 A 與功能里程碑 Phase↔M 對照表重複 | 刪除架構書附錄 A 的重複 Phase↔M 表格，只保留治理路線與指向「功能里程碑計畫」的權威說明。 | `內部人員交易報表轉媒體儲存系統_系統架構與治理計畫書.md` 附錄 A |
| RB-01 admin 初始化不具體 | 補上 Qutora `system-status`、`initial-setup`、`login` 的 curl.exe 命令、預期結果與 token / 密碼遮罩要求。 | `runbooks/RB-01-qutora-startup.md` |
| 非核心任務卡缺少 `drill_stage: Backlog` | 17 張非核心任務卡補上 `drill_stage: "Backlog"`，並在 tasks README 明確標示未補齊不得開工。 | `tasks/TASK-RPT-0005`、`0006`、`0009`、`0011`、`0012`、`0015`、`0016`、`0017`、`0020`、`0026`、`0027`、`0029`、`0030`、`0031`、`0032`、`0034`、`0039`、`tasks/README.md` |
| PC 正式簽核表無範本 | 新增 `ProductionCandidate` sign-off record 格式與 Markdown 範本。 | `runbooks/RB-03-evidence-standard.md` |

## 2026-07-07：Pilot 與 Production Candidate 核心任務卡完整格式升級

範圍：升級第三批 Pilot 核心任務卡 `TASK-RPT-0013`、`TASK-RPT-0018`、`TASK-RPT-0021`、`TASK-RPT-0022`、`TASK-RPT-0028`、`TASK-RPT-0033`、`TASK-RPT-0035`、`TASK-RPT-0036`、`TASK-RPT-0037`，以及第四批 Production Candidate 核心任務卡 `TASK-RPT-0038`、`TASK-RPT-0040`、`TASK-RPT-0041`、`TASK-RPT-0042`、`TASK-RPT-0043`、`TASK-RPT-0044`、`TASK-RPT-0045`。這 16 張卡已補齊 Qutora 演練場景、落地設計、影響範圍、Fail-Closed 規則、10 條 validators、10 條 test cases、reviewer / human gate / ADR gate。

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| Pilot 批次補齊新舊驗證、雙製比對、PDF 主檔完整性、PDF reconciliation、報表查詢、稽核 Hash Chain、告警路由、角色管理與 Data Scope 管理任務卡。 | `tasks/TASK-RPT-0013`、`0018`、`0021`、`0022`、`0028`、`0033`、`0035`、`0036`、`0037` |
| Production Candidate 批次補齊 break-glass、Go / No-Go、Rollback、UAT、Pilot 舊系統下線、Release Acceptance 與舊系統覆蓋確認任務卡。 | `tasks/TASK-RPT-0038`、`0040`、`0041`、`0042`、`0043`、`0044`、`0045` |
| `tasks/README.md` 更新第三批與第四批核心卡狀態，標示已升級為完整任務卡。 | `tasks/README.md` |
| 產卡模板補強完整任務卡 frontmatter、stage、role、evidence 與 gate 欄位要求，避免未來重產卡退回摘要格式。 | `tools/generate_reportdemo_task_cards.py` |

## 2026-07-07：MVP2 核心任務卡完整格式升級

範圍：升級 MVP2 第二批核心任務卡 `TASK-RPT-0007`、`TASK-RPT-0008`、`TASK-RPT-0010`、`TASK-RPT-0014`、`TASK-RPT-0019`、`TASK-RPT-0023`、`TASK-RPT-0024`、`TASK-RPT-0025`。這批卡已補齊真實 Qutora 演練場景、落地設計、影響範圍、Fail-Closed 規則、10 條 validators、10 條 test cases、reviewer / human gate / ADR gate，evidence 路徑統一為 `evidence/MVP2/<TASK-ID>/`。

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| `TASK-RPT-0007` 補齊匯入批次管理規格，包含批次狀態機、錯誤碼、rollback 與 Qutora 抽取邊界。 | `tasks/TASK-RPT-0007-m1-01-import-batch-management.task.md` |
| `TASK-RPT-0008` 補齊 MariaDB staging tables 規格，包含 staging schema、欄位對應、索引與驗證規則。 | `tasks/TASK-RPT-0008-m1-02-staging-tables.task.md` |
| `TASK-RPT-0010` 補齊 audit write foundation 規格，包含 fail-closed matrix、audit event schema 與 payload hash。 | `tasks/TASK-RPT-0010-m1-04-audit-write-foundation.task.md` |
| `TASK-RPT-0014` 補齊 Data Scope foundation 規格，包含 Role / Data Scope / Confidentiality deny-by-default 規則。 | `tasks/TASK-RPT-0014-m2-04-data-scope-foundation.task.md` |
| `TASK-RPT-0019` 補齊 PDF metadata 規格，包含 Qutora metadata 對應、主檔 Hash、機密等級與版本欄位。 | `tasks/TASK-RPT-0019-m4-01-pdf-metadata.task.md` |
| `TASK-RPT-0023` 補齊下載閘道落地設計，包含 API、資料表、狀態機、錯誤碼、權限檢查、稽核欄位與 fail-closed 規則。 | `tasks/TASK-RPT-0023-m5-01-download-gateway.task.md` |
| `TASK-RPT-0024` 補齊動態浮水印處理規格，明確定義浮水印為外流追蹤、嚇阻與竄改偵測輔助，不宣稱絕對防竄改。 | `tasks/TASK-RPT-0024-m5-02-dynamic-watermark.task.md` |
| `TASK-RPT-0025` 補齊下載副本 Hash 規格，區分主檔 Hash、下載副本 Hash 與 audit payload hash。 | `tasks/TASK-RPT-0025-m5-03-download-copy-hash.task.md` |
| `tasks/README.md` 更新第二批核心卡狀態，標示 MVP2 核心卡已升級為完整任務卡。 | `tasks/README.md` |

## 2026-07-06：MVP1 核心任務卡完整格式升級

範圍：只升級 MVP1 第一批核心任務卡 `TASK-RPT-0001` 到 `TASK-RPT-0004`。其他任務卡仍維持摘要格式，未補齊完整任務卡規格前不得正式開工或 closure。

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| `TASK-RPT-0001` 補齊 Qutora 文件 / 報表功能盤點、真實場景、影響範圍、10 條 validators、10 條 test cases、reviewer / human gate / ADR。 | `tasks/TASK-RPT-0001-m0-01-legacy-report-inventory.task.md` |
| `TASK-RPT-0002` 補齊 Qutora DB / entity / provider 資料來源盤點、MariaDB 轉換風險、10 條 validators、10 條 test cases。 | `tasks/TASK-RPT-0002-m0-02-legacy-data-source-inventory.task.md` |
| `TASK-RPT-0003` 補齊 Golden Dataset / 合成 PDF / metadata / hash baseline 規格與正式資料禁用 gate。 | `tasks/TASK-RPT-0003-m0-03-legacy-result-baseline.task.md` |
| `TASK-RPT-0004` 補齊 Qutora startup、DB provider、PDF / storage / auth PoC 規格與 MVP2 前置 Gate。 | `tasks/TASK-RPT-0004-m0-04-third-party-cross-platform-poc.task.md` |
| 四張核心卡 evidence 統一改為 `evidence/MVP1/TASK-RPT-000x/`。 | `tasks/TASK-RPT-0001` 到 `TASK-RPT-0004` |

## 2026-07-06：計畫文件包收斂與演練執行層重整

範圍：文件包治理、演練計畫合併、runbook 新增、evidence 規則、任務卡開工 gate 與 archive 封存。不修改 Qutora submodule、不跑 migration、不重新產 PDF、不一次升級全部 45 張任務卡。

## 新增

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| 新增唯一演練執行指南，合併 MVP1、MVP2、Pilot、Production Candidate、三人責任矩陣與 Gate 總表。 | `drills/分階段演練與驗收計畫.md` |
| 新增 Qutora 啟動 runbook。 | `runbooks/RB-01-qutora-startup.md` |
| 新增合成 PDF 與 metadata runbook。 | `runbooks/RB-02-seed-data-synthetic-pdf.md` |
| 新增 evidence 命名、驗收與 Gate package 標準。 | `runbooks/RB-03-evidence-standard.md`、`evidence/README.md` |
| 新增 rollback dry run runbook。 | `runbooks/RB-04-rollback-rehearsal.md` |
| 新增 evidence stage 骨架。 | `evidence/MVP1/`、`evidence/MVP2/`、`evidence/Pilot/`、`evidence/ProductionCandidate/` |
| 新增核心任務卡分批升級清單與 Stage 對照。 | `tasks/README.md` |

## 修改

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| README 改為唯一入口，吸收原演練文件索引的文件權威順序、三人首讀清單與 12 步路線。 | `README.md` |
| 《系統架構與治理計畫書》附錄 A 改為治理路線，細節指向功能里程碑與分階段演練計畫；附錄 C 補註本演練依 ADR-013 固定 MariaDB。 | `內部人員交易報表轉媒體儲存系統_系統架構與治理計畫書.md` 附錄 A / C |
| 《功能里程碑計畫》補充唯一 Phase↔M 對照與演練執行層引用。 | `內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md` §0 |
| Agent Team 計畫書補明與 README、分階段演練計畫、tasks README、任務卡與 runbooks 的引用關係；派工範例標示為非規範性。 | `內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md` |
| ADR-012、ADR-013、ADR-014 的影響範圍更新為新的單一演練計畫與 runbooks。 | `決策紀錄樣板ADR.md` |
| 產卡模板補上 Stage、角色、evidence 與完整任務卡 gate 欄位。 | `tools/generate_reportdemo_task_cards.py` |

## 刪除、封存或取代

| 舊文件 / 舊說法 | 新位置 / 取代方式 |
| --- | --- |
| `drills/演練總計畫書.md` | 已移入 `archive/`；有效內容併入 `drills/分階段演練與驗收計畫.md`。 |
| `drills/MVP1兩週風險驗證計畫.md` | 已移入 `archive/`；有效內容併入 `drills/分階段演練與驗收計畫.md` 的 MVP1 章節。 |
| `drills/MVP2兩週調整驗證計畫.md` | 已移入 `archive/`；有效內容併入 `drills/分階段演練與驗收計畫.md` 的 MVP2 章節。 |
| `drills/Pilot與平行作業驗證計畫.md` | 已移入 `archive/`；有效內容併入 `drills/分階段演練與驗收計畫.md` 的 Pilot 章節。 |
| `drills/上線候選與Rollback計畫.md` | 已移入 `archive/`；有效內容併入 `drills/分階段演練與驗收計畫.md` 與 `runbooks/RB-04-rollback-rehearsal.md`。 |
| `drills/演練文件索引與引用關係.md` | 已移入 `archive/`；權威順序改由 `README.md` 維護。 |
| `drills/演練版本異動摘要ChangeLog.md` | 已移入 `archive/`；根目錄 `版本異動摘要ChangeLog.md` 為唯一 active ChangeLog。 |
| 根目錄三份 PDF 快照 | 已移入 `archive/`；Markdown 穩定後再視需要重新產 PDF。 |
| 「每份 drills 文件各自維護 Gate」 | 已 superseded。Gate 統一維護於 `drills/分階段演練與驗收計畫.md`。 |

## 改列 ADR 或人類簽核

| 事項 | 規則 |
| --- | --- |
| 修改 Qutora 原始碼 | 需另開 ADR 或人類簽核；本輪不修改。 |
| 變更 MariaDB 作為本演練目標 DB | 需更新 ADR-013。 |
| 任務卡未具備完整規格仍要開工 | 需 human sign-off；預設不得開工。 |
| Production Candidate 進入正式 Go / No-Go | 需業務、稽核、資安、維運與 Tech Lead 共同簽核。 |

## 2026-07-03：演練文件群與 Qutora 舊系統定義

本次新增 `drills/` 演練文件群，並將 Qutora 直接定義為本演練舊系統。原獨立 Qutora 對照表已刪除，內容併入演練總計畫與 MVP1 兩週風險驗證計畫。2026-07-06 後，本 repo 的唯一 active ChangeLog 為本文件；原 `drills/演練版本異動摘要ChangeLog.md` 已封存。

| 異動 | 併入文件 / 章節 |
| --- | --- |
| 新增演練總計畫、MVP1、MVP2、Pilot、上線候選計畫、演練文件索引與演練 ChangeLog。 | `drills/` |
| 新增 ADR-012「本演練舊系統採用 Qutora」、ADR-013「本演練目標資料庫採用 MariaDB」、ADR-014「兩週 MVP 節奏與完整任務卡開工 Gate」。 | `決策紀錄樣板ADR.md` |
| README 與 tasks README 改為直接定義 Qutora 為本演練舊系統。 | `README.md`、`tasks/README.md` |
| 原獨立 Qutora 對照表已 superseded 並刪除。 | 內容已併入 `drills/分階段演練與驗收計畫.md` 與 `runbooks/RB-01-qutora-startup.md`。 |

## 2026-07-02：Agent Team 文件升版批次

本次新增 Agent Team 計畫書 v1.0，並將三份核心文件、任務卡 README、45 張任務卡與產卡模板同步到同一套 Agent Team 協作與簽核邊界。PDF 不在本次更新範圍，`tasks.zip` 也不重新打包。

## 新增

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| 新增《Agent Team 計畫書 v1.0》，定義本任務 Agent Team 協作 source of truth。 | `內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md` |
| 新增 Agent 角色：Captain / Coordinator、Implementer、Security / Permission、Audit / Evidence、QA / Security / DevOps、Reviewer。 | Agent Team 計畫書 §3 |
| 新增 M5-01 下載閘道與 M5-02 動態浮水印的 Agent 派工範例。 | Agent Team 計畫書 §4、§5 |
| 新增 Agent 違規阻擋機制：任務卡 scope、Permission Broker、lease / fencing、tool sandbox、validator / reviewer、closure gate。 | Agent Team 計畫書 §8 |
| 新增 ADR-011「Agent Team 自動決策、人類簽核與違規阻擋邊界」。 | `決策紀錄樣板ADR.md` §14 |
| 新增本 Change Log 文件，供各計畫書引用。 | `版本異動摘要ChangeLog.md` |

## 修改

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| 《系統架構與治理計畫書》由 v1.3 升版為 v1.4。 | `系統架構與治理計畫書.md` 標題 |
| 加入文件權威順序：架構以系統架構文件為準，Agent Team 協作以 Agent Team 計畫書為準，功能拆解以功能里程碑與任務卡為準，決策以 ADR 為準。 | `系統架構與治理計畫書.md` §1 |
| 新增 Agent Team 相關附錄，說明協作、違規阻擋與簽核邊界。 | `系統架構與治理計畫書.md` 附錄 H |
| 《功能里程碑計畫》由 v1.0 升版為 v1.1。 | `功能里程碑計畫.md` 標題 |
| 第 0 章新增任務卡派工需依 Agent Team 計畫書 v1.0。 | `功能里程碑計畫.md` §0 |
| M5、M7、M8、M9 的驗收補強 reviewer、human sign-off 與 ADR gate 引用。 | `功能里程碑計畫.md` M5 / M7 / M8 / M9 |
| 《ADR / 決策紀錄》由 v1.0 升版為 v1.1，Top 10 擴充為 Top 11。 | `決策紀錄樣板ADR.md` §3、§15 |
| `tasks/README.md` 新增 Agent Team 派工契約。 | `tasks/README.md` |
| 45 張 `TASK-RPT-*` 任務卡新增 `agent_team_plan` frontmatter 與統一 Implementation Contract。 | `tasks/TASK-RPT-*.task.md` |
| 產卡模板同步新增 Agent Team 引用，避免重新產卡時遺失。 | `tools/generate_reportdemo_task_cards.py` |

## 刪除或取代

| 舊說法 / 舊假設 | 新說法 / 取代方式 |
| --- | --- |
| 「人類原則上不需要介入」 | 已 superseded。改為「隊長 AI 可自動處理低風險、可回復、已有規則的執行決策；資安、稽核、資料、正式切換與架構決策必須人類或 ADR 簽核」。 |
| Agent Team may depend on an external codebase or existing Team Agents runtime. | Superseded. Agent Team rules are governed by this simulation project documents and do not depend on external codebase/runtime. |
| 任務卡只列 validators，未明確要求 Agent role / reviewer / human gate。 | 已取代。任務卡與 README 需檢查 role、reviewer、validator、human sign-off 與 ADR gate。 |

## 改列 ADR 或人類簽核

下列事項不得由 Agent Team 自動決定，需人類簽核或 ADR：

* DB 最終選型與 Shadow DB 升格主庫。
* 舊系統正式基準、並行期限與下線條件。
* AD / LDAPS / OIDC / SAML、API session、MFA 與 signed URL 策略。
* PDF library 商用授權、數位簽章、timestamp 與 PDF 長期驗證需求。
* Golden Dataset 與正式資料 Shadow Validation 使用邊界。
* 權限模型、Admin 職責分離、Data Scope 與 break-glass。
* 稽核 fail-closed、hash chain 範圍、WORM / immutable 保存。
* Object Storage、NAS、WORM 與保存年限。
* Pilot、Go / No-Go、rollback window 與舊系統下線。
