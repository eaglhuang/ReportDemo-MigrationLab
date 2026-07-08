---
task_id: TASK-RPT-0045
source_milestone: M10-02
title: "舊系統覆蓋確認"
status: planned
owner: "QA / Security / DevOps"
priority: P0
milestone: M10
drill_stage: "ProductionCandidate"
execution_mode: "ai-with-human-review"
primary_role: "QA / Security / DevOps"
closure_reviewer: "Tech Lead / Captain"
support_roles:
  - "Tech Lead / Captain"
  - "Backend / DBA"
depends_on:
  - "TASK-RPT-0001"
  - "TASK-RPT-0002"
  - "TASK-RPT-0044"
related_plan: "drills/分階段演練與驗收計畫.md"
agent_team_plan: "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
evidence_path: "evidence/ProductionCandidate/TASK-RPT-0045/"
scopePaths:
  - "tasks/TASK-RPT-0045-m10-02-legacy-coverage-confirmation.task.md"
  - "evidence/ProductionCandidate/TASK-RPT-0045/**"
  - "evidence/Pilot/TASK-RPT-0005/qutora-component-conversion-map.md"
  - "evidence/Pilot/TASK-RPT-0009/module-porting-comparison-report.md"
  - "runbooks/RB-03-evidence-standard.md"
  - "runbooks/RB-04-rollback-rehearsal.md"
  - "open-source-sandbox/qutora-api"
deliverables:
  - "evidence/ProductionCandidate/TASK-RPT-0045/design-spec.md"
  - "evidence/ProductionCandidate/TASK-RPT-0045/legacy-coverage-matrix.md"
  - "evidence/ProductionCandidate/TASK-RPT-0045/unported-qutora-api-list.md"
  - "evidence/ProductionCandidate/TASK-RPT-0045/real-aspnet-intake-startup-pack.md"
  - "evidence/ProductionCandidate/TASK-RPT-0045/validation-result.md"
  - "evidence/ProductionCandidate/TASK-RPT-0045/review-and-signoff.md"
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
# TASK-RPT-0045 - M10-02 舊系統覆蓋確認

## 任務目標

建立 ProductionCandidate 階段可執行、可驗收、可留下證據的「舊系統必要功能覆蓋矩陣」任務規格。完成後，三人小隊可以依本卡執行開發、驗證或 Gate 檢查，並判斷是否允許進入下一階段。

## 真實功能帶入場景

確認 Qutora 作為本演練舊系統的必要功能已被新系統覆蓋或有明確例外，包含上傳、metadata、下載、audit、權限、資料搬移與 ADR-018 轉換軌的代碼移植結果。

## 舊系統覆蓋

- 本演練舊系統採用 Qutora，覆蓋範圍以 Qutora 的文件、metadata、下載、audit、SQL Server DB 與權限相關行為為主。
- 本卡不得假設新系統可以忽略舊系統輸入、輸出、排序、狀態與例外案例。
- 若本卡新增 Qutora 原本沒有的控管，需在 evidence 中標示為治理強化，而非舊系統差異錯誤。
- ADR-018 轉換軌需在本卡收口：每個 Qutora API / controller / service / entity / storage provider 至少標示為 `ported`、`wrapped`、`reused`、`rewritten`、`documented_exception` 之一，並連回 `TASK-RPT-0005` conversion map 或 `TASK-RPT-0009` porting comparison report。
- 真實 ASP.NET 系統尚未進場；本卡需輸出具名交接物 `real-aspnet-intake-startup-pack.md`，作為正式專案第一週 code archaeology 與返工盤點的啟動包。

## 落地設計

### API / Service / Gate

| 類型 | 名稱 | 說明 |
| --- | --- | --- |
| Internal Service | `executeTASKRPT0045(context)` | 執行舊系統必要功能覆蓋矩陣並產出 evidence。 |
| Internal Gate | `evaluateTASKRPT0045Gate(package_id)` | 驗證本卡是否允許進入下一階段。 |

### 資料表

| Table | 主要欄位 | 用途 |
| --- | --- | --- |
| `legacy_coverage_matrix` | `legacy_coverage_matrix_id`, `status`, `created_at`, `updated_at`, `payload_hash` | 支援舊系統必要功能覆蓋矩陣。 |
| `coverage_gap` | `coverage_gap_id`, `status`, `created_at`, `updated_at`, `payload_hash` | 支援舊系統必要功能覆蓋矩陣。 |
| `coverage_exception_signoff` | `coverage_exception_signoff_id`, `status`, `created_at`, `updated_at`, `payload_hash` | 支援舊系統必要功能覆蓋矩陣。 |
| `unported_qutora_api` | `qutora_path`, `api_or_module`, `reason`, `planned_disposition`, `owner`, `adr_ref` | 記錄未移植 Qutora API / module 與例外理由。 |
| `real_aspnet_intake_item` | `item_type`, `expected_source`, `qutora_mapping`, `required_evidence`, `owner`, `status` | 支援真實 ASP.NET 系統進場啟動包。 |

