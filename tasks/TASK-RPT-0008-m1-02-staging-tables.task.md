---
task_id: TASK-RPT-0008
source_milestone: M1-02
title: "建立 Staging 資料表"
status: planned
owner: backend-dba
priority: P0
milestone: M1
drill_stage: "MVP2"
primary_role: "Backend / DBA"
support_roles:
  - "Tech Lead / Captain"
  - "QA / Security / DevOps"
depends_on:
  - "TASK-RPT-0002"
  - "TASK-RPT-0007"
related_plan: "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
drill_plan: "drills/分階段演練與驗收計畫.md"
evidence_path: "evidence/MVP2/TASK-RPT-0008/"
scopePaths:
  - "tasks/TASK-RPT-0008-m1-02-staging-tables.task.md"
  - "evidence/MVP2/TASK-RPT-0008/**"
  - "evidence/MVP1/TASK-RPT-0002/**"
  - "evidence/MVP2/TASK-RPT-0007/**"
deliverables:
  - "evidence/MVP2/TASK-RPT-0008/mariadb-schema-v0.md"
  - "evidence/MVP2/TASK-RPT-0008/qutora-to-mariadb-mapping.md"
  - "evidence/MVP2/TASK-RPT-0008/staging-validation-rules.md"
validators:
  - "V-0008-01"
  - "V-0008-02"
  - "V-0008-03"
  - "V-0008-04"
  - "V-0008-05"
  - "V-0008-06"
  - "V-0008-07"
  - "V-0008-08"
  - "V-0008-09"
  - "V-0008-10"
evidence:
  required: command-backed
rollback:
  strategy: drop-staging-schema-and-recreate-from-baseline
  notes: "MVP2 staging 可重建；錯誤時丟棄 staging schema 與資料，保留 Qutora baseline 不變。"
outOfScope:
  - "正式主庫 schema"
  - "大量效能調校"
  - "正式資料 migration"
nonGoals:
  - "取代 ADR-001 正式 DB 選型"
---
# TASK-RPT-0008 - M1-02 建立 Staging 資料表

## 任務目標

設計 MariaDB staging schema v0，承接 Qutora SQL Server 的 document、metadata、storage、user、audit baseline，並保留 legacy reference 與驗證欄位。

## 真實功能帶入場景

使用 `TASK-RPT-0002` 的 Qutora DB inventory 與 `TASK-RPT-0007` 的 batch 設計，建立可匯入 MVP1 合成 PDF metadata 的 staging 表與欄位對照。

## 舊系統覆蓋

| Qutora 來源 | MariaDB staging | 重點 |
| --- | --- | --- |
| Document | `stg_document` | legacy_document_id、filename、content_type、size。 |
| Metadata | `stg_document_metadata` | report_code、data_date、confidentiality、department。 |
| Storage | `stg_storage_ref` | bucket/provider/path/hash reference。 |
| User / Role | `stg_principal_ref` | 下載人與權限 baseline。 |
| Audit | `stg_audit_ref` | source audit id / action / timestamp。 |

## 落地設計

| 項目 | 定義 |
| --- | --- |
| API | 無 API；以 migration / SQL script / schema doc 為交付。 |
| 資料表 | `stg_import_batch`、`stg_document`、`stg_document_metadata`、`stg_storage_ref`、`stg_principal_ref`、`stg_audit_ref`。 |
| 狀態機 | staging item 狀態：`raw`、`mapped`、`invalid`、`ready_for_validation`。 |
| 錯誤碼 | `TYPE_CONVERSION_FAILED`、`REQUIRED_FIELD_MISSING`、`LEGACY_REF_MISSING`、`INDEX_MISSING`。 |
| 權限檢查 | staging 寫入限 migration operator；查詢限 reviewer / auditor。 |
| 稽核欄位 | created_by、created_at、source_batch_id、source_hash、row_hash。 |
| fail-closed | legacy reference、row hash、required metadata 缺失時，不得進入下載 / 浮水印 PoC。 |

## 影響範圍

