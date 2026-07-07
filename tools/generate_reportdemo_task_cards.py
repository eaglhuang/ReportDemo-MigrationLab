from __future__ import annotations

import re
from pathlib import Path


# Template governance note:
# If this generator is used again, preserve the tasks/README.md gate:
# Qutora is the drill legacy system, MariaDB is the drill target DB,
# drill execution is governed by drills/分階段演練與驗收計畫.md,
# evidence paths follow runbooks/RB-03-evidence-standard.md,
# MariaDB drill setup follows runbooks/RB-05-mariadb-environment.md,
# MVP2 PoC code belongs under poc/ or tools/ per ADR-015,
# AI-led execution mode follows ADR-016 and RB-06,
# and a task card must not start until its full design spec includes
# 10 validators, 10 test cases, impact scope, rollback, reviewer,
# human gate, and ADR references.
ROOT = Path(__file__).resolve().parents[1]
TASK_DIR = ROOT / "tasks"
PLAN_PATH = ROOT / "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"
AGENT_TEAM_PLAN = "內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md"
RELATED_PLAN = "內部人員交易報表轉媒體儲存系統_功能里程碑計畫.md"


SLUGS = {
    "M0-01": "legacy-report-inventory",
    "M0-02": "legacy-data-source-inventory",
    "M0-03": "legacy-result-baseline",
    "M0-04": "third-party-cross-platform-poc",
    "M0-05": "sp-sql-refactor-classification",
    "M0-06": "role-raci-critical-path",
    "M1-01": "import-batch-management",
    "M1-02": "staging-tables",
    "M1-03": "legacy-transform-porting",
    "M1-04": "audit-write-foundation",
    "M2-01": "validation-rule-versioning",
    "M2-02": "validation-result-severity",
    "M2-03": "legacy-new-validation-compare",
    "M2-04": "data-scope-foundation",
    "M3-01": "report-template-versioning",
    "M3-02": "report-generation-job",
    "M3-03": "report-version-state-machine",
    "M3-04": "dual-report-production-compare",
    "M4-01": "pdf-metadata",
    "M4-02": "pdf-storage-zone",
    "M4-03": "pdf-master-integrity-check",
    "M4-04": "pdf-reconciliation",
    "M5-01": "download-gateway",
    "M5-02": "dynamic-watermark",
    "M5-03": "download-copy-hash",
    "M5-03A": "download-copy-retention-policy",
    "M5-04": "high-confidential-pdf-control",
    "M6-01": "report-search",
    "M6-02": "secure-preview",
    "M6-03": "review-workflow",
    "M6-04": "regeneration-workflow",
    "M6-05": "void-workflow",
    "M7-01": "audit-query-hash-chain",
    "M7-02": "log-sensitive-data-protection",
    "M7-03": "alert-severity-routing",
    "M8-01": "role-management",
    "M8-02": "data-scope-management",
    "M8-03": "break-glass-workflow",
    "M9-01": "shadow-db",
    "M9-02": "go-no-go-gate",
    "M9-03": "rollback-runbook",
    "M9-04": "uat-training-operations-manual",
    "M9-05": "pilot-legacy-shutdown-gate",
    "M10-01": "release-acceptance",
    "M10-02": "legacy-coverage-confirmation",
}

