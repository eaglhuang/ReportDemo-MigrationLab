---
task_id: TASK-RPT-0023
source_milestone: M5-01
title: "建立下載閘道"
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
  - "TASK-RPT-0014"
  - "TASK-RPT-0019"
  - "TASK-RPT-0010"
related_plan: "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
drill_plan: "drills/分階段演練與驗收計畫.md"
evidence_path: "evidence/MVP2/TASK-RPT-0023/"
scopePaths:
  - "src/**"
  - "tasks/TASK-RPT-0023-m5-01-download-gateway.task.md"
  - "evidence/MVP2/TASK-RPT-0023/**"
  - "runbooks/RB-05-mariadb-environment.md"
  - "poc/download-gateway/**"
  - "poc/validators/**"
deliverables:
  - "evidence/MVP2/TASK-RPT-0023/download-gateway-api.md"
  - "evidence/MVP2/TASK-RPT-0023/download-state-machine.md"
  - "evidence/MVP2/TASK-RPT-0023/fail-closed-test-result.md"
  - "evidence/MVP2/TASK-RPT-0023/src-build-test-result.md"
validators:
  - "V-0023-01"
  - "V-0023-02"
  - "V-0023-03"
  - "V-0023-04"
  - "V-0023-05"
  - "V-0023-06"
  - "V-0023-07"
  - "V-0023-08"
  - "V-0023-09"
  - "V-0023-10"
evidence:
  required: command-backed
rollback:
  strategy: disable-new-download-route-and-return-to-qutora
  notes: "下載閘道失敗時停用新下載路徑，回到 Qutora 舊路徑；不得直接暴露主檔儲存位置。"
outOfScope:
  - "正式 signed URL 供應商整合"
  - "高機密安全預覽"
  - "長期下載副本保存"
nonGoals:
  - "繞過 Data Scope 直接下載"
---
# TASK-RPT-0023 - M5-01 建立下載閘道

## 任務目標

定義 MVP2 下載閘道落地規格，確保所有 PDF 下載都經過授權、Data Scope、metadata、audit、watermark 與 hash 流程，不得直接存取主檔。

## 真實功能帶入場景

使用 MVP1 Qutora baseline PDF 與 MVP2 MariaDB metadata，模擬使用者透過新系統下載 PDF。下載成功前必須通過 Role、Data Scope、metadata ready、audit writable 與 watermark-ready 檢查。

## 舊系統覆蓋

| Qutora 來源 | 新下載閘道對應 | 用途 |
| --- | --- | --- |
| Qutora download | legacy baseline | 比對下載結果與 hash。 |
| Document id | pdf_id / legacy_document_id | 下載對象。 |
| Permission | Data Scope decision | 授權判斷。 |
| AuditLog | download audit | 操作追蹤。 |

## 落地設計

| 項目 | 定義 |
| --- | --- |
| API | `POST /api/download-requests` 建立請求；`GET /api/download-requests/{id}/file` 取檔。 |
| 資料表 | `download_request`、`download_decision`、`download_error`。 |
| 狀態機 | `requested`、`authorized`、`watermark_pending`、`hashing`、`ready`、`delivered`、`denied`、`failed_closed`、`expired`、`cancelled`。 |
| 錯誤碼 | `AUTH_REQUIRED`、`AUTH_DENIED`、`SCOPE_DENIED`、`PDF_NOT_READY`、`AUDIT_FAILED`、`WATERMARK_FAILED`、`HASH_FAILED`、`RATE_LIMITED`、`REQUEST_EXPIRED`、`REQUEST_CANCELLED`、`STATE_CONFLICT`。 |
| 權限檢查 | 先驗 session / role，再驗 Data Scope，再驗機密等級，再驗 audit writable。 |
| 稽核欄位 | download_id、user_id、ip、user_agent、pdf_id、version、decision、reason、correlation_id。 |
| fail-closed | 權限不明、metadata invalid、audit fail、watermark fail、hash fail 時不得回傳 PDF。 |

## 影響範圍

- 直接影響 `TASK-RPT-0024` 動態浮水印與 `TASK-RPT-0025` 下載副本 hash。
- 影響 Pilot 下載平行作業。
- 不暴露 object storage / NAS 直接路徑。

## 輸入與輸出

| 類型 | 內容 |
| --- | --- |
| 輸入 | PDF metadata、Data Scope decision、audit writer、Qutora baseline PDF。 |
| 輸出 | API contract、狀態機、錯誤碼、fail-closed test result。 |

## 完成定義

- 所有下載都有 download_id 與 audit。
- 未授權、audit fail、watermark fail 不得回傳 PDF。
- 主檔不可被直接下載。
- `src/ReportDemo.DownloadGateway` 實作需通過 `src/README.md` 的 build / test contract。

## Validators

| ID | 輸入條件 | 執行方式 / Evidence | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| V-0023-01 | API contract | 檢查 request/response | 欄位完整 | contract 不明 |
| V-0023-02 | metadata ready | 模擬合法下載 | 狀態到 ready | 無 ready |
| V-0023-03 | role denied | 模擬無 role | `AUTH_DENIED` | 越權成功 |
| V-0023-04 | scope denied | 模擬跨部門 | `SCOPE_DENIED` | 越權成功 |
| V-0023-05 | pdf invalid | metadata invalid | `PDF_NOT_READY` | 仍下載 |
| V-0023-06 | audit fail | 模擬 audit unavailable | `AUDIT_FAILED` + fail-closed | 仍下載 |
| V-0023-07 | watermark fail | 模擬 watermark fail | `WATERMARK_FAILED` + fail-closed | 回傳未浮水印 PDF |
| V-0023-08 | hash fail | 模擬 hash fail | `HASH_FAILED` + fail-closed | 回傳檔案 |
| V-0023-09 | audit 欄位 | 檢查 sample event | 欄位完整 | 缺 user/ip/pdf |
| V-0023-10 | evidence path | 檢查 `evidence/MVP2/TASK-RPT-0023/` | 符合 RB-03 | evidence 散落 |

