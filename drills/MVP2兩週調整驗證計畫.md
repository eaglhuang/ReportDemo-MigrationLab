# MVP2 兩週調整驗證計畫

版本：v1.0  
狀態：draft  
最後更新：2026-07-03

## 1. 目標

MVP2 目標是在 MVP1 已證明 Qutora 可作為本演練舊系統後，用 2 週驗證第一批新系統關鍵風險：MariaDB 初版轉換、下載閘道 PoC、動態浮水印 PoC、下載副本 hash 與第一批可自動化 validator。

MVP2 不是完整搬移，也不是正式上線候選；它的價值是盡早驗證最容易失敗的技術接點。

## 2. 真實功能帶入範圍

- 從 Qutora SQL Server 抽取文件、metadata、使用者、權限與 audit 樣本。
- 建立 MariaDB 初版目標 schema，保留 Qutora document id 與 legacy reference。
- 建立下載閘道 PoC：以 Qutora 下載結果作為舊系統 baseline，新系統下載必須經授權、稽核與 hash。
- 建立動態浮水印 PoC：下載副本加入下載人、部門、時間、來源 IP、下載序號、文件 id 與查核碼。
- 建立 validator 雛形：DB 筆數、metadata 欄位、PDF hash、權限拒絕、audit 欄位。

## 3. 交付物

- `evidence/MVP2/mariadb-schema-v0.md`
- `evidence/MVP2/qutora-to-mariadb-mapping.md`
- `evidence/MVP2/download-gateway-poc.md`
- `evidence/MVP2/watermark-poc.md`
- `evidence/MVP2/validator-results.md`
- MVP2 結論：Go to Pilot / 調整策略 / 回到 MVP1 補洞。

## 4. Validators

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| V-MVP2-01 | MVP1 metadata export | 匯入 MariaDB staging | 筆數與 MVP1 匯出一致 | 筆數不一致且無差異說明 |
| V-MVP2-02 | Qutora document sample | 建立 legacy reference 對照 | 每筆保留 Qutora document id | legacy reference 遺失 |
| V-MVP2-03 | MariaDB schema v0 | 檢查必要索引 | document id、report code、confidentiality 可查詢 | 關鍵查詢需 full scan |
| V-MVP2-04 | 有授權使用者 | 呼叫下載閘道 PoC | 回傳檔案與 download id | 無 download id |
| V-MVP2-05 | 無授權使用者 | 呼叫下載閘道 PoC | fail-closed 拒絕 | 越權下載成功 |
| V-MVP2-06 | 下載成功 | 查詢下載稽核 | 有 user、document、IP、time、result | 稽核欄位缺失 |
| V-MVP2-07 | 下載成功 | 計算下載副本 hash | hash 被記錄且可重算 | hash 不可重現 |
| V-MVP2-08 | 浮水印 PoC PDF | 檢查可見浮水印欄位 | 至少包含 user、time、serial、check code | 浮水印缺核心欄位 |
| V-MVP2-09 | 下載閘道錯誤 | 模擬 PDF 不存在 | 回傳標準錯誤碼且有 audit | 靜默失敗或無 audit |
| V-MVP2-10 | 完成前 9 項 | 產出 MVP2 validation summary | reviewer 可追溯每項 evidence | evidence 不完整 |

## 5. Test Cases

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| TC-MVP2-01 | MVP1 有 3 份 PDF | 執行 SQL Server 到 MariaDB 抽樣移轉 | MariaDB 有 3 筆文件 metadata | 移轉不可重跑 |
| TC-MVP2-02 | metadata 有機密等級 | 查詢 MariaDB confidentiality | 機密等級正確映射 | 機密等級遺失 |
| TC-MVP2-03 | 使用者有權限 | 透過下載閘道下載 PDF | 成功下載並產生 audit | 直接繞過 gateway |
| TC-MVP2-04 | 使用者無權限 | 透過下載閘道下載 PDF | 回傳 forbidden | 越權成功 |
| TC-MVP2-05 | PDF 主檔存在 | 執行浮水印處理 | 產生下載副本，不覆蓋主檔 | 主檔被修改 |
| TC-MVP2-06 | 來源 IP 存在 | 產生浮水印 | PDF 可見來源 IP 或內部識別 | IP 欄位缺失 |
| TC-MVP2-07 | 下載副本產生 | 比對主檔 hash 與副本 hash | 兩者分開記錄 | hash 混用 |
| TC-MVP2-08 | 模擬 PDF library 失敗 | 呼叫下載 | fail-closed，不回傳未浮水印 PDF | 回傳未處理 PDF |
| TC-MVP2-09 | 模擬 audit 寫入失敗 | 呼叫下載 | 關鍵下載 fail-closed | 下載成功但無 audit |
| TC-MVP2-10 | reviewer 重跑案例 | 重跑 TC-MVP2-03 與 TC-MVP2-08 | 結果一致且 evidence 可追溯 | 不可重現 |

## 6. 進入 Pilot Gate

- MariaDB schema v0 可承接 MVP1 的 Qutora metadata。
- 下載閘道 PoC 已具備授權、audit、download id、錯誤碼與 fail-closed。
- 動態浮水印 PoC 不修改 PDF 主檔，且下載副本 hash 可重算。
- 至少 10 條 validators 與 10 條 test cases 可重跑。
- 若 PDF library、MariaDB mapping 或 audit fail-closed 無法成立，不得進入 Pilot。

