---
task_id: TASK-RPT-0009
source_milestone: M1-03
title: "移植或重寫舊資料轉換邏輯"
status: planned
owner: "Backend / DBA"
priority: P0
milestone: M1
drill_stage: "Pilot"
execution_mode: "requires-full-spec-before-start"
evidence_path: "evidence/Pilot/TASK-RPT-0009/"
primary_role: "Backend / DBA"
closure_reviewer: "Tech Lead / Captain"
support_roles:
  - "Tech Lead / Captain"
  - "QA / Security / DevOps"
workstreams:
  - id: "0009a"
    title: "Documents CRUD / versioning 移植"
    dri: "Backend / DBA"
    closure_reviewer: "Tech Lead / Captain"
  - id: "0009b"
    title: "Approval 工作流移植（Qutora 5 個 Approval services）"
    dri: "Backend / DBA"
    closure_reviewer: "QA / Security / DevOps"
  - id: "0009c"
    title: "Shares + Email 通知移植"
    dri: "Backend / DBA"
    closure_reviewer: "QA / Security / DevOps"
  - id: "0009d"
    title: "Admin / Settings / ApiKeys 殘餘移植"
    dri: "Backend / DBA"
    closure_reviewer: "Tech Lead / Captain"
depends_on:
  - "TASK-RPT-0005"
  - "TASK-RPT-0008"
related_plan: "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
scopePaths:
  - "tasks/TASK-RPT-*-legacy-transform-porting.task.md"
  - "evidence/Pilot/TASK-RPT-0009/**"
  - "src/ReportDemo.Import/**"
  - "src/ReportDemo.Documents/**"
  - "db/migrations/reportdemo/**"
  - "legacy/舊系統報表模組_功能別103.xxx"
  - "legacy/舊系統資料轉換_SP_功能別103.sql"
deliverables:
  - "evidence/Pilot/TASK-RPT-0009/module-porting-comparison-report.md"
  - "evidence/Pilot/TASK-RPT-0009/implementation-notes.md"
  - "evidence/Pilot/TASK-RPT-0009/validation-result.md"
  - Target system implementation artifacts: code, DB migration, tests, and operation docs
validators:
  - "git diff --check"
  - "dotnet build src/ReportDemo.sln --no-restore"
  - "dotnet test src/ReportDemo.sln --no-build"
  - After target implementation location is created, add: Golden Dataset / Shadow Validation comparison command
evidence:
  required: command-backed
rollback:
  strategy: revert-commit-or-feature-flag-disable
  notes: "若已進入正式資料流程，需先依 rollback runbook 停用新功能並回復舊系統路徑。"
atomizationImpact:
  ownerAtomOrMap: "reportdemo.m1.legacy-transform-porting"
  mapUpdates:
    - After target implementation location is created, add actual module/path map
  notes: "This card defines the functional work package first; add actual module/map and file boundaries after the implementation location is created."
outOfScope:
  - "使用未脫敏正式資料進行開發或一般測試"
  - "未完成舊系統覆蓋比對即切換正式流程"
  - "繞過 Admin、Data Scope、稽核與告警要求"
nonGoals:
  - "未經 conversion map、workstream 與 evidence 對帳就一次性重寫所有舊系統功能"
  - "在未完成 PoC / Gate 前承諾最終技術選型"
---
# TASK-RPT-0009 - M1-03 移植或重寫舊資料轉換邏輯

## Goal

完成 `M1-03` 對應功能，並能證明新系統涵蓋舊系統必要行為；未知舊系統程式碼先以象徵性代號標記，後續盤點時替換為真實名稱。

## 2026-07-08 轉換軌重新定義（ADR-018）

本卡解除範圍外裁減，承接 `TASK-RPT-0005` conversion map 中「標為移植且未被 0023/0024/0025/0028 承接」的**全部** Qutora 模組（ADR-018 全功能轉換口徑）：

- 範圍以卡內 workstreams 分工，不新增正式子卡。每日派工單引用格式如 `TASK-RPT-0009 / 0009b`；evidence 檔名用 `0009a-*.md` 前綴（沿用 0004 慣例）。

