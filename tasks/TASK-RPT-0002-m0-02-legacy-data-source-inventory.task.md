---
task_id: TASK-RPT-0002
source_milestone: M0-02
title: "盤點既有資料來源"
status: planned
owner: "Backend / DBA"
priority: P0
milestone: M0
drill_stage: "MVP1"
execution_mode: "ai-with-human-review"
primary_role: "Backend / DBA"
closure_reviewer: "Tech Lead / Captain"
support_roles:
  - "Tech Lead / Captain"
  - "QA / Security / DevOps"
depends_on: []
related_plan: "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
drill_plan: "drills/分階段演練與驗收計畫.md"
runbooks:
  - "runbooks/RB-01-qutora-startup.md"
  - "runbooks/RB-03-evidence-standard.md"
evidence_path: "evidence/MVP1/TASK-RPT-0002/"
scopePaths:
  - "tasks/TASK-RPT-0002-m0-02-legacy-data-source-inventory.task.md"
  - "evidence/MVP1/TASK-RPT-0002/**"
  - "open-source-sandbox/qutora-api/Qutora.Infrastructure/Persistence/ApplicationDbContext.cs"
  - "open-source-sandbox/qutora-api/Qutora.Database.SqlServer/**"
  - "open-source-sandbox/qutora-api/Qutora.Domain/Entities/**"
deliverables:
  - "evidence/MVP1/TASK-RPT-0002/qutora-db-inventory.md"
  - "evidence/MVP1/TASK-RPT-0002/source-table-map.csv"
  - "evidence/MVP1/TASK-RPT-0002/migration-risk-register.md"
validators:
  - "V-0002-01"
  - "V-0002-02"
  - "V-0002-03"
  - "V-0002-04"
  - "V-0002-05"
  - "V-0002-06"
  - "V-0002-07"
  - "V-0002-08"
  - "V-0002-09"
  - "V-0002-10"
evidence:
  required: command-backed
rollback:
  strategy: documentation-only-revert
  notes: "本卡只盤點資料來源；若盤點錯誤，修正 inventory 與 risk register，不修改 Qutora DB。"
outOfScope:
  - "修改 Qutora schema"
  - "將正式資料匯入演練環境"
  - "執行 MSSQL 到 MariaDB migration"
nonGoals:
  - "完成正式 DB 選型"
  - "建立完整資料轉換程式"
---
# TASK-RPT-0002 - M0-02 盤點既有資料來源

## 任務目標

盤點 Qutora 作為本演練舊系統時可提供的資料來源、資料表、entity、關聯、更新來源與抽取風險，形成 MVP2 MariaDB 初版轉換的輸入基準。

## 真實功能帶入場景

Backend / DBA 以 Qutora SQL Server / `QutoraDB` 為舊系統資料來源，先靜態盤點 EF `ApplicationDbContext`、entity 與 SQL Server migration，再於 Qutora 可啟動後補 runtime schema evidence。

## 舊系統覆蓋

| 資料來源 | Qutora 對應 | 用途 |
| --- | --- | --- |
| 文件主檔 | `Document` | 報表 / PDF 主資料。 |
| 文件版本 | `DocumentVersion` | 版本與下載 baseline。 |
| metadata | `Metadata`、`MetadataSchema` | 報表代號、資料日期、機密等級。 |
| 使用者 / 角色 | `ApplicationUser`、`ApplicationRole` | 權限與下載人 baseline。 |
| bucket / provider | `StorageBucket`、`StorageProvider` | 儲存層與主檔位置。 |
| audit | `AuditLog` | 操作追蹤與稽核 baseline。 |

## 落地設計

| 項目 | 定義 |
| --- | --- |
| 盤點方式 | 靜態 entity / migration 盤點 + runtime DB schema 抽樣。 |
| 輸出格式 | Markdown inventory + CSV table map + risk register。 |
| 權限檢查 | 標記哪些資料表含使用者、角色、bucket permission 或敏感欄位。 |
| 稽核欄位 | 記錄 audit table 欄位與可否支援 user/action/time/entity id。 |
| fail-closed | 若無法取得 DB schema 或無法確認核心資料表，不得進入 MVP2 migration。 |

## 影響範圍

- 影響 `TASK-RPT-0003` 的 baseline 欄位與資料抽樣。
- 影響 `TASK-RPT-0008` 的 MariaDB staging tables。
- 影響 `TASK-RPT-0010` 的 audit write foundation。
- 不修改 Qutora DB、不建立 migration、不使用正式資料。

