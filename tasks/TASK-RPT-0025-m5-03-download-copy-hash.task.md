---
task_id: TASK-RPT-0025
source_milestone: M5-03
title: "下載副本 Hash"
status: planned
owner: "QA / Security / DevOps"
priority: P0
milestone: M5
drill_stage: "MVP2"
execution_mode: "ai-with-human-review"
primary_role: "QA / Security / DevOps"
closure_reviewer: "Tech Lead / Captain"
support_roles:
  - "Tech Lead / Captain"
  - "Backend / DBA"
depends_on:
  - "TASK-RPT-0023"
  - "TASK-RPT-0024"
  - "TASK-RPT-0010"
related_plan: "drills/分階段演練與驗收計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
evidence_path: "evidence/MVP2/TASK-RPT-0025/"
scopePaths:
  - "src/**"
  - "tasks/TASK-RPT-0025-m5-03-download-copy-hash.task.md"
  - "evidence/MVP2/TASK-RPT-0025/**"
  - "runbooks/RB-03-evidence-standard.md"
  - "poc/validators/**"
  - "open-source-sandbox/qutora-api"
deliverables:
  - "evidence/MVP2/TASK-RPT-0025/download-copy-hash-model.md"
  - "evidence/MVP2/TASK-RPT-0025/hash-calculation-points.md"
  - "evidence/MVP2/TASK-RPT-0025/hash-validation-result.md"
evidence:
  required: command-backed
rollback:
  strategy: disable-new-download-output-and-keep-qutora-download-only
  notes: "若下載副本 Hash 無法計算或稽核寫入失敗，不得交付新路徑下載檔；MVP2 可回到 Qutora 原下載路徑。"
outOfScope:
  - "長期保存所有下載副本檔案"
  - "WORM / Immutable Archive 正式採購與部署"
  - "正式數位簽章與 timestamp 驗證鏈"
nonGoals:
  - "本卡不取代 PDF 主檔完整性檢查"
  - "本卡不決定下載副本保留年限"
---
# TASK-RPT-0025 - M5-03 下載副本 Hash

## 任務目標

建立 MVP2 可驗證的下載副本 Hash 規格，確保每次經下載閘道與浮水印處理後產生的 PDF 副本，都能留下不可靜默遺失的檔案指紋、metadata 與稽核事件。此卡支援外流追蹤、竄改偵測與事後舉證。

## 真實功能帶入場景

本演練舊系統採用 Qutora。MVP2 以 Qutora 合成 PDF 為主檔來源，經 `TASK-RPT-0023` 下載閘道與 `TASK-RPT-0024` 動態浮水印後，計算下載副本 Hash 並保存於 MariaDB 目標模型。預設只保存 Hash 與 metadata，不長期保存副本檔案本身。

## 舊系統覆蓋

- 覆蓋 Qutora 使用者下載 PDF 後，系統需能事後查核「哪一次下載輸出了哪一份副本」的能力。
- 若 Qutora 原本只記錄下載事件但沒有副本 Hash，MVP2 應列為新增稽核強化，不視為舊系統功能缺口。
- 新系統不得只保存主檔 Hash；必須區分主檔 Hash 與加浮水印後的下載副本 Hash。

## 落地設計

### API / Service

| 類型 | 名稱 | 說明 |
| --- | --- | --- |
| Internal Service | `recordDownloadCopyHash(download_id, master_hash, copy_hash)` | 記錄單次下載副本 Hash。 |
| Internal Service | `calculateSha256(stream)` | 以 streaming 方式計算 PDF Hash，避免整檔載入記憶體。 |
| Internal Service | `verifyDownloadCopyHash(download_id, file_stream)` | 事後驗證下載副本是否與紀錄相符。 |

### 資料表

| Table | 主要欄位 | 用途 |
| --- | --- | --- |
| `download_copy_hash` | `download_id`, `pdf_id`, `master_hash`, `copy_hash`, `hash_algorithm`, `created_at` | 保存下載副本檔案指紋。 |
| `download_integrity_event` | `event_id`, `download_id`, `event_type`, `payload_hash`, `created_at` | 保存 Hash 相關稽核事件。 |
| `download_copy_metadata` | `download_id`, `file_size`, `watermark_policy_id`, `check_code`, `storage_mode` | 保存可查核 metadata。 |

### 狀態機

```text
watermarked -> hashing -> recorded -> ready_to_deliver
watermarked -> failed_closed
hashing -> mismatch
hashing -> failed_closed
```

### Hash 計算時點

| Hash | 時點 | 用途 |
| --- | --- | --- |
| `master_hash` | PDF 主檔入庫或 baseline 建立時 | 驗證主檔未被異動。 |
| `copy_hash` | 動態浮水印套用完成後、檔案交付前 | 驗證每次下載副本。 |
| `payload_hash` | audit event 寫入前 | 驗證稽核 payload 完整性。 |

### 錯誤碼

| Code | 說明 | Fail-Closed |
| --- | --- | --- |
| `MASTER_HASH_MISSING` | 找不到 PDF 主檔 Hash。 | Yes |
| `COPY_HASH_FAILED` | 下載副本 Hash 計算失敗。 | Yes |
| `HASH_MISMATCH` | 事後驗證 Hash 不一致。 | Yes |
| `AUDIT_FAILED` | Hash 事件稽核寫入失敗。 | Yes |
| `METADATA_INCOMPLETE` | Hash metadata 缺漏。 | Yes |

### 權限檢查

- 查詢下載副本 Hash 必須具備 Audit 或 Security role，不得開放一般下載者任意查詢全量紀錄。
- 下載副本 Hash 不得包含 PDF 明文內容或可還原內容的敏感資料。
- 高權限查詢必須寫入 audit event，且不可讓管理權限自動取得 PDF 內容權限。