### 狀態機

```text
inventory -> mapped -> verified -> confirmed; verified -> exception_required
```

### 錯誤碼

| Code | 說明 | Fail-Closed |
| --- | --- | --- |
| `LEGACY_SCOPE_MISSING` | legacy scope missing。 | Yes |
| `MAPPING_MISSING` | mapping missing。 | Yes |
| `VALIDATION_MISSING` | validation missing。 | Yes |
| `EXCEPTION_UNSIGNED` | exception unsigned。 | Yes |
| `AUDIT_FAILED` | audit failed。 | Yes |

### 權限檢查

- 任何查詢、變更、簽核或 Gate 操作都必須先通過 Role 檢查，再套用 Data Scope 或階段權限。
- Admin 可管理設定，不代表可直接讀取報表內容或稽核敏感資料。
- 高機密、break-glass、正式切換、舊系統下線與例外放行必須觸發 human gate 或 ADR gate。

### 稽核欄位

| 欄位 | 說明 |
| --- | --- |
| `event_type` | `task-rpt-0045.started`, `task-rpt-0045.completed`, `task-rpt-0045.failed_closed` |
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
| Output | 本卡設計規格、legacy coverage matrix、未移植 Qutora API / module 清單、真實 ASP.NET 系統進場啟動包、validator 結果、test case 結果、review 紀錄、Gate 是否可通過的建議。 |

## ADR-018 轉換軌收口

`legacy-coverage-matrix.md` 必須逐項整併下列來源，不得只寫總結：

| 來源 | 必填欄位 |
| --- | --- |
| `TASK-RPT-0005` conversion map | Qutora 元件、分類、對應任務卡、DRI、closure reviewer、比對方式。 |
| `TASK-RPT-0009` porting comparison report | Qutora 元件、`src/` 模組路徑、輸入樣本、輸出差異、RB-07 差異等級、處置。 |
| MVP2 / Pilot 核心卡 | 0023 / 0024 / 0025 / 0028 等 C# 實作是否計入轉換軌、對應 validators、未通過項。 |
| 每日排程 §8 documented exceptions | 7 張裁減卡、裁減理由、human / ADR sign-off 條件。 |
| 未移植 Qutora API / module | 名稱、路徑、未移植理由、是否可 documented exception、正式專案 owner。 |

若任一 Qutora API / module 無法歸入 `ported`、`wrapped`、`reused`、`rewritten` 或 `documented_exception`，本卡不得 closure。

## 真實 ASP.NET 系統進場啟動包

`real-aspnet-intake-startup-pack.md` 是 W14 next-phase recommendation 的具名交接物，不新增獨立 docs。至少需包含：

| 區塊 | 內容 |
| --- | --- |
| 進場清單 | 真實 ASP.NET repo、DB schema、stored procedure、batch job、report template、auth/session、file storage、audit/log、部署方式、排程器與外部介面。 |
| Qutora 映射 | 哪些 Qutora conversion-map 分類可沿用到真實系統，哪些只可作參考。 |
| 必返工項 | Qutora 無法代表的正式資料、法遵規則、券商報表計算、正式權限模型、正式下線責任。 |
| 第一週 code archaeology 派工 | Tech Lead / Captain、Backend / DBA、QA / Security / DevOps 每日輸入、輸出、evidence path 與 Gate。 |
| 阻擋條件 | 無 repo、無 DB dump / schema、無報表樣本、無權限模型、無正式 owner 或無脫敏規則時，不得宣稱可估工或可切換。 |

## 完成定義

- 本卡所有 deliverables 已產生並放在 `evidence/ProductionCandidate/TASK-RPT-0045/`。
- `legacy-coverage-matrix.md` 已列出每個 Qutora API / module 的處置狀態。
- `unported-qutora-api-list.md` 已列出未移植項與 documented exception / next-phase owner。
- `real-aspnet-intake-startup-pack.md` 已完成並通過 reviewer 檢查。
- 10 條 validators 與 10 條 test cases 皆有可重跑 evidence。
- reviewer 已確認產出與 evidence，且產出者不得自我驗收。
- 若觸發 human gate 或 ADR gate，必須有簽核或決策紀錄後才可 closure。

## Validators

