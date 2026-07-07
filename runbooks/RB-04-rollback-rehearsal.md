# RB-04 Rollback Rehearsal

目的：定義演練用最小 rollback dry run，確保新路徑失敗時能停用新功能、回到 Qutora 舊系統路徑，並留下 RTO / RPO、restore、break-glass 與稽核 evidence。

## 適用時機

- Pilot rollback dry run。
- Production Candidate Go / No-Go 前。
- `TASK-RPT-0041` Rollback Runbook 驗收。

## 前置條件

- Qutora 可依 RB-01 啟動並登入。
- MariaDB 可依 RB-05 啟動、dump、restore。
- evidence 命名依 RB-03。
- 若使用 break-glass，需先完成 dual-control 代理簽核。

## Rollback 七步驟

| 步驟 | 執行標籤 | 內容 |
| --- | --- | --- |
| 1 | `[AI->HUMAN]` | 啟用 freeze：停止新的下載閘道、浮水印、Hash 或 migration job；需人類確認影響範圍。 |
| 2 | `[AI->HUMAN]` | 停止新系統寫入：暫停 MariaDB migration / staging import；需人類確認無資料遺失風險。 |
| 3 | `[AI]` | 驗證 Qutora API 與 SQL Server 仍可用，輸出 command-backed evidence。 |
| 4 | `[HUMAN]` | 將使用者路徑切回 Qutora download path 或舊系統唯讀路徑；正式環境不得由 AI 自行切換。 |
| 5 | `[AI->HUMAN]` | 記錄 rollback window 內的使用者影響、audit event 與 open issue。 |
| 6 | `[AI]` | 驗證 MariaDB、PDF storage、設定與 audit backup 可 restore 到隔離環境。 |
| 7 | `[HUMAN]` | 產出 RTO / RPO 接受結論與 Go / No-Go 建議。 |

## MariaDB Backup / Restore 命令

產生備份：

```powershell
docker exec reportdemo-mariadb sh -c "mariadb-dump -u`$MARIADB_USER -p`$MARIADB_PASSWORD reportdemo_migration" > evidence/ProductionCandidate/TASK-RPT-0041/mariadb-backup.sql
```

還原到隔離 DB：

```powershell
docker exec reportdemo-mariadb sh -c "mariadb -uroot -p`$MARIADB_ROOT_PASSWORD -e 'CREATE DATABASE IF NOT EXISTS reportdemo_restore CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;'"
Get-Content evidence/ProductionCandidate/TASK-RPT-0041/mariadb-backup.sql | docker exec -i reportdemo-mariadb sh -c "mariadb -u`$MARIADB_USER -p`$MARIADB_PASSWORD reportdemo_restore"
```

驗證：

```powershell
docker exec reportdemo-mariadb sh -c "mariadb -u`$MARIADB_USER -p`$MARIADB_PASSWORD -e 'SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = \"reportdemo_restore\";'"
```

## Break-glass Dry Run

Break-glass 的 dual-control 本質上不可由 AI 代理簽核。AI 可協助產生 request 草稿、檢查清單與 evidence 摘要，但下列 6 步驟均需人類或指定人類代理確認：

1. `[HUMAN]` Tech Lead / Captain 建立 break-glass request，指定目的、範圍、期限與風險。
2. `[HUMAN]` QA / Security / DevOps 以 Security proxy 身分核准或拒絕。
3. `[HUMAN]` Backend / DBA 只取得限時、限範圍 token 或操作窗口。
4. `[HUMAN]` 執行一個低風險維修動作，例如查詢 rollback 狀態，不得讀取報表內容。
5. `[AI->HUMAN]` 到期後確認 token 或權限失效，AI 可協助檢查，人類需接受結果。
6. `[AI->HUMAN]` 寫入 audit evidence：申請、核准、啟用、操作、到期、事後覆核。

阻擋條件：

- 無 dual-control。
- token 不會到期。
- 權限範圍超出核准內容。
- break-glass audit 無法追蹤。

## Evidence

輸出到：

```text
evidence/ProductionCandidate/TASK-RPT-0041/rollback-dry-run.md
```

至少包含：

- rollback 步驟清單與執行時間。
- freeze / disable 新路徑的證據。
- Qutora 回復路徑驗證。
- MariaDB dump / restore 命令與結果。
- RTO / RPO。
- break-glass dry run evidence。
- open risks 與 Go / No-Go 建議。

## 阻擋條件

- 無法回到 Qutora 路徑。
- rollback 無 audit。
- restore 後資料筆數或 hash 不一致。
- break-glass 權限無法追蹤。
