# RB-01 Qutora Startup

目的：讓三人小隊能在乾淨環境中啟動本演練舊系統 Qutora，並產出可驗收的啟動 evidence。

AI 主導模式：本 runbook 可由 `[AI]` 執行命令與整理 evidence，但啟動成功、敏感資訊遮罩與 MVP1 Gate 必須由 `[HUMAN]` reviewer 驗收。

## 前置條件

- 已在 repo 根目錄執行。
- 已安裝 Git、Docker Desktop 或相容 Docker runtime。
- 不修改 Qutora 原始碼。

## 步驟

1. 初始化 submodule。

```powershell
git submodule update --init --recursive
git submodule status
```

2. 確認 Qutora commit。

```text
de156e0eb72d58772a76e570eb711db344bedfc0
```

3. 準備 Qutora `.env`（放在 repo 的 `runbooks/`，不放進 submodule，避免 submodule 出現 untracked 內容）。

```powershell
if (-not (Test-Path runbooks/.env.qutora)) {
  Copy-Item open-source-sandbox/qutora-api/samples/env.sqlserver.example runbooks/.env.qutora
}
```

檢查 `runbooks/.env.qutora` 至少包含 SQL Server、JWT 與 API 所需設定。密碼、JWT secret 與連線字串可保留在本機 `.env.qutora`，但不得把真實密碼、完整 token 或未遮罩連線字串寫入 evidence。`.env.qutora` 已被 `.gitignore` 排除，不得改名為未被排除的檔名。

4. 檢查 Docker Compose。

```powershell
docker compose --env-file runbooks/.env.qutora -f open-source-sandbox/qutora-api/samples/docker-compose.sqlserver.yml config --quiet
```

預期輸出：無錯誤即通過。會出現一行 `the attribute 'version' is obsolete` warning，這來自 Qutora 官方 compose 檔，屬預期輸出、不算失敗，不需要修改 submodule。

5. 啟動 SQL Server 與 Qutora。

```powershell
docker compose --env-file runbooks/.env.qutora -f open-source-sandbox/qutora-api/samples/docker-compose.sqlserver.yml up -d
```

6. 記錄 container 狀態。

```powershell
docker compose --env-file runbooks/.env.qutora -f open-source-sandbox/qutora-api/samples/docker-compose.sqlserver.yml ps
```

7. 確認存取端點。

| 項目 | 預設位置 | Evidence 規則 |
| --- | --- | --- |
| Qutora API | `http://localhost:8080` | 記錄 HTTP status 與回應摘要。 |
| Swagger / OpenAPI | `http://localhost:8080/swagger` | 若可用，記錄頁面可開啟；若不可用，改記 API endpoint evidence。 |
| SQL Server | `localhost:1433` | 記錄可連線到 `QutoraDB`；密碼需遮罩。 |
| Admin account | `admin@qutora.local` | 只記錄帳號與角色，不記錄密碼。 |

8. 初始化 admin user。

注意：不要用 `curl.exe -d '{...}'` 直接帶 JSON。Windows PowerShell 傳參給原生執行檔時會剝除 JSON 內的雙引號，API 會收到不合法 JSON 而回 400。統一改用 PowerShell 原生 `Invoke-RestMethod`。

先確認系統尚未初始化：

```powershell
Invoke-RestMethod -Uri http://localhost:8080/api/auth/system-status
```

預期尚未初始化時回傳 `isInitialized: false`。接著建立第一個 admin：

```powershell
$setupBody = @{
  email            = "admin@qutora.local"
  password         = "AdminPassword123!"
  firstName        = "Admin"
  lastName         = "User"
  organizationName = "ReportDemo Migration Lab"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/auth/initial-setup `
  -ContentType "application/json" -Body $setupBody
```

預期回應包含 `System setup completed successfully. Please log in.`。此 endpoint 只能執行一次；若回傳 already initialized，需改以登入驗證既有 admin 是否可用，不得刪除正式或有用的 Docker volume。

9. 登入 admin，確認可取得 token。

```powershell
$loginBody = @{
  email    = "admin@qutora.local"
  password = "AdminPassword123!"
} | ConvertTo-Json

$login = Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/auth/login `
  -ContentType "application/json" -Body $loginBody
$login | Select-Object -Property * -ExcludeProperty *token* | Format-List
```

登入回應需保存遮罩後的 evidence：可記錄 HTTP status、`success`、角色或 token 欄位是否存在，但不得把完整 JWT 或密碼寫入 repo。後續呼叫 API 時以 `-Headers @{ Authorization = "Bearer $($login.token)" }` 帶入授權（實際 token 欄位名稱以回應為準）。

## SQL Server 盤點命令

供 `TASK-RPT-0002` 與 V-MVP1-09 使用。SQL Server 容器名稱固定為 `qutora-sqlserver`（見 compose 檔），2022 image 內建 `mssql-tools18`：

```powershell
docker exec qutora-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "<MSSQL_SA_PASSWORD>" -d QutoraDB -C -Q "SELECT name FROM sys.tables ORDER BY name"
```

匯出資料表清單到 evidence（密碼取自 `runbooks/.env.qutora`，不得寫入 evidence）：

```powershell
docker exec qutora-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "<MSSQL_SA_PASSWORD>" -d QutoraDB -C -s "," -W -Q "SELECT t.name AS table_name, c.name AS column_name, ty.name AS data_type, c.max_length, c.is_nullable FROM sys.tables t JOIN sys.columns c ON t.object_id = c.object_id JOIN sys.types ty ON c.user_type_id = ty.user_type_id ORDER BY t.name, c.column_id" > evidence/MVP1/TASK-RPT-0002/qutora-schema-inventory.csv
```

若 image 內找不到 `mssql-tools18`，改試 `/opt/mssql-tools/bin/sqlcmd`（省略 `-C`），並把實際可用路徑記入 evidence。

## Evidence

輸出到：

```text
evidence/MVP1/TASK-RPT-0001/qutora-startup.md
```

至少包含：

- submodule status（應為 clean，無 untracked 內容）。
- `runbooks/.env.qutora` 已由 sample 建立，敏感值已遮罩。
- Docker Compose config 結果，需使用 `--env-file runbooks/.env.qutora`。
- container list。
- API health 或 root endpoint 回應。
- API / Swagger / SQL Server 端點可用性。
- SQL Server / `QutoraDB` 連線結果。
- `GET /api/auth/system-status` 結果。
- `POST /api/auth/initial-setup` 結果，密碼不得明文進 evidence。
- `POST /api/auth/login` 結果，JWT / refresh token 需遮罩。

## 失敗處理

- Compose 解析失敗：先停在 MVP1，不得進入 MVP2。
- API 無法啟動：保留 logs，建立 blocking issue。
- DB 無法連線：不得產生 migration baseline。
- admin 初始化失敗：保留 `system-status`、`initial-setup` HTTP status、container logs，先停在 MVP1。
- 已初始化但無法登入：admin token 不可用，MVP1 Gate 不得通過。
