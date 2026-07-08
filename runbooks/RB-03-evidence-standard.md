# RB-03 Evidence Standard

## 0. 2026-07-08 全域 Finding 嚴重度與 Risk / Blocker Log

本 runbook 是全 repo 的 evidence 與 finding 嚴重度 source of truth。各任務卡、daily dispatch、RB-07 平行作業差異、Gate summary 若使用 P0-P3，均以本節定義為準。

### 全域 Finding 嚴重度字典

| Severity | 定義 | Gate 規則 | 典型例子 |
| --- | --- | --- | --- |
| P0 | 資安、資料完整性、權限、audit、rollback 或正式資料邊界出現不可接受缺失 | 立即停止當前 Gate；不得以 workaround 放行 | 越權下載成功、audit fail-open、hash mismatch 未阻擋、rollback 無法回復 |
| P1 | 核心功能錯誤且沒有可接受 workaround | 阻擋當前 Gate，必須修復或 human sign-off 降級 | 下載閘道 happy path 不穩、MariaDB mapping 影響核心欄位、Pilot 差異不可解釋 |
| P2 | 有 workaround 或可限期修復，不阻擋當日工作但需 owner 與目標關閉日 | 可進下一日，但不得在 Gate package 留白 | 非核心欄位格式差異、可重跑的 validator flake、文件 evidence 缺截圖 |
| P3 | 改善項、文件品質、下一階段優化 | 不阻擋 Gate；進 next-phase recommendation | wording、附錄補強、非關鍵效能優化 |

### Risk / Blocker Log 慣例

風險與 blocker 不新增 docs；執行時累積在 evidence：

```text
evidence/<Stage>/risk-blocker-log.md
```

建議欄位：

| 欄位 | 說明 |
| --- | --- |
| id | 穩定 ID，例如 `RISK-MVP2-0001` |
| date | 首次發現日期 |
| source | daily dispatch、task id、validator、Gate review |
| severity | P0 / P1 / P2 / P3 |
| owner | 單一 human owner |
| status | open / investigating / mitigated / closed / accepted |
| target_close_date | 目標關閉日 |
| action | 下一步處置 |
| evidence_ref | 對應 evidence 或 task path |
| closed_at | 關閉時間；未關閉留空 |

規則：

- 任何 P0/P1 finding 或 `[GATE]` blocker 必須當日入簿。
- `blocked` 任務卡必須引用 risk-blocker-log 的 id。
- 每週五 Gate day 由 Tech Lead / Captain 檢查未關閉項；W12 risk register 只能從本簿收斂，不得臨時重造。

目的：統一演練 evidence 命名、保存、驗收與 Gate package 格式，避免每個任務各寫各的證據。

## 路徑規則

```text
evidence/<Stage>/<TASK-ID>/
```

範例：

```text
evidence/MVP2/TASK-RPT-0023/download-gateway-poc.md
```

Stage 固定為：

- `MVP1`
- `MVP2`
- `Pilot`
- `ProductionCandidate`

## Evidence Index

每個 Stage 至少建立：

```text
evidence/<Stage>/index.md
```

建議欄位：

| 欄位 | 說明 |
| --- | --- |
| task_id | 任務卡 ID |
| artifact | 證據檔案 |
| producer | 產出者，可填人類、AI agent 或 AI session。 |
| reviewer | 驗收者，必須是人類 reviewer 或指定人類代理；不得由同一個 producer 自審。 |
| command | 可重跑命令或手動步驟 |
| result | pass / fail / blocked |
| reviewed_at | 驗收時間 |
| notes | 差異或例外說明 |

MVP1 可直接複製下列範本作為起點：

```text
evidence/MVP1/.index-template.md
```

其他 Stage 也應沿用同一欄位；若任務涉及人類簽核、ADR 或 rollback，需在 `notes` 補上 ADR 編號、簽核人與 rollback evidence 路徑。

若採 AI 主導三人併行模式，需額外遵守：

- `producer` 可填 AI agent / session，但 `reviewer` 必須填人類 reviewer 或指定人類代理。
- 產出該 evidence 的 AI session、Agent 或人類 producer 不得單獨擔任 reviewer。
- AI 週末產出的草稿不得直接列為正式 evidence；需下一工作日由人類 review 後才可納入。
- Gate summary 需補充 AI 產出占比、人類抽驗比例與 reviewer_conflict 是否存在。

## 驗收原則

- 誰產出 evidence，誰不得單獨驗收。
- Gate evidence 必須能讓 reviewer 重跑或追溯。
- 權限、稽核、資料一致性與 rollback evidence 缺失時，不得進入下一階段。
- 敏感資訊需遮罩；不得把未脫敏正式資料放入 repo。
- AI 產出速度不得取代 reviewer 容量；未 review 的 AI 產出不得 closure。

## Gate Package

每個 Stage 結束需產出：

```text
evidence/<Stage>/gate-summary.md
```

內容包含：

- 本階段 validators 結果。
- 本階段 test cases 結果。
- blocking issue。
- 例外簽核。
- 下一階段 Go / No-Go 建議。
- AI 產出占比、人類抽驗比例與未 review 的 AI 產出清單。
- reviewer_conflict 與第二層 review 結果。

## Production Candidate Sign-off Record

`ProductionCandidate` 階段需額外產出正式候選簽核表：

```text
evidence/ProductionCandidate/sign-off-record.md
```

建議格式：

| 欄位 | 說明 |
| --- | --- |
| release_candidate_id | 正式候選版本或 commit |
| evidence_package | Go / No-Go evidence package 路徑 |
| business_proxy | 業務代理簽核人 |
| audit_proxy | 稽核代理簽核人 |
| security_proxy | 資安代理簽核人 |
| operations_proxy | 維運代理簽核人 |
| decision | go / no-go / conditional-go |
| conditions | conditional-go 的限制條件 |
| signed_at | 簽核時間 |
| adr_refs | 相關 ADR |
| open_risks | 未關閉風險 |
| rollback_ready | yes / no |
| notes | 補充說明 |

範本：

```markdown
# Production Candidate Sign-off Record

| Role | Proxy / Owner | Decision | Signed at | Notes |
| --- | --- | --- | --- | --- |
| Business Owner |  |  |  |  |
| Audit Owner |  |  |  |  |
| Security Owner |  |  |  |  |
| Operations Owner |  |  |  |  |
| Final Go / No-Go Approver |  |  |  |  |

## Evidence Package

- release_candidate_id:
- gate_summary:
- rollback_evidence:
- open_blockers:
- adr_refs:

## Decision

- decision:
- conditions:
- rollback_ready:
- final_notes:
```

三人小隊可代理填寫演練用欄位，但正式 Go / No-Go、舊系統下線、資安例外與稽核例外不得由 Agent 或單一工程角色自行簽核。
