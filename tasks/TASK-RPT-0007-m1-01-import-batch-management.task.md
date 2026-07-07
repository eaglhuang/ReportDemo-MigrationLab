---
task_id: TASK-RPT-0007
source_milestone: M1-01
title: "建立匯入批次管理"
status: planned
owner: "Backend / DBA"
priority: P0
milestone: M1
drill_stage: "MVP2"
execution_mode: "ai-with-human-review"
primary_role: "Backend / DBA"
closure_reviewer: "Tech Lead / Captain"
support_roles:
  - "Tech Lead / Captain"
  - "QA / Security / DevOps"
depends_on:
  - "TASK-RPT-0001"
  - "TASK-RPT-0002"
  - "TASK-RPT-0003"
related_plan: "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
drill_plan: "drills/分階段演練與驗收計畫.md"
evidence_path: "evidence/MVP2/TASK-RPT-0007/"
scopePaths:
  - "tasks/TASK-RPT-0007-m1-01-import-batch-management.task.md"
  - "evidence/MVP2/TASK-RPT-0007/**"
  - "evidence/MVP1/TASK-RPT-0002/**"
  - "evidence/MVP1/TASK-RPT-0003/**"
deliverables:
  - "evidence/MVP2/TASK-RPT-0007/import-batch-state-design.md"
  - "evidence/MVP2/TASK-RPT-0007/qutora-extract-batch-plan.md"
  - "evidence/MVP2/TASK-RPT-0007/retry-and-rollback-notes.md"
validators:
  - "V-0007-01"
  - "V-0007-02"
  - "V-0007-03"
  - "V-0007-04"
  - "V-0007-05"
  - "V-0007-06"
  - "V-0007-07"
  - "V-0007-08"
  - "V-0007-09"
  - "V-0007-10"
evidence:
  required: command-backed
rollback:
  strategy: disable-import-batch-and-delete-staging-run
  notes: "MVP2 僅設計與演練批次，不碰正式資料；若批次失敗，標記 failed 並丟棄該批 staging。"
outOfScope:
  - "正式 CDC / ETL 上線"
  - "使用未脫敏正式資料"
  - "修改 Qutora 原始碼"
nonGoals:
  - "建立完整排程平台"
---
# TASK-RPT-0007 - M1-01 建立匯入批次管理

## 任務目標

定義 Qutora 舊系統資料抽取到 MariaDB staging 的最小批次管理規格，讓 MVP2 可以重跑、追蹤、失敗回復與產出 evidence。

## 真實功能帶入場景

從 MVP1 的 Qutora document / metadata / audit baseline 選取一批合成資料，建立 import batch 設計，記錄批次狀態、來源範圍、筆數、hash、錯誤、重跑與 rollback 規則。

## 舊系統覆蓋

| 舊系統來源 | 承接方式 | 備註 |
| --- | --- | --- |
| Qutora `Document` | batch source scope | 以 legacy document id 作主 reference。 |
| Qutora `Metadata` | batch item metadata | 作 MariaDB staging 輸入。 |
| Qutora `AuditLog` | evidence reference | 驗證抽取操作可追蹤。 |

## 落地設計

| 項目 | 定義 |
| --- | --- |
| API | MVP2 可先用 CLI / script 觸發；正式 API 延後。 |
| 資料表 | `import_batch`、`import_batch_item`、`import_batch_error`。 |
| 狀態機 | `created` -> `extracting` -> `staged` -> `validated` -> `closed`；失敗為 `failed`，重跑為新 batch。 |
| 錯誤碼 | `SRC_UNAVAILABLE`、`DUPLICATE_LEGACY_ID`、`METADATA_INVALID`、`HASH_MISMATCH`、`AUDIT_WRITE_FAILED`。 |
| 權限檢查 | 只有 migration operator 可建立批次；讀取需 reviewer 或 auditor role。 |
| 稽核欄位 | batch_id、source_system、requested_by、started_at、finished_at、status、item_count、source_hash。 |
| fail-closed | audit 寫入失敗、來源範圍不明、批次 hash 不可重算時，批次不得 close。 |

