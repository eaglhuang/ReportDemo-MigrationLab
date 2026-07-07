# RB-09 Backup Recovery Policy

目的：定義演練用備份、回復、備份驗證、保存、加密與事故應變決策樹。RB-04 定義「如何做一次 rollback dry run」；本文件定義「什麼情境要備份、多久驗證、何時回復、誰決策」。

適用階段：W10-W14、`TASK-RPT-0040`、`TASK-RPT-0041`、`TASK-RPT-0044`。

## 1. 備份範圍

| 類型 | 範圍 | 頻率 | 保存 | 加密 |
| --- | --- | --- | --- | --- |
| MariaDB metadata | schema、staging、pdf metadata、audit pointer。 | 每日一次，cutover 前一次。 | 演練期保留至少 7 代。 | 備份檔需加密或存放於受控目錄。 |
| PDF master hash manifest | 檔名、legacy reference、SHA-256、size。 | 每批次 / 每次 Pilot run。 | 與 evidence 同保存。 | 不含 PDF 明文內容。 |
| 設定檔 | `.env` sample、routing config、policy config。 | 每次變更前後。 | 至少 7 代。 | 不保存 secret 明文。 |
| Evidence package | Gate、validator、review notes。 | 每日收工與 Gate day。 | 全演練保存。 | 不含 token / secret。 |

## 2. 備份驗證頻率

| 驗證 | 頻率 | 通過條件 |
| --- | --- | --- |
| Dump 可產生 | 每日或每批次 | dump 檔存在且大小合理。 |
| Restore 到隔離 DB | 每週至少 1 次，W10 起每次 Gate 前 1 次。 | restore 後 row count / checksum 一致。 |
| PDF hash manifest 重算 | 每次 Pilot / PC package | master hash 一致。 |
| 設定回復 | Cutover rehearsal 前 | routing / policy 可回復到前一版。 |

## 3. DR 情境分級

| 情境 | 等級 | 回復方式 | 目標 |
| --- | --- | --- | --- |
| Container 掛掉 | P2 | 重啟 container，驗證 health。 | 30 分鐘內恢復演練。 |
| MariaDB metadata 損毀 | P1 | restore 最近 dump 到隔離 DB，比對後替換。 | RTO 4 小時內，RPO 15 分鐘或最近批次。 |
| PDF master 遺失或 hash 不一致 | P0 | 停止下載，回到 Qutora 路徑，重建 master hash。 | 不輸出不可驗證 PDF。 |
| 權限設定誤放 | P0 | freeze 新路徑，撤回設定，啟動 incident review。 | 越權風險歸零。 |
| Audit 寫入失敗 | P0 | fail-closed，停止相關操作，回復 audit writer。 | 不允許靜默遺失。 |
| 誤刪 metadata / evidence | P1 | restore 備份，補 postmortem。 | 可追溯缺口有紀錄。 |

## 4. 事故應變一頁決策樹

```text
事件發生
  |
  +-- 是否涉及越權 / audit 遺失 / 未浮水印 PDF / 主檔 hash 不一致？
  |      |
  |      +-- 是：P0 -> freeze 新路徑 -> 通知 Captain + Security/Audit proxy -> 啟動 rollback 或回 Qutora -> 產 postmortem
  |      |
  |      +-- 否
  |
  +-- 是否涉及 metadata 損毀、批次不可重跑、RTO/RPO 風險？
  |      |
  |      +-- 是：P1 -> 停止 Gate -> restore 到隔離環境 -> reviewer 驗證 -> human 決定是否恢復
  |      |
  |      +-- 否
  |
  +-- 是否為可解釋格式 / 效能 / 文件差異？
         |
         +-- 是：P2/P3 -> 登記 owner + SLA -> 不得靜默關閉
```

## 5. 通報與 Postmortem

| 等級 | 通報 | 接手 | Postmortem |
| --- | --- | --- | --- |
| P0 | 即時訊息 + Email + daily report | Captain + QA / Security / DevOps | 必須，24 小時內草稿。 |
| P1 | 即時訊息或 Email | 對應 owner + reviewer | 必須，3 工作日內。 |
| P2 | daily report | 任務 owner | 視需要。 |
| P3 | weekly summary | 任務 owner | 不需要。 |

Postmortem 最少包含：

- 事件時間線。
- 影響範圍。
- root cause。
- 回復步驟。
- RTO / RPO 是否達標。
- 防止再發措施。
- 是否需 ADR 或任務卡更新。

## 6. Gate 要求

上線候選或 cutover rehearsal 前，必須具備：

- 最近一次 MariaDB restore evidence。
- 最近一次 PDF hash manifest 重算。
- rollback dry run 結果。
- P0 / P1 incident 為 0，或已簽核降級。
- 備份檔未含 secret 明文。

