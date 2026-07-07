---
task_id: TASK-RPT-0014
source_milestone: M2-04
title: "建立 Data Scope 基礎規則"
status: planned
owner: "QA / Security / DevOps"
priority: P0
milestone: M2
drill_stage: "MVP2"
execution_mode: "ai-with-human-review"
primary_role: "QA / Security / DevOps"
closure_reviewer: "Tech Lead / Captain"
support_roles:
  - "Tech Lead / Captain"
  - "Backend / DBA"
depends_on:
  - "TASK-RPT-0010"
  - "TASK-RPT-0008"
related_plan: "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
drill_plan: "drills/分階段演練與驗收計畫.md"
evidence_path: "evidence/MVP2/TASK-RPT-0014/"
scopePaths:
  - "tasks/TASK-RPT-0014-m2-04-data-scope-foundation.task.md"
  - "evidence/MVP2/TASK-RPT-0014/**"
  - "open-source-sandbox/qutora-api/Qutora.Domain/Entities/BucketPermission.cs"
  - "open-source-sandbox/qutora-api/Qutora.Application/Services/DocumentAuthorizationService.cs"
deliverables:
  - "evidence/MVP2/TASK-RPT-0014/data-scope-rule-model.md"
  - "evidence/MVP2/TASK-RPT-0014/permission-matrix.md"
  - "evidence/MVP2/TASK-RPT-0014/negative-access-tests.md"
validators:
  - "V-0014-01"
  - "V-0014-02"
  - "V-0014-03"
  - "V-0014-04"
  - "V-0014-05"
  - "V-0014-06"
  - "V-0014-07"
  - "V-0014-08"
  - "V-0014-09"
  - "V-0014-10"
evidence:
  required: command-backed
rollback:
  strategy: deny-by-default-when-scope-unknown
  notes: "Data Scope 規則不明時一律拒絕下載或查詢，不得用全域允許作 fallback。"
outOfScope:
  - "完整 Admin UI"
  - "正式 AD 群組同步"
  - "break-glass 流程"
nonGoals:
  - "取代 M8-02 Data Scope 管理"
---
# TASK-RPT-0014 - M2-04 建立 Data Scope 基礎規則

## 任務目標

定義 MVP2 下載與查詢所需的最小 Data Scope 規則，讓 Role 控制「可做什麼」，Data Scope 控制「可看哪些資料」，並以 deny-by-default 防止越權。

## 真實功能帶入場景

以 Qutora bucket permission、document authorization 與合成 PDF metadata 中的 department / confidentiality 作為演練基礎，設計 MVP2 的 Data Scope 判定矩陣。

## 舊系統覆蓋

| Qutora 來源 | Data Scope 對應 | 用途 |
| --- | --- | --- |
| `BucketPermission` | bucket scope | 儲存區權限。 |
| `DocumentAuthorizationService` | authorization decision | 下載 / 查詢授權參考。 |
| Metadata department | department scope | 部門範圍。 |
| Metadata confidentiality | confidentiality scope | 機密等級。 |

## 落地設計

| 項目 | 定義 |
| --- | --- |
| API | MVP2 先定義 `canAccess(user, action, document)` contract；實作可延後。 |
| 資料表 | `role_permission`、`data_scope_assignment`、`document_scope_projection`。 |
| 狀態機 | scope assignment：`draft`、`active`、`revoked`。 |
| 錯誤碼 | `SCOPE_NOT_FOUND`、`SCOPE_DENIED`、`ROLE_DENIED`、`CONFIDENTIALITY_DENIED`。 |
| 權限檢查 | 先驗 Role，再驗 Data Scope，再驗機密等級。 |
| 稽核欄位 | user_id、role、scope_rule_id、document_id、decision、reason、correlation_id。 |
| fail-closed | scope 不存在、metadata 不完整、規則衝突時拒絕存取。 |

## 影響範圍