- 影響 MVP2 MariaDB migration、下載閘道 PoC、metadata 查詢與 PDF hash。
- 影響 `TASK-RPT-0014` Data Scope 與 `TASK-RPT-0023` 下載授權。
- 不改正式 schema、不改 Qutora。

## 輸入與輸出

| 類型 | 內容 |
| --- | --- |
| 輸入 | Qutora table map、import batch design、Golden Dataset metadata export。 |
| 輸出 | MariaDB schema v0、mapping table、staging validation rules。 |

## 完成定義

- 每個 MVP2 必要欄位都有 Qutora source、MariaDB target、型別、nullable、index、驗證規則。
- 每列 staging 都可追溯 source_batch_id 與 legacy_document_id。
- row_hash / source_hash 規則明確。

## Validators

| ID | 輸入條件 | 執行方式 / Evidence | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| V-0008-01 | Qutora table map 完成 | 檢查 mapping | 核心表都有 target | 表缺 target |
| V-0008-02 | metadata export 完成 | 檢查欄位 mapping | report_code 等欄位完整 | 核心欄位缺失 |
| V-0008-03 | batch 設計完成 | 檢查 `source_batch_id` | 所有表可追溯批次 | 無 batch ref |
| V-0008-04 | legacy ids 可用 | 檢查 unique key | legacy ref 唯一 | 重複未處理 |
| V-0008-05 | 型別轉換完成 | 檢查 conversion note | datetime / unicode / guid 有規則 | 型別風險未記錄 |
| V-0008-06 | 索引規則完成 | 檢查 index 清單 | report_code / date / confidentiality 可查 | 關鍵查詢無索引 |
| V-0008-07 | row_hash 規則完成 | 檢查 hash 欄位 | hash 可重算 | hash 規則不明 |
| V-0008-08 | 權限規則完成 | 檢查 DB role | 寫入與查詢分離 | 權限過寬 |
| V-0008-09 | validation rules 完成 | 模擬缺欄 | 可分類 invalid | 缺欄仍 ready |
| V-0008-10 | evidence 路徑正確 | 檢查 `evidence/MVP2/TASK-RPT-0008/` | 符合 RB-03 | evidence 散落 |

## Test Cases

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| TC-0008-01 | 3 筆 baseline | 映射到 `stg_document` | 3 筆都有 legacy id | 筆數不一致 |
| TC-0008-02 | metadata 完整 | 映射 metadata 表 | 欄位可回讀 | 欄位遺失 |
| TC-0008-03 | 缺 report_code | 執行 validation | `REQUIRED_FIELD_MISSING` | 缺欄仍通過 |
| TC-0008-04 | 重複 legacy id | 執行 unique check | 拒絕或 invalid | 重複成功 |
| TC-0008-05 | datetime 欄位 | 檢查時區規則 | 規則明確 | 時區不明 |
| TC-0008-06 | unicode 欄位 | 檢查字元集 | 使用 utf8mb4 | 中文風險未處理 |
| TC-0008-07 | 查 report_code | 檢查 index 設計 | 不需 full scan | 無索引 |
| TC-0008-08 | 查 confidentiality | 檢查 index / enum | 可查詢 | 分級不可查 |
| TC-0008-09 | row_hash 抽查 | 重算 hash | 一致 | 不一致 |
| TC-0008-10 | reviewer review | 抽查 5 欄 mapping | 可追溯來源 | 來源不明 |

## Reviewer / Human Gate / ADR

| 項目 | 規則 |
| --- | --- |
| Reviewer | Backend / DBA 產出，QA / Security / DevOps 複核資料完整性與敏感欄位。 |
| Human Gate | 若 staging 需承接受控正式資料，需人類簽核。 |
| ADR | 若 MariaDB 無法承接必要型別或查詢模式，需回到 ADR-013 或 ADR-001。 |

## Notes

- 2026-07-07 | upgraded | MVP2 核心卡完整格式升級，evidence 改為 `evidence/MVP2/TASK-RPT-0008/`。
