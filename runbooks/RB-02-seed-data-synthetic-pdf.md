# RB-02 Seed Data And Synthetic PDF

目的：建立不含正式資料的合成 PDF 與 metadata，作為 Qutora 舊系統 baseline、MariaDB 移轉與下載 / 浮水印 PoC 的共同測試資料。

## 資料原則

- 不得使用未脫敏正式資料。
- 測試資料需可重複產生。
- 每份 PDF 需具備可追蹤的報表代號、資料日期、機密等級與樣本序號。

## 建議欄位

| 欄位 | 範例 | 用途 |
| --- | --- | --- |
| report_code | `RPT-INSIDER-001` | 報表代號 |
| report_name | `內部人員交易明細樣本` | 報表名稱 |
| data_date | `2026-07-06` | 資料日期 |
| confidentiality | `internal` / `confidential` / `high` | 機密等級 |
| sample_serial | `SYN-0001` | 合成資料序號 |
| owner_department | `Compliance` | Data Scope 測試 |
| legacy_document_id | Qutora document id | 舊系統 reference |

## 操作流程

1. 產生至少 3 份合成 PDF。
2. 透過 Qutora 上傳 PDF。
3. 建立或填入 metadata schema。
4. 下載同一批 PDF 並計算 SHA-256。
5. 匯出 metadata 與 document id 對照。

## Evidence

輸出到：

```text
evidence/MVP1/TASK-RPT-0003/
```

至少包含：

- `metadata-export.json`
- `pdf-baseline-hash.csv`
- PDF 樣本產製方式。
- Qutora document id 與 sample serial 對照。

## 驗收

- reviewer 可用同一批輸入重建 metadata 與 hash。
- 不得出現正式客戶、員工、交易或券商資料。
- 若欄位無法映射到 Qutora metadata，需記錄在 mapping gap。
