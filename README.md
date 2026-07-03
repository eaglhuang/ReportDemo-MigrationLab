# ReportDemo Migration Lab

本 repo 是「內部人員交易報表轉媒體儲存系統」的獨立模擬搬移實驗室，用來保存計畫書、任務卡、ADR、PDF 交付物，以及後續舊系統替身的執行演練證據。

## Source Of Truth

- Agent Team 協作與派工：`內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md`
- 系統架構與治理：`內部人員交易報表轉媒體儲存系統_系統架構與治理計畫書.md`
- 功能拆解與任務卡：`內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md`、`tasks/`
- 人類決策與 ADR：`決策紀錄樣板ADR.md`
- 版本異動：`版本異動摘要ChangeLog.md`

## Open Source Sandbox

`open-source-sandbox/qutora-api` 以 git submodule 管理，作為本案模擬舊系統替身。

```powershell
git submodule update --init --recursive
```

目前固定的 Qutora commit：

```text
de156e0eb72d58772a76e570eb711db344bedfc0
```

## Local Run Notes

Qutora 官方 Docker Compose 範例位於：

```text
open-source-sandbox/qutora-api/samples/docker-compose.sqlserver.yml
```

預計演練流程：

1. 啟動 SQL Server Express + Qutora API。
2. 初始化 admin user。
3. 用合成 PDF / Golden Dataset 做上傳、查詢、下載、版本、權限與稽核驗證。
4. 對照本 repo 的任務卡與計畫書，輸出演練證據。

正式資料不得用於本模擬環境。