## Test Cases

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| TC-0023-01 | 合法使用者 | 建立下載請求 | 回傳 download_id | 無 id |
| TC-0023-02 | 合法請求 | 取檔 | 狀態 delivered | 取檔失敗 |
| TC-0023-03 | 無 role | 建立請求 | denied | 成功 |
| TC-0023-04 | 跨部門 | 建立請求 | denied | 成功 |
| TC-0023-05 | 高機密不足 | 建立請求 | denied | 成功 |
| TC-0023-06 | audit fail | 建立請求 | failed_closed | 成功 |
| TC-0023-07 | watermark fail | 取檔 | failed_closed | 回傳 PDF |
| TC-0023-08 | hash fail | 取檔 | failed_closed | 回傳 PDF |
| TC-0023-09 | 直接 storage path | 嘗試存取 | 不可取得 | 可直接下載 |
| TC-0023-10 | reviewer 抽查 | 查 audit + state | 可追溯 | 不可追蹤 |

## Reviewer / Human Gate / ADR

| 項目 | 規則 |
| --- | --- |
| Reviewer | Backend / DBA 產出，QA / Security / DevOps 對負向測試具 blocking 權限。 |
| Human Gate | 若下載 URL TTL、signed URL 或 session 模式需定案，需人類簽核。 |
| ADR | API session / signed URL 策略需對應 ADR-003。 |

## Notes

## 2026-07-08 落地補強：M5-01 下載閘道

本卡是 M5-01 的唯一實作契約。階段計畫與每日派工單只引用本卡，不重貼本段。

### API Contract

| API | 用途 | 必要檢查 |
| --- | --- | --- |
| `POST /api/download-requests` | 建立下載請求並回傳 `download_id` | session、role、Data Scope、PDF metadata ready、audit writable |
| `GET /api/download-requests/{download_id}` | 查詢狀態 | requester 或具 audit / admin 權限 |
| `GET /api/download-requests/{download_id}/file` | 只在 `ready` 狀態交付浮水印副本 | request ownership、copy_hash recorded、audit pre-delivery written |
| `POST /api/download-requests/{download_id}/cancel` | 取消尚未交付的請求 | request ownership、狀態仍可取消 |

### Tables

| Table | Required Fields |
| --- | --- |
| `download_request` | `download_id`, `pdf_id`, `requester_user_id`, `role_ids`, `data_scope_id`, `status`, `correlation_id`, `created_at`, `expires_at` |
| `download_decision` | `decision_id`, `download_id`, `decision`, `reason_code`, `decided_by`, `decided_at`, `payload_hash` |
| `download_error` | `error_id`, `download_id`, `error_code`, `safe_message`, `internal_detail_ref`, `created_at` |
| `download_audit_event` | `event_id`, `download_id`, `event_type`, `user_id`, `ip`, `user_agent`, `pdf_id`, `report_code`, `report_version`, `decision`, `reason_code`, `master_hash`, `copy_hash`, `correlation_id`, `payload_hash`, `created_at` |

### State Machine

```text
requested -> authorized -> watermark_pending -> hashing -> ready -> delivered
requested -> denied
authorized -> failed_closed
watermark_pending -> failed_closed
hashing -> failed_closed
ready -> expired
requested -> cancelled
authorized -> cancelled
```

### Error Codes

`AUTH_REQUIRED`, `AUTH_DENIED`, `SCOPE_DENIED`, `PDF_NOT_READY`, `AUDIT_FAILED`, `WATERMARK_FAILED`, `HASH_FAILED`, `RATE_LIMITED`, `REQUEST_EXPIRED`, `REQUEST_CANCELLED`, `STATE_CONFLICT`.

### Fail-Closed Rules

- 權限未知、role / Data Scope 無法判定、PDF metadata 缺漏、master hash 缺漏、audit writer 不可用、watermark policy 不可用、watermark job 失敗、copy hash 未完成或 mismatch：一律不得輸出檔案。
- `GET /file` 不得直接讀 master PDF；只能讀已完成浮水印且已記錄 `copy_hash` 的副本。
- 任何 denied / failed_closed 都必須先寫 audit；audit 寫入失敗時只回錯誤碼，不回檔案。

### Blocking Test Cases

| ID | Input | 執行方式 | 預期結果 | 阻擋上線條件 |
| --- | --- | --- | --- | --- |
| TC-0023-B01 | 合法使用者、scope 內 PDF | `POST` 建請求後 `GET /file` | `delivered`，有 audit、watermark、copy_hash | 任一證據缺漏 |
| TC-0023-B02 | 未登入 | `POST /api/download-requests` | `AUTH_REQUIRED`，無檔案 | 回傳下載或建立 request |
| TC-0023-B03 | role 不符 | `POST /api/download-requests` | `AUTH_DENIED`，有 denied audit | 越權成功 |
| TC-0023-B04 | Data Scope 外 PDF | `POST /api/download-requests` | `SCOPE_DENIED`，有 denied audit | 越權成功 |
| TC-0023-B05 | audit writer unavailable | 建請求或取檔 | `AUDIT_FAILED`，無檔案 | audit fail 仍可下載 |

- 2026-07-07 | upgraded | MVP2 核心卡完整格式升級，evidence 改為 `evidence/MVP2/TASK-RPT-0023/`。
