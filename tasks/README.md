---
owner: "Tech Lead / Captain"
status: active
created_at: 2026-07-02
---

# ReportDemo Task Card Index

This directory turns the function milestone plan into dispatchable task cards for the standalone ReportDemo simulation project only.

## Task Card Contract

- Every `TASK-RPT-*` card is a dispatchable unit with one accountable human DRI.
- `primary_role` is the DRI. It must be exactly one human role: `Tech Lead / Captain`, `Backend / DBA`, or `QA / Security / DevOps`.
- `support_roles` are contributors only; support roles do not own closure.
- `closure_reviewer` is the reviewer who can approve closure. It must be a human role and must not equal `primary_role`.
- AI can draft, implement, test, summarize, and prepare evidence, but AI can never be DRI, closure reviewer, human-only gate, or ADR decision maker.
- `owner` is kept only for legacy compatibility and must equal `primary_role`; new logic should read `primary_role`.
- Evidence must live under `evidence/<Stage>/<TASK-ID>/` unless a task card explicitly narrows the path.
- Before the implementation location exists, use `scopePaths`, `deliverables`, validators, and evidence folders as the delivery boundary.

## Workstream Rule

A task card can contain internal workstreams such as `0004a`, `0004b`, `0004c` when the work is useful to divide but should still close as one card.

Formal child task cards are allowed only when the child can be independently scheduled, independently gated, and independently closed. Any formal split must be recorded in `版本異動摘要ChangeLog.md`.

Daily dispatch may reference a workstream as `TASK-RPT-0004 / 0004b contributor`; this does not create a second DRI.

## Core Card Batches

| Batch | Stage | Core cards | Closure focus |
| --- | --- | --- | --- |
| 1 | MVP1 | `TASK-RPT-0001`, `TASK-RPT-0002`, `TASK-RPT-0003`, `TASK-RPT-0004` | Qutora capability, data source, Golden Dataset, third-party PoC. |
| 2 | MVP2 | `TASK-RPT-0007`, `TASK-RPT-0008`, `TASK-RPT-0010`, `TASK-RPT-0014`, `TASK-RPT-0019`, `TASK-RPT-0023`, `TASK-RPT-0024`, `TASK-RPT-0025` | MariaDB, staging, audit, Data Scope, PDF metadata, download / watermark / hash. |
| 3 | Pilot | `TASK-RPT-0005`, `TASK-RPT-0009`（轉換軌，ADR-018）, `TASK-RPT-0013`, `TASK-RPT-0018`, `TASK-RPT-0021`, `TASK-RPT-0022`, `TASK-RPT-0028`, `TASK-RPT-0033`, `TASK-RPT-0035`, `TASK-RPT-0036`, `TASK-RPT-0037` | Parallel validation, PDF integrity, search, audit, role/data scope, Qutora conversion track. |
| 4 | Production Candidate | `TASK-RPT-0038`, `TASK-RPT-0040`, `TASK-RPT-0041`, `TASK-RPT-0042`, `TASK-RPT-0043`, `TASK-RPT-0044`, `TASK-RPT-0045` | Break-glass, Go / No-Go, rollback, UAT, release acceptance. |

## Stage Contract

- `drill_stage` must be one of `MVP1`, `MVP2`, `Pilot`, `ProductionCandidate`, or `Backlog`.
- `execution_mode` must be one of `ai-with-human-review`, `human-only`, or `requires-full-spec-before-start`.
- `ai-with-human-review` means AI may execute, but closure still requires the human `closure_reviewer`.
- `human-only` means AI may only prepare context or evidence drafts; final action is human-only.
- `requires-full-spec-before-start` means the task cannot start until a concrete spec / runbook / gate is added.

## Task Status Lifecycle

任務卡狀態由 DRI 在 EOD 更新 frontmatter；狀態只反映任務卡本身，不取代 daily dispatch 或 evidence。

| Status | 使用時機 | 必填條件 |
| --- | --- | --- |
| `planned` | 尚未開始或尚未排入今日主責 | 可保持預設 |
| `in-progress` | DRI 已開始產出 deliverables / evidence | Notes 記錄開始日期或 dispatch ref |
| `blocked` | 因 P0/P1、缺前置、缺 human decision、環境不可用而無法推進 | 必須引用 `evidence/<Stage>/risk-blocker-log.md` 的 id |
| `done` | deliverables、validators、evidence 已完成且 closure reviewer 通過 | Notes 必須記錄 reviewer、review date、evidence ref |
| `exception` | 依 MVP v1 scope cut 或 documented exception 不納入 baseline | 必須引用 Gate / ChangeLog / ADR 或 W14 exception evidence |

