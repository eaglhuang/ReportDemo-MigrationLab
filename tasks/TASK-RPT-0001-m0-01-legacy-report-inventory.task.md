---
task_id: TASK-RPT-0001
source_milestone: M0-01
title: "盤點既有報表"
status: planned
owner: project-captain
priority: P0
milestone: M0
drill_stage: "MVP1"
execution_mode: "ai-with-human-review"
primary_role: "Tech Lead / Captain"
support_roles:
  - "Backend / DBA"
  - "QA / Security / DevOps"
depends_on: []
related_plan: "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
drill_plan: "drills/分階段演練與驗收計畫.md"
runbooks:
  - "runbooks/RB-01-qutora-startup.md"
  - "runbooks/RB-03-evidence-standard.md"
evidence_path: "evidence/MVP1/TASK-RPT-0001/"
scopePaths:
  - "tasks/TASK-RPT-0001-m0-01-legacy-report-inventory.task.md"
  - "drills/分階段演練與驗收計畫.md"
  - "evidence/MVP1/TASK-RPT-0001/**"
  - "open-source-sandbox/qutora-api/Qutora.API/Controllers/DocumentsController.cs"
  - "open-source-sandbox/qutora-api/Qutora.Domain/Entities/Document.cs"
  - "open-source-sandbox/qutora-api/Qutora.Domain/Entities/DocumentVersion.cs"
  - "open-source-sandbox/qutora-api/Qutora.Domain/Entities/Metadata.cs"
deliverables:
  - "evidence/MVP1/TASK-RPT-0001/report-inventory.md"
  - "evidence/MVP1/TASK-RPT-0001/qutora-document-feature-map.md"
  - "evidence/MVP1/TASK-RPT-0001/gap-and-decision-log.md"
validators:
  - "V-0001-01"
  - "V-0001-02"
  - "V-0001-03"
  - "V-0001-04"
  - "V-0001-05"
  - "V-0001-06"
  - "V-0001-07"
  - "V-0001-08"
  - "V-0001-09"
  - "V-0001-10"
evidence:
  required: command-backed
rollback:
  strategy: documentation-only-revert
  notes: "本卡只產出盤點與 evidence；若盤點錯誤，以修正報表清單與 gap log 為回復方式，不修改 Qutora。"
outOfScope:
  - "修改 Qutora 原始碼"
  - "匯入或使用未脫敏正式資料"
  - "決定正式專案報表廢止或下線"
nonGoals:
  - "一次盤點真實券商所有報表"
  - "建立完整新系統報表引擎"
---
# TASK-RPT-0001 - M0-01 盤點既有報表

## 任務目標

建立本演練舊系統 Qutora 的「報表 / 文件功能盤點基準」。本演練以 Qutora 的文件、版本、metadata、分類、下載與分享能力模擬舊系統報表模組；本卡需列出哪些 Qutora 功能可對應到原計畫中的報表功能，哪些功能缺口需在後續任務卡補齊。

## 真實功能帶入場景

三人小隊依 `RB-01` 啟動 Qutora 後，使用 Qutora 的 Documents API 或資料庫結構盤點舊系統可提供的文件 / 報表能力。若尚未啟動 runtime，可先以 Qutora 原始碼與 EF entity 作靜態盤點，但進入 MVP1 Gate 前必須補上可重跑 evidence。

## 舊系統覆蓋

| 舊系統能力 | Qutora 對應元件 | 盤點重點 |
| --- | --- | --- |
| 報表主檔 | `Document`、`DocumentVersion` | document id、版本、檔名、content type、大小、狀態。 |
| 報表欄位 / 查詢條件 | `Metadata`、`MetadataSchema` | report_code、data_date、confidentiality、department 等可否建模。 |
| 報表分類 | `Category`、`StorageBucket` | 分類、儲存區、權限邊界。 |
| 報表下載 | `DocumentsController`、`DocumentService` | 下載入口、授權檢查、回應格式。 |
| 報表稽核 | `AuditLog`、`AuditLoggingMiddleware` | 上傳、查詢、下載是否可追蹤。 |

## 落地設計

| 項目 | 定義 |
| --- | --- |
| 盤點方式 | 靜態盤點 Qutora API / entity / DTO，並在 Qutora 可啟動後補 runtime evidence。 |
| 輸出格式 | Markdown 清單 + gap log，不建立新資料表。 |
| 權限檢查 | 只記錄 Qutora 現有權限入口與缺口，不變更權限設定。 |
| 稽核欄位 | 記錄 Qutora 是否可提供 user、document id、action、time、IP 或替代 log。 |
| fail-closed | 若 Qutora 無法啟動或文件功能不可驗證，本卡標記 blocked，不得進入 MVP2。 |

## 影響範圍

- 影響 `MVP1` 是否能成立為後續搬移基準。
- 影響 `TASK-RPT-0003` 的 baseline 選樣。
- 影響 `TASK-RPT-0019`、`TASK-RPT-0023`、`TASK-RPT-0024` 對 PDF metadata、下載閘道與浮水印的欄位假設。
- 不影響 Qutora 原始碼、不建立 migration、不修改 DB schema。

