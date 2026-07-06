# RB-03 Evidence Standard

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
| producer | 產出者 |
| reviewer | 驗收者 |
| command | 可重跑命令或手動步驟 |
| result | pass / fail / blocked |
| reviewed_at | 驗收時間 |
| notes | 差異或例外說明 |

## 驗收原則

- 誰產出 evidence，誰不得單獨驗收。
- Gate evidence 必須能讓 reviewer 重跑或追溯。
- 權限、稽核、資料一致性與 rollback evidence 缺失時，不得進入下一階段。
- 敏感資訊需遮罩；不得把未脫敏正式資料放入 repo。

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