DEPENDENCIES = {
    "M0-01": [],
    "M0-02": [],
    "M0-03": ["TASK-RPT-0001", "TASK-RPT-0002"],
    "M0-04": ["TASK-RPT-0001", "TASK-RPT-0002"],
    "M0-05": ["TASK-RPT-0002", "TASK-RPT-0004"],
    "M0-06": ["TASK-RPT-0001", "TASK-RPT-0002", "TASK-RPT-0003", "TASK-RPT-0004", "TASK-RPT-0005"],
    "M1-01": ["TASK-RPT-0006"],
    "M1-02": ["TASK-RPT-0002", "TASK-RPT-0007"],
    "M1-03": ["TASK-RPT-0005", "TASK-RPT-0008"],
    "M1-04": ["TASK-RPT-0007"],
    "M2-01": ["TASK-RPT-0003", "TASK-RPT-0009"],
    "M2-02": ["TASK-RPT-0011"],
    "M2-03": ["TASK-RPT-0011", "TASK-RPT-0012"],
    "M2-04": ["TASK-RPT-0006", "TASK-RPT-0010"],
    "M3-01": ["TASK-RPT-0001", "TASK-RPT-0013"],
    "M3-02": ["TASK-RPT-0015"],
    "M3-03": ["TASK-RPT-0016"],
    "M3-04": ["TASK-RPT-0015", "TASK-RPT-0016", "TASK-RPT-0017"],
    "M4-01": ["TASK-RPT-0017", "TASK-RPT-0018"],
    "M4-02": ["TASK-RPT-0004", "TASK-RPT-0019"],
    "M4-03": ["TASK-RPT-0019", "TASK-RPT-0020"],
    "M4-04": ["TASK-RPT-0020", "TASK-RPT-0021"],
    "M5-01": ["TASK-RPT-0014", "TASK-RPT-0020"],
    "M5-02": ["TASK-RPT-0023"],
    "M5-03": ["TASK-RPT-0023", "TASK-RPT-0024"],
    "M5-03A": ["TASK-RPT-0025"],
    "M5-04": ["TASK-RPT-0023", "TASK-RPT-0024", "TASK-RPT-0025", "TASK-RPT-0026"],
    "M6-01": ["TASK-RPT-0014", "TASK-RPT-0017", "TASK-RPT-0023"],
    "M6-02": ["TASK-RPT-0024", "TASK-RPT-0028"],
    "M6-03": ["TASK-RPT-0017", "TASK-RPT-0028"],
    "M6-04": ["TASK-RPT-0017", "TASK-RPT-0030"],
    "M6-05": ["TASK-RPT-0017", "TASK-RPT-0030"],
    "M7-01": ["TASK-RPT-0010", "TASK-RPT-0022", "TASK-RPT-0025"],
    "M7-02": ["TASK-RPT-0010"],
    "M7-03": ["TASK-RPT-0010", "TASK-RPT-0021", "TASK-RPT-0033", "TASK-RPT-0034"],
    "M8-01": ["TASK-RPT-0014", "TASK-RPT-0033"],
    "M8-02": ["TASK-RPT-0014", "TASK-RPT-0036"],
    "M8-03": ["TASK-RPT-0035", "TASK-RPT-0036", "TASK-RPT-0037"],
    "M9-01": ["TASK-RPT-0004", "TASK-RPT-0005", "TASK-RPT-0018"],
    "M9-02": ["TASK-RPT-0018", "TASK-RPT-0039"],
    "M9-03": ["TASK-RPT-0040"],
    "M9-04": ["TASK-RPT-0040", "TASK-RPT-0041"],
    "M9-05": ["TASK-RPT-0040", "TASK-RPT-0041", "TASK-RPT-0042"],
    "M10-01": ["TASK-RPT-0043"],
    "M10-02": ["TASK-RPT-0001", "TASK-RPT-0002", "TASK-RPT-0044"],
}

OWNER_BY_MILESTONE = {
    "M0": "Tech Lead / Captain",
    "M1": "Backend / DBA",
    "M2": "QA / Security / DevOps",
    "M3": "Backend / DBA",
    "M4": "Backend / DBA",
    "M5": "Backend / DBA",
    "M6": "Backend / DBA",
    "M7": "QA / Security / DevOps",
    "M8": "QA / Security / DevOps",
    "M9": "Tech Lead / Captain",
    "M10": "Tech Lead / Captain",
}

STAGE_BY_TASK = {
    "TASK-RPT-0001": "MVP1",
    "TASK-RPT-0002": "MVP1",
    "TASK-RPT-0003": "MVP1",
    "TASK-RPT-0004": "MVP1",
    "TASK-RPT-0007": "MVP2",
    "TASK-RPT-0008": "MVP2",
    "TASK-RPT-0010": "MVP2",
    "TASK-RPT-0014": "MVP2",
    "TASK-RPT-0019": "MVP2",
    "TASK-RPT-0023": "MVP2",
    "TASK-RPT-0024": "MVP2",
    "TASK-RPT-0025": "MVP2",
    "TASK-RPT-0013": "Pilot",
    "TASK-RPT-0018": "Pilot",
    "TASK-RPT-0021": "Pilot",
    "TASK-RPT-0022": "Pilot",
    "TASK-RPT-0028": "Pilot",
    "TASK-RPT-0033": "Pilot",
    "TASK-RPT-0035": "Pilot",
    "TASK-RPT-0036": "Pilot",
    "TASK-RPT-0037": "Pilot",
    "TASK-RPT-0038": "ProductionCandidate",
    "TASK-RPT-0040": "ProductionCandidate",
    "TASK-RPT-0041": "ProductionCandidate",
    "TASK-RPT-0042": "ProductionCandidate",
    "TASK-RPT-0043": "ProductionCandidate",
    "TASK-RPT-0044": "ProductionCandidate",
    "TASK-RPT-0045": "ProductionCandidate",
}

