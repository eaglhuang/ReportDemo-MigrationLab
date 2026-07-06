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
