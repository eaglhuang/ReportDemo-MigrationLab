---
task_id: TASK-RPT-0039
source_milestone: M9-01
title: "建立 Shadow DB"
status: planned
owner: project-captain-devops
priority: P0
milestone: M9
drill_stage: "Backlog"
execution_mode: "requires-full-spec-before-start"
depends_on:
  - "TASK-RPT-0004"
  - "TASK-RPT-0005"
  - "TASK-RPT-0018"
related_plan: "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
scopePaths:
  - "tasks/TASK-RPT-*-shadow-db.task.md"
  - "evidence/M9-01/**"
  - "infra/migration/reportdemo/**"
  - "runbooks/reportdemo/**"
  - "legacy/舊系統報表模組_功能別901.xxx"
  - "legacy/舊系統資料轉換_SP_功能別901.sql"
deliverables:
  - "evidence/M9-01/implementation-notes.md"
  - "evidence/M9-01/validation-result.md"
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
  ownerAtomOrMap: "reportdemo.m9.shadow-db"
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
# TASK-RPT-0039 - M9-01 建立 Shadow DB

## Goal

完成 `M9-01` 對應功能，並能證明新系統涵蓋舊系統必要行為；未知舊系統程式碼先以象徵性代號標記，後續盤點時替換為真實名稱。

## Legacy Coverage

- 需對照：`legacy/舊系統報表模組_功能別901.xxx`
- 需對照：`legacy/舊系統資料轉換_SP_功能別901.sql`
- 若本卡涉及重寫，必須保留舊系統輸入、輸出、排序、欄位、狀態與例外案例的比對紀錄。

## Functional Scope
- 保留 MSSQL 作為正式 leader。
- 建立經 PoC 選定的 Shadow DB / follower。
- 透過 CDC、ETL、Outbox 或批次同步將資料寫入 Shadow DB。
- Shadow DB 只做比對與驗證，不影響正式報表結果。

## Implementation Contract

- 優先採漸進式承接：沿用、封裝、移植、重寫、廢止候選需逐項記錄。
- 不得用未脫敏正式資料做一般開發或測試；正式資料只可進受控 Shadow Validation。
- 涉及權限、資料範圍、PDF、稽核、告警或 break-glass 時，安全性與可稽核性優先於便利性。
- 每個可觀測流程需留下 trace ID / correlation ID，方便新舊系統比對與事故追蹤。

- Agent Team 派工、role、reviewer、validator、human sign-off 與 ADR gate 需依 Agent Team 計畫書 v1.0 執行：`內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md`。

## Deliverables

- 實作程式碼、DB migration、設定檔或文件，依本卡 `scopePaths` 控制。
- `evidence/M9-01/implementation-notes.md`
- `evidence/M9-01/validation-result.md`

## Validators

- `git diff --check`
- After target implementation location is created, add: dotnet test or equivalent automated tests
- After target implementation location is created, add: Golden Dataset / Shadow Validation comparison command

## Acceptance Criteria
- 同步錯誤進入 DLQ 或錯誤清單。
- Shadow DB 不影響正式報表產出。
- Shadow DB 的網段隔離、DB 權限、加密、備份、資料保留、存取稽核與 DBA 責任已確認。

## Rollback

以 feature flag、路由切回舊系統、回復 migration 或 revert commit 為優先；若已接觸正式流程，必須先確認資料一致性與稽核紀錄完整。

## Notes

- 2026-07-02 | planned | Card generated from the function milestone plan; waiting for human confirmation of priority, owner, and target implementation location path.
- 2026-07-02 | planned | 已同步 Agent Team 計畫書 v1.0；正式派工前需確認 role、reviewer、validator、human/ADR gate 與違規阻擋機制。
