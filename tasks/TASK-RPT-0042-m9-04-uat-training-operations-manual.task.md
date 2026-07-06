---
task_id: TASK-RPT-0042
source_milestone: M9-04
title: "UAT 訓練與操作手冊"
status: planned
owner: project-captain
priority: P0
milestone: M9
drill_stage: "ProductionCandidate"
primary_role: "QA / Validation"
support_roles:
  - "Tech Lead / Captain"
  - "Audit / Evidence Agent"
depends_on:
  - "TASK-RPT-0040"
  - "TASK-RPT-0041"
related_plan: "drills/分階段演練與驗收計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
evidence_path: "evidence/ProductionCandidate/TASK-RPT-0042/"
scopePaths:
  - "tasks/TASK-RPT-0042-m9-04-uat-training-operations-manual.task.md"
  - "evidence/ProductionCandidate/TASK-RPT-0042/**"
  - "runbooks/RB-03-evidence-standard.md"
  - "runbooks/RB-04-rollback-rehearsal.md"
  - "open-source-sandbox/qutora-api"
deliverables:
  - "evidence/ProductionCandidate/TASK-RPT-0042/design-spec.md"
  - "evidence/ProductionCandidate/TASK-RPT-0042/validation-result.md"
  - "evidence/ProductionCandidate/TASK-RPT-0042/review-and-signoff.md"
evidence:
  required: command-backed
rollback:
  strategy: block-next-gate-and-return-to-qutora-or-last-approved-state
  notes: "若本卡驗證失敗，不得進入下一個 Gate；必要時回到 Qutora 路徑或上一個已核准狀態。"
outOfScope:
  - "使用未脫敏正式資料進行一般測試"
  - "未完成 evidence 與 human gate 即宣告 closure"
  - "繞過 Agent Team 計畫書、RB-03 或 ADR 決策邊界"
nonGoals:
  - "本卡不修改 Qutora 原始碼"
  - "本卡不取代 ADR 或正式人類簽核"
---
# TASK-RPT-0042 - M9-04 UAT 訓練與操作手冊

## 任務目標

建立 ProductionCandidate 階段可執行、可驗收、可留下證據的「UAT、訓練與操作交接」任務規格。完成後，三人小隊可以依本卡執行開發、驗證或 Gate 檢查，並判斷是否允許進入下一階段。

## 真實功能帶入場景

建立三人小隊與模擬業務/稽核/維運可照做的 UAT、操作、告警處理、rollback 與證據保存手冊。

## 舊系統覆蓋

- 本演練舊系統採用 Qutora，覆蓋範圍以 Qutora 的文件、metadata、下載、audit、SQL Server DB 與權限相關行為為主。
- 本卡不得假設新系統可以忽略舊系統輸入、輸出、排序、狀態與例外案例。
- 若本卡新增 Qutora 原本沒有的控管，需在 evidence 中標示為治理強化，而非舊系統差異錯誤。

## 落地設計

### API / Service / Gate

| 類型 | 名稱 | 說明 |
| --- | --- | --- |
| Internal Service | `executeTASKRPT0042(context)` | 執行UAT、訓練與操作交接並產出 evidence。 |
| Internal Gate | `evaluateTASKRPT0042Gate(package_id)` | 驗證本卡是否允許進入下一階段。 |

### 資料表

| Table | 主要欄位 | 用途 |
| --- | --- | --- |
| `uat_session` | `uat_session_id`, `status`, `created_at`, `updated_at`, `payload_hash` | 支援UAT、訓練與操作交接。 |
| `training_attendance` | `training_attendance_id`, `status`, `created_at`, `updated_at`, `payload_hash` | 支援UAT、訓練與操作交接。 |
| `operations_manual_version` | `operations_manual_version_id`, `status`, `created_at`, `updated_at`, `payload_hash` | 支援UAT、訓練與操作交接。 |

### 狀態機

```text
draft -> reviewed -> published -> acknowledged; reviewed -> rework
```

### 錯誤碼

| Code | 說明 | Fail-Closed |
| --- | --- | --- |
| `MANUAL_INCOMPLETE` | manual incomplete。 | Yes |
| `ATTENDANCE_MISSING` | attendance missing。 | Yes |
| `UAT_FAILED` | uat failed。 | Yes |
| `SIGNOFF_MISSING` | signoff missing。 | Yes |
| `AUDIT_FAILED` | audit failed。 | Yes |

### 權限檢查

- 任何查詢、變更、簽核或 Gate 操作都必須先通過 Role 檢查，再套用 Data Scope 或階段權限。
- Admin 可管理設定，不代表可直接讀取報表內容或稽核敏感資料。
- 高機密、break-glass、正式切換、舊系統下線與例外放行必須觸發 human gate 或 ADR gate。

### 稽核欄位

| 欄位 | 說明 |
| --- | --- |
| `event_type` | `task-rpt-0042.started`, `task-rpt-0042.completed`, `task-rpt-0042.failed_closed` |
| `actor_id` | 執行者或 Agent identity。 |
| `correlation_id` | 串接 Qutora、新系統、validator 與 Gate 的追蹤 ID。 |
| `payload_hash` | 稽核 payload hash。 |
| `decision_ref` | human gate 或 ADR gate 關聯編號。 |

### Fail-Closed 規則

- 核心 evidence 缺漏時，不得進入下一階段。
- 稽核寫入失敗時，不得 closure。
- 權限檢查失敗時，不得以人工便利性繞過。
- 發現 P0/P1 風險時，必須阻擋 Gate 並升級人類決策。