PRIMARY_ROLE_BY_MILESTONE = {
    "M0": "Tech Lead / Captain",
    "M1": "Backend / DBA",
    "M2": "Backend / DBA",
    "M3": "Backend / DBA",
    "M4": "Backend / DBA",
    "M5": "Backend / DBA",
    "M6": "Backend / DBA",
    "M7": "QA / Security / DevOps",
    "M8": "QA / Security / DevOps",
    "M9": "Tech Lead / Captain",
    "M10": "Tech Lead / Captain",
}


def drill_stage(task_id: str) -> str:
    return STAGE_BY_TASK.get(task_id, "Backlog")


def primary_role(milestone: str) -> str:
    return PRIMARY_ROLE_BY_MILESTONE.get(milestone, "Tech Lead / Captain")


def closure_reviewer(role: str) -> str:
    if role == "Tech Lead / Captain":
        return "QA / Security / DevOps"
    return "Tech Lead / Captain"


def execution_mode(task_id: str) -> str:
    if drill_stage(task_id) == "Backlog":
        return "requires-full-spec-before-start"
    if task_id in {"TASK-RPT-0038", "TASK-RPT-0040", "TASK-RPT-0043", "TASK-RPT-0044"}:
        return "human-only"
    return "ai-with-human-review"


def support_roles(milestone: str) -> list[str]:
    role = primary_role(milestone)
    return [candidate for candidate in ["Tech Lead / Captain", "Backend / DBA", "QA / Security / DevOps"] if candidate != role]


def parse_sections() -> list[dict[str, object]]:
    text = PLAN_PATH.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^### (M\d+-\d+A?) (.+)$", text, flags=re.MULTILINE))
    sections = []
    for index, match in enumerate(matches):
        code = match.group(1)
        title = match.group(2).strip()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end() : end]
        feature, acceptance = split_feature_acceptance(body)
        sections.append({"code": code, "title": title, "feature": feature, "acceptance": acceptance})
    return sections


def split_feature_acceptance(body: str) -> tuple[list[str], list[str]]:
    feature_part = body
    acceptance_part = ""
    if "驗收條件：" in body:
        feature_part, acceptance_part = body.split("驗收條件：", 1)
    if "功能描述：" in feature_part:
        feature_part = feature_part.split("功能描述：", 1)[1]
    return extract_bullets(feature_part), extract_bullets(acceptance_part)


def extract_bullets(text: str) -> list[str]:
    bullets = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("* "):
            bullets.append(line[2:].strip())
    return bullets


def yaml_list(items: list[str], indent: int = 2) -> str:
    if not items:
        return " []"
    pad = " " * indent
    return "\n" + "\n".join(f'{pad}- "{item}"' for item in items)


def legacy_placeholders(code: str) -> list[str]:
    numeric = code.replace("M", "").replace("-", "").replace("A", "A")
    return [
        f"legacy/舊系統報表模組_功能別{numeric}.xxx",
        f"legacy/舊系統資料轉換_SP_功能別{numeric}.sql",
    ]


def task_scope(code: str) -> list[str]:
    milestone = code.split("-")[0]
    base = [
        f"tasks/TASK-RPT-*-{SLUGS[code]}.task.md",
        "evidence/<Stage>/<TASK-ID>/**",
    ]
    module_paths = {
        "M0": ["inventory/**", "decision-records/**"],
        "M1": ["src/ReportDemo.Import/**", "db/migrations/reportdemo/**", "runbooks/RB-05-mariadb-environment.md", "poc/migration/**"],
        "M2": ["src/ReportDemo.Validation/**", "db/migrations/reportdemo/**"],
        "M3": ["src/ReportDemo.Reporting/**", "templates/reportdemo/**"],
        "M4": ["src/ReportDemo.DocumentStorage/**", "infra/storage/reportdemo/**", "poc/migration/**"],
        "M5": ["src/ReportDemo.DownloadGateway/**", "src/ReportDemo.Watermark/**", "poc/download-gateway/**", "poc/watermark/**", "poc/validators/**"],
        "M6": ["src/ReportDemo.Web/**", "src/ReportDemo.Workflow/**"],
        "M7": ["src/ReportDemo.Audit/**", "src/ReportDemo.Alerting/**"],
        "M8": ["src/ReportDemo.Admin/**", "src/ReportDemo.Security/**"],
        "M9": ["infra/migration/reportdemo/**", "runbooks/reportdemo/**"],
        "M10": ["acceptance/**", "runbooks/reportdemo/**"],
    }
    return base + module_paths.get(milestone, []) + legacy_placeholders(code)


