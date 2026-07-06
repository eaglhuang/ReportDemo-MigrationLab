# 內部人員交易報表轉媒體儲存系統
## 版本異動摘要 Change Log

## 2026-07-07：Pilot 與 Production Candidate 核心任務卡完整格式升級

範圍：升級第三批 Pilot 核心任務卡 `TASK-RPT-0013`、`TASK-RPT-0018`、`TASK-RPT-0021`、`TASK-RPT-0022`、`TASK-RPT-0028`、`TASK-RPT-0033`、`TASK-RPT-0035`、`TASK-RPT-0036`、`TASK-RPT-0037`，以及第四批 Production Candidate 核心任務卡 `TASK-RPT-0038`、`TASK-RPT-0040`、`TASK-RPT-0041`、`TASK-RPT-0042`、`TASK-RPT-0043`、`TASK-RPT-0044`、`TASK-RPT-0045`。這 16 張卡已補齊 Qutora 演練場景、落地設計、影響範圍、Fail-Closed 規則、10 條 validators、10 條 test cases、reviewer / human gate / ADR gate。

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| Pilot 批次補齊新舊驗證、雙製比對、PDF 主檔完整性、PDF reconciliation、報表查詢、稽核 Hash Chain、告警路由、角色管理與 Data Scope 管理任務卡。 | `tasks/TASK-RPT-0013`、`0018`、`0021`、`0022`、`0028`、`0033`、`0035`、`0036`、`0037` |
| Production Candidate 批次補齊 break-glass、Go / No-Go、Rollback、UAT、Pilot 舊系統下線、Release Acceptance 與舊系統覆蓋確認任務卡。 | `tasks/TASK-RPT-0038`、`0040`、`0041`、`0042`、`0043`、`0044`、`0045` |
| `tasks/README.md` 更新第三批與第四批核心卡狀態，標示已升級為完整任務卡。 | `tasks/README.md` |
| 產卡模板補強完整任務卡 frontmatter、stage、role、evidence 與 gate 欄位要求，避免未來重產卡退回摘要格式。 | `tools/generate_reportdemo_task_cards.py` |

## 2026-07-07：MVP2 核心任務卡完整格式升級

範圍：升級 MVP2 第二批核心任務卡 `TASK-RPT-0007`、`TASK-RPT-0008`、`TASK-RPT-0010`、`TASK-RPT-0014`、`TASK-RPT-0019`、`TASK-RPT-0023`、`TASK-RPT-0024`、`TASK-RPT-0025`。這批卡已補齊真實 Qutora 演練場景、落地設計、影響範圍、Fail-Closed 規則、10 條 validators、10 條 test cases、reviewer / human gate / ADR gate，evidence 路徑統一為 `evidence/MVP2/<TASK-ID>/`。

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| `TASK-RPT-0007` 補齊匯入批次管理規格，包含批次狀態機、錯誤碼、rollback 與 Qutora 抽取邊界。 | `tasks/TASK-RPT-0007-m1-01-import-batch-management.task.md` |
| `TASK-RPT-0008` 補齊 MariaDB staging tables 規格，包含 staging schema、欄位對應、索引與驗證規則。 | `tasks/TASK-RPT-0008-m1-02-staging-tables.task.md` |
| `TASK-RPT-0010` 補齊 audit write foundation 規格，包含 fail-closed matrix、audit event schema 與 payload hash。 | `tasks/TASK-RPT-0010-m1-04-audit-write-foundation.task.md` |
| `TASK-RPT-0014` 補齊 Data Scope foundation 規格，包含 Role / Data Scope / Confidentiality deny-by-default 規則。 | `tasks/TASK-RPT-0014-m2-04-data-scope-foundation.task.md` |
| `TASK-RPT-0019` 補齊 PDF metadata 規格，包含 Qutora metadata 對應、主檔 Hash、機密等級與版本欄位。 | `tasks/TASK-RPT-0019-m4-01-pdf-metadata.task.md` |
| `TASK-RPT-0023` 補齊下載閘道落地設計，包含 API、資料表、狀態機、錯誤碼、權限檢查、稽核欄位與 fail-closed 規則。 | `tasks/TASK-RPT-0023-m5-01-download-gateway.task.md` |
| `TASK-RPT-0024` 補齊動態浮水印處理規格，明確定義浮水印為外流追蹤、嚇阻與竄改偵測輔助，不宣稱絕對防竄改。 | `tasks/TASK-RPT-0024-m5-02-dynamic-watermark.task.md` |
| `TASK-RPT-0025` 補齊下載副本 Hash 規格，區分主檔 Hash、下載副本 Hash 與 audit payload hash。 | `tasks/TASK-RPT-0025-m5-03-download-copy-hash.task.md` |
| `tasks/README.md` 更新第二批核心卡狀態，標示 MVP2 核心卡已升級為完整任務卡。 | `tasks/README.md` |

