# RB-05 MariaDB Environment

目的：提供 MVP2 / Pilot 可重複啟動的 MariaDB 目標資料庫環境，作為 Qutora SQL Server metadata 移轉、staging schema、下載閘道與 rollback restore 的共同基礎。

AI 主導模式：本 runbook 可由 `[AI]` 執行環境建立、schema skeleton、dump / restore 命令，但 DB 邊界、資料一致性與 rollback 接受標準必須由 `[HUMAN]` reviewer 驗收。

## 決策邊界

- 本 runbook 依 ADR-013，僅適用 ReportDemo 演練。
- 不取代正式專案 DB 最終選型。
- MariaDB 版本固定 `mariadb:11.4`。
- 字元集固定 `utf8mb4`，collation 固定 `utf8mb4_unicode_ci`。

## 1. 建立環境檔

```powershell
Copy-Item runbooks/env.mariadb.example runbooks/.env.mariadb
```

必要欄位：

| 欄位 | 預設 | 說明 |
| --- | --- | --- |
| MARIADB_ROOT_PASSWORD | `RootPassword123!` | root 密碼，演練可用，正式不可沿用。 |
| MARIADB_DATABASE | `reportdemo_migration` | MVP2 目標 DB。 |
| MARIADB_USER | `reportdemo_user` | migration / PoC 使用者。 |
| MARIADB_PASSWORD | `ReportDemoPassword123!` | migration / PoC 密碼。 |
| MARIADB_PORT | `3307` | 避免與本機 3306 衝突。 |

## 2. 啟動 MariaDB

```powershell
docker compose -f runbooks/docker-compose.mariadb.yml --env-file runbooks/.env.mariadb up -d
docker compose -f runbooks/docker-compose.mariadb.yml --env-file runbooks/.env.mariadb ps
```

## 3. 連線驗證

```powershell
docker exec reportdemo-mariadb sh -c "mariadb -u`$MARIADB_USER -p`$MARIADB_PASSWORD `$MARIADB_DATABASE -e 'SELECT VERSION(); SHOW VARIABLES LIKE \"character_set_database\"; SHOW VARIABLES LIKE \"collation_database\";'"
```

預期：

- DB 可連線。
- `character_set_database = utf8mb4`。
- `collation_database = utf8mb4_unicode_ci`。

## 4. 建立 MVP2 staging schema skeleton

```powershell
docker exec reportdemo-mariadb sh -c "mariadb -u`$MARIADB_USER -p`$MARIADB_PASSWORD `$MARIADB_DATABASE -e 'CREATE TABLE IF NOT EXISTS stg_document (legacy_document_id VARCHAR(128) NOT NULL, report_code VARCHAR(64) NOT NULL, data_date DATE NOT NULL, confidentiality VARCHAR(32) NOT NULL, file_hash_sha256 CHAR(64), created_at DATETIME DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (legacy_document_id), INDEX ix_report_code (report_code), INDEX ix_confidentiality (confidentiality));'"
```

## 5. Dump / Restore

產生 dump：

```powershell
docker exec reportdemo-mariadb sh -c "mariadb-dump -u`$MARIADB_USER -p`$MARIADB_PASSWORD `$MARIADB_DATABASE" > evidence/MVP2/TASK-RPT-0008/mariadb-dump.sql
```

還原到 restore DB：

```powershell
docker exec reportdemo-mariadb sh -c "mariadb -uroot -p`$MARIADB_ROOT_PASSWORD -e 'CREATE DATABASE IF NOT EXISTS reportdemo_restore CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;'"
Get-Content evidence/MVP2/TASK-RPT-0008/mariadb-dump.sql | docker exec -i reportdemo-mariadb sh -c "mariadb -u`$MARIADB_USER -p`$MARIADB_PASSWORD reportdemo_restore"
```

## Evidence

輸出到：

```text
evidence/MVP2/TASK-RPT-0008/mariadb-environment.md
```

至少包含：

- compose config / ps。
- MariaDB version。
- charset / collation。
- staging schema skeleton 建立結果。
- dump / restore 命令與結果。

## 失敗處理

- MariaDB 無法啟動：MVP2 不得開工。
- charset / collation 不符：不得匯入 metadata。
- dump / restore 失敗：不得進入 Pilot。
## Teardown

演練結束或需要重建 MariaDB staging 時，依下列步驟清理。Teardown 前必須確認 dump、restore evidence 與 mapping 檔案已保存。

```powershell
docker compose -f runbooks/docker-compose.mariadb.yml --env-file runbooks/.env.mariadb down
```

若需要連 MariaDB volume 一起清除，需先完成 `mariadb-dump` 並由 Captain / Backend / DBA 確認可重建：

```powershell
docker compose -f runbooks/docker-compose.mariadb.yml --env-file runbooks/.env.mariadb down -v
```

清理驗證：

- `docker ps` 不應再看到 `reportdemo-mariadb`。
- 若使用 `down -v`，下一次 MVP2 必須重新執行 RB-05、`TASK-RPT-0008` staging schema 與 `TASK-RPT-0007` batch import。
- 不得刪除 `evidence/MVP2/**`、`evidence/Pilot/**` 或 dump / restore evidence，除非另有測試重置任務與人類核准。
