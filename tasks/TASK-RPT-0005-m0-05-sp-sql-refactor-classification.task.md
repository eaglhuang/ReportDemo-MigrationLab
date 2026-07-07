---
task_id: TASK-RPT-0005
source_milestone: M0-05
title: "建立 SP / SQL 改造分類"
status: planned
owner: project-captain
priority: P0
milestone: M0
drill_stage: "Backlog"
execution_mode: "requires-full-spec-before-start"
depends_on:
  - "TASK-RPT-0002"
  - "TASK-RPT-0004"
related_plan: "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
scopePaths:
  - "tasks/TASK-RPT-*-sp-sql-refactor-classification.task.md"
  - "evidence/M0-05/**"
  - "inventory/**"
  - "decision-records/**"
  - "legacy/舊系統報表模組_功能別005.xxx"
  - "legacy/舊系統資料轉換_SP_功能別005.sql"
deliverables:
  - "evidence/M0-05/implementation-notes.md"
  - "evidence/M0-05/validation-result.md"
  - Target system implementation artifacts: code, DB migration, tests, and operation docs
validators:
  - "git diff --check"
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
- `evidence/M0-05/implementation-notes.md`
- `evidence/M0-05/validation-result.md`

## Validators

- `git diff --check`
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
