---
task_id: TASK-RPT-0019
source_milestone: M4-01
title: "建立 PDF metadata"
status: planned
owner: backend-storage-devops
priority: P0
milestone: M4
drill_stage: "MVP2"
primary_role: "Backend / DBA"
support_roles:
  - "Tech Lead / Captain"
  - "QA / Security / DevOps"
depends_on:
  - "TASK-RPT-0008"
  - "TASK-RPT-0014"
related_plan: "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
drill_plan: "drills/分階段演練與驗收計畫.md"
evidence_path: "evidence/MVP2/TASK-RPT-0019/"
scopePaths:
  - "tasks/TASK-RPT-0019-m4-01-pdf-metadata.task.md"
  - "evidence/MVP2/TASK-RPT-0019/**"
  - "evidence/MVP1/TASK-RPT-0003/**"
  - "evidence/MVP2/TASK-RPT-0008/**"
deliverables:
  - "evidence/MVP2/TASK-RPT-0019/pdf-metadata-model.md"
  - "evidence/MVP2/TASK-RPT-0019/metadata-mapping.md"
  - "evidence/MVP2/TASK-RPT-0019/metadata-validation-result.md"
validators:
  - "V-0019-01"
  - "V-0019-02"
  - "V-0019-03"
  - "V-0019-04"
  - "V-0019-05"
  - "V-0019-06"
  - "V-0019-07"
  - "V-0019-08"
  - "V-0019-09"
  - "V-0019-10"
evidence:
  required: command-backed
rollback:
  strategy: revert-metadata-projection
  notes: "metadata projection 錯誤時回復 staging baseline，不修改 PDF 主檔。"
outOfScope:
  - "PDF 主檔儲存區實作"
  - "全文搜尋索引"
  - "正式報表產製"
nonGoals:
  - "建立完整報表查詢 UI"
---
# TASK-RPT-0019 - M4-01 建立 PDF metadata

## 任務目標

定義 MVP2 PDF metadata 模型，將 Qutora baseline 與 MariaDB staging 的欄位投影成下載閘道與浮水印可使用的報表 metadata。

## 真實功能帶入場景

使用 MVP1 合成 PDF 與 Qutora metadata export，建立新系統 `pdf_metadata` 概念模型，確保每份 PDF 都有 legacy reference、報表代號、資料日期、機密等級、部門、主檔 hash、版本與可稽核欄位。

## 舊系統覆蓋

| Qutora 來源 | PDF metadata 欄位 | 用途 |
| --- | --- | --- |
| Document id | legacy_document_id | 舊系統反查。 |
| Metadata | report_code / data_date / confidentiality | 查詢、授權、浮水印。 |
| Storage provider | master_object_ref | 主檔定位但不得直接暴露。 |
| Download baseline | master_hash | 完整性檢查。 |

## 落地設計

| 項目 | 定義 |
| --- | --- |
| API | MVP2 先定義 metadata read contract；下載閘道只讀 metadata。 |
| 資料表 | `pdf_metadata`、`pdf_version`、`pdf_integrity_ref`。 |
| 狀態機 | `imported`、`metadata_validated`、`hash_verified`、`ready_for_download`、`invalid`。 |
| 錯誤碼 | `PDF_META_MISSING`、`PDF_HASH_MISSING`、`PDF_SCOPE_MISSING`、`PDF_VERSION_INVALID`。 |
| 權限檢查 | metadata 可查詢不代表可下載；下載需經 M5-01。 |
| 稽核欄位 | legacy_document_id、report_code、version、batch_id、row_hash、updated_at。 |
| fail-closed | metadata、scope、hash 任一缺失，PDF 不得進入下載閘道。 |

## 影響範圍

- 影響下載閘道授權、浮水印欄位、下載副本 hash 與 Pilot 查詢。
- 不直接暴露主檔儲存路徑。

## 輸入與輸出

| 類型 | 內容 |
| --- | --- |
| 輸入 | Golden Dataset、MariaDB staging mapping、Data Scope 規則。 |
| 輸出 | metadata model、mapping、validation result。 |

## 完成定義

- 每份 MVP2 PDF 都有 legacy id、report_code、data_date、confidentiality、department、version、hash。
- metadata 缺失時可分類錯誤且 fail-closed。
- 下載閘道與浮水印可直接引用欄位。

## Validators

| ID | 輸入條件 | 執行方式 / Evidence | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| V-0019-01 | baseline metadata | 檢查 mapping | 欄位完整 | 缺核心欄位 |
| V-0019-02 | legacy id | 檢查唯一性 | 每份唯一 | 重複 |
| V-0019-03 | report_code | 檢查可查詢 | 可作索引 | 不可查 |
| V-0019-04 | confidentiality | 檢查分級 | 可供 Data Scope | 缺分級 |
| V-0019-05 | department | 檢查部門欄位 | 可判斷 scope | 缺 scope |
| V-0019-06 | master_hash | 檢查 hash 欄位 | 可重算 | hash 缺失 |
| V-0019-07 | version | 檢查版本規則 | 可判斷最新版 | 版本不明 |
| V-0019-08 | storage ref | 檢查不直接暴露 | 只能 gateway 使用 | 直接暴露路徑 |
| V-0019-09 | invalid case | 模擬缺欄 | fail-closed | 缺欄仍 ready |
| V-0019-10 | evidence path | 檢查 `evidence/MVP2/TASK-RPT-0019/` | 符合 RB-03 | evidence 散落 |

## Test Cases

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| TC-0019-01 | 3 份 baseline PDF | 建立 metadata projection | 3 筆 ready | 筆數不一致 |
| TC-0019-02 | 缺 report_code | validate | `PDF_META_MISSING` | 通過 |
| TC-0019-03 | 缺 hash | validate | `PDF_HASH_MISSING` | 通過 |
| TC-0019-04 | 缺 department | validate | `PDF_SCOPE_MISSING` | 通過 |
| TC-0019-05 | 重複 legacy id | validate | invalid | 通過 |
| TC-0019-06 | version 不一致 | validate | `PDF_VERSION_INVALID` | 通過 |
| TC-0019-07 | 查 report_code | 查詢設計 | 命中正確 PDF | 查詢錯誤 |
| TC-0019-08 | 查 high confidentiality | 查詢設計 | 可分類 | 分級錯誤 |
| TC-0019-09 | gateway 讀 metadata | 模擬 input | 取得必要欄位 | 欄位不足 |
| TC-0019-10 | reviewer 抽查 | 抽查 3 筆 | 可追溯 Qutora | 來源不明 |

## Reviewer / Human Gate / ADR

| 項目 | 規則 |
| --- | --- |
| Reviewer | Backend / DBA 產出，QA / Security / DevOps 複核敏感欄位與 fail-closed。 |
| Human Gate | 若 metadata 欄位不足以支援機密分級，需人類決定縮 MVP 或補資料。 |
| ADR | 若 PDF metadata 保存策略影響長期保存或 WORM，需更新 ADR-008。 |

## Notes

- 2026-07-07 | upgraded | MVP2 核心卡完整格式升級，evidence 改為 `evidence/MVP2/TASK-RPT-0019/`。
