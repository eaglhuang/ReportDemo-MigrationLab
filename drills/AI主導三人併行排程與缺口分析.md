# ReportDemo AI 主導三人併行排程與缺口分析

版本：v1.0  
狀態：active  
最後更新：2026-07-07

## 1. 文件目的

本文件在 `drills/分階段演練與驗收計畫.md` 之上，補充「三人皆具 AI 開發環境」時的壓縮排程與缺口分析。它不取代原演練計畫的 Gate、evidence、rollback、ADR 或 human sign-off；它只回答：AI 主開發後，三人小隊如何在每日 8 小時、週末不工作的限制下重排工作。

## 2. 執行前提

| 前提 | 內容 |
| --- | --- |
| 團隊規模 | 3 人：Tech Lead / Captain、Backend / DBA、QA / Security / DevOps。 |
| AI 環境 | 三人皆已具備可立即使用的 AI 開發環境。 |
| 工作模式 | AI 主開發、產生程式碼、測試、runbook、validator、evidence 草稿；人類負責監控、決策、審查、驗收數據與簽核。 |
| 工時限制 | 每人每日最多 8 小時，每週 5 個工作日，週末不排正式工作。 |
| 團隊容量 | 每週最多 120 人時；至少 20% 保留給 review、驗收、整合、返工與卡點處理。 |
| 正式限制 | AI 不得取代 human / ADR gate，不得使用未脫敏正式資料，不得修改 Qutora submodule 作為第一階段原則。 |

## 3. 標籤

| 標籤 | 定義 | 可交付 | 不可越界 |
| --- | --- | --- | --- |
| `[AI]` | AI 主責執行。 | 程式碼、SQL、PoC、validator、測試、文件草稿、evidence 草稿、差異分析。 | 不得自行接受風險、放行 Gate、使用正式資料或改變治理邊界。 |
| `[AI->HUMAN]` | AI 先產出，人類 review 後才算完成。 | 負向測試、資安檢查、稽核 evidence、差異分類草稿。 | 未經人類 review 不得 closure。 |
| `[HUMAN]` | 只能由人類或指定人類代理主導。 | ADR、資安 / 稽核例外、權限模型接受、Go / No-Go、簽核、驗收數據接受。 | 不得把 human gate 交給 AI 代簽。 |
| `[GATE]` | 階段阻擋條件。 | Gate summary、sign-off record、blocking finding 裁決。 | 未通過不得進下一階段。 |

## 4. 時程估算

| 情境 | 用途 | 週數 | 條件 |
| --- | --- | ---: | --- |
| Best Case | AI 環境順、PoC 不卡、人類 review queue 很順。 | 8 到 10 週 | 只可作為挑戰目標，不作正式承諾。 |
| Base Plan | 建議採用的正式演練口徑。 | 12 到 14 週 | 每週保留 review / rework 容量，Pilot 前置 Backlog 能按時補齊。 |
| Risk Buffer | Qutora / PDF / 權限 / 稽核 / rollback 卡住。 | 16 到 18 週 | W3 MVP2 fail-closed evidence 不足時自動切回。 |

建議採用 **14 週完成 Production Candidate 演練** 作為 Base Plan。若 W3 結束時下載閘道、浮水印、hash 或 audit fail-closed 任一項無法留下可重跑 evidence，需立即改採 16 到 18 週保守排程。

## 5. 14 週 AI 主導排程