## 2026-07-06：MVP1 核心任務卡完整格式升級

範圍：只升級 MVP1 第一批核心任務卡 `TASK-RPT-0001` 到 `TASK-RPT-0004`。其他任務卡仍維持摘要格式，未補齊完整任務卡規格前不得正式開工或 closure。

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| `TASK-RPT-0001` 補齊 Qutora 文件 / 報表功能盤點、真實場景、影響範圍、10 條 validators、10 條 test cases、reviewer / human gate / ADR。 | `tasks/TASK-RPT-0001-m0-01-legacy-report-inventory.task.md` |
| `TASK-RPT-0002` 補齊 Qutora DB / entity / provider 資料來源盤點、MariaDB 轉換風險、10 條 validators、10 條 test cases。 | `tasks/TASK-RPT-0002-m0-02-legacy-data-source-inventory.task.md` |
| `TASK-RPT-0003` 補齊 Golden Dataset / 合成 PDF / metadata / hash baseline 規格與正式資料禁用 gate。 | `tasks/TASK-RPT-0003-m0-03-legacy-result-baseline.task.md` |
| `TASK-RPT-0004` 補齊 Qutora startup、DB provider、PDF / storage / auth PoC 規格與 MVP2 前置 Gate。 | `tasks/TASK-RPT-0004-m0-04-third-party-cross-platform-poc.task.md` |
| 四張核心卡 evidence 統一改為 `evidence/MVP1/TASK-RPT-000x/`。 | `tasks/TASK-RPT-0001` 到 `TASK-RPT-0004` |

## 2026-07-06：計畫文件包收斂與演練執行層重整

範圍：文件包治理、演練計畫合併、runbook 新增、evidence 規則、任務卡開工 gate 與 archive 封存。不修改 Qutora submodule、不跑 migration、不重新產 PDF、不一次升級全部 45 張任務卡。

## 新增

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| 新增唯一演練執行指南，合併 MVP1、MVP2、Pilot、Production Candidate、三人責任矩陣與 Gate 總表。 | `drills/分階段演練與驗收計畫.md` |
| 新增 Qutora 啟動 runbook。 | `runbooks/RB-01-qutora-startup.md` |
| 新增合成 PDF 與 metadata runbook。 | `runbooks/RB-02-seed-data-synthetic-pdf.md` |
| 新增 evidence 命名、驗收與 Gate package 標準。 | `runbooks/RB-03-evidence-standard.md`、`evidence/README.md` |
| 新增 rollback dry run runbook。 | `runbooks/RB-04-rollback-rehearsal.md` |
| 新增 evidence stage 骨架。 | `evidence/MVP1/`、`evidence/MVP2/`、`evidence/Pilot/`、`evidence/ProductionCandidate/` |
| 新增核心任務卡分批升級清單與 Stage 對照。 | `tasks/README.md` |

## 修改

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| README 改為唯一入口，吸收原演練文件索引的文件權威順序、三人首讀清單與 12 步路線。 | `README.md` |
| 《系統架構與治理計畫書》附錄 A 改為治理路線，細節指向功能里程碑與分階段演練計畫；附錄 C 補註本演練依 ADR-013 固定 MariaDB。 | `內部人員交易報表轉媒體儲存系統_系統架構與治理計畫書.md` 附錄 A / C |
| 《功能里程碑計畫》補充唯一 Phase↔M 對照與演練執行層引用。 | `內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md` §0 |
| Agent Team 計畫書補明與 README、分階段演練計畫、tasks README、任務卡與 runbooks 的引用關係；派工範例標示為非規範性。 | `內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md` |
| ADR-012、ADR-013、ADR-014 的影響範圍更新為新的單一演練計畫與 runbooks。 | `決策紀錄樣板ADR.md` |
| 產卡模板補上 Stage、角色、evidence 與完整任務卡 gate 欄位。 | `tools/generate_reportdemo_task_cards.py` |