def task_card(seq: int, section: dict[str, object]) -> tuple[str, str]:
    code = str(section["code"])
    title = str(section["title"])
    task_id = f"TASK-RPT-{seq:04d}"
    milestone = code.split("-")[0]
    stage = drill_stage(task_id)
    mode = execution_mode(task_id)
    role = primary_role(milestone)
    reviewer = closure_reviewer(role)
    slug = SLUGS[code]
    filename = f"{task_id}-{code.lower()}-{slug}.task.md"
    owner = OWNER_BY_MILESTONE[milestone]
    depends = DEPENDENCIES.get(code, [])
    feature = section["feature"] or ["依功能里程碑計畫完成本項功能交付。"]
    acceptance = section["acceptance"] or ["完成本項功能驗收並留下簽核紀錄。"]
    priority = "P0" if milestone in {"M0", "M1", "M2", "M7", "M8", "M9", "M10"} else "P1"
    suffix = task_id[-4:]
    validators = [
        f"V-{suffix}-01: verify Qutora baseline input and target output are documented",
        f"V-{suffix}-02: verify data tables or artifacts include status, error code, and payload hash",
        f"V-{suffix}-03: verify state machine includes review, sign-off, and closure boundaries",
        f"V-{suffix}-04: verify P0/P1 failures are fail-closed or block the next gate",
        f"V-{suffix}-05: verify Role and Data Scope checks are separated",
        f"V-{suffix}-06: verify audit event and correlation_id are recorded",
        f"V-{suffix}-07: verify evidence is written under the RB-03 evidence path",
        f"V-{suffix}-08: verify reviewer is independent from producer",
        f"V-{suffix}-09: verify human gate and ADR gate triggers are explicit",
        f"V-{suffix}-10: git diff --check",
    ]
    test_cases = [
        f"TC-{suffix}-01: happy path with Qutora synthetic data",
        f"TC-{suffix}-02: missing Qutora baseline must block the gate",
        f"TC-{suffix}-03: MariaDB metadata mismatch must create an issue",
        f"TC-{suffix}-04: unauthorized role must be denied and audited",
        f"TC-{suffix}-05: Data Scope mismatch must deny or mask data",
        f"TC-{suffix}-06: audit write failure must fail closed",
        f"TC-{suffix}-07: missing human sign-off must block closure",
        f"TC-{suffix}-08: ADR-required condition must block closure until decided",
        f"TC-{suffix}-09: validator rerun must be reproducible",
        f"TC-{suffix}-10: rollback path must return to Qutora or last approved state",
    ]
    content = f"""---
task_id: {task_id}
source_milestone: {code}
title: "{title}"
status: planned
owner: {owner}
priority: {priority}
milestone: {milestone}
depends_on:{yaml_list(depends)}
related_plan: "{RELATED_PLAN}"
agent_team_plan: "{AGENT_TEAM_PLAN}"
drill_stage: "{stage}"
execution_mode: "{mode}"
primary_role: "{role}"
closure_reviewer: "{reviewer}"
support_roles:{yaml_list(support_roles(milestone))}
evidence_path: "evidence/{stage}/{task_id}/"
scopePaths:{yaml_list(task_scope(code))}
deliverables:
  - "evidence/{stage}/{task_id}/implementation-notes.md"
  - "evidence/{stage}/{task_id}/validation-result.md"
  - Target system implementation artifacts: code, DB migration, tests, and operation docs
validators:{yaml_list(validators)}
evidence:
  required: command-backed
rollback:
  strategy: revert-commit-or-feature-flag-disable
  notes: "若已進入正式資料流程，需先依 rollback runbook 停用新功能並回復舊系統路徑。"
atomizationImpact:
  ownerAtomOrMap: "reportdemo.{milestone.lower()}.{slug}"
  mapUpdates:
    - After target implementation location is created, add actual module/path map
  notes: "This card defines the functional work package first; add actual module/map and file boundaries after the implementation location is created."
outOfScope:
  - "使用未脫敏正式資料進行開發或一般測試"
  - "未完成舊系統覆蓋比對即切換正式流程"
  - "繞過 Admin、Data Scope、稽核與告警要求"
nonGoals:
  - "一次性重寫所有舊系統功能"
  - "在未完成 PoC / Gate 前承諾最終技術選型"
---
# {task_id} - {code} {title}

## Goal

完成 `{code}` 對應功能，並能證明新系統涵蓋舊系統必要行為；未知舊系統程式碼先以象徵性代號標記，後續盤點時替換為真實名稱。

## Legacy Coverage

- 需對照：`{legacy_placeholders(code)[0]}`
- 需對照：`{legacy_placeholders(code)[1]}`
- 若本卡涉及重寫，必須保留舊系統輸入、輸出、排序、欄位、狀態與例外案例的比對紀錄。

## Functional Scope
{chr(10).join(f"- {item}" for item in feature)}

## Implementation Contract

- 優先採漸進式承接：沿用、封裝、移植、重寫、廢止候選需逐項記錄。
- 不得用未脫敏正式資料做一般開發或測試；正式資料只可進受控 Shadow Validation。
- 涉及權限、資料範圍、PDF、稽核、告警或 break-glass 時，安全性與可稽核性優先於便利性。
- 每個可觀測流程需留下 trace ID / correlation ID，方便新舊系統比對與事故追蹤。
- 未補齊任務目標、真實功能帶入場景、落地設計、影響範圍、輸入輸出、完成定義、10 條 validators、10 條 test cases、風險回復、reviewer、human gate 與 ADR gate 前，不得正式開工或 closure。
- Agent Team 派工、role、reviewer、validator、human sign-off 與 ADR gate 需依 Agent Team 計畫書 v1.0 執行：`內部人員交易報表轉媒體儲存系統_Agent Team計畫書.md`。
- 分階段演練、三人責任矩陣、validators、test cases 與 Gate 需依 `drills/分階段演練與驗收計畫.md` 執行。
- Evidence 需依 `runbooks/RB-03-evidence-standard.md` 寫入 `evidence/{stage}/{task_id}/`。
- MariaDB 演練環境需依 `runbooks/RB-05-mariadb-environment.md` 建立；MVP2 PoC 程式碼落點需依 ADR-015 放在 `poc/` 或 `tools/`。
- 若採 AI 主導三人併行排程，需依 ADR-016 與 `runbooks/RB-06-ai-dispatch-cycle.md` 標示 `[AI]`、`[AI->HUMAN]`、`[HUMAN]` 或 `[GATE]`；AI 產出不得取代 human / ADR gate。

## Impact Scope

- 影響 `{stage}` 階段 Gate、evidence package 與後續任務卡開工順序。
- 影響 Qutora 舊系統覆蓋判斷、新系統功能驗證、權限與稽核證據。
- 若本卡觸發資安、稽核、資料、正式切換或架構決策，必須改列 human gate 或 ADR gate。

## Deliverables

- 實作程式碼、DB migration、設定檔或文件，依本卡 `scopePaths` 控制。
- `evidence/{stage}/{task_id}/implementation-notes.md`
- `evidence/{stage}/{task_id}/validation-result.md`

## Validators

{chr(10).join(f"- {item}" for item in validators)}

## Test Cases

{chr(10).join(f"- {item}" for item in test_cases)}

## Acceptance Criteria
{chr(10).join(f"- {item}" for item in acceptance)}

## Rollback

以 feature flag、路由切回舊系統、回復 migration 或 revert commit 為優先；若已接觸正式流程，必須先確認資料一致性與稽核紀錄完整。

## Reviewer / Human Gate / ADR

- Reviewer：依 `closure_reviewer` 指派，且不得等於 `primary_role`；AI 不得擔任 DRI 或 closure reviewer。
- Human Gate：正式資料、權限放寬、稽核例外、正式切換與舊系統下線必須人類簽核。
- ADR Gate：DB、Object Storage / WORM、SSO / API session、PDF library、稽核 fail-closed、Go / No-Go 或架構邊界變更必須 ADR。

## Notes

- 2026-07-02 | planned | 已同步 Agent Team 計畫書 v1.0；正式派工前需確認 role、reviewer、validator、human/ADR gate 與違規阻擋機制。

- 2026-07-02 | planned | Card generated from the function milestone plan; waiting for human confirmation of priority, owner, and target implementation location path.
"""
    return filename, content


