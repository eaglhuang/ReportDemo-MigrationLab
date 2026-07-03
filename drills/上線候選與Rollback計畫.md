# 上線候選與 Rollback 計畫

版本：v1.0  
狀態：draft  
最後更新：2026-07-03

## 1. 目標

上線候選階段目標是確認系統具備正式切換前的證據鏈：Go / No-Go 條件、備份、restore、rollback、break-glass、緊急維修通道、稽核證據與人類簽核。

本階段仍可決定 No-Go；保守穩定優先於趕時程。

## 2. 真實功能帶入範圍

- 以 Pilot 通過的 Qutora 舊系統資料集作為上線候選資料。
- 建立 final migration package：PDF 主檔、metadata、MariaDB 資料、稽核 seed、設定與權限矩陣。
- 執行備份與 restore：MariaDB、PDF storage、設定、audit evidence。
- 執行 rollback：停用新下載路徑、回到 Qutora 舊系統路徑、保留切換期間 evidence。
- 執行 break-glass：限時、限範圍、雙人覆核、完整 audit。

## 3. 交付物

- `evidence/ProductionCandidate/go-no-go-checklist.md`
- `evidence/ProductionCandidate/backup-restore-result.md`
- `evidence/ProductionCandidate/rollback-result.md`
- `evidence/ProductionCandidate/break-glass-result.md`
- `evidence/ProductionCandidate/sign-off-record.md`
- 最終結論：Go / No-Go / 延後上線。

## 4. Validators

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| V-PC-01 | Pilot evidence | 檢查所有 P0/P1 finding | 無 open P0/P1 | 仍有 P0/P1 |
| V-PC-02 | final migration package | 檢查 manifest | DB、PDF、metadata、設定齊全 | manifest 不完整 |
| V-PC-03 | MariaDB backup | 執行 restore 到隔離環境 | 筆數與 hash 一致 | restore 失敗 |
| V-PC-04 | PDF storage backup | 抽樣還原主檔 | master hash 一致 | hash 不一致 |
| V-PC-05 | 設定備份 | 還原權限矩陣 | 權限結果一致 | 權限漂移 |
| V-PC-06 | rollback runbook | dry run rollback | 可回到 Qutora 舊路徑 | rollback 步驟失敗 |
| V-PC-07 | break-glass 流程 | 模擬緊急授權 | 限時、限範圍、雙人覆核、audit | 無雙人覆核或 audit |
| V-PC-08 | Go / No-Go checklist | 人類簽核檢查 | 業務、資安、稽核、維運簽核齊全 | 任一必要簽核缺失 |
| V-PC-09 | 告警通道 | 模擬 critical event | 即時通報正確對象 | critical 未通報 |
| V-PC-10 | 最終 evidence | reviewer 抽查 | 可重建切換與回復流程 | evidence 不足 |

## 5. Test Cases

| ID | 輸入條件 | 執行方式 | 預期結果 | 阻擋條件 |
| --- | --- | --- | --- | --- |
| TC-PC-01 | final package ready | 執行正式切換 rehearsal | 新路徑可查詢與下載 | rehearsal 失敗 |
| TC-PC-02 | 切換後資料 | 比對 Qutora 與新系統抽樣 | 抽樣一致或差異已簽核 | 未解釋差異 |
| TC-PC-03 | 新系統下載失敗 | 執行 fallback | 回到舊路徑且留下 audit | fallback 不可用 |
| TC-PC-04 | MariaDB 故障 | restore 最近備份 | RTO/RPO 符合門檻 | 超出門檻 |
| TC-PC-05 | PDF storage 故障 | 還原抽樣 PDF | hash 一致且可下載 | 主檔不可還原 |
| TC-PC-06 | 權限設定錯誤 | 啟動緊急修復 | 修復需雙人覆核與 evidence | 單人可改高權限 |
| TC-PC-07 | audit 寫入失敗 | 執行關鍵操作 | fail-closed 或進核准 retry | 靜默成功 |
| TC-PC-08 | critical alert | 觸發告警 | 即時訊息與 email 依嚴重度送出 | 通報漏送 |
| TC-PC-09 | break-glass 到期 | 檢查權限回收 | 權限自動失效 | 權限殘留 |
| TC-PC-10 | Go / No-Go 會議 | 檢查 evidence pack | 可做出 Go / No-Go 決策 | 證據不足需延後 |

## 6. Go / No-Go Gate

Go 前必須具備：

- Pilot 差異已清零或全部簽核。
- DB、PDF、設定、audit evidence 的 backup / restore 演練通過。
- rollback dry run 通過，且 Qutora 舊路徑仍可作為回復基準。
- 權限、Data Scope、audit fail-closed、告警、break-glass 均通過。
- 業務、資安、稽核、維運、Tech Lead 完成簽核。

任一 P0/P1 風險未關閉，或證據不足以支持 rollback，均為 No-Go。

