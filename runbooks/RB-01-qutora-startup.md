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

6. 依 Qutora README 或 samples 說明初始化 admin user。

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

## 失敗處理

- Compose 解析失敗：先停在 MVP1，不得進入 MVP2。
- API 無法啟動：保留 logs，建立 blocking issue。
- DB 無法連線：不得產生 migration baseline。