```yaml
workstreams:
  - id: "0009a"
    title: "Documents CRUD / versioning"
    dri: "Backend / DBA"
  - id: "0009b"
    title: "Approval 工作流（5 services）"
    dri: "Backend / DBA"
  - id: "0009c"
    title: "Shares + Email 通知"
    dri: "Backend / DBA"
  - id: "0009d"
    title: "Admin / Settings / ApiKeys 殘餘"
    dri: "Backend / DBA"
```
- 注意：Qutora 的 Approval / Shares 是**文件審批與分享**功能，屬本卡轉換軌；與 M6 報表覆核/重產/作廢卡（0030/0031/0032，維持裁減）是不同的東西，不得混淆。
- workstream 的中間驗收由 AI reviewer（獨立 session）依 RB-06 決策包模式完成；人類驗收走每日 hands-on TC + 週五 Demo Day（結果制雙層，ADR-016）。workstream 完成不等於整卡完成；整卡 closure 仍需 `closure_reviewer` 確認。
- 目標：以 ASP.NET Core (C#) 移植到 `src/`；Documents / Approval / Shares / Admin / Auth 相關行為都必須有下落。
- 每個移植模組必附**雙製比對 evidence**：同一輸入在 Qutora 舊路徑與 `src/` 新路徑的輸出比對，差異依 RB-07 字典分類；P0 差異未關閉不得 closure。
- 交付物 `module-porting-comparison-report.md` 每列需含：Qutora 元件、`src/` 模組路徑、輸入樣本、Qutora 輸出摘要、新平台輸出摘要、差異等級、處置、owner、reviewer、evidence link。
- C# 實作需通過 `src/README.md` 的 Engineering Start Contract；build / test 結果需保存到本卡 evidence path。
- 分工：Backend / DBA 為 DRI，AI 主力產 C# 代碼與比對腳本；QA / Security / DevOps 驗證比對 evidence 可重跑（closure reviewer）；Tech Lead 裁決「沿用 vs 移植」邊界爭議。
- HTML5 19 功能域前端不在本卡，掛 `TASK-RPT-0028`。
- 完整規格（10 validators / 10 test cases）依排程於 W5-W6 升級後才可開工；排程落點 W7-W9 併行。

## Legacy Coverage

- 需對照：`legacy/舊系統報表模組_功能別103.xxx`
- 需對照：`legacy/舊系統資料轉換_SP_功能別103.sql`
- 若本卡涉及重寫，必須保留舊系統輸入、輸出、排序、欄位、狀態與例外案例的比對紀錄。

## Functional Scope
- 盤點舊系統資料轉換 SQL、stored procedure 或程式邏輯。
- 對結果可靠的邏輯先移植或封裝。
- 對效能差或不可維護的邏輯重寫並建立比對測試。

## Implementation Contract

- 優先採漸進式承接：沿用、封裝、移植、重寫、廢止候選需逐項記錄。
- 不得用未脫敏正式資料做一般開發或測試；正式資料只可進受控 Shadow Validation。
- 涉及權限、資料範圍、PDF、稽核、告警或 break-glass 時，安全性與可稽核性優先於便利性。
- 每個可觀測流程需留下 trace ID / correlation ID，方便新舊系統比對與事故追蹤。

- Agent Team 派工、role、reviewer、validator、human sign-off 與 ADR gate 需依 Agent Team 計畫書 v1.0 執行：`內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md`。

## Deliverables

- 實作程式碼、DB migration、設定檔或文件，依本卡 `scopePaths` 控制。
- `evidence/Pilot/TASK-RPT-0009/module-porting-comparison-report.md`
- `evidence/Pilot/TASK-RPT-0009/implementation-notes.md`
- `evidence/Pilot/TASK-RPT-0009/validation-result.md`

## Validators

- `git diff --check`
- `dotnet build src/ReportDemo.sln --no-restore`
- `dotnet test src/ReportDemo.sln --no-build`
- After target implementation location is created, add: Golden Dataset / Shadow Validation comparison command

## Acceptance Criteria
- 新舊轉換結果筆數一致。
- 主要欄位值一致。
- 差異有紀錄與處理結論。

## Rollback

以 feature flag、路由切回舊系統、回復 migration 或 revert commit 為優先；若已接觸正式流程，必須先確認資料一致性與稽核紀錄完整。

## Notes

- 2026-07-02 | planned | Card generated from the function milestone plan; waiting for human confirmation of priority, owner, and target implementation location path.
- 2026-07-02 | planned | 已同步 Agent Team 計畫書 v1.0；正式派工前需確認 role、reviewer、validator、human/ADR gate 與違規阻擋機制。
