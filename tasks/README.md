---
owner: project-captain
status: active
related_plan: 內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md
agent_team_plan: 內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md
created_at: 2026-07-02
---

# ReportDemo Task Card Index

This directory turns the function milestone plan into dispatchable task cards for the standalone ReportDemo simulation project only.

## Task Card Contract

- 每張 `TASK-RPT-*` 卡都必須對應一個功能里程碑項目。
- 本演練舊系統採用 Qutora；任務卡中的「舊系統」若未另行限定，均指 `open-source-sandbox/qutora-api` 固定 commit 的 Qutora。
- 每張卡都要保留舊系統覆蓋欄位；MVP1/MVP2 核心任務卡應優先引用 Qutora 具體元件，例如 Documents API、Metadata Schema、Audit Logs、SQL Server DB、Storage Provider。非核心卡若尚未盤點完成，才可暫用 `舊系統報表模組_功能別XXX.xxx` 或 `舊系統資料轉換_SP_功能別XXX.sql` 代稱。
- 任務卡不得跳過 Golden Dataset、Shadow Validation、權限、Data Scope、稽核與 rollback 驗證。
- Before the target implementation location exists, use `scopePaths`, `deliverables`, and evidence folders as the delivery boundary; add concrete paths later.
- 摘要任務卡未補齊完整設計規格前不得開工；完整規格至少包含任務目標、真實功能場景、落地設計、影響範圍、輸入輸出、完成定義、10 條 validators、10 條 test cases、風險回復、reviewer / human gate / ADR。
- 未升級為完整格式的任務卡只能作為規劃摘要，不得正式開工或 closure。
- Evidence 路徑應依 `runbooks/RB-03-evidence-standard.md` 採 `evidence/<Stage>/<TASK-ID>/`。
- MVP2 PoC 程式碼落點依 ADR-015，只能放在 `poc/` 與 `tools/`；不得修改 `open-source-sandbox/qutora-api` 作為第一階段原則。
- MariaDB 演練環境依 `runbooks/RB-05-mariadb-environment.md` 建立，任務卡若涉及 M1 / M5 / migration 應在 `scopePaths` 納入對應 PoC 或 runbook。
- 若採 AI 主導三人併行排程，任務卡 execution notes 需標示 `[AI]`、`[AI->HUMAN]`、`[HUMAN]` 或 `[GATE]`；AI 可產出實作與 evidence 草稿，但 human / ADR gate 不得由 AI 取代。

## Core Card Batches

| Batch | Stage | Core cards | 開工條件 |
| --- | --- | --- | --- |
| 1 | MVP1 | `TASK-RPT-0001`、`TASK-RPT-0002`、`TASK-RPT-0003`、`TASK-RPT-0004` | 已升級為完整任務卡；正式開工前仍需依 RB-01 啟動 Qutora，並依 RB-03 建立 evidence index。 |
| 2 | MVP2 | `TASK-RPT-0007`、`TASK-RPT-0008`、`TASK-RPT-0010`、`TASK-RPT-0014`、`TASK-RPT-0019`、`TASK-RPT-0023`、`TASK-RPT-0024`、`TASK-RPT-0025` | 已升級為完整任務卡；MVP1 Gate 通過後，可依 MariaDB / 下載 / 浮水印 PoC 順序領卡執行。 |
| 3 | Pilot | `TASK-RPT-0013`、`TASK-RPT-0018`、`TASK-RPT-0021`、`TASK-RPT-0022`、`TASK-RPT-0028`、`TASK-RPT-0033`、`TASK-RPT-0035`、`TASK-RPT-0036`、`TASK-RPT-0037` | 已升級為完整任務卡；MVP2 Gate 通過後，可依批次移轉、權限、稽核、告警驗證與平行作業順序領卡執行。 |
| 4 | Production Candidate | `TASK-RPT-0038`、`TASK-RPT-0040`、`TASK-RPT-0041`、`TASK-RPT-0042`、`TASK-RPT-0043`、`TASK-RPT-0044`、`TASK-RPT-0045` | 已升級為完整任務卡；Pilot Gate 通過後，可依 break-glass、Go / No-Go、rollback、UAT、下線與 release acceptance 順序領卡執行。 |

其餘 17 張非核心任務卡已標記 `drill_stage: "Backlog"`；它們只可作為規劃摘要，未補齊完整任務卡規格前不得正式開工或 closure。

## Stage 對照規則

- 任務卡 frontmatter 後續升級時，應補 `drill_stage`、`primary_role`、`support_roles` 與 `evidence_path`。
- `drill_stage` 只能使用 `MVP1`、`MVP2`、`Pilot`、`ProductionCandidate` 或 `Backlog`。
- 非核心任務卡預設為 `Backlog`，直到被納入某一階段並補齊完整規格。
- `execution_mode` 可使用 `ai-with-human-review`、`human-only` 或 `requires-full-spec-before-start`。
- `ai-with-human-review` 表示 AI 可主開發，但需人類 review；`human-only` 表示任務本質涉及 human / ADR gate；`requires-full-spec-before-start` 表示任務未補齊完整規格前不得開工。

## Drill Plan Contract

- 演練唯一執行指南：`drills/分階段演練與驗收計畫.md`。
- Evidence 標準：`runbooks/RB-03-evidence-standard.md`。
- Rollback 演練：`runbooks/RB-04-rollback-rehearsal.md`。
- 版本異動：根目錄 `版本異動摘要ChangeLog.md` 是唯一 active ChangeLog。
- Qutora 作為本演練舊系統的決策依 ADR-012；不得再以獨立 Qutora 對照表維護。
- MariaDB 作為本演練目標資料庫的決策依 ADR-013；此決策不取代正式專案最終 DB 選型。
- 2 週 MVP 節奏與完整任務卡開工 Gate 依 ADR-014。
- 演練 PoC 技術棧與程式碼落點依 ADR-015；正式實作技術棧仍需另行 ADR。
- AI 主導三人併行排程依 ADR-016、`drills/AI主導三人併行排程與缺口分析.md` 與 `runbooks/RB-06-ai-dispatch-cycle.md`；週末不排正式工作，每人每日最多 8 小時。

## Agent Team Dispatch Contract

- `Agent Team plan v1.0` is the task dispatch source of truth and does not depend on any external codebase or existing Team Agents runtime.
- 正式接卡前需確認 Agent role、reviewer、validator、human sign-off 與 ADR gate。
- M5、M7、M8、M9 或涉及正式資料的任務卡，需額外納入 Security / Permission、Audit / Evidence、QA / Validation 或人類簽核。
- 若 Agent 自動決策與資安、稽核或 ADR 衝突，任務卡不得 closure，需先升級人類或 ADR 裁決。
- 違規阻擋機制至少包含：任務卡 scope、tool sandbox / CI scope check、validator / reviewer、command-backed evidence 與 closure gate。
- AI 產出速度不得取代 reviewer 容量；producer 不得自審，且每週需保留 review / rework 容量。

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
