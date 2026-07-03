# 演練版本異動摘要 ChangeLog

## 2026-07-03：Qutora 舊系統定義與演練文件群建立

## 新增

| 異動 | 併入文件 |
| --- | --- |
| 新增演練總入口，明確定義本演練舊系統採用 Qutora。 | `drills/演練總計畫書.md` |
| 新增 MVP1 兩週風險驗證計畫，列出 Qutora 啟動、PDF、metadata、DB、下載、audit 的 validators 與 test cases。 | `drills/MVP1兩週風險驗證計畫.md` |
| 新增演練文件索引與引用關係，固定三份主文件、ADR、Agent Team、drills 與 tasks 的引用方向。 | `drills/演練文件索引與引用關係.md` |
| 新增 ADR-012「本演練舊系統採用 Qutora」。 | `決策紀錄樣板ADR.md` |

## 修改

| 異動 | 併入文件 |
| --- | --- |
| README 改為說明 Qutora 是本演練舊系統，不再稱為舊系統替身。 | `README.md` |
| tasks README 新增 Qutora 舊系統定義與完整任務卡開工 gate。 | `tasks/README.md` |
| 根目錄 ChangeLog 加入本次演練文件群引用。 | `版本異動摘要ChangeLog.md` |

## 刪除或取代

| 舊說法 / 舊文件 | 新說法 / 取代方式 |
| --- | --- |
| `runbooks/Qutora舊系統替身演練對照表.md` | 已 superseded。內容併入 `drills/演練總計畫書.md` 與 `drills/MVP1兩週風險驗證計畫.md`。 |
| 「Qutora 是舊系統替身」 | 已 superseded。改為「本演練舊系統採用 Qutora」。 |
| 「沙盒對照表」 | 已 superseded。不再維護獨立對照表。 |

## 改列 ADR 或人類簽核

- Qutora 作為本演練舊系統：ADR-012。
- 是否允許修改 Qutora 原始碼：若要修改，需新增 ADR 或人類簽核。
- 若要把 Qutora 驗證結果外推到真實券商舊系統，需人類簽核，且不得自動宣稱等價。

