# RB-04 Rollback Rehearsal

目的：建立演練用最小 rollback 流程，證明新路徑失敗時仍可回到 Qutora 舊系統路徑，並保留切換期間 evidence。

## 適用階段

- Pilot rollback dry run。
- Production Candidate Go / No-Go 前演練。
- M9-03 任務卡正式化前的最小可行版本。

## Rollback 流程

1. 停用新下載路徑或 feature flag。
2. 停止新的 MariaDB 寫入或 migration job。
3. 確認 Qutora API 與 SQL Server 仍可用。
4. 將使用者路由回 Qutora 舊路徑。
5. 保存 rollback window 期間的下載、錯誤、audit 與告警 evidence。
6. 驗證 MariaDB、PDF storage、設定與 audit backup 可 restore 到隔離環境。
7. 產出 RTO / RPO 紀錄。

## Evidence

輸出到：

```text
evidence/ProductionCandidate/TASK-RPT-0041/rollback-dry-run.md
```

至少包含：

- rollback 開始與結束時間。
- 停用的新路徑。
- Qutora 舊路徑驗證結果。
- restore 結果。
- RTO / RPO。
- 未解決風險。

## 阻擋條件

- 無法回到 Qutora 舊路徑。
- rollback 期間無 audit。
- restore 結果無法證明資料一致。
- break-glass 權限無法追蹤。
