---
task_id: TASK-RPT-0044
source_milestone: M10-01
title: "功能驗收"
status: planned
owner: project-captain-qa
priority: P0
milestone: M10
depends_on:
  - "TASK-RPT-0043"
related_plan: "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
scopePaths:
  - "tasks/TASK-RPT-*-release-acceptance.task.md"
  - "evidence/M10-01/**"
  - "acceptance/**"
  - "runbooks/reportdemo/**"
  - "legacy/舊系統報表模組_功能別1001.xxx"
  - "legacy/舊系統資料轉換_SP_功能別1001.sql"
deliverables:
  - "evidence/M10-01/implementation-notes.md"
  - "evidence/M10-01/validation-result.md"
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
  ownerAtomOrMap: "reportdemo.m10.release-acceptance"
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
# TASK-RPT-0044 - M10-01 功能驗收

## Goal

完成 `M10-01` 對應功能，並能證明新系統涵蓋舊系統必要行為；未知舊系統程式碼先以象徵性代號標記，後續盤點時替換為真實名稱。

## Legacy Coverage

- 需對照：`legacy/舊系統報表模組_功能別1001.xxx`
- 需對照：`legacy/舊系統資料轉換_SP_功能別1001.sql`
- 若本卡涉及重寫，必須保留舊系統輸入、輸出、排序、欄位、狀態與例外案例的比對紀錄。

## Functional Scope
- 依功能里程碑計畫完成本項功能交付。

## Implementation Contract

- 優先採漸進式承接：沿用、封裝、移植、重寫、廢止候選需逐項記錄。
- 不得用未脫敏正式資料做一般開發或測試；正式資料只可進受控 Shadow Validation。
- 涉及權限、資料範圍、PDF、稽核、告警或 break-glass 時，安全性與可稽核性優先於便利性。
- 每個可觀測流程需留下 trace ID / correlation ID，方便新舊系統比對與事故追蹤。

- Agent Team 派工、role、reviewer、validator、human sign-off 與 ADR gate 需依 Agent Team 計畫書 v1.0 執行：`內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md`。

## Deliverables

- 實作程式碼、DB migration、設定檔或文件，依本卡 `scopePaths` 控制。
- `evidence/M10-01/implementation-notes.md`
- `evidence/M10-01/validation-result.md`

## Validators

- `git diff --check`
- After target implementation location is created, add: dotnet test or equivalent automated tests
- After target implementation location is created, add: Golden Dataset / Shadow Validation comparison command

## Acceptance Criteria
- 舊系統必要報表範圍已覆蓋。
- Golden Dataset 全案例與 expected result 比對通過。
- 新舊報表雙製比對通過。
- PDF 主檔 Hash 與下載副本 Hash 可追蹤。
- 未授權使用者無法查詢、預覽、下載報表。
- 高機密報表下載需通過額外控管。
- 稽核紀錄完整，且稽核查詢本身有紀錄。
- Critical 事件能在 5 分鐘內通報。
- 批次重跑不會產生重複資料。
- 報表重產不覆蓋舊版。
- 作廢流程需覆核並保留歷史。
- NFR、RTO、RPO、批次完成時間、下載延遲與錯誤率達標或有核准例外。
- 備份還原與 rollback runbook 演練通過。

## Rollback

以 feature flag、路由切回舊系統、回復 migration 或 revert commit 為優先；若已接觸正式流程，必須先確認資料一致性與稽核紀錄完整。

## Notes

- 2026-07-02 | planned | Card generated from the function milestone plan; waiting for human confirmation of priority, owner, and target implementation location path.
- 2026-07-02 | planned | 已同步 Agent Team 計畫書 v1.0；正式派工前需確認 role、reviewer、validator、human/ADR gate 與違規阻擋機制。
