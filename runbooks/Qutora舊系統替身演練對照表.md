# Qutora 舊系統替身演練對照表

版本：v1.0  
狀態：草案  
適用範圍：ReportDemo Migration Lab 執行演練

## 1. 結論

Qutora 應定位為「舊系統替身」與「執行演練沙盒」，不是原計畫中券商內部人員交易報表舊系統的等價替代品。

本專案可以用 Qutora 驗證以下能力：

- 既有 ASP.NET / .NET API 系統如何被盤點、啟動、凍結版本與納入遷移演練。
- 既有 SQL Server 資料庫如何作為 legacy leader，被新系統以 Shadow Validation 或資料抽取方式比對。
- 既有文件管理、下載、權限、稽核與儲存流程如何被對照到新系統的下載閘道、浮水印、稽核與治理設計。
- Agent Team 如何基於舊系統替身進行任務拆解、證據收集、驗收與人類決策升級。

本專案不應宣稱 Qutora 已涵蓋券商內部人員交易報表的完整業務邏輯、正式資料、法遵規則或報表計算結果。

## 2. 對照原則

Qutora 的使用方式採「功能替身」而非「業務等價」：

- 可用 Qutora 的文件、分類、metadata、下載與稽核功能，模擬舊系統中的報表媒體儲存與查閱流程。
- 可用 Qutora 的 SQL Server Docker Compose 環境，模擬舊系統 MSSQL leader。
- 可用合成 PDF、脫敏 PDF 或 Golden Dataset 輸出 PDF，模擬舊系統既有報表成品。
- 不修改 Qutora 原始碼作為第一階段原則；先以設定、測試資料、API 操作與外部驗證腳本完成演練。
- 若後續確定需要修改 Qutora，只能作為「舊系統客製化模擬層」，不得混入新系統目標架構。

## 3. 舊系統與 Qutora 對照表

| 原計畫中的舊系統概念 | Qutora 替身元件 | 可驗證內容 | 限制 |
| --- | --- | --- | --- |
| 舊系統報表媒體儲存 | Document / DocumentVersion / StorageProvider | PDF 主檔上傳、版本、儲存路徑、metadata | 不等於券商報表產製邏輯 |
| 舊系統 PDF 查閱與下載 | Documents API / Shared Documents | 查詢、下載、分享、下載路徑控管 | 不含新系統下載閘道與動態浮水印 |
| 舊系統報表分類 | Category / Metadata Schema | 報表分類、欄位、搜尋條件 | 需自行定義模擬報表代號與欄位 |
| 舊系統權限群組 | Roles / Claims / Bucket Permissions / API Keys | 管理權限、API 權限、儲存桶權限 | 不等同 AD / SSO / Data Scope 完整模型 |
| 舊系統稽核紀錄 | Audit Logs / Audit Middleware | 操作紀錄、API 存取紀錄、基礎事件追蹤 | 不等同 Hash Chain、WORM 或金融級不可竄改稽核 |
| 舊系統資料庫 | SQL Server container / QutoraDB | DB schema、資料抽取、備份、Shadow DB 演練 | 不是原券商 DB schema，不能驗證 SP 業務結果 |
| 舊系統批次或排程 | 外部 seed script / API replay / 測試腳本 | 產生測試資料、重複執行、驗證輸出 | Qutora 本身不代表券商 batch job |
| 舊系統報表產製 | 合成 PDF 或 Golden Dataset PDF | 新舊 PDF 檔案比對、hash、metadata、下載流程 | 不驗證報表計算與業務規則 |
| 舊系統浮水印 | 樣本 PDF 或新系統側處理 | 可作為新系統 M5-02 驗收輸入 | Qutora 不應被宣稱具備完整浮水印安全能力 |

## 4. 建議演練流程

1. 啟動 Qutora SQL Server Docker Compose，固定 submodule commit 與環境設定。
2. 建立模擬 admin、一般使用者、稽核使用者與 API key。
3. 匯入一批合成 PDF，使用報表代號、部門、機密等級、產製批次、版本號作為 metadata。
4. 將 Qutora DB 與檔案儲存區視為舊系統 leader，執行資料盤點與 baseline hash。
5. 以 API 或 SQL 抽取 metadata 與檔案資訊，產出 Shadow Validation 輸入。
6. 對照功能里程碑 M0、M4、M5、M7、M8、M9 任務卡，記錄可驗證項目與缺口。
7. 對下載、權限、稽核、PDF hash、版本差異建立 evidence，作為後續新系統演練的舊系統基準。

## 5. 不可宣稱事項

以下事項不得因導入 Qutora 而宣稱已完成：

- 不得宣稱已涵蓋正式券商內部人員交易報表全部功能。
- 不得宣稱已驗證原舊系統 SP、view、trigger、batch job 與報表計算邏輯。
- 不得宣稱已完成正式資料遷移；測試仍應使用合成資料、脫敏資料或受控 Shadow Validation Data。
- 不得宣稱 Qutora 權限模型等同正式 AD / SSO / RBAC + Data Scope 模型。
- 不得宣稱 Qutora 稽核紀錄等同 Hash Chain、WORM、不可竄改稽核鏈。
- 不得宣稱 Qutora 已完成 PDF 動態浮水印、數位簽章、timestamp 或高機密安全預覽。

## 6. 對任務卡的影響

Qutora 可優先支援下列任務卡的演練：

- M0-01：舊系統報表與功能盤點，可用 Qutora 文件、分類與 metadata 模擬。
- M0-02：舊系統資料來源盤點，可用 Qutora SQL Server schema 與 storage volume 模擬。
- M0-03：舊系統結果基準，可用合成 PDF hash、metadata export 與下載結果模擬。
- M4-01 至 M4-04：PDF metadata、儲存區、主檔完整性與 reconciliation。
- M5-01：下載閘道，可用 Qutora 下載 API 作為舊下載路徑 baseline。
- M5-02：動態浮水印，可用 Qutora 原始 PDF 作為未加浮水印的輸入基準。
- M5-03：下載副本 hash，可用 Qutora 下載輸出建立 hash 對照。
- M7-01 至 M7-03：稽核查詢、log 保護、警示分級，可用 Qutora audit log 作基礎事件來源。
- M8-01 至 M8-03：角色、資料範圍與 break-glass，可用 Qutora 權限能力做差距分析。
- M9-01 至 M9-05：Shadow DB、Go/No-Go、Rollback、Pilot 與舊系統下線門檻。

## 7. 建議補強項目

為了讓演練更貼近原計畫，建議後續新增但不急於第一天完成：

- `fixtures/legacy-reports/`：存放合成 PDF 與 Golden Dataset PDF。
- `fixtures/legacy-metadata/`：存放報表代號、機密等級、部門、批次與預期 hash。
- `scripts/legacy-seed/`：透過 Qutora API 建立分類、metadata schema、使用者與文件。
- `scripts/legacy-validate/`：輸出 Qutora DB / API / 檔案 hash 的 evidence。
- `runbooks/qutora-startup.md`：記錄啟動、初始化、匯入、驗證與關閉流程。

## 8. 驗收口徑

Qutora 替身演練完成時，至少應產出：

- 固定 Qutora commit、Docker Compose 設定與啟動紀錄。
- 一批可重複匯入的合成 PDF 與 metadata。
- 舊系統替身 baseline：PDF hash、metadata export、下載 API 結果、audit log。
- 差距清單：哪些能力由 Qutora 覆蓋，哪些能力由新系統或外部驗證腳本補上。
- 人類簽核紀錄：確認 Qutora 僅作為演練替身，不作為正式券商舊系統等價證明。
