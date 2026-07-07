---
task_id: TASK-RPT-0003
source_milestone: M0-03
title: "建立舊系統結果基準"
status: planned
owner: "QA / Security / DevOps"
priority: P0
milestone: M0
drill_stage: "MVP1"
execution_mode: "ai-with-human-review"
primary_role: "QA / Security / DevOps"
closure_reviewer: "Tech Lead / Captain"
support_roles:
  - "Tech Lead / Captain"
  - "Backend / DBA"
depends_on:
  - "TASK-RPT-0001"
  - "TASK-RPT-0002"
related_plan: "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
drill_plan: "drills/分階段演練與驗收計畫.md"
runbooks:
  - "runbooks/RB-02-seed-data-synthetic-pdf.md"
  - "runbooks/RB-03-evidence-standard.md"
evidence_path: "evidence/MVP1/TASK-RPT-0003/"
scopePaths:
  - "tasks/TASK-RPT-0003-m0-03-legacy-result-baseline.task.md"
  - "evidence/MVP1/TASK-RPT-0003/**"
  - "runbooks/RB-02-seed-data-synthetic-pdf.md"
  - "open-source-sandbox/qutora-api/Qutora.API/Controllers/DocumentsController.cs"
  - "open-source-sandbox/qutora-api/Qutora.Shared/DTOs/**"
deliverables:
  - "evidence/MVP1/TASK-RPT-0003/golden-dataset-definition.md"
  - "evidence/MVP1/TASK-RPT-0003/metadata-export.json"
  - "evidence/MVP1/TASK-RPT-0003/pdf-baseline-hash.csv"
  - "evidence/MVP1/TASK-RPT-0003/expected-result.md"
  - "evidence/MVP1/TASK-RPT-0003/baseline-review.md"
validators:
  - "V-0003-01"
  - "V-0003-02"
  - "V-0003-03"
  - "V-0003-04"
  - "V-0003-05"
  - "V-0003-06"
  - "V-0003-07"
  - "V-0003-08"
  - "V-0003-09"
  - "V-0003-10"
evidence:
  required: command-backed
rollback:
  strategy: discard-and-regenerate-synthetic-baseline
  notes: "本卡只使用合成 PDF 與 metadata；若 baseline 錯誤，丟棄該批合成資料並重新產生，不得以正式資料修補。"
outOfScope:
  - "使用未脫敏正式資料建立 Golden Dataset"
  - "宣稱 Qutora baseline 等同真實券商報表結果"
  - "建立完整 PDF 浮水印或下載閘道"
nonGoals:
  - "完成所有報表規則比對"
  - "承諾正式環境資料品質"
---
# TASK-RPT-0003 - M0-03 建立舊系統結果基準

## 任務目標

建立 MVP1 可重複執行的 Qutora 舊系統 baseline：合成 PDF、metadata、下載 hash、expected result 與資料血緣。此 baseline 是 MVP2 MariaDB 移轉、下載閘道與浮水印 PoC 的共同輸入。

## 真實功能帶入場景

QA / Security / DevOps 依 `RB-02` 建立至少 3 份合成 PDF，透過 Qutora 上傳，補上 metadata，下載同一批 PDF 並計算 SHA-256。所有資料都必須是合成資料，不得使用未脫敏正式資料。

## 舊系統覆蓋

| Baseline 項目 | Qutora 對應 | 目的 |
| --- | --- | --- |
| 合成 PDF 主檔 | Qutora document upload | 模擬舊系統報表 PDF。 |
| metadata | Qutora metadata schema / metadata | 模擬報表代號、資料日期、部門、機密等級。 |
| 下載 hash | Qutora document download | 建立舊路徑下載結果指紋。 |
| expected result | 人工定義的合成資料預期 | 支援後續 validator 重跑。 |
| 資料血緣 | sample serial / generated_at / owner | 證明非正式資料且可重建。 |

## 落地設計

| 項目 | 定義 |
| --- | --- |
| 資料集 | 至少 3 份合成 PDF：一般、機密、高機密各 1 份。 |
| 欄位 | report_code、data_date、confidentiality、sample_serial、owner_department、legacy_document_id。 |
| Hash 時點 | PDF 產生後計算原始 hash；Qutora 下載後計算下載 hash；兩者差異需說明。 |
| 權限檢查 | 至少一個有權限與一個無權限下載情境。 |
| 稽核欄位 | user、document id、action、time、IP 或替代 log。 |
| fail-closed | 若 baseline 含正式資料、hash 不可重算或 expected result 不明，不得進入 MVP2。 |

## 影響範圍

