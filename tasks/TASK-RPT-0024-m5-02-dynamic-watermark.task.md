---
task_id: TASK-RPT-0024
source_milestone: M5-02
title: "動態浮水印處理"
status: planned
owner: "Backend / DBA"
priority: P0
milestone: M5
drill_stage: "MVP2"
execution_mode: "ai-with-human-review"
primary_role: "Backend / DBA"
closure_reviewer: "Tech Lead / Captain"
support_roles:
  - "Tech Lead / Captain"
  - "QA / Security / DevOps"
depends_on:
  - "TASK-RPT-0023"
  - "TASK-RPT-0010"
  - "TASK-RPT-0019"
related_plan: "drills/分階段演練與驗收計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
evidence_path: "evidence/MVP2/TASK-RPT-0024/"
scopePaths:
  - "tasks/TASK-RPT-0024-m5-02-dynamic-watermark.task.md"
  - "evidence/MVP2/TASK-RPT-0024/**"
  - "runbooks/RB-02-seed-data-synthetic-pdf.md"
  - "runbooks/RB-03-evidence-standard.md"
  - "poc/watermark/**"
  - "open-source-sandbox/qutora-api"
deliverables:
  - "evidence/MVP2/TASK-RPT-0024/watermark-field-policy.md"
  - "evidence/MVP2/TASK-RPT-0024/watermark-processing-flow.md"
  - "evidence/MVP2/TASK-RPT-0024/watermark-poc-result.md"
evidence:
  required: command-backed
rollback:
  strategy: disable-watermark-download-path-and-keep-qutora-download-only
  notes: "若浮水印產生失敗或欄位缺漏，不得輸出未加浮水印的 PDF；MVP2 可回到 Qutora 原下載路徑並保留失敗證據。"
outOfScope:
  - "正式數位簽章與 timestamp 量產導入"
  - "極高機密文件安全預覽與 session recording"
  - "宣稱 PDF 浮水印可 100% 防止竄改、截圖、翻拍或重製"
nonGoals:
  - "本卡不導入商用 PDF library 採購決策"
  - "本卡不建立完整 PDF/A 或 PAdES-LTV 長期驗證流程"
---
# TASK-RPT-0024 - M5-02 動態浮水印處理

## 任務目標

建立 MVP2 可驗證的動態浮水印處理規格與 PoC，確保經下載閘道授權的 PDF 必須先套用可追蹤浮水印，才可交付給使用者。此卡的重點不是宣稱 PDF 無法被竄改，而是讓外流可追蹤、竄改可偵測、責任可歸屬、證據可保存。

## 真實功能帶入場景

本演練舊系統採用 Qutora。MVP2 以 Qutora 既有文件下載行為為基準，挑選合成 PDF 與 metadata，經 `TASK-RPT-0023` 下載閘道授權後，產生含動態浮水印的下載副本。浮水印內容至少包含下載人、部門、下載時間、來源 IP、下載序號、報表版本與查核碼。

## 舊系統覆蓋

- 覆蓋 Qutora 文件下載流程中「使用者取得 PDF 檔案」的必要行為。
- 新系統不得繞過 Qutora baseline metadata，也不得直接把未加浮水印的主檔輸出給使用者。
- 若 Qutora 原本沒有浮水印能力，MVP2 應明確記錄這是新增控管，不得把差異誤判為資料搬移失敗。

## 落地設計

### API / Service

| 類型 | 名稱 | 說明 |
| --- | --- | --- |
| Internal Service | `generateWatermarkedCopy(download_id, pdf_id, viewer_context)` | 由下載閘道呼叫，產生單次下載副本。 |
| Internal Service | `resolveWatermarkPolicy(confidentiality_level, report_code)` | 依機密等級與報表代號決定浮水印欄位與強度。 |
| Internal Service | `generateCheckCode(download_id)` | 產生可反查下載紀錄的查核碼或 QR Code payload。 |

### 資料表

| Table | 主要欄位 | 用途 |
| --- | --- | --- |
| `watermark_policy` | `policy_id`, `confidentiality_level`, `required_fields`, `render_mode`, `enabled` | 管理不同機密等級的浮水印政策。 |
| `watermark_job` | `job_id`, `download_id`, `pdf_id`, `status`, `started_at`, `completed_at`, `error_code` | 記錄每次浮水印處理狀態。 |
| `watermark_check_code` | `check_code`, `download_id`, `expires_at`, `payload_hash` | 支援外流文件反查下載事件。 |

### 狀態機

```text
pending -> rendering -> watermarked -> handed_to_hash
pending -> failed_closed
rendering -> failed_closed
```

### 錯誤碼