## 影響範圍

- 影響 `ProductionCandidate` 階段 Gate、evidence package 與後續任務卡開工順序。
- 影響 Qutora 舊系統覆蓋判斷、新系統功能驗證、權限與稽核證據。
- 影響 `drills/分階段演練與驗收計畫.md` 的階段驗收與 `tasks/README.md` 的核心卡狀態。

## 輸入與輸出

| 類型 | 內容 |
| --- | --- |
| Input | Qutora baseline、MariaDB metadata、任務前置卡 evidence、RB-03 evidence index、必要 ADR 或 human sign-off。 |
| Output | 本卡設計規格、validator 結果、test case 結果、review 紀錄、Gate 是否可通過的建議。 |

## 完成定義

- 本卡所有 deliverables 已產生並放在 `evidence/ProductionCandidate/TASK-RPT-0042/`。
- 10 條 validators 與 10 條 test cases 皆有可重跑 evidence。
- reviewer 已確認產出與 evidence，且產出者不得自我驗收。
- 若觸發 human gate 或 ADR gate，必須有簽核或決策紀錄後才可 closure。

## Validators

| ID | Validator | Evidence |
| --- | --- | --- |
| V-0042-01 | 驗證 UAT、訓練與操作交接 規格包含 Qutora 輸入、MariaDB 輸出與 evidence 路徑。 | `evidence/ProductionCandidate/TASK-RPT-0042/V-0042-01.md` |
| V-0042-02 | 驗證 `uat_session` 等資料表欄位足以保存狀態、錯誤碼與 payload hash。 | `evidence/ProductionCandidate/TASK-RPT-0042/V-0042-02.md` |
| V-0042-03 | 驗證狀態機不得略過 review、sign-off 與 closure。 | `evidence/ProductionCandidate/TASK-RPT-0042/V-0042-03.md` |
| V-0042-04 | 驗證所有 P0 / P1 失敗情境皆 fail-closed 或阻擋 Gate。 | `evidence/ProductionCandidate/TASK-RPT-0042/V-0042-04.md` |
| V-0042-05 | 驗證權限檢查遵守 Role 與 Data Scope 分離。 | `evidence/ProductionCandidate/TASK-RPT-0042/V-0042-05.md` |
| V-0042-06 | 驗證所有關鍵操作都有 audit event 與 correlation_id。 | `evidence/ProductionCandidate/TASK-RPT-0042/V-0042-06.md` |
| V-0042-07 | 驗證 evidence 依 RB-03 放在本卡指定目錄。 | `evidence/ProductionCandidate/TASK-RPT-0042/V-0042-07.md` |
| V-0042-08 | 驗證 reviewer 與產出者不可為同一人。 | `evidence/ProductionCandidate/TASK-RPT-0042/V-0042-08.md` |
| V-0042-09 | 驗證 human gate / ADR gate 有明確觸發條件。 | `evidence/ProductionCandidate/TASK-RPT-0042/V-0042-09.md` |
| V-0042-10 | 驗證 `git diff --check` 無格式錯誤。 | `evidence/ProductionCandidate/TASK-RPT-0042/V-0042-10.md` |

## Test Cases

| ID | Input | 執行方式 | 預期結果 | 阻擋上線條件 |
| --- | --- | --- | --- | --- |
| TC-0042-01 | 正常 Qutora 合成資料 | 執行UAT、訓練與操作交接 happy path | 產出成功結果與 audit event | 無成功 evidence |
| TC-0042-02 | 缺少 Qutora baseline | 執行流程 | 回傳 baseline 缺漏錯誤並阻擋 Gate | 缺 baseline 仍通過 |
| TC-0042-03 | MariaDB metadata 不一致 | 執行流程 | 產生 mismatch issue 並要求 review | mismatch 未被記錄 |
| TC-0042-04 | 未授權角色 | 呼叫流程或查詢 API | 拒絕並寫入 audit event | 越權成功 |
| TC-0042-05 | Data Scope 不符 | 以跨部門資料執行 | 拒絕或遮罩結果 | 跨 scope 可見 |
| TC-0042-06 | 稽核寫入失敗 | 模擬 audit failure | fail-closed 或阻擋 Gate | 稽核失敗仍放行 |
| TC-0042-07 | 人工簽核缺漏 | 送交 Gate | 回傳 signoff missing | 未簽核仍進下一階段 |
| TC-0042-08 | ADR 觸發條件成立 | 送交 Gate | 標示 ADR required | 未開 ADR 仍 closure |
| TC-0042-09 | 重跑同一批資料 | 重複執行 validator | 結果可重現且 evidence 可追蹤 | 不可重跑或結果漂移 |
| TC-0042-10 | rollback / 回復情境 | 依 RB-04 或任務 rollback 執行 | 可回到 Qutora 或安全狀態 | 回復路徑不可用 |

## Reviewer / Human Gate / ADR

- Reviewer：QA / Validation 與 Tech Lead / Captain, Audit / Evidence Agent 交叉 review；產出者不得自我驗收。
- Human Gate：UAT 驗收、操作手冊發布與訓練簽收需人類簽核。
- ADR Gate：若變更 DB、Object Storage / WORM、SSO / API session、PDF library、稽核 fail-closed、Go / No-Go 或架構邊界，必須 ADR。

## Notes

- 本卡依 Agent Team 計畫書分派 role、reviewer、validator、human sign-off 與 ADR gate。
- Evidence 命名與保存依 `runbooks/RB-03-evidence-standard.md`。