### 稽核欄位

| 欄位 | 說明 |
| --- | --- |
| `event_type` | `download_hash.started`, `download_hash.recorded`, `download_hash.failed_closed`, `download_hash.verified` |
| `download_id` | 對應下載請求。 |
| `pdf_id` | 對應 PDF metadata。 |
| `master_hash` | PDF 主檔 Hash。 |
| `copy_hash` | 下載副本 Hash。 |
| `hash_algorithm` | MVP2 固定 `SHA-256`。 |
| `correlation_id` | 跨下載、浮水印與 Hash 的追蹤 ID。 |

### Fail-Closed 規則

- 主檔 Hash 缺漏時，不得交付下載副本。
- 下載副本 Hash 計算失敗時，不得交付檔案。
- Hash 紀錄或稽核寫入失敗時，不得交付檔案。
- Hash mismatch 必須阻擋 Gate，並產出 incident evidence。

## 影響範圍

- 影響下載閘道的檔案交付前最後一個 Gate。
- 影響浮水印流程的輸出檔傳遞方式與暫存策略。
- 影響 audit event schema、MariaDB 欄位型別、索引與保存政策。
- 影響未來 WORM / Object Storage / 下載副本保留政策的 ADR。

## 輸入與輸出

| 類型 | 內容 |
| --- | --- |
| Input | PDF 主檔 Hash、浮水印後 PDF stream、下載請求、查核碼、使用者上下文。 |
| Output | `download_copy_hash` 紀錄、Hash 稽核事件、驗證報告、Gate evidence。 |

## 完成定義

- 3 份合成 PDF 下載副本皆可產生 `SHA-256` Hash。
- 同一主檔不同下載副本因浮水印欄位不同而產生不同 `copy_hash`。
- Hash 計算、保存、查詢、驗證皆留下 command-backed evidence。
- Validators 與 Test Cases 各 10 條皆有 evidence。

## Validators

| ID | Validator | Evidence |
| --- | --- | --- |
| V-0025-01 | 驗證 Hash 演算法固定為 `SHA-256` 並寫入 metadata。 | `hash-calculation-points.md` |
| V-0025-02 | 驗證主檔 Hash 與下載副本 Hash 欄位分離。 | `download-copy-hash-model.md` |
| V-0025-03 | 驗證 3 份下載副本皆有 `copy_hash`。 | `hash-validation-result.md` |
| V-0025-04 | 驗證同一主檔兩次下載的 `copy_hash` 不同。 | `same-master-two-downloads.log` |
| V-0025-05 | 驗證主檔 Hash 缺漏時 fail-closed。 | `master-hash-missing.log` |
| V-0025-06 | 驗證 Hash 計算失敗時不交付檔案。 | `copy-hash-failed.log` |
| V-0025-07 | 驗證 Hash 稽核事件包含 `payload_hash`。 | `download-hash-audit-events.jsonl` |
| V-0025-08 | 驗證 Audit role 以外使用者不可查詢全量 Hash 紀錄。 | `hash-query-permission.log` |
| V-0025-09 | 驗證 Hash mismatch 會阻擋 Gate。 | `hash-mismatch-gate-block.log` |
| V-0025-10 | 驗證 `git diff --check` 無格式錯誤。 | `git-diff-check.log` |

## Test Cases

| ID | Input | 執行方式 | 預期結果 | 阻擋上線條件 |
| --- | --- | --- | --- | --- |
| TC-0025-01 | 一般報表主檔 + 浮水印副本 | 計算 Hash | 寫入 `master_hash` 與 `copy_hash` | 只保存主檔 Hash |
| TC-0025-02 | 同一 PDF 兩次下載 | 比對兩次 `copy_hash` | `copy_hash` 不同且可追蹤各自 download_id | Hash 重複且無合理原因 |
| TC-0025-03 | 缺少主檔 Hash | 執行下載流程 | 回傳 `MASTER_HASH_MISSING` | 仍交付副本 |
| TC-0025-04 | Hash service 模擬失敗 | 執行下載流程 | 回傳 `COPY_HASH_FAILED` | 仍交付副本 |
| TC-0025-05 | Audit 寫入失敗 | 執行 Hash 記錄 | 回傳 `AUDIT_FAILED` | 稽核失敗仍交付 |
| TC-0025-06 | 一般使用者查詢 Hash 全量表 | 呼叫查詢流程 | 拒絕並留下 audit event | 一般使用者可查全量 |
| TC-0025-07 | Audit 使用者查詢指定下載 | 呼叫查詢流程 | 回傳 metadata，不回傳 PDF 內容 | 查詢暴露明文內容 |
| TC-0025-08 | 下載後提供副本檔重新驗證 | 執行 verify | Hash 相符並記錄 verified event | 驗證流程無 evidence |
| TC-0025-09 | 人為修改副本後驗證 | 執行 verify | 回傳 `HASH_MISMATCH` 並阻擋 Gate | mismatch 未阻擋 |
| TC-0025-10 | 大型 PDF stream | streaming Hash | 不需整檔載入記憶體，保留耗時紀錄 | 記憶體不可控或無效能紀錄 |

## Reviewer / Human Gate / ADR

- Reviewer：QA / Security / DevOps、QA / Security / DevOps。
- Human Gate：若要長期保存下載副本檔案本身，必須資安、稽核與資料保存 owner 簽核。
- ADR Gate：WORM / Immutable Archive、下載副本保存年限、Hash DB 是否獨立於業務 DB 需 ADR。

## Notes

- MVP2 預設保存 Hash 與 metadata，不保存完整下載副本檔案，以降低資料外洩面與儲存成本。
- 本卡依 Agent Team 計畫書分派 role、reviewer、validator、human sign-off 與 ADR gate。
