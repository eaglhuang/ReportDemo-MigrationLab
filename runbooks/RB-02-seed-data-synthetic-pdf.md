# RB-02 Seed Data And Synthetic PDF

目的：建立不含正式資料、可重複產生的合成 PDF 與 metadata，作為 Qutora 舊系統 baseline、MariaDB 移轉、下載閘道與浮水印 PoC 的共同測試資料。

## 原則

- 不得使用未脫敏正式資料。
- 合成資料必須可重跑；同一組輸入應產生可比對的 metadata 與 hash evidence。
- PDF 內容只放假資料、報表代號、資料日期、機密等級、sample serial 與 trace id。
- reviewer 必須能用同一指令重建資料集。

## 產生工具

使用 repo 內建工具：

```powershell
python tools/generate_synthetic_pdf.py --count 3 --out evidence/MVP1/TASK-RPT-0003/synthetic-pdf
```

Pilot 可改產 20 份：

```powershell
python tools/generate_synthetic_pdf.py --count 20 --out evidence/Pilot/synthetic-pdf
```

工具會產生：

| 檔案 | 說明 |
| --- | --- |
| `*.pdf` | 合成 PDF 主檔。 |
| `metadata-export.json` | Qutora / MariaDB mapping 可用 metadata。 |
| `pdf-baseline-hash.csv` | PDF 檔名、SHA-256、大小、sample serial。 |

## Metadata 欄位

| 欄位 | 範例 | 說明 |
| --- | --- | --- |
| report_code | `RPT-INSIDER-001` | 報表代號 |
| report_name | `內部人員交易報表樣本` | 報表名稱 |
| data_date | `2026-07-06` | 資料日期 |
| confidentiality | `internal` / `confidential` / `high` | 機密等級 |
| sample_serial | `SYN-0001` | 合成資料序號 |
| owner_department | `Compliance` | Data Scope 測試欄位 |
| legacy_document_id | 空值，待 Qutora 上傳後回填 | 舊系統 reference |
| trace_id | `TRACE-SYN-0001` | 跨流程追蹤用 |

## MVP1 操作流程

1. 產生 3 份合成 PDF 與 metadata。
2. 依 RB-01 啟動 Qutora 並登入 admin。
3. 透過 Qutora API 或 Swagger 上傳 PDF。
4. 回填 Qutora document id 到 `metadata-export.json` 的 `legacy_document_id`。
5. 下載同一批 PDF 並計算 SHA-256，與 `pdf-baseline-hash.csv` 比對。
6. 將上傳、查詢、下載、hash 與 audit / log evidence 寫入 `evidence/MVP1/TASK-RPT-0003/`。

## Evidence

輸出到：

```text
evidence/MVP1/TASK-RPT-0003/
```

至少包含：

- `synthetic-pdf/metadata-export.json`
- `synthetic-pdf/pdf-baseline-hash.csv`
- 合成 PDF 檔案。
- Qutora document id 與 sample serial 對應。
- reviewer 重跑工具後的 hash 比對紀錄。

## 驗收

- `metadata-export.json` 必須能支援 Qutora baseline 與 MariaDB staging mapping。
- `pdf-baseline-hash.csv` 必須可被 reviewer 重算驗證。
- 若 Qutora 不支援自訂 metadata 欄位，需在 `qutora-limitation.md` 記錄限制與替代方案。