## 刪除、封存或取代

| 舊文件 / 舊說法 | 新位置 / 取代方式 |
| --- | --- |
| `drills/演練總計畫書.md` | 已移入 `archive/`；有效內容併入 `drills/分階段演練與驗收計畫.md`。 |
| `drills/MVP1兩週風險驗證計畫.md` | 已移入 `archive/`；有效內容併入 `drills/分階段演練與驗收計畫.md` 的 MVP1 章節。 |
| `drills/MVP2兩週調整驗證計畫.md` | 已移入 `archive/`；有效內容併入 `drills/分階段演練與驗收計畫.md` 的 MVP2 章節。 |
| `drills/Pilot與平行作業驗證計畫.md` | 已移入 `archive/`；有效內容併入 `drills/分階段演練與驗收計畫.md` 的 Pilot 章節。 |
| `drills/上線候選與Rollback計畫.md` | 已移入 `archive/`；有效內容併入 `drills/分階段演練與驗收計畫.md` 與 `runbooks/RB-04-rollback-rehearsal.md`。 |
| `drills/演練文件索引與引用關係.md` | 已移入 `archive/`；權威順序改由 `README.md` 維護。 |
| `drills/演練版本異動摘要ChangeLog.md` | 已移入 `archive/`；根目錄 `版本異動摘要ChangeLog.md` 為唯一 active ChangeLog。 |
| 根目錄三份 PDF 快照 | 已移入 `archive/`；Markdown 穩定後再視需要重新產 PDF。 |
| 「每份 drills 文件各自維護 Gate」 | 已 superseded。Gate 統一維護於 `drills/分階段演練與驗收計畫.md`。 |

## 改列 ADR 或人類簽核

| 事項 | 規則 |
| --- | --- |
| 修改 Qutora 原始碼 | 需另開 ADR 或人類簽核；本輪不修改。 |
| 變更 MariaDB 作為本演練目標 DB | 需更新 ADR-013。 |
| 任務卡未具備完整規格仍要開工 | 需 human sign-off；預設不得開工。 |
| Production Candidate 進入正式 Go / No-Go | 需業務、稽核、資安、維運與 Tech Lead 共同簽核。 |

## 2026-07-03：演練文件群與 Qutora 舊系統定義

本次新增 `drills/` 演練文件群，並將 Qutora 直接定義為本演練舊系統。原獨立 Qutora 對照表已刪除，內容併入演練總計畫與 MVP1 兩週風險驗證計畫。2026-07-06 後，本 repo 的唯一 active ChangeLog 為本文件；原 `drills/演練版本異動摘要ChangeLog.md` 已封存。

| 異動 | 併入文件 / 章節 |
| --- | --- |
| 新增演練總計畫、MVP1、MVP2、Pilot、上線候選計畫、演練文件索引與演練 ChangeLog。 | `drills/` |
| 新增 ADR-012「本演練舊系統採用 Qutora」、ADR-013「本演練目標資料庫採用 MariaDB」、ADR-014「兩週 MVP 節奏與完整任務卡開工 Gate」。 | `決策紀錄樣板ADR.md` |
| README 與 tasks README 改為直接定義 Qutora 為本演練舊系統。 | `README.md`、`tasks/README.md` |
| 原獨立 Qutora 對照表已 superseded 並刪除。 | 內容已併入 `drills/分階段演練與驗收計畫.md` 與 `runbooks/RB-01-qutora-startup.md`。 |

## 2026-07-02：Agent Team 文件升版批次

本次新增 Agent Team 計畫書 v1.0，並將三份核心文件、任務卡 README、45 張任務卡與產卡模板同步到同一套 Agent Team 協作與簽核邊界。PDF 不在本次更新範圍，`tasks.zip` 也不重新打包。

