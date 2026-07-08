---
task_id: TASK-RPT-0005
source_milestone: M0-05
title: "建立 SP / SQL 改造分類"
status: planned
owner: "Tech Lead / Captain"
priority: P0
milestone: M0
drill_stage: "Pilot"
execution_mode: "requires-full-spec-before-start"
evidence_path: "evidence/Pilot/TASK-RPT-0005/"
primary_role: "Tech Lead / Captain"
closure_reviewer: "QA / Security / DevOps"
support_roles:
  - "Backend / DBA"
  - "QA / Security / DevOps"
depends_on:
  - "TASK-RPT-0002"
  - "TASK-RPT-0004"
related_plan: "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
scopePaths:
  - "tasks/TASK-RPT-*-sp-sql-refactor-classification.task.md"
  - "evidence/Pilot/TASK-RPT-0005/**"
  - "inventory/**"
  - "decision-records/**"
  - "legacy/舊系統報表模組_功能別005.xxx"
  - "legacy/舊系統資料轉換_SP_功能別005.sql"
deliverables:
  - "evidence/Pilot/TASK-RPT-0005/qutora-component-conversion-map.md"
  - "evidence/Pilot/TASK-RPT-0005/implementation-notes.md"
  - "evidence/Pilot/TASK-RPT-0005/validation-result.md"
  - Target system implementation artifacts: code, DB migration, tests, and operation docs
validators:
  - "git diff --check"
  - "Get-ChildItem -Directory open-source-sandbox/qutora-api/Qutora.API/Controllers | Measure-Object | Select-Object -ExpandProperty Count # expected: 19"
  - "Select-String -Path open-source-sandbox/qutora-api/Qutora.API/Controllers/*.cs -Pattern '\\[Http(Get|Post|Put|Delete|Patch)' | Measure-Object | Select-Object -ExpandProperty Count # expected: 173"
  - After target implementation location is created, add: dotnet test or equivalent automated tests
  - After target implementation location is created, add: Golden Dataset / Shadow Validation comparison command
evidence:
  required: command-backed
rollback:
  strategy: revert-commit-or-feature-flag-disable
  notes: "若已進入正式資料流程，需先依 rollback runbook 停用新功能並回復舊系統路徑。"
atomizationImpact:
  ownerAtomOrMap: "reportdemo.m0.sp-sql-refactor-classification"
  mapUpdates:
    - After target implementation location is created, add actual module/path map
  notes: "This card defines the functional work package first; add actual module/map and file boundaries after the implementation location is created."
outOfScope:
  - "使用未脫敏正式資料進行開發或一般測試"
  - "未完成舊系統覆蓋比對即切換正式流程"
  - "繞過 Admin、Data Scope、稽核與告警要求"
nonGoals:
  - "一次性重寫所有舊系統功能"
  - "在未完成 PoC / Gate 前承諾最終技術選型"
---
# TASK-RPT-0005 - M0-05 建立 SP / SQL 改造分類

## Goal

完成 `M0-05` 對應功能，並能證明新系統涵蓋舊系統必要行為；未知舊系統程式碼先以象徵性代號標記，後續盤點時替換為真實名稱。

## 2026-07-08 轉換軌重新定義（ADR-018）

本卡解除範圍外裁減，轉換來源具體化為 Qutora ASP.NET 代碼（固定 commit，唯讀）：

- 目標：把 Qutora 的 controllers / services / entities / storage providers / 查詢邏輯，逐項分類為 **沿用（演練期呼叫舊 API）/ 封裝（adapter）/ 移植（port 到 `src/` C#）/ 重寫**，引用功能里程碑 §0 四式。
- 交付物：`evidence/Pilot/TASK-RPT-0005/qutora-component-conversion-map.md`——每列含 Qutora 元件、程式路徑、公開 API / service 行為、分類（沿用 / 封裝 / 移植 / 重寫 / 廢止候選）、理由、對應任務卡或 0009 workstream、DRI、closure reviewer、比對方式；controller 數必須對到 19，endpoint 數必須對到 173。
- 分工：Backend / DBA 以 AI 產分析草稿；Tech Lead / Captain 裁決分類（DRI）；QA / Security / DevOps 驗證分類表可追溯（closure reviewer）。
- W5 檢查點：conversion map 定案時評估工作量；若 AI 背景軌無法在 W9 前完成全移植、173 endpoints 對帳與 Demo Day 第 4 項 P0=0，則依每日排程 §9 觸發 15-17 週 re-baseline。
- 完整規格（10 validators / 10 test cases）依排程於 W4 升級後才可開工。

## Legacy Coverage

- 需對照：`legacy/舊系統報表模組_功能別005.xxx`
- 需對照：`legacy/舊系統資料轉換_SP_功能別005.sql`
- 若本卡涉及重寫，必須保留舊系統輸入、輸出、排序、欄位、狀態與例外案例的比對紀錄。

## Functional Scope
- 將 stored procedure、view、trigger、batch job 分類為保留、封裝、重寫或淘汰。
- 標記 T-SQL、cursor、temp table、transaction、lock、日期函式與排序規則等相容性風險。
- 建立每個 DB 物件的舊系統對照與驗證方式。

## Implementation Contract

- 優先採漸進式承接：沿用、封裝、移植、重寫、廢止候選需逐項記錄。
- 不得用未脫敏正式資料做一般開發或測試；正式資料只可進受控 Shadow Validation。
- 涉及權限、資料範圍、PDF、稽核、告警或 break-glass 時，安全性與可稽核性優先於便利性。
- 每個可觀測流程需留下 trace ID / correlation ID，方便新舊系統比對與事故追蹤。

- Agent Team 派工、role、reviewer、validator、human sign-off 與 ADR gate 需依 Agent Team 計畫書 v1.0 執行：`內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md`。

## Deliverables

- 實作程式碼、DB migration、設定檔或文件，依本卡 `scopePaths` 控制。
- `evidence/Pilot/TASK-RPT-0005/qutora-component-conversion-map.md`
- `evidence/Pilot/TASK-RPT-0005/implementation-notes.md`
- `evidence/Pilot/TASK-RPT-0005/validation-result.md`

## Validators

- `git diff --check`
- `Get-ChildItem -Directory open-source-sandbox/qutora-api/Qutora.API/Controllers | Measure-Object | Select-Object -ExpandProperty Count` must equal 19
- `Select-String -Path open-source-sandbox/qutora-api/Qutora.API/Controllers/*.cs -Pattern '\[Http(Get|Post|Put|Delete|Patch)' | Measure-Object | Select-Object -ExpandProperty Count` must equal 173
- After target implementation location is created, add: dotnet test or equivalent automated tests
- After target implementation location is created, add: Golden Dataset / Shadow Validation comparison command

## Acceptance Criteria
- 每個高風險 DB 物件都有處理策略。
- 重寫項目有預期結果與比對方式。
- 淘汰項目有業務或稽核確認。

## Rollback

以 feature flag、路由切回舊系統、回復 migration 或 revert commit 為優先；若已接觸正式流程，必須先確認資料一致性與稽核紀錄完整。

## Notes

- 2026-07-02 | planned | Card generated from the function milestone plan; waiting for human confirmation of priority, owner, and target implementation location path.
- 2026-07-02 | planned | 已同步 Agent Team 計畫書 v1.0；正式派工前需確認 role、reviewer、validator、human/ADR gate 與違規阻擋機制。
