# ReportDemo PoC Workspace

本目錄是 ReportDemo 演練專用 PoC 程式碼落點，依 ADR-015 管理。

## 邊界

- 僅用於演練下載閘道、動態浮水印、MariaDB metadata migration 與 validator。
- 不修改 Qutora submodule。
- 不代表正式系統最終架構或正式 SDK 採購決策。

## 建議結構

```text
poc/
├─ README.md
├─ download-gateway/
├─ watermark/
├─ migration/
└─ validators/
```

## 技術棧

- 語言：Python 3。
- PDF PoC：優先使用標準函式庫產生測試 PDF；若 MVP2 需要更完整浮水印，可在 ADR-015 記錄演練限定 library。
- MariaDB client：先以 `docker exec mariadb` 與 SQL 檔完成；若需要 Python client，需在 ADR-015 補充套件與安裝方式。