- 直接影響 `TASK-RPT-0023` 下載閘道授權。
- 影響 `TASK-RPT-0024` 浮水印欄位與下載人責任歸屬。
- 影響 Pilot 的跨部門與高機密負向測試。
- 不建立完整 Admin 管理介面。

## 輸入與輸出

| 類型 | 內容 |
| --- | --- |
| 輸入 | Qutora permission 盤點、metadata baseline、audit event schema。 |
| 輸出 | Data Scope rule model、permission matrix、negative access tests。 |

## 完成定義

- Role 與 Data Scope 已清楚分離。
- 至少包含部門、bucket、機密等級三種 scope 因素。
- 有權限與無權限案例皆有 audit。
- scope unknown 時 fail-closed。

## Validators

| ID | 輸入條件 | 執行方式 / Evidence | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| V-0014-01 | Qutora permission 可讀 | 檢查 bucket permission | 舊系統參考明確 | 來源不明 |
| V-0014-02 | metadata 可用 | 檢查 department / confidentiality | scope 欄位可用 | 欄位缺失 |
| V-0014-03 | role model 完成 | 檢查 role_permission | action 與 scope 分離 | role 自動取得資料 |
| V-0014-04 | scope assignment 完成 | 檢查狀態機 | 可 revoke | 無撤銷 |
| V-0014-05 | decision order 完成 | 檢查 Role -> Scope -> Confidentiality | 順序明確 | 規則衝突 |
| V-0014-06 | error code 完成 | 模擬拒絕案例 | 可分類原因 | 只回 generic error |
| V-0014-07 | audit 規則完成 | 檢查 decision audit | 拒絕也記錄 | 拒絕無 audit |
| V-0014-08 | fail-closed 完成 | scope missing | 拒絕 | fallback allow |
| V-0014-09 | negative tests 完成 | 檢查測試矩陣 | 至少 5 個負向案例 | 負向不足 |
| V-0014-10 | evidence 路徑正確 | 檢查 `evidence/MVP2/TASK-RPT-0014/` | 符合 RB-03 | evidence 散落 |

## Test Cases

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| TC-0014-01 | user 有 download role + same dept | 判斷 access | allow | 合法被拒且無說明 |
| TC-0014-02 | user 無 download role | 判斷 access | `ROLE_DENIED` | 越權成功 |
| TC-0014-03 | user 有 role 但跨部門 | 判斷 access | `SCOPE_DENIED` | 越權成功 |
| TC-0014-04 | user 有 role 但高機密不足 | 判斷 access | `CONFIDENTIALITY_DENIED` | 越權成功 |
| TC-0014-05 | document metadata 缺部門 | 判斷 access | fail-closed | fallback allow |
| TC-0014-06 | scope revoked | 判斷 access | denied | revoke 無效 |
| TC-0014-07 | admin 管理權限 | 判斷 report access | 不自動取得內容權限 | admin 越權看內容 |
| TC-0014-08 | audit 寫入失敗 | 判斷敏感下載 | fail-closed | 下載成功 |
| TC-0014-09 | reason code 檢查 | 檢查拒絕訊息 | 不洩漏敏感資料 | 訊息洩漏 |
| TC-0014-10 | reviewer 抽查矩陣 | 檢查 6 個案例 | 結果一致 | 矩陣不可重現 |

## Reviewer / Human Gate / ADR

| 項目 | 規則 |
| --- | --- |
| Reviewer | QA / Security / DevOps 主審；Tech Lead / Captain 確認職責分離。 |
| Human Gate | 若 Admin 是否可看報表內容、極高機密是否可下載仍未決，需人類簽核。 |
| ADR | 權限模型或 Admin 職責分離若調整，需更新 ADR-005。 |

## Notes

- 2026-07-07 | upgraded | MVP2 核心卡完整格式升級，evidence 改為 `evidence/MVP2/TASK-RPT-0014/`。
