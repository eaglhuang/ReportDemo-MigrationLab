---
task_id: TASK-RPT-0010
source_milestone: M1-04
title: "建立稽核寫入基礎"
status: planned
owner: backend-dba
priority: P0
milestone: M1
drill_stage: "MVP2"
primary_role: "QA / Security / DevOps"
support_roles:
  - "Tech Lead / Captain"
  - "Backend / DBA"
depends_on:
  - "TASK-RPT-0007"
related_plan: "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
drill_plan: "drills/分階段演練與驗收計畫.md"
evidence_path: "evidence/MVP2/TASK-RPT-0010/"
scopePaths:
  - "tasks/TASK-RPT-0010-m1-04-audit-write-foundation.task.md"
  - "evidence/MVP2/TASK-RPT-0010/**"
  - "open-source-sandbox/qutora-api/Qutora.Domain/Entities/AuditLog.cs"
  - "open-source-sandbox/qutora-api/Qutora.Application/Middleware/AuditLoggingMiddleware.cs"
deliverables:
  - "evidence/MVP2/TASK-RPT-0010/audit-event-schema.md"
  - "evidence/MVP2/TASK-RPT-0010/fail-closed-matrix.md"
  - "evidence/MVP2/TASK-RPT-0010/audit-sample-events.md"
validators:
  - "V-0010-01"
  - "V-0010-02"
  - "V-0010-03"
  - "V-0010-04"
  - "V-0010-05"
  - "V-0010-06"
  - "V-0010-07"
  - "V-0010-08"
  - "V-0010-09"
  - "V-0010-10"
evidence:
  required: command-backed
rollback:
  strategy: block-operation-when-audit-is-unavailable
  notes: "關鍵操作 audit 寫入失敗時 fail-closed；一般查詢可進 retry queue，但不得靜默遺失。"
outOfScope:
  - "完整 WORM / Hash Chain 實作"
  - "正式 SIEM 整合"
  - "長期稽核保存政策定案"
nonGoals:
  - "取代 M7-01 稽核查詢與 Hash Chain"
---
# TASK-RPT-0010 - M1-04 建立稽核寫入基礎

## 任務目標

定義 MVP2 所需的最小稽核事件 schema、寫入規則、fail-closed 邊界與 evidence 格式，支援匯入批次、staging、下載閘道、浮水印與下載副本 hash。

## 真實功能帶入場景

以 Qutora `AuditLog` 與 middleware 為舊系統參考，定義新系統 MVP2 的 audit event：import batch、staging validation、download request、watermark generation、download hash。

## 舊系統覆蓋

| Qutora 來源 | 新系統 audit 對應 | 用途 |
| --- | --- | --- |
| `AuditLog` | `audit_event` | 事件主表。 |
| `AuditLoggingMiddleware` | audit writer policy | 參考自動記錄方式。 |
| User / document id | subject / object | 下載與資料追蹤。 |

## 落地設計

| 項目 | 定義 |
| --- | --- |
| API | 內部 audit writer interface；MVP2 可先文件化。 |
| 資料表 | `audit_event`，欄位含 event_id、event_type、actor_id、object_type、object_id、batch_id、result、payload_hash、created_at。 |
| 狀態機 | `accepted`、`persisted`、`retry_pending`、`failed_closed`。 |
| 錯誤碼 | `AUDIT_UNAVAILABLE`、`AUDIT_PAYLOAD_INVALID`、`AUDIT_HASH_FAILED`、`AUDIT_RETRY_EXHAUSTED`。 |
| 權限檢查 | 只有系統服務帳號可寫；查詢需 auditor / reviewer。 |
| 稽核欄位 | actor、action、object、correlation_id、ip、user_agent、result、payload_hash。 |
| fail-closed | 下載、權限變更、break-glass、批次 close 的 audit 寫入失敗時，不得回傳成功。 |

## 影響範圍

- 影響 `TASK-RPT-0023` 下載閘道、`TASK-RPT-0024` 浮水印、`TASK-RPT-0025` 下載副本 hash。
- 影響 MVP2 Gate 是否可證明敏感操作沒有靜默遺失。
- 不取代 M7-01 Hash Chain。

## 輸入與輸出

| 類型 | 內容 |
| --- | --- |
| 輸入 | Qutora audit 盤點、import batch 狀態、下載 / 浮水印 PoC 事件需求。 |
| 輸出 | audit event schema、fail-closed matrix、sample events。 |

## 完成定義

- MVP2 所有敏感操作都有 audit event type。
- fail-closed 與 retry 邊界明確。
- 每個 sample event 有 payload hash 或替代 integrity 欄位。

## Validators

| ID | 輸入條件 | 執行方式 / Evidence | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| V-0010-01 | Qutora audit 來源可讀 | 檢查 AuditLog / middleware | 舊系統參考明確 | 來源不明 |
| V-0010-02 | import batch 事件需求 | 定義 event type | batch 事件完整 | 缺 close / fail |
| V-0010-03 | download 事件需求 | 定義 event type | 下載成功/拒絕/失敗都有事件 | 只記成功 |
| V-0010-04 | watermark 事件需求 | 定義 event type | 產生 / 失敗都有事件 | 失敗無 audit |
| V-0010-05 | payload hash 規則 | 檢查 hash 定義 | 可重算 | hash 規則不明 |
| V-0010-06 | fail-closed matrix | 模擬 audit fail | 關鍵操作拒絕 | 關鍵操作仍成功 |
| V-0010-07 | retry 規則 | 檢查一般查詢事件 | 不靜默遺失 | 靜默丟棄 |
| V-0010-08 | 權限規則 | 檢查 writer / reader | 寫查分離 | 權限過寬 |
| V-0010-09 | sample events | 抽查 5 筆 sample | 欄位完整 | 欄位缺失 |
| V-0010-10 | evidence 路徑正確 | 檢查 `evidence/MVP2/TASK-RPT-0010/` | 符合 RB-03 | evidence 散落 |

## Test Cases

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| TC-0010-01 | batch created | 產生 audit sample | 有 batch_id / actor | 缺 batch |
| TC-0010-02 | batch failed | 產生 audit sample | result = failed | 失敗無紀錄 |
| TC-0010-03 | download allowed | 產生 audit sample | 有 document id / result | 缺 object |
| TC-0010-04 | download denied | 產生 audit sample | result = denied | 只記成功 |
| TC-0010-05 | watermark success | 產生 audit sample | 有 watermark serial | 缺序號 |
| TC-0010-06 | watermark fail | 模擬 PDF library fail | audit + fail-closed | 回傳未處理 PDF |
| TC-0010-07 | audit unavailable | 模擬寫入失敗 | 關鍵操作 rejected | 操作成功 |
| TC-0010-08 | payload tamper | 重算 hash | mismatch 可偵測 | mismatch 不可見 |
| TC-0010-09 | auditor 查詢 | 檢查查詢權限 | auditor 可查 | 查詢被阻擋 |
| TC-0010-10 | non-auditor 查詢 | 檢查查詢權限 | 拒絕 | 越權可查 |

## Reviewer / Human Gate / ADR

| 項目 | 規則 |
| --- | --- |
| Reviewer | QA / Security / DevOps 主審；Backend / DBA 複核資料表與 hash。 |
| Human Gate | 若要放寬關鍵操作 fail-closed，必須人類與稽核簽核。 |
| ADR | 若 audit DB 獨立、WORM 或 Hash Chain 範圍提前定案，需更新 ADR-006。 |

## Notes

- 2026-07-07 | upgraded | MVP2 核心卡完整格式升級，evidence 改為 `evidence/MVP2/TASK-RPT-0010/`。