def readme(sections: list[dict[str, object]]) -> str:
    rows = []
    for seq, section in enumerate(sections, start=1):
        code = str(section["code"])
        milestone = code.split("-")[0]
        title = str(section["title"])
        task_id = f"TASK-RPT-{seq:04d}"
        filename = f"{task_id}-{code.lower()}-{SLUGS[code]}.task.md"
        depends = ", ".join(DEPENDENCIES.get(code, [])) or "none"
        rows.append(f"| [{task_id}](./{filename}) | {code} | {milestone} | {title} | planned | {depends} |")
    return f"""---
owner: "Tech Lead / Captain"
status: active
related_plan: {RELATED_PLAN}
agent_team_plan: {AGENT_TEAM_PLAN}
created_at: 2026-07-02
---

# ReportDemo Task Card Index

This directory turns the function milestone plan into dispatchable task cards for the standalone ReportDemo simulation project only.

## Task Card Contract

- 每張 `TASK-RPT-*` 卡都必須對應一個功能里程碑項目。
- 本演練舊系統採用 Qutora；任務卡中的「舊系統」若未另行限定，均指 `open-source-sandbox/qutora-api` 固定 commit 的 Qutora。
- 每張卡都要保留舊系統覆蓋欄位；MVP1/MVP2 核心任務卡應優先引用 Qutora 具體元件。非核心卡若尚未盤點完成，才可暫用 `舊系統報表模組_功能別XXX.xxx` 或 `舊系統資料轉換_SP_功能別XXX.sql` 代稱。
- 任務卡不得跳過 Golden Dataset、Shadow Validation、權限、Data Scope、稽核與 rollback 驗證。
- Before the target implementation location exists, use `scopePaths`, `deliverables`, and evidence folders as the delivery boundary; add concrete paths later.
- 摘要任務卡未補齊完整設計規格前不得開工；完整規格至少包含任務目標、真實功能場景、落地設計、影響範圍、輸入輸出、完成定義、10 條 validators、10 條 test cases、風險回復、reviewer / human gate / ADR。

## Drill Plan Contract

- 演練唯一執行指南：`drills/分階段演練與驗收計畫.md`。
- Evidence 標準：`runbooks/RB-03-evidence-standard.md`。
- Rollback 演練：`runbooks/RB-04-rollback-rehearsal.md`。
- MariaDB 演練環境：`runbooks/RB-05-mariadb-environment.md`。
- AI 派工循環：`runbooks/RB-06-ai-dispatch-cycle.md`。
- Qutora 作為本演練舊系統的決策依 ADR-012；不得再以獨立 Qutora 對照表維護。
- MariaDB 作為本演練目標資料庫的決策依 ADR-013；此決策不取代正式專案最終 DB 選型。
- 2 週 MVP 節奏與完整任務卡開工 Gate 依 ADR-014。
- 演練 PoC 技術棧與程式碼落點依 ADR-015；正式實作技術棧仍需另行 ADR。
- AI 主導三人併行排程依 ADR-016；週末不排正式工作，每人每日最多 8 小時。

## Agent Team Dispatch Contract

- `Agent Team plan v1.0` is the task dispatch source of truth and does not depend on any external codebase or existing Team Agents runtime.
- 正式接卡前需確認 Agent role、reviewer、validator、human sign-off 與 ADR gate。
- M5、M7、M8、M9 或涉及正式資料的任務卡，需額外納入 QA / Security / DevOps、QA / Security / DevOps、QA / Security / DevOps 或人類簽核。
- 若 Agent 自動決策與資安、稽核或 ADR 衝突，任務卡不得 closure，需先升級人類或 ADR 裁決。
- 違規阻擋機制至少包含：任務卡 scope、tool sandbox / CI scope check、validator / reviewer、command-backed evidence 與 closure gate。

## Task Roster

| Task ID | Source | Milestone | Title | Status | Depends |
|---|---|---|---|---|---|
{chr(10).join(rows)}

## Sequencing Note

建議先完成 M0 盤點與 PoC，再進入 M1/M9-01 的資料遷移基礎；M2-M5 可在資料基準穩定後分流開發，但 M7/M8 的稽核、告警、Admin 與 break-glass 不應延到最後才補。
"""


def main() -> None:
    sections = parse_sections()
    TASK_DIR.mkdir(parents=True, exist_ok=True)
    (TASK_DIR / "README.md").write_text(readme(sections), encoding="utf-8", newline="\n")
    for seq, section in enumerate(sections, start=1):
        filename, content = task_card(seq, section)
        (TASK_DIR / filename).write_text(content, encoding="utf-8", newline="\n")
    print(f"generated {len(sections)} task cards in {TASK_DIR}")


if __name__ == "__main__":
    main()
