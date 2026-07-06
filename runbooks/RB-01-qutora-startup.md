# RB-01 Qutora Startup

目的：讓三人小隊能在乾淨環境中啟動本演練舊系統 Qutora，並產出可驗收的啟動 evidence。

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

3. 準備 Qutora sample `.env`。

```powershell
if (-not (Test-Path open-source-sandbox/qutora-api/samples/.env)) {
  Copy-Item open-source-sandbox/qutora-api/samples/env.sqlserver.example open-source-sandbox/qutora-api/samples/.env
}
```

檢查 `open-source-sandbox/qutora-api/samples/.env` 至少包含 SQL Server、JWT 與 API 所需設定。密碼、JWT secret 與連線字串可保留在本機 `.env`，但不得把真實密碼、完整 token 或未遮罩連線字串寫入 evidence。

4. 檢查 Docker Compose。

```powershell
docker compose --env-file open-source-sandbox/qutora-api/samples/.env -f open-source-sandbox/qutora-api/samples/docker-compose.sqlserver.yml config --quiet
```

5. 啟動 SQL Server 與 Qutora。

```powershell
docker compose --env-file open-source-sandbox/qutora-api/samples/.env -f open-source-sandbox/qutora-api/samples/docker-compose.sqlserver.yml up -d
```

6. 記錄 container 狀態。

```powershell
docker compose --env-file open-source-sandbox/qutora-api/samples/.env -f open-source-sandbox/qutora-api/samples/docker-compose.sqlserver.yml ps
```

7. 確認存取端點。

| 項目 | 預設位置 | Evidence 規則 |
| --- | --- | --- |
| Qutora API | `http://localhost:8080` | 記錄 HTTP status 與回應摘要。 |
| Swagger / OpenAPI | `http://localhost:8080/swagger` | 若可用，記錄頁面可開啟；若不可用，改記 API endpoint evidence。 |
| SQL Server | `localhost:1433` | 記錄可連線到 `QutoraDB`；密碼需遮罩。 |
| Admin account | `admin@qutora.local` | 只記錄帳號與角色，不記錄密碼。 |

8. 初始化 admin user。

先確認系統尚未初始化：

```powershell
curl.exe http://localhost:8080/api/auth/system-status
```

預期尚未初始化時回傳 `isInitialized: false`。接著建立第一個 admin：

```powershell
curl.exe -X POST http://localhost:8080/api/auth/initial-setup `
  -H "Content-Type: application/json" `
  -d '{ "email": "admin@qutora.local", "password": "AdminPassword123!", "firstName": "Admin", "lastName": "User", "organizationName": "ReportDemo Migration Lab" }'
```

預期回應包含 `System setup completed successfully. Please log in.`。此 endpoint 只能執行一次；若回傳 already initialized，需改以登入驗證既有 admin 是否可用，不得刪除正式或有用的 Docker volume。

9. 登入 admin，確認可取得 token。

```powershell
curl.exe -X POST http://localhost:8080/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{ "email": "admin@qutora.local", "password": "AdminPassword123!" }'
```

登入回應需保存遮罩後的 evidence：可記錄 HTTP status、`success`、角色或 token 欄位是否存在，但不得把完整 JWT 或密碼寫入 repo。

## Evidence

輸出到：

```text
evidence/MVP1/TASK-RPT-0001/qutora-startup.md
```

至少包含：

- submodule status。
- `.env` 已由 sample 建立，敏感值已遮罩。
- Docker Compose config 結果，需使用 `--env-file open-source-sandbox/qutora-api/samples/.env`。
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
