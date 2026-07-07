---
task_id: TASK-RPT-0023
source_milestone: M5-01
title: "建立下載閘道"
status: planned
owner: backend-security
priority: P0
milestone: M5
drill_stage: "MVP2"
execution_mode: "ai-with-human-review"
primary_role: "Backend / DBA"
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
  - "tasks/TASK-RPT-0023-m5-01-download-gateway.task.md"
  - "evidence/MVP2/TASK-RPT-0023/**"
  - "runbooks/RB-05-mariadb-environment.md"
  - "poc/download-gateway/**"
  - "poc/validators/**"
deliverables:
  - "evidence/MVP2/TASK-RPT-0023/download-gateway-api.md"
  - "evidence/MVP2/TASK-RPT-0023/download-state-machine.md"
  - "evidence/MVP2/TASK-RPT-0023/fail-closed-test-result.md"
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
| 狀態機 | `requested`、`authorized`、`watermark_pending`、`ready`、`delivered`、`denied`、`failed_closed`。 |
| 錯誤碼 | `AUTH_DENIED`、`SCOPE_DENIED`、`PDF_NOT_READY`、`AUDIT_FAILED`、`WATERMARK_FAILED`、`HASH_FAILED`。 |
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

- 2026-07-07 | upgraded | MVP2 核心卡完整格式升級，evidence 改為 `evidence/MVP2/TASK-RPT-0023/`。
