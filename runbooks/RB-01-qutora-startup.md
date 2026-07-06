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

3. 檢查 Docker Compose。

```powershell
docker compose -f open-source-sandbox/qutora-api/samples/docker-compose.sqlserver.yml config --quiet
```

4. 啟動 SQL Server 與 Qutora。

```powershell
docker compose -f open-source-sandbox/qutora-api/samples/docker-compose.sqlserver.yml up -d
```

5. 記錄 container 狀態。

```powershell
docker compose -f open-source-sandbox/qutora-api/samples/docker-compose.sqlserver.yml ps
```

6. 初始化 admin user。

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

7. 登入 admin，確認可取得 token。

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
- Docker Compose config 結果。
- container list。
- API health 或 root endpoint 回應。
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
