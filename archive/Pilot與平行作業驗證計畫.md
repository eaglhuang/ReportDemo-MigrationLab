# 封存聲明

本文件已封存並停止維護。有效內容已併入 `drills/分階段演練與驗收計畫.md` 的 Pilot 章節；請勿再以本文件作為 active source of truth。

---

# Pilot 與平行作業驗證計畫

版本：v1.0  
狀態：draft  
最後更新：2026-07-03

## 1. 目標

Pilot 目標是把 MVP2 的 PoC 擴大成一組可代表實務風險的完整流程：從 Qutora 抽取 PDF 與 metadata，轉入 MariaDB 與新系統儲存層，透過下載閘道與浮水印輸出，並以平行作業方式比對新舊結果。

Pilot 仍不代表正式上線，只用於證明擴大資料量、權限、稽核、告警與 rollback 是否可控。

## 2. 真實功能帶入範圍

- 以 Qutora 中一批合成 PDF 作為 Pilot 報表集合。
- 抽取 Qutora SQL Server 資料並轉入 MariaDB。
- 對照新舊文件 metadata、PDF 主檔 hash、下載副本 hash。
- 套用 RBAC + Data Scope 初版規則。
- 對下載、拒絕、錯誤、浮水印失敗、audit 失敗建立分級 log 與告警。
- 執行一輪平行作業：Qutora 舊路徑與新系統路徑都產生可比對 evidence。

## 3. 交付物

- `evidence/Pilot/pilot-scope.md`
- `evidence/Pilot/migration-batch-result.md`
- `evidence/Pilot/parallel-run-compare.csv`
- `evidence/Pilot/security-audit-result.md`
- `evidence/Pilot/pilot-risk-log.md`
- Pilot 結論：Go to Production Candidate / 擴大 Pilot / 回到 MVP2 調整。

## 4. Validators

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| V-PILOT-01 | Pilot PDF 清單 | 檢查 Qutora document ids | 每筆有唯一 legacy reference | reference 重複或缺失 |
| V-PILOT-02 | Pilot batch | 執行 migration dry run | 成功產出 batch id | 無 batch id |
| V-PILOT-03 | migration 完成 | 比對筆數 | Qutora 與 MariaDB 筆數一致 | 無差異說明的不一致 |
| V-PILOT-04 | PDF 主檔移轉 | 比對 master hash | hash 一致 | 主檔 hash 不一致 |
| V-PILOT-05 | Data Scope 規則 | 權限矩陣驗證 | 可看與不可看結果符合矩陣 | 越權 |
| V-PILOT-06 | 下載流程 | 批次下載抽樣 | 每次有 download id、hash、audit | 任一欄位缺失 |
| V-PILOT-07 | audit log | 查詢 Pilot 操作 | 可用 correlation id 串接 | trace 中斷 |
| V-PILOT-08 | 告警規則 | 模擬高風險錯誤 | 送出正確嚴重度 | 嚴重錯誤未告警 |
| V-PILOT-09 | 平行作業 | 比對 Qutora 舊路徑與新路徑 | 差異被分類並可解釋 | 未分類差異 |
| V-PILOT-10 | Pilot evidence | reviewer 抽查 | evidence 足以重建流程 | 證據不足 |

## 5. Test Cases

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| TC-PILOT-01 | 20 份合成 PDF | 執行 Pilot migration | 全部進入 MariaDB staging | 任一筆無原因失敗 |
| TC-PILOT-02 | 有一筆重複 metadata | 執行 migration | 進入 rejected 或 warning | 靜默覆蓋 |
| TC-PILOT-03 | 一般使用者 | 查詢可見文件 | 僅看到授權範圍 | 看到未授權文件 |
| TC-PILOT-04 | Admin 使用者 | 管理角色但不自動取得報表內容 | Admin 無內容權限時不可下載 | Admin 自動越權 |
| TC-PILOT-05 | 高機密樣本 | 嘗試下載 | 依策略拒絕或要求額外 gate | 未加控管直接下載 |
| TC-PILOT-06 | audit DB 暫時失敗 | 執行關鍵下載 | fail-closed 或進明確 retry 策略 | 靜默遺失 audit |
| TC-PILOT-07 | PDF 主檔缺失 | 執行下載 | 標準錯誤碼與告警 | 500 無上下文 |
| TC-PILOT-08 | 大檔 PDF | 執行浮水印 | 在效能門檻內完成或明確 timeout | 長時間卡死 |
| TC-PILOT-09 | 平行作業日 | 匯出新舊 compare report | 差異列出 owner 與處理狀態 | 差異無 owner |
| TC-PILOT-10 | rollback dry run | 回復 Pilot batch | 查詢與下載回到切換前狀態 | 無法回復 |

## 6. 進入 Production Candidate Gate

- Pilot batch 完成且差異皆已分類。
- 權限、Data Scope、audit、告警均無 P0/P1 open finding。
- rollback dry run 通過。
- 平行作業 evidence 已由 Tech Lead、QA / Security、Backend / DBA review。
- 若有未解釋資料差異、越權、audit 遺失或 rollback 失敗，不得進入 Production Candidate。