| Code | 說明 | Fail-Closed |
| --- | --- | --- |
| `WATERMARK_POLICY_MISSING` | 找不到對應浮水印政策。 | Yes |
| `PDF_RENDER_FAILED` | PDF 套印或輸出失敗。 | Yes |
| `FONT_MISSING` | 中文字型或必要字型不可用。 | Yes |
| `CHECK_CODE_FAILED` | 查核碼產生或寫入失敗。 | Yes |
| `AUDIT_FAILED` | 浮水印事件稽核寫入失敗。 | Yes |

### 權限檢查

- 必須先通過 `TASK-RPT-0023` 下載閘道授權，不可直接呼叫浮水印服務輸出檔案。
- 浮水印欄位中的使用者、部門、來源 IP 與下載序號必須來自已驗證的下載上下文，不可由 client 任意傳入。
- 高機密或極高機密政策若尚未定義，預設拒絕下載，不得降級套用一般浮水印。

### 稽核欄位

| 欄位 | 說明 |
| --- | --- |
| `event_type` | `watermark.started`, `watermark.completed`, `watermark.failed_closed` |
| `download_id` | 對應下載請求。 |
| `pdf_id` | 對應 PDF metadata。 |
| `policy_id` | 套用的浮水印政策。 |
| `check_code` | 外流追蹤查核碼。 |
| `payload_hash` | 浮水印事件 payload hash。 |
| `correlation_id` | 跨下載閘道、浮水印、Hash 的追蹤 ID。 |

### Fail-Closed 規則

- 浮水印處理失敗時，不得輸出 PDF。
- 查核碼產生失敗時，不得降級輸出無查核碼副本。
- 稽核寫入失敗時，不得交付檔案。
- 字型缺漏造成浮水印不可讀時，不得視為成功。

## 影響範圍

- 影響 `TASK-RPT-0023` 下載閘道的 `watermark_pending` 與 `ready` 狀態銜接。
- 影響 `TASK-RPT-0025` 下載副本 Hash 的計算時點。
- 影響 PDF library 選型、中文字型封裝、容器映像與 CPU / memory sizing。
- 影響資安、稽核、外流追查與高機密報表下載政策。

## 輸入與輸出

| 類型 | 內容 |
| --- | --- |
| Input | Qutora 合成 PDF、PDF metadata、下載閘道授權結果、使用者上下文、浮水印政策。 |
| Output | 含動態浮水印的下載副本、`watermark_job` 狀態、查核碼、稽核事件、PoC evidence。 |

## 完成定義

- 至少 3 份合成 PDF 可產出含動態浮水印副本。
- 每份副本可從查核碼反查 `download_id` 與使用者上下文。
- 未通過下載閘道授權、浮水印失敗、查核碼失敗、稽核失敗時皆 fail-closed。
- Validators 與 Test Cases 各 10 條皆有 evidence。

## Validators

| ID | Validator | Evidence |
| --- | --- | --- |
| V-0024-01 | 驗證所有浮水印欄位都有來源欄位與不可由 client 覆寫的說明。 | `watermark-field-policy.md` |
| V-0024-02 | 驗證一般、機密、高機密政策至少各有一筆 policy 定義。 | `watermark-policy-sample.json` |
| V-0024-03 | 驗證未授權下載請求無法呼叫浮水印輸出。 | `unauthorized-watermark-block.log` |
| V-0024-04 | 驗證 3 份合成 PDF 產出後肉眼可辨識下載人、時間、序號。 | `watermark-poc-result.md` |
| V-0024-05 | 驗證查核碼可反查 `download_id`。 | `check-code-lookup.log` |
| V-0024-06 | 驗證字型缺漏時狀態為 `failed_closed`。 | `font-missing-fail-closed.log` |
| V-0024-07 | 驗證浮水印事件皆寫入 audit event。 | `watermark-audit-events.jsonl` |
| V-0024-08 | 驗證浮水印失敗不會輸出未加浮水印 PDF。 | `no-raw-pdf-output.log` |
| V-0024-09 | 驗證浮水印副本交給 `TASK-RPT-0025` 後才計算下載副本 Hash。 | `handoff-to-hash.log` |
| V-0024-10 | 驗證 `git diff --check` 無格式錯誤。 | `git-diff-check.log` |

## Test Cases