## 影響範圍

- 影響 `TASK-RPT-0008` MariaDB staging table 設計。
- 影響 `TASK-RPT-0010` audit write foundation。
- 影響 `TASK-RPT-0023` 下載閘道可追溯的來源批次。
- 不修改 Qutora、不跑正式 migration。

## 輸入與輸出

| 類型 | 內容 |
| --- | --- |
| 輸入 | MVP1 Qutora DB inventory、Golden Dataset、metadata export、PDF hash manifest。 |
| 輸出 | import batch 狀態設計、抽取批次規格、retry / rollback notes。 |

## 完成定義

- 批次狀態、錯誤碼、重跑與 rollback 規則可被 reviewer 判斷。
- 每一批資料都有 source scope、item count、hash、operator、evidence。
- 無 audit 或 hash 的批次不得被視為成功。

## Validators

| ID | 輸入條件 | 執行方式 / Evidence | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| V-0007-01 | MVP1 baseline 完成 | 檢查 source scope | batch source 明確 | source 不明 |
| V-0007-02 | document ids 可用 | 檢查 legacy id 清單 | 無重複 | 重複未處理 |
| V-0007-03 | metadata 可用 | 檢查 batch item 欄位 | 欄位完整 | 缺核心欄位 |
| V-0007-04 | hash manifest 可用 | 設計 source_hash | 可重算 | hash 規則不明 |
| V-0007-05 | 狀態機完成 | 檢查狀態轉移 | 無跳狀態 | 可跳過 validation |
| V-0007-06 | 錯誤碼完成 | 模擬 3 種錯誤 | 錯誤可分類 | 靜默失敗 |
| V-0007-07 | 權限規則完成 | 檢查 operator / reviewer | 職責分離 | 任意人可 close |
| V-0007-08 | audit 規則完成 | 檢查 audit 欄位 | 可追蹤操作者 | audit 缺失 |
| V-0007-09 | rollback 規則完成 | 檢查 failed batch 行為 | 可丟棄 staging | 污染下一批 |
| V-0007-10 | evidence 路徑正確 | 檢查 `evidence/MVP2/TASK-RPT-0007/` | 符合 RB-03 | evidence 散落 |

## Test Cases

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| TC-0007-01 | 3 筆 Qutora document | 建立 batch design | item_count = 3 | 筆數不明 |
| TC-0007-02 | 重複 legacy id | 模擬建立 batch | 回傳 `DUPLICATE_LEGACY_ID` | 重複仍成功 |
| TC-0007-03 | 缺 metadata | 模擬 item validate | 回傳 `METADATA_INVALID` | 缺欄仍 staged |
| TC-0007-04 | hash 不一致 | 模擬 hash check | 回傳 `HASH_MISMATCH` | hash mismatch 被忽略 |
| TC-0007-05 | audit 寫入失敗 | 模擬 close batch | fail-closed | close 成功 |
| TC-0007-06 | operator 建立批次 | 檢查權限 | 可建立 | operator 無法建立 |
| TC-0007-07 | 非 operator 建立批次 | 檢查權限 | 拒絕 | 越權成功 |
| TC-0007-08 | failed batch | 執行重跑設計 | 新 batch id | 覆蓋原 batch |
| TC-0007-09 | reviewer 查 evidence | 抽查 batch 記錄 | 可追溯 | evidence 不足 |
| TC-0007-10 | Gate review | 檢查所有 validators | 可進入 staging 設計 | 任一 P0 缺口 |

## Reviewer / Human Gate / ADR

| 項目 | 規則 |
| --- | --- |
| Reviewer | Backend / DBA 產出，QA / Security / DevOps 複核 fail-closed 與 evidence。 |
| Human Gate | 若批次需接觸受控正式資料，必須人類簽核。 |
| ADR | 若從 batch 改成 CDC / 雙寫，需新增 ADR 或更新 DB 遷移決策。 |

## Notes

- 2026-07-07 | upgraded | MVP2 核心卡完整格式升級，evidence 改為 `evidence/MVP2/TASK-RPT-0007/`。