## 輸入與輸出

| 類型 | 內容 |
| --- | --- |
| 輸入 | Qutora 固定 commit、SQL Server provider、EF migrations、entity、runtime DB schema evidence。 |
| 輸出 | `qutora-db-inventory.md`、`source-table-map.csv`、`migration-risk-register.md`。 |

## 完成定義

- 已列出 MVP1/MVP2 必要資料表與 entity。
- 每個核心資料欄位都有用途、型別、敏感性、migration 風險與後續任務。
- 已標記 MariaDB 轉換風險，例如 identity、GUID、datetime、nvarchar、json、索引、FK。
- evidence 可由 reviewer 依 Qutora commit 或 runtime schema 重跑。

## Validators

| ID | 輸入條件 | 執行方式 / Evidence | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| V-0002-01 | Qutora 原始碼可讀 | 檢查 `ApplicationDbContext` | 可列出核心 DbSet 或 repository | 無 DB 入口 |
| V-0002-02 | SQL Server provider 可讀 | 檢查 SQL Server migration | 可列出初始 schema 來源 | migration 不可定位 |
| V-0002-03 | entity 可讀 | 盤點 Document / Metadata / Audit | 核心 entity 欄位完整 | 核心 entity 缺失 |
| V-0002-04 | 使用者 entity 可讀 | 盤點 user / role / permission | 權限資料來源可追溯 | 權限來源不明 |
| V-0002-05 | storage entity 可讀 | 盤點 bucket / provider | PDF 儲存來源可追溯 | 儲存來源不明 |
| V-0002-06 | audit entity 可讀 | 盤點 audit 欄位 | 可支援操作追蹤或記錄缺口 | audit 來源不明 |
| V-0002-07 | inventory 完成 | 檢查 `source-table-map.csv` | 每列含 table/entity/key/risk | 欄位不完整 |
| V-0002-08 | migration risk 完成 | 檢查風險 register | 每個高風險型別有對策 | 高風險無對策 |
| V-0002-09 | evidence 路徑正確 | 檢查 `evidence/MVP1/TASK-RPT-0002/` | 符合 RB-03 | 使用舊 `M0-02` 路徑 |
| V-0002-10 | reviewer 可重跑 | reviewer 抽查 3 張表來源 | 結果一致 | 無法重現 |

## Test Cases

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| TC-0002-01 | 全新 clone | 搜尋 DB context | 找到資料模型入口 | 入口不明 |
| TC-0002-02 | SQL Server migration 存在 | 匯出 migration 表清單 | 產生 table inventory | 表清單不可產出 |
| TC-0002-03 | Document entity 存在 | 記錄欄位與 key | 主檔欄位可映射 | key 不明 |
| TC-0002-04 | Metadata entity 存在 | 記錄 schema / value 結構 | 可支援報表屬性 | metadata 不可映射 |
| TC-0002-05 | User / Role entity 存在 | 記錄權限關聯 | 可支援後續 Data Scope | 權限關聯不明 |
| TC-0002-06 | Storage entity 存在 | 記錄 bucket/provider 欄位 | 可支援 PDF storage 盤點 | 儲存關聯不明 |
| TC-0002-07 | Audit entity 存在 | 記錄 audit 欄位 | 可支援 MVP1 audit sample | audit 欄位不足且無替代 |
| TC-0002-08 | `source-table-map.csv` 完成 | reviewer 抽查 5 列 | 每列可追溯來源 | 任一列無來源 |
| TC-0002-09 | risk register 完成 | 檢查 MariaDB 風險 | 型別與索引風險已標示 | 風險未標示 |
| TC-0002-10 | MVP1 Gate review | QA / Security / DevOps 複核 | 可判斷是否進入 baseline | 缺核心資料來源 |

## Reviewer / Human Gate / ADR

| 項目 | 規則 |
| --- | --- |
| Reviewer | Backend / DBA 自查後，由 QA / Security / DevOps 抽查資料來源與敏感欄位。 |
| Human Gate | 若 Qutora DB schema 不足以支撐 PDF / metadata / audit baseline，需人類決定縮 MVP 或調整演練。 |
| ADR | 若要變更本演練目標 DB 或修改 Qutora schema，需更新 ADR-013 或新增 ADR。 |

## Notes

- 2026-07-06 | upgraded | MVP1 核心卡已補齊完整任務卡格式，evidence 改為 `evidence/MVP1/TASK-RPT-0002/`。