| ID | Input | 執行方式 | 預期結果 | 阻擋上線條件 |
| --- | --- | --- | --- | --- |
| TC-0024-01 | 一般報表 PDF + 合法下載請求 | 呼叫浮水印服務 | 產出含下載人與下載時間的 PDF | 無浮水印仍交付 |
| TC-0024-02 | 機密報表 PDF + 合法下載請求 | 呼叫浮水印服務 | 產出含查核碼與下載序號的 PDF | 查核碼缺漏 |
| TC-0024-03 | 高機密報表 PDF + 合法下載請求 | 套用高機密 policy | 使用較強浮水印政策或明確拒絕 | 自動降級成一般政策 |
| TC-0024-04 | 未授權下載請求 | 直接呼叫浮水印服務 | 回傳拒絕且無輸出檔案 | 未授權仍輸出 PDF |
| TC-0024-05 | 缺少部門欄位 | 產生浮水印 | 回傳 `WATERMARK_POLICY_MISSING` 或 metadata error | 產出欄位不完整 PDF |
| TC-0024-06 | 字型檔缺漏 | 產生中文浮水印 | 回傳 `FONT_MISSING` 並 fail-closed | 產出亂碼或不可讀浮水印 |
| TC-0024-07 | 查核碼服務失敗 | 產生浮水印 | 回傳 `CHECK_CODE_FAILED` 並 fail-closed | 無查核碼仍交付 |
| TC-0024-08 | 稽核寫入失敗 | 產生浮水印 | 回傳 `AUDIT_FAILED` 並 fail-closed | 稽核失敗仍交付 |
| TC-0024-09 | 同一 PDF 兩次下載 | 產生兩份副本 | 兩份副本下載序號與查核碼不同 | 重用相同追蹤碼 |
| TC-0024-10 | 3 份 PDF 批次處理 | 執行 PoC 批次 | 成功率、耗時與錯誤紀錄可量測 | 沒有效能與錯誤 evidence |

## Reviewer / Human Gate / ADR

- Reviewer：QA / Security / DevOps、QA / Security / DevOps。
- Human Gate：若要把高機密報表從「拒絕下載」改成「可下載」，必須人類資安 / 稽核簽核。
- ADR Gate：正式 PDF library、數位簽章、timestamp、極高機密安全預覽需 ADR。

## Notes

## 2026-07-08 落地補強：M5-02 動態浮水印

本卡是 M5-02 的唯一實作契約；Hash 持久化由 `TASK-RPT-0025` 承擔。

### Watermark Fields

| 欄位 | 來源 | 必填 |
| --- | --- | --- |
| viewer_name / viewer_id | session user profile | Yes |
| department | user attribute 或 Data Scope context | Yes |
| role_names | authorization context | Yes |
| download_time | server time | Yes |
| source_ip | request context | Yes |
| download_id | `TASK-RPT-0023` | Yes |
| report_code / report_version | PDF metadata | Yes |
| confidentiality_level | PDF metadata | Yes |
| check_code / QR payload | `generateCheckCode(download_id)` | Yes |
| environment_marker | config：dev / test / pilot / prod | Yes |

### Master / Copy Flow

```text
master_pdf immutable
  -> authorize by download gateway
  -> create transient working copy
  -> render watermark using server-side fields
  -> write watermarked copy
  -> hand off stream to TASK-RPT-0025 for copy_hash
  -> deliver only after audit + copy_hash success
```

- master PDF 不得被覆寫。
- 未浮水印副本不得被傳回 client。
- working copy 若未完成 hash 與 audit，必須清理或標記 `failed_closed`。

### Hash Timing

| Hash | 計算時點 | Owner |
| --- | --- | --- |
| `master_hash` | PDF ingest / baseline 建立時 | `TASK-RPT-0019` / `TASK-RPT-0021` |
| `watermark_payload_hash` | watermark job 開始前，針對欄位 payload | `TASK-RPT-0024` |
| `copy_hash` | 浮水印渲染完成後、交付前 | `TASK-RPT-0025` |
| `audit_payload_hash` | audit event 寫入前 | `TASK-RPT-0010` / `TASK-RPT-0025` |

### Failure Handling

- policy missing、font missing、render failed、check code failed、audit failed、hash handoff failed：一律 `failed_closed`，不得輸出 PDF。
- 使用者看見安全錯誤碼；內部錯誤細節只寫入 evidence / audit reference，不回傳 stack trace。
- 同一 master PDF 被同一使用者下載兩次，也應產生不同 `download_id` 與可追蹤副本；若 `copy_hash` 相同，必須記錄 watermark payload 完全相同的原因。

### Performance Considerations

- PDF 以 stream 處理，避免整檔載入記憶體。
- 大檔或批次下載走 async job；`GET /file` 只取 `ready` 狀態。
- 字型與 watermark template 可快取，但 watermark payload 不可跨請求共用。
- MVP2 至少要有 3 份一般 PDF 與 1 次大檔 / 批次壓力證據；Pilot 補 50MB 或 20 files batch 證據。

- PDF 浮水印只能提高移除成本、降低外流意願、留下追蹤線索與支援竄改偵測，不得寫成絕對防竄改。
- 本卡依 Agent Team 計畫書分派 role、reviewer、validator、human sign-off 與 ADR gate。