- 直接影響 MVP2 MariaDB 抽樣移轉、下載閘道 PoC、浮水印 PoC。
- 影響 Pilot 平行作業差異比對的資料格式。
- 不修改 Qutora 原始碼、不新增正式資料、不建立正式報表邏輯。

## 輸入與輸出

| 類型 | 內容 |
| --- | --- |
| 輸入 | `TASK-RPT-0001` 報表 / 文件功能盤點、`TASK-RPT-0002` 資料來源盤點、`RB-02` 合成資料規則。 |
| 輸出 | Golden Dataset 定義、metadata export、PDF hash manifest、expected result、baseline review。 |

## 完成定義

- Golden Dataset 不含未脫敏正式資料。
- 每筆 baseline 都有 legacy document id、metadata、hash、expected result。
- reviewer 可依文件重建或重跑至少 2 個案例。
- Shadow Validation Data 與 Golden Dataset 邊界已明確標示。

## Validators

| ID | 輸入條件 | 執行方式 / Evidence | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| V-0003-01 | `RB-02` 可讀 | 檢查合成資料欄位 | 欄位完整且不含正式資料 | 欄位不足或疑似正式資料 |
| V-0003-02 | 合成 PDF 已產生 | 記錄 PDF 來源與 sample serial | 每份 PDF 可追溯 | 來源不明 |
| V-0003-03 | PDF 已上傳 Qutora | 記錄 legacy document id | 每份 PDF 有 id | id 缺失 |
| V-0003-04 | metadata 已設定 | 匯出 `metadata-export.json` | 欄位可回讀 | metadata 缺欄 |
| V-0003-05 | PDF 可下載 | 計算下載 hash | hash 可重算 | hash 不可重現 |
| V-0003-06 | expected result 已定義 | 檢查 `expected-result.md` | 每筆有預期結果 | expected result 缺失 |
| V-0003-07 | 權限案例已定義 | 有權限 / 無權限下載 evidence | 授權與拒絕可區分 | 越權成功 |
| V-0003-08 | audit / log 可查 | 記錄操作追蹤 | 可對應 user/time/document | 無追蹤紀錄 |
| V-0003-09 | evidence 路徑正確 | 檢查 `evidence/MVP1/TASK-RPT-0003/` | 符合 RB-03 | 使用舊 `M0-03` 路徑 |
| V-0003-10 | reviewer 可重跑 | 重跑 2 份 PDF hash 與 metadata | 結果一致 | 不可重現 |

## Test Cases

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| TC-0003-01 | 無正式資料 | 產生 3 份合成 PDF | 3 份檔案有 sample serial | 少於 3 份 |
| TC-0003-02 | PDF 已產生 | 計算原始 SHA-256 | hash manifest 完成 | hash 缺失 |
| TC-0003-03 | Qutora 可用 | 上傳 3 份 PDF | 取得 3 個 document id | 上傳失敗 |
| TC-0003-04 | PDF 已上傳 | 設定 metadata | report_code 等欄位可回讀 | 欄位不可保存 |
| TC-0003-05 | PDF 已上傳 | 下載同一份 PDF | 下載 hash 可記錄 | 下載失敗 |
| TC-0003-06 | metadata export 完成 | 檢查 JSON 欄位 | 每筆有 legacy id 與機密等級 | 欄位缺失 |
| TC-0003-07 | 有權限帳號 | 下載 baseline PDF | 成功且有 evidence | 下載無 evidence |
| TC-0003-08 | 無權限帳號 | 嘗試下載 baseline PDF | 被拒絕或需明確記錄 Qutora 缺口 | 越權未標記 |
| TC-0003-09 | audit 可查 | 查詢上傳 / 下載 log | 可追蹤操作 | 無 log 且無替代 |
| TC-0003-10 | reviewer 重跑 | 重跑 hash 與 metadata 抽查 | 結果一致 | 不可重現 |

## Reviewer / Human Gate / ADR

| 項目 | 規則 |
| --- | --- |
| Reviewer | QA / Security / DevOps 產出後，由 Backend / DBA 複核 metadata 與 hash；Tech Lead / Captain 判定 Gate。 |
| Human Gate | 若需要使用受控正式資料做 Shadow Validation，必須人類簽核，且不得混入 Golden Dataset。 |
| ADR | 若要變更 Golden Dataset 與正式資料邊界，需新增或更新相關 ADR。 |

## Notes

- 2026-07-06 | upgraded | MVP1 核心卡已補齊完整任務卡格式，evidence 改為 `evidence/MVP1/TASK-RPT-0003/`。