規則：

- DRI 可把 `planned` 改為 `in-progress` 或 `blocked`。
- `done` 只能在 closure_reviewer 完成 review 後設定；producer 不得自審。
- `exception` 不代表完成，只代表本輪 baseline 顯式裁減。
- daily roster 若顯示完成，但任務卡仍是 `planned`，以任務卡為待更新狀態，EOD 必須補正。

## Drill Plan Contract

- Stage Gate scope: `drills/分階段演練與驗收計畫.md`.
- Daily WHAT/WHEN roster: `drills/每日任務卡排程.md`.
- Daily HOW and dispatch format: `runbooks/RB-06-ai-dispatch-cycle.md`.
- Evidence standard: `runbooks/RB-03-evidence-standard.md`.
- Rollback rehearsal: `runbooks/RB-04-rollback-rehearsal.md`.
- Qutora boundary: ADR-012.
- MariaDB boundary: ADR-013.
- MVP PoC boundary: ADR-015.
- AI collaboration boundary: ADR-016.
- New-platform assumption and Qutora conversion track: ADR-018（HTML5 + ASP.NET Core C#，落點 `src/`；0005 分類、0009 殘餘移植；既有 MVP2/Pilot 卡的 C# 實作計入轉換軌）。

## Agent Team Dispatch Contract

- Agent Team plan v1.0 is a human role and review model, not a separate runtime dependency.
- Every task must keep producer, DRI, and closure reviewer distinguishable.
- Security, audit, formal data, rollback, release, and Go / No-Go remain human-gated.

## Source Code Contract

Any task whose `scopePaths` include `src/**` must follow `src/README.md`.

- Minimum commands: `dotnet restore src/ReportDemo.sln`, `dotnet build src/ReportDemo.sln --no-restore`, and `dotnet test src/ReportDemo.sln --no-build`.
- Build and test output must be saved or summarized under that task's evidence path.
- AI may write C# code and tests, but closure still requires the human `closure_reviewer`.
- A `src/` task cannot be marked `done` if the solution does not build, tests cannot run, or the task lacks evidence explaining why a test is intentionally deferred.
- Qutora conversion tasks must link code changes to `TASK-RPT-0005` conversion map and, when applicable, `TASK-RPT-0009` module porting comparison report.
## Task Roster