| ID | Validator | Evidence |
| --- | --- | --- |
| V-0045-01 | 驗證 舊系統必要功能覆蓋矩陣 規格包含 Qutora 輸入、MariaDB 輸出、ADR-018 轉換軌與 evidence 路徑。 | `evidence/ProductionCandidate/TASK-RPT-0045/V-0045-01.md` |
| V-0045-02 | 驗證 `legacy_coverage_matrix` 等資料表欄位足以保存狀態、錯誤碼與 payload hash。 | `evidence/ProductionCandidate/TASK-RPT-0045/V-0045-02.md` |
| V-0045-03 | 驗證狀態機不得略過 review、sign-off 與 closure。 | `evidence/ProductionCandidate/TASK-RPT-0045/V-0045-03.md` |
| V-0045-04 | 驗證所有 P0 / P1 失敗情境皆 fail-closed 或阻擋 Gate。 | `evidence/ProductionCandidate/TASK-RPT-0045/V-0045-04.md` |
| V-0045-05 | 驗證權限檢查遵守 Role 與 Data Scope 分離。 | `evidence/ProductionCandidate/TASK-RPT-0045/V-0045-05.md` |
| V-0045-06 | 驗證所有關鍵操作都有 audit event 與 correlation_id。 | `evidence/ProductionCandidate/TASK-RPT-0045/V-0045-06.md` |
| V-0045-07 | 驗證 evidence 依 RB-03 放在本卡指定目錄。 | `evidence/ProductionCandidate/TASK-RPT-0045/V-0045-07.md` |
| V-0045-08 | 驗證 reviewer 與產出者不可為同一人。 | `evidence/ProductionCandidate/TASK-RPT-0045/V-0045-08.md` |
| V-0045-09 | 驗證 human gate / ADR gate 有明確觸發條件。 | `evidence/ProductionCandidate/TASK-RPT-0045/V-0045-09.md` |
| V-0045-10 | 驗證真實 ASP.NET 系統進場啟動包包含進場清單、Qutora 映射、必返工項、第一週 code archaeology 派工與阻擋條件。 | `evidence/ProductionCandidate/TASK-RPT-0045/V-0045-10.md` |

## Test Cases

| ID | Input | 執行方式 | 預期結果 | 阻擋上線條件 |
| --- | --- | --- | --- | --- |
| TC-0045-01 | 正常 Qutora 合成資料與 conversion map | 執行舊系統必要功能覆蓋矩陣 happy path | 產出成功結果、coverage matrix 與 audit event | 無成功 evidence |
| TC-0045-02 | 缺少 Qutora baseline | 執行流程 | 回傳 baseline 缺漏錯誤並阻擋 Gate | 缺 baseline 仍通過 |
| TC-0045-03 | MariaDB metadata 不一致 | 執行流程 | 產生 mismatch issue 並要求 review | mismatch 未被記錄 |
| TC-0045-04 | 未授權角色 | 呼叫流程或查詢 API | 拒絕並寫入 audit event | 越權成功 |
| TC-0045-05 | Data Scope 不符 | 以跨部門資料執行 | 拒絕或遮罩結果 | 跨 scope 可見 |
| TC-0045-06 | 稽核寫入失敗 | 模擬 audit failure | fail-closed 或阻擋 Gate | 稽核失敗仍放行 |
| TC-0045-07 | 人工簽核缺漏 | 送交 Gate | 回傳 signoff missing | 未簽核仍進下一階段 |
| TC-0045-08 | ADR 觸發條件成立 | 送交 Gate | 標示 ADR required | 未開 ADR 仍 closure |
| TC-0045-09 | 未移植 Qutora API / module | 建立 coverage matrix | 產生 documented exception 或 blocking gap，且有 owner | 未移植項未列出 |
| TC-0045-10 | 真實 ASP.NET 系統尚未進場 | 產生 intake startup pack | 明確列出進場清單、返工項與阻擋條件 | 只寫 next-phase recommendation 空話 |

## Reviewer / Human Gate / ADR

- Reviewer：QA / Security / DevOps 與 Tech Lead / Captain, QA / Security / DevOps 交叉 review；產出者不得自我驗收。
- Human Gate：任何未覆蓋但允許上線的例外必須人類簽核。
- ADR Gate：若變更 DB、Object Storage / WORM、SSO / API session、PDF library、稽核 fail-closed、Go / No-Go 或架構邊界，必須 ADR。

## Notes

- 本卡依 Agent Team 計畫書分派 role、reviewer、validator、human sign-off 與 ADR gate。
- Evidence 命名與保存依 `runbooks/RB-03-evidence-standard.md`。
- 2026-07-07 | scoped | 覆蓋矩陣必須逐項列出 `drills/每日任務卡排程.md` §8 的 7 張範圍外任務卡與裁減理由，作為「未覆蓋但已裁決」證據，並彙整進 next-phase recommendation，不得留白。
- 2026-07-08 | scoped | 依 ADR-018 補入 Qutora API / module 全功能覆蓋矩陣、未移植項清單與 `real-aspnet-intake-startup-pack.md`，作為真實 ASP.NET 系統進場的具名交接物。