## 新增

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| 新增《Agent Team 計畫書 v1.0》，定義本任務 Agent Team 協作 source of truth。 | `內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md` |
| 新增 Agent 角色：Captain / Coordinator、Implementer、Security / Permission、Audit / Evidence、QA / Validation、Reviewer。 | Agent Team 計畫書 §3 |
| 新增 M5-01 下載閘道與 M5-02 動態浮水印的 Agent 派工範例。 | Agent Team 計畫書 §4、§5 |
| 新增 Agent 違規阻擋機制：任務卡 scope、Permission Broker、lease / fencing、tool sandbox、validator / reviewer、closure gate。 | Agent Team 計畫書 §8 |
| 新增 ADR-011「Agent Team 自動決策、人類簽核與違規阻擋邊界」。 | `決策紀錄樣板ADR.md` §14 |
| 新增本 Change Log 文件，供各計畫書引用。 | `版本異動摘要ChangeLog.md` |

## 修改

| 異動 | 併入文件 / 章節或任務卡 |
| --- | --- |
| 《系統架構與治理計畫書》由 v1.3 升版為 v1.4。 | `系統架構與治理計畫書.md` 標題 |
| 加入文件權威順序：架構以系統架構文件為準，Agent Team 協作以 Agent Team 計畫書為準，功能拆解以功能里程碑與任務卡為準，決策以 ADR 為準。 | `系統架構與治理計畫書.md` §1 |
| 新增 Agent Team 相關附錄，說明協作、違規阻擋與簽核邊界。 | `系統架構與治理計畫書.md` 附錄 H |
| 《功能里程碑計畫》由 v1.0 升版為 v1.1。 | `功能里程碑計畫.md` 標題 |
| 第 0 章新增任務卡派工需依 Agent Team 計畫書 v1.0。 | `功能里程碑計畫.md` §0 |
| M5、M7、M8、M9 的驗收補強 reviewer、human sign-off 與 ADR gate 引用。 | `功能里程碑計畫.md` M5 / M7 / M8 / M9 |
| 《ADR / 決策紀錄》由 v1.0 升版為 v1.1，Top 10 擴充為 Top 11。 | `決策紀錄樣板ADR.md` §3、§15 |
| `tasks/README.md` 新增 Agent Team 派工契約。 | `tasks/README.md` |
| 45 張 `TASK-RPT-*` 任務卡新增 `agent_team_plan` frontmatter 與統一 Implementation Contract。 | `tasks/TASK-RPT-*.task.md` |
| 產卡模板同步新增 Agent Team 引用，避免重新產卡時遺失。 | `tools/generate_reportdemo_task_cards.py` |

## 刪除或取代

| 舊說法 / 舊假設 | 新說法 / 取代方式 |
| --- | --- |
| 「人類原則上不需要介入」 | 已 superseded。改為「隊長 AI 可自動處理低風險、可回復、已有規則的執行決策；資安、稽核、資料、正式切換與架構決策必須人類或 ADR 簽核」。 |
| Agent Team may depend on an external codebase or existing Team Agents runtime. | Superseded. Agent Team rules are governed by this simulation project documents and do not depend on external codebase/runtime. |
| 任務卡只列 validators，未明確要求 Agent role / reviewer / human gate。 | 已取代。任務卡與 README 需檢查 role、reviewer、validator、human sign-off 與 ADR gate。 |

## 改列 ADR 或人類簽核

下列事項不得由 Agent Team 自動決定，需人類簽核或 ADR：

* DB 最終選型與 Shadow DB 升格主庫。
* 舊系統正式基準、並行期限與下線條件。
* AD / LDAPS / OIDC / SAML、API session、MFA 與 signed URL 策略。
* PDF library 商用授權、數位簽章、timestamp 與 PDF 長期驗證需求。
* Golden Dataset 與正式資料 Shadow Validation 使用邊界。
* 權限模型、Admin 職責分離、Data Scope 與 break-glass。
* 稽核 fail-closed、hash chain 範圍、WORM / immutable 保存。
* Object Storage、NAS、WORM 與保存年限。
* Pilot、Go / No-Go、rollback window 與舊系統下線。