## 輸入與輸出

| 類型 | 內容 |
| --- | --- |
| 輸入 | Qutora 固定 commit、Qutora API / entity / DTO、`RB-01` 啟動 evidence。 |
| 輸出 | `report-inventory.md`、`qutora-document-feature-map.md`、`gap-and-decision-log.md`。 |

## 完成定義

- 已列出 Qutora 可代表的舊系統報表 / 文件能力。
- 每個正式演練必要能力都有承接方式：直接使用 Qutora、以 metadata 模擬、以後續任務補齊或列為不做。
- 每個缺口都有後續任務卡或 ADR / human gate。
- evidence 可由 reviewer 依相同 commit 重新取得。

## Validators

| ID | 輸入條件 | 執行方式 / Evidence | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| V-0001-01 | repo 可讀 | `git submodule status` | Qutora commit 為 `de156e0...` | commit 不一致且無說明 |
| V-0001-02 | Qutora 原始碼存在 | 檢查 Documents / Metadata / Audit 相關檔案 | 盤點來源可追溯到具體檔案 | 只用口頭描述 |
| V-0001-03 | Documents API 可定位 | 記錄 API / service / entity 對照 | 每個文件能力有來源 | 找不到來源 |
| V-0001-04 | Metadata 元件可定位 | 記錄 metadata schema 與欄位能力 | 可支援報表代號、日期、機密等級或記錄缺口 | 缺口未記錄 |
| V-0001-05 | Download 路徑可定位 | 記錄下載入口與授權檢查位置 | 後續 M5-01 可承接 | 下載入口不明 |
| V-0001-06 | Audit 元件可定位 | 記錄 audit log 或 middleware 能力 | 可支援 MVP1 操作追蹤或記錄替代方案 | 無 audit 說明 |
| V-0001-07 | 盤點清單完成 | 檢查 `report-inventory.md` | 至少列出主檔、metadata、下載、權限、稽核 | 缺任何核心能力 |
| V-0001-08 | 缺口清單完成 | 檢查 `gap-and-decision-log.md` | 每個缺口都有 owner / next task / gate | 缺口無處理策略 |
| V-0001-09 | Evidence 路徑正確 | 檢查 `evidence/MVP1/TASK-RPT-0001/` | 符合 RB-03 | evidence 散落舊路徑 |
| V-0001-10 | Reviewer 可重跑 | reviewer 依 evidence 重查 2 個來源 | 結果一致 | 來源不可重現 |

## Test Cases

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| TC-0001-01 | 全新 clone | 初始化 submodule 後讀取 Qutora 檔案 | 可定位 Documents 相關元件 | submodule 無法取得 |
| TC-0001-02 | Qutora 原始碼可讀 | 搜尋 document entity / DTO | 可列出主檔欄位 | 欄位來源不明 |
| TC-0001-03 | Qutora 原始碼可讀 | 搜尋 metadata schema | 可列出 metadata 建模能力 | metadata 不可建模且無替代 |
| TC-0001-04 | Qutora 原始碼可讀 | 搜尋 download endpoint | 可列出下載路徑 | 下載路徑不明 |
| TC-0001-05 | Qutora 原始碼可讀 | 搜尋 authorization / permission | 可列出權限檢查入口 | 權限檢查不明 |
| TC-0001-06 | Qutora 原始碼可讀 | 搜尋 audit log | 可列出 audit 入口或替代 log | audit 完全不可追蹤 |
| TC-0001-07 | 初版盤點清單 | reviewer 抽查 5 筆功能對照 | 5 筆皆可追溯來源 | 任一筆無來源 |
| TC-0001-08 | gap log 完成 | 檢查缺口是否有 task / ADR | 缺口可追蹤 | 缺口沒有下一步 |
| TC-0001-09 | 盤點包含不做項 | 檢查 out-of-scope | 不做理由明確 | 不做項混入 MVP1 |
| TC-0001-10 | MVP1 Gate review | 由 QA / Security / DevOps 複核 | 可決定是否進入 TASK-RPT-0002 / 0003 | reviewer 無法判斷 |

## Reviewer / Human Gate / ADR

| 項目 | 規則 |
| --- | --- |
| Reviewer | QA / Security / DevOps 複核 evidence；Tech Lead / Captain 負責 closure 判定。 |
| Human Gate | 若 Qutora 的文件能力不足以代表本演練舊系統，需人類決定是否換 repo、縮 MVP 或改演練目標。 |
| ADR | 若要修改 Qutora 原始碼或更換舊系統，需新增 ADR 或更新 ADR-012。 |

## Notes

- 2026-07-06 | upgraded | MVP1 核心卡已補齊完整任務卡格式，evidence 改為 `evidence/MVP1/TASK-RPT-0001/`。