| 週次 | 主要目標 | AI 主導工作 | 人類主導工作 | Gate / Evidence |
| --- | --- | --- | --- | --- |
| W1 | MVP1 完成 | `[AI]` 讀 Qutora 原始碼、產出 inventory 草稿、跑合成 PDF、整理 metadata / hash evidence。 | `[HUMAN]` 確認 Qutora 能力限制、接受 fallback、審查 MVP1 Gate。 | `[GATE]` Qutora 可啟動；PDF / metadata / DB / audit baseline 可重跑。 |
| W2 | MVP2 基礎 | `[AI]` 產 MariaDB staging SQL、mapping、audit event schema、Data Scope matrix。 | `[HUMAN]` 審查 MariaDB 演練邊界、Data Scope 是否符合最小權限。 | `[GATE]` staging 可重建；audit / scope 失敗時 fail-closed。 |
| W3 | MVP2 下載與浮水印 PoC | `[AI]` 產 `poc/download-gateway`、`poc/watermark`、hash validator 與測試。 | `[HUMAN]` 驗收越權、未浮水印輸出、audit 寫入失敗等阻擋案例。 | `[GATE]` MVP2 validators 可追溯；不可繞過下載閘道。 |
| W4 | Pilot 前置補洞 1 | `[AI]` 升級 `TASK-RPT-0011`、`0012`、`0015`、`0016`、`0017` 規格與最小 PoC。 | `[HUMAN]` 決定 validation rule 與 report template 的演練範圍。 | `[GATE]` 新舊驗證與雙製比對不再依賴未定義 Backlog。 |
| W5 | Pilot 前置補洞 2 | `[AI]` 升級 `TASK-RPT-0020`、`0034`、`0039` 規格與 evidence skeleton。 | `[HUMAN]` 審查 PDF storage、log sensitive masking、Shadow DB 邊界。 | `[GATE]` Pilot 核心卡依賴清空或均有可驗收替代方案。 |
| W6 | Pilot 批次移轉 | `[AI]` 產批次移轉腳本、reconciliation report、差異分類器。 | `[HUMAN]` 審查差異分類與可接受偏差。 | `[GATE]` Qutora 與 MariaDB 筆數 / hash 差異可解釋。 |
| W7 | Pilot 雙製與 PDF integrity | `[AI]` 產雙製比對、PDF 主檔 hash manifest、reconciliation evidence。 | `[HUMAN]` 驗收 PDF 主檔不可被靜默異動。 | `[GATE]` 主檔 hash、metadata、版本、legacy reference 可追溯。 |
| W8 | Pilot 權限、稽核、告警 | `[AI]` 產權限負向測試、audit query、log routing simulation。 | `[HUMAN]` 審查資安、稽核與告警嚴重度路由。 | `[GATE]` 越權不得通過；稽核不可靜默遺失。 |
| W9 | Pilot 平行作業收斂 | `[AI]` 彙整 Pilot gate package、open issues、返工清單。 | `[HUMAN]` 決定 Pilot 是否可進 Production Candidate。 | `[GATE]` 平行作業差異已分類、blocking issue 有 owner。 |
| W10 | Production Candidate 基礎 | `[AI]` 產 backup / restore script、rollback evidence 草稿、UAT checklist。 | `[HUMAN]` 決定 RTO / RPO 門檻與 rollback 接受標準。 | `[GATE]` restore 到隔離環境成功，RTO / RPO 可量測。 |
| W11 | Break-glass 與維運 | `[AI]` 產 break-glass dry run 記錄草稿、權限到期檢查、維運手冊草稿。 | `[HUMAN]` 執行 dual-control、核准與限時操作；審查 MFA / PAM 是否列正式決策。 | `[GATE]` 緊急權限限時、限範圍、可稽核。 |
| W12 | UAT 與 Go / No-Go package | `[AI]` 產 UAT evidence、Go / No-Go package、release candidate report。 | `[HUMAN]` 業務 / 稽核 / 資安 / 維運代理簽核。 | `[GATE]` sign-off record 完整，open risks 可接受。 |
| W13 | 修補 blocking findings | `[AI]` 修正 validator、文件、PoC、evidence 缺口。 | `[HUMAN]` 重驗阻擋項與 ADR 未決項。 | `[GATE]` blocking findings 歸零或降級並簽核。 |
| W14 | 最終演練收斂 | `[AI]` 打包 final evidence、產生總結與交接清單。 | `[HUMAN]` 最終 Go / No-Go 演練決策；確認是否進真實專案下一階段。 | `[GATE]` Production Candidate evidence package 可審核、可重跑、可追溯。 |

## 6. 每日固定循環

| 時段 | Tech Lead / Captain | Backend / DBA | QA / Security / DevOps |
| --- | --- | --- | --- |
| 09:00-09:30 | `[HUMAN]` daily triage、決定今日 Gate / blocker。 | `[AI->HUMAN]` 回報 AI 產出與風險。 | `[AI->HUMAN]` 回報測試 / evidence 狀態。 |
| 09:30-12:00 | `[AI]` 產任務拆解、review checklist、ADR 草稿。 | `[AI]` 產 SQL / PoC / migration / API。 | `[AI]` 產 validator / test / evidence script。 |
| 13:00-15:30 | `[AI->HUMAN]` review AI 產出、合併衝突、裁定 scope。 | `[AI->HUMAN]` 修正 AI 產出並跑本機驗證。 | `[AI->HUMAN]` 重跑測試、整理失敗與遮罩敏感資訊。 |
| 15:30-17:00 | `[HUMAN]` blocker review、是否升級 ADR / human gate。 | `[AI]` 補 implementation notes。 | `[AI]` 補 evidence index、gate summary。 |
| 17:00-18:00 | `[GATE]` 當日可重跑證據檢查；未過項目進 blocker list。 | `[AI->HUMAN]` 交付可重跑命令。 | `[AI->HUMAN]` 確認 producer 不自審。 |