| Task ID | Source | Milestone | Title | Status | Depends |
|---|---|---|---|---|---|
| [TASK-RPT-0001](./TASK-RPT-0001-m0-01-legacy-report-inventory.task.md) | M0-01 | M0 | 盤點既有報表 | planned | none |
| [TASK-RPT-0002](./TASK-RPT-0002-m0-02-legacy-data-source-inventory.task.md) | M0-02 | M0 | 盤點既有資料來源 | planned | none |
| [TASK-RPT-0003](./TASK-RPT-0003-m0-03-legacy-result-baseline.task.md) | M0-03 | M0 | 建立舊系統結果基準 | planned | TASK-RPT-0001, TASK-RPT-0002 |
| [TASK-RPT-0004](./TASK-RPT-0004-m0-04-third-party-cross-platform-poc.task.md) | M0-04 | M0 | 建立第三方與跨平台 PoC | planned | TASK-RPT-0001, TASK-RPT-0002 |
| [TASK-RPT-0005](./TASK-RPT-0005-m0-05-sp-sql-refactor-classification.task.md) | M0-05 | M0 | 建立 SP / SQL 改造分類 | planned | TASK-RPT-0002, TASK-RPT-0004 |
| [TASK-RPT-0006](./TASK-RPT-0006-m0-06-role-raci-critical-path.task.md) | M0-06 | M0 | 建立角色、RACI 與關鍵依賴 | planned | TASK-RPT-0001, TASK-RPT-0002, TASK-RPT-0003, TASK-RPT-0004, TASK-RPT-0005 |
| [TASK-RPT-0007](./TASK-RPT-0007-m1-01-import-batch-management.task.md) | M1-01 | M1 | 建立匯入批次管理 | planned | TASK-RPT-0006 |
| [TASK-RPT-0008](./TASK-RPT-0008-m1-02-staging-tables.task.md) | M1-02 | M1 | 建立 Staging 資料表 | planned | TASK-RPT-0002, TASK-RPT-0007 |
| [TASK-RPT-0009](./TASK-RPT-0009-m1-03-legacy-transform-porting.task.md) | M1-03 | M1 | 移植或重寫舊資料轉換邏輯 | planned | TASK-RPT-0005, TASK-RPT-0008 |
| [TASK-RPT-0010](./TASK-RPT-0010-m1-04-audit-write-foundation.task.md) | M1-04 | M1 | 建立稽核寫入基礎 | planned | TASK-RPT-0007 |
| [TASK-RPT-0011](./TASK-RPT-0011-m2-01-validation-rule-versioning.task.md) | M2-01 | M2 | 建立檢核規則版本 | planned | TASK-RPT-0003, TASK-RPT-0009 |
| [TASK-RPT-0012](./TASK-RPT-0012-m2-02-validation-result-severity.task.md) | M2-02 | M2 | 建立檢核結果等級 | planned | TASK-RPT-0011 |
| [TASK-RPT-0013](./TASK-RPT-0013-m2-03-legacy-new-validation-compare.task.md) | M2-03 | M2 | 建立新舊檢核比對 | planned | TASK-RPT-0011, TASK-RPT-0012 |
| [TASK-RPT-0014](./TASK-RPT-0014-m2-04-data-scope-foundation.task.md) | M2-04 | M2 | 建立 Data Scope 基礎規則 | planned | TASK-RPT-0006, TASK-RPT-0010 |
| [TASK-RPT-0015](./TASK-RPT-0015-m3-01-report-template-versioning.task.md) | M3-01 | M3 | 建立報表模板版本 | planned | TASK-RPT-0001, TASK-RPT-0013 |
| [TASK-RPT-0016](./TASK-RPT-0016-m3-02-report-generation-job.task.md) | M3-02 | M3 | 建立報表產生任務 | planned | TASK-RPT-0015 |
| [TASK-RPT-0017](./TASK-RPT-0017-m3-03-report-version-state-machine.task.md) | M3-03 | M3 | 建立報表版本與狀態機 | planned | TASK-RPT-0016 |
| [TASK-RPT-0018](./TASK-RPT-0018-m3-04-dual-report-production-compare.task.md) | M3-04 | M3 | 建立新舊報表雙製比對 | planned | TASK-RPT-0015, TASK-RPT-0016, TASK-RPT-0017 |
| [TASK-RPT-0019](./TASK-RPT-0019-m4-01-pdf-metadata.task.md) | M4-01 | M4 | 建立 PDF metadata | planned | TASK-RPT-0017, TASK-RPT-0018 |
| [TASK-RPT-0020](./TASK-RPT-0020-m4-02-pdf-storage-zone.task.md) | M4-02 | M4 | 建立 PDF 儲存區 | planned | TASK-RPT-0004, TASK-RPT-0019 |
| [TASK-RPT-0021](./TASK-RPT-0021-m4-03-pdf-master-integrity-check.task.md) | M4-03 | M4 | 建立 PDF 主檔完整性檢查 | planned | TASK-RPT-0019, TASK-RPT-0020 |
| [TASK-RPT-0022](./TASK-RPT-0022-m4-04-pdf-reconciliation.task.md) | M4-04 | M4 | 建立 PDF reconciliation 處理 | planned | TASK-RPT-0020, TASK-RPT-0021 |
| [TASK-RPT-0023](./TASK-RPT-0023-m5-01-download-gateway.task.md) | M5-01 | M5 | 建立下載閘道 | planned | TASK-RPT-0014, TASK-RPT-0020 |
| [TASK-RPT-0024](./TASK-RPT-0024-m5-02-dynamic-watermark.task.md) | M5-02 | M5 | 建立動態浮水印 | planned | TASK-RPT-0023 |
| [TASK-RPT-0025](./TASK-RPT-0025-m5-03-download-copy-hash.task.md) | M5-03 | M5 | 建立下載副本 Hash | planned | TASK-RPT-0023, TASK-RPT-0024 |
| [TASK-RPT-0026](./TASK-RPT-0026-m5-03a-download-copy-retention-policy.task.md) | M5-03A | M5 | 建立下載副本保存策略 | planned | TASK-RPT-0025 |
| [TASK-RPT-0027](./TASK-RPT-0027-m5-04-high-confidential-pdf-control.task.md) | M5-04 | M5 | 建立高機密 PDF 控制 | planned | TASK-RPT-0023, TASK-RPT-0024, TASK-RPT-0025, TASK-RPT-0026 |
| [TASK-RPT-0028](./TASK-RPT-0028-m6-01-report-search.task.md) | M6-01 | M6 | 建立報表查詢 | planned | TASK-RPT-0014, TASK-RPT-0017, TASK-RPT-0023 |
| [TASK-RPT-0029](./TASK-RPT-0029-m6-02-secure-preview.task.md) | M6-02 | M6 | 建立安全預覽 | planned | TASK-RPT-0024, TASK-RPT-0028 |
| [TASK-RPT-0030](./TASK-RPT-0030-m6-03-review-workflow.task.md) | M6-03 | M6 | 建立覆核流程 | planned | TASK-RPT-0017, TASK-RPT-0028 |
| [TASK-RPT-0031](./TASK-RPT-0031-m6-04-regeneration-workflow.task.md) | M6-04 | M6 | 建立重產流程 | planned | TASK-RPT-0017, TASK-RPT-0030 |
| [TASK-RPT-0032](./TASK-RPT-0032-m6-05-void-workflow.task.md) | M6-05 | M6 | 建立作廢流程 | planned | TASK-RPT-0017, TASK-RPT-0030 |
| [TASK-RPT-0033](./TASK-RPT-0033-m7-01-audit-query-hash-chain.task.md) | M7-01 | M7 | 建立稽核查詢與 Hash Chain | planned | TASK-RPT-0010, TASK-RPT-0022, TASK-RPT-0025 |
| [TASK-RPT-0034](./TASK-RPT-0034-m7-02-log-sensitive-data-protection.task.md) | M7-02 | M7 | 建立 Log 敏感資料防護 | planned | TASK-RPT-0010 |
| [TASK-RPT-0035](./TASK-RPT-0035-m7-03-alert-severity-routing.task.md) | M7-03 | M7 | 建立告警分級 | planned | TASK-RPT-0010, TASK-RPT-0021, TASK-RPT-0033, TASK-RPT-0034 |
| [TASK-RPT-0036](./TASK-RPT-0036-m8-01-role-management.task.md) | M8-01 | M8 | 建立角色管理 | planned | TASK-RPT-0014, TASK-RPT-0033 |
| [TASK-RPT-0037](./TASK-RPT-0037-m8-02-data-scope-management.task.md) | M8-02 | M8 | 建立資料範圍管理 | planned | TASK-RPT-0014, TASK-RPT-0036 |
| [TASK-RPT-0038](./TASK-RPT-0038-m8-03-break-glass-workflow.task.md) | M8-03 | M8 | 建立 break-glass 流程 | planned | TASK-RPT-0035, TASK-RPT-0036, TASK-RPT-0037 |
| [TASK-RPT-0039](./TASK-RPT-0039-m9-01-shadow-db.task.md) | M9-01 | M9 | 建立 Shadow DB | planned | TASK-RPT-0004, TASK-RPT-0005, TASK-RPT-0018 |
| [TASK-RPT-0040](./TASK-RPT-0040-m9-02-go-no-go-gate.task.md) | M9-02 | M9 | 建立 Go / No-Go Gate | planned | TASK-RPT-0018, TASK-RPT-0039 |
| [TASK-RPT-0041](./TASK-RPT-0041-m9-03-rollback-runbook.task.md) | M9-03 | M9 | 建立 Rollback Runbook | planned | TASK-RPT-0040 |
| [TASK-RPT-0042](./TASK-RPT-0042-m9-04-uat-training-operations-manual.task.md) | M9-04 | M9 | 建立 UAT、訓練與操作手冊 | planned | TASK-RPT-0040, TASK-RPT-0041 |
| [TASK-RPT-0043](./TASK-RPT-0043-m9-05-pilot-legacy-shutdown-gate.task.md) | M9-05 | M9 | 建立 Pilot 與舊系統下線 Gate | planned | TASK-RPT-0040, TASK-RPT-0041, TASK-RPT-0042 |
| [TASK-RPT-0044](./TASK-RPT-0044-m10-01-release-acceptance.task.md) | M10-01 | M10 | 功能驗收 | planned | TASK-RPT-0043 |
| [TASK-RPT-0045](./TASK-RPT-0045-m10-02-legacy-coverage-confirmation.task.md) | M10-02 | M10 | 舊系統覆蓋確認 | planned | TASK-RPT-0001, TASK-RPT-0002, TASK-RPT-0044 |

## Sequencing Note

建議先完成 M0 盤點與 PoC，再進入 M1/M9-01 的資料遷移基礎；M2-M5 可在資料基準穩定後分流開發，但 M7/M8 的稽核、告警、Admin 與 break-glass 不應延到最後才補。
