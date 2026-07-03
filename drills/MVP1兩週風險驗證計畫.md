# MVP1 兩週風險驗證計畫

版本：v1.0  
狀態：draft  
最後更新：2026-07-03

## 1. 目標

MVP1 目標是在 2 週內確認本演練舊系統 Qutora 可被穩定啟動、操作、盤點與作為後續搬移基準。MVP1 不追求完整新系統功能，而是盡早暴露舊系統來源、PDF、metadata、DB、下載、權限與 audit evidence 是否可用。

## 2. 真實功能帶入範圍

本階段直接使用 Qutora 的真實功能：

- Qutora API 與 SQL Server Docker Compose 啟動。
- Admin user 初始化與 API 存取。
- PDF 文件上傳、查詢、下載與版本資訊。
- Metadata schema、分類與報表識別欄位。
- SQL Server / `QutoraDB` schema 與資料抽取。
- Audit log 或可替代的 API 操作紀錄。
- Storage Provider / 檔案儲存路徑盤點。

## 3. 交付物

- `evidence/MVP1/qutora-startup.md`
- `evidence/MVP1/qutora-db-inventory.md`
- `evidence/MVP1/pdf-baseline-hash.csv`
- `evidence/MVP1/metadata-export.json`
- `evidence/MVP1/audit-sample.md`
- MVP1 結論：Go to MVP2 / 調整策略 / 暫停演練。

## 4. Validators

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| V-MVP1-01 | Docker 可用、submodule 已初始化 | `docker compose config --quiet` | Compose 設定可解析 | Compose 解析失敗 |
| V-MVP1-02 | Qutora container 啟動 | 呼叫 health 或 root API | API 可回應 | API 無法啟動或反覆重啟 |
| V-MVP1-03 | SQL Server container 啟動 | 連線 `QutoraDB` | DB 可連線 | DB 無法連線 |
| V-MVP1-04 | 已初始化 admin | 登入或取得 API token | 可取得授權存取 | 無法建立或登入 admin |
| V-MVP1-05 | 有合成 PDF | 透過 Qutora 上傳 PDF | 回傳 document id | 上傳失敗或檔案遺失 |
| V-MVP1-06 | 已上傳 PDF | 查詢文件 metadata | metadata 可讀取 | metadata 不完整 |
| V-MVP1-07 | 已上傳 PDF | 下載同一文件 | 下載檔案 hash 可計算 | 下載失敗 |
| V-MVP1-08 | 已執行上傳/下載 | 查詢 audit 或替代 log | 可找到操作紀錄 | 無任何可追蹤紀錄 |
| V-MVP1-09 | DB 可連線 | 匯出主要資料表清單 | 產出 schema inventory | 無法盤點 schema |
| V-MVP1-10 | 完成前 9 項 | 產出 MVP1 evidence index | evidence 可被 reviewer 追溯 | evidence 不完整 |

## 5. Test Cases

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| TC-MVP1-01 | 全新環境 | 依 README 初始化 Qutora | 30 分鐘內可啟動 API 與 DB | 初始化步驟不可重複 |
| TC-MVP1-02 | admin 已建立 | 建立一般使用者 | 使用者可被查詢 | 使用者建立失敗 |
| TC-MVP1-03 | 一般使用者存在 | 上傳 3 份合成 PDF | 產生 3 筆 document | 筆數不一致 |
| TC-MVP1-04 | PDF 已上傳 | 設定報表代號與機密等級 metadata | metadata 可回讀 | 欄位不可保存 |
| TC-MVP1-05 | PDF 已上傳 | 以報表代號查詢 | 只回傳符合條件文件 | 查詢條件失效 |
| TC-MVP1-06 | 使用者有權限 | 下載 PDF | 成功下載且 hash 可記錄 | 下載不可追蹤 |
| TC-MVP1-07 | 使用者無權限 | 嘗試下載 PDF | 回傳拒絕或未授權 | 越權下載成功 |
| TC-MVP1-08 | 已執行下載 | 查詢 audit/log | 可對應使用者、時間、document id | audit 缺關鍵欄位 |
| TC-MVP1-09 | DB 有資料 | 匯出 document / metadata 表樣本 | 匯出可重跑且無正式資料 | 匯出含正式資料 |
| TC-MVP1-10 | evidence 完整 | reviewer 依 evidence 重跑 2 個案例 | 結果一致 | 重跑不可重現 |

## 6. 進入 MVP2 Gate

MVP1 必須滿足：

- Qutora API、SQL Server、PDF 上傳、查詢、下載可重複執行。
- 至少 3 份合成 PDF 具備 metadata、hash 與下載紀錄。
- 可產出 DB schema inventory 與基本 audit evidence。
- 未使用正式資料。
- 已確認 Qutora 作為本演練舊系統的限制，並由人類接受是否進入 MVP2。