週末不排正式工作。若 AI 在週末自動產出草稿，視為非正式輸入，必須等下一個工作日由人類 review 後才可納入 evidence 或任務 closure。

## 7. WIP 與 Review 上限

| 規則 | 內容 |
| --- | --- |
| 每人每日 review 上限 | 原則上最多 3 張任務卡或 3 組 evidence package。 |
| AI 產出限制 | AI 可多產草稿，但超過 review queue 的內容不得標記完成。 |
| 不得自審 | 產出該 evidence 的 AI session、Agent 或人類 producer，不得單獨擔任 reviewer。 |
| blocking 優先 | 資安、稽核、資料一致性、權限、rollback、Go / No-Go 類 finding 優先於新增功能。 |
| 每週容量保留 | 至少 20% 團隊容量保留給 review、整合、返工與 Gate。 |

## 8. 必須補強的缺口

| 缺口 | 影響 | 修正方式 |
| --- | --- | --- |
| 原排程未區分 AI 主導情境。 | 人類可能誤以為所有情境都需 18 週或都可 6 週完成。 | 本文件作為 AI 主導排程補充；原演練計畫保留穩健 Gate。 |
| 任務卡未明確標示 `[AI]` / `[AI->HUMAN]` / `[HUMAN]` / `[GATE]`。 | 派工時容易把決策交給 AI 或把 AI 可做的工作塞給人類。 | `tasks/README.md` 加 `execution_mode` 規則；核心卡後續逐批補欄位。 |
| Pilot 核心卡依賴 Backlog 卡。 | 若不補 `0011/0012/0015/0016/0017/0020/0034/0039`，W6 後會卡住。 | W4-W5 排入 Pilot 前置補洞，不得省略。 |
| AI 產出速度快，但 reviewer 容量固定。 | 可能出現大量未驗收程式與 evidence。 | 每週保留至少 20% 團隊容量給 review / rework；producer 不得自審。 |
| 人類 Gate 未量化每日節奏。 | 可能每天都在寫，直到週末才發現不能過 Gate。 | 每日 17:00 做當日 evidence / blocker 檢查。 |
| 週末 AI 草稿歸屬不明。 | 可能產生未審查內容被誤納入 evidence。 | 週末 AI 產出只能算 draft，下一工作日 review 後才可用。 |
| `poc/` 還是骨架。 | MVP2 壓縮到 3 週的前提不成立。 | W2-W3 必須補最小下載閘道、浮水印、hash validator。 |
| 正式技術選型仍未決。 | AI PoC 可能被誤當正式架構。 | ADR-015 僅限演練；正式 PDF library、SSO、Object Storage、WORM 仍需 ADR。 |

## 9. 不可被 AI 壓縮的 Gate

| Gate | 不可壓縮原因 |
| --- | --- |
| 正式資料使用邊界 | 涉及法遵、資安與資料治理，需人類簽核。 |
| DB / PDF library / Storage 正式選型 | 涉及授權、維運、成本與長期風險，需 ADR。 |
| 權限模型與 Admin 職責分離 | 涉及越權與稽核責任，需人類確認。 |
| Audit fail-closed 與 WORM / 保存政策 | 涉及證據能力與監理風險，需稽核 / 資安參與。 |
| Pilot / Go-No-Go / 舊系統下線 | 涉及正式責任歸屬，AI 只能彙整建議。 |

## 10. 結論

建議採用：

```text
MVP1: 1 週
MVP2: 2 週
Pilot 前置補洞: 2 週
Pilot: 4 週
Production Candidate: 3 週
修補與收斂: 2 週
總計: 14 週
```

此 14 週是 AI 主導三人小隊的 Base Plan，不是保證時程。若 W3 結束時 MVP2 的下載閘道、浮水印、hash、audit fail-closed 任一項不能留下可重跑 evidence，需立即改採 16 到 18 週保守排程。
