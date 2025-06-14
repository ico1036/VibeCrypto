# Workflow State & Rules (STM + Rules + Log)

*This file contains the dynamic state, embedded rules, active plan, and log for the current session.*
*It is read and updated frequently by the AI during its operational loop.*

---

## State

*Holds the current status of the workflow.*

```yaml
Phase: ANALYZE
Status: READY
CurrentTaskID: BuildCryptoBacktester
CurrentStep: null
CurrentItem: null
```

---

## Plan

*Contains the step-by-step implementation plan generated during the BLUEPRINT phase.*

**Task: SummarizeItemsIteratively**

*   `[ ] Step 1: 데이터 다운로드 모듈 구현 (CCXT, mcp)`
*   `[ ] Step 2: 전략 등록/수정/삭제 시스템 구현`
*   `[ ] Step 3: 백테스트/포워드테스트 엔진 구현`
*   `[ ] Step 4: 성능지표 계산 모듈 구현`
*   `[ ] Step 5: 시각화/리포트 모듈 구현`
*   `[ ] Step 6: Streamlit 웹앱 구현`
*   `[ ] Step 7: 샘플 전략/데이터/리포트 제공`

---

## Cards

```yaml
- id: sma_btc_1h
  strategy: SMA_Cross
  params:
    fast: 20
    slow: 60
  symbol: BTC/USDT
  timeframe: 1h
  backtest_period: [2021-01-01, 2022-01-01]
  fee: 0.0005
  use_fast_backtest_yn: 0

- id: rsi_eth_4h
  strategy: RSI_MeanRev
  params:
    rsi_period: 14
    rsi_thresh: 30
  symbol: ETH/USDT
  timeframe: 4h
  backtest_period: [2021-01-01, 2022-01-01]
  fee: 0.0005
  use_fast_backtest_yn: 0
```

---

## Rules

*Embedded rules governing the AI's autonomous operation.*

**# --- Core Workflow Rules ---**

RULE_WF_PHASE_ANALYZE:
  **Constraint:** Goal is understanding request/context. NO solutioning or implementation planning.

RULE_WF_PHASE_BLUEPRINT:
  **Constraint:** Goal is creating a detailed, unambiguous step-by-step plan. NO code implementation.

RULE_WF_PHASE_CONSTRUCT:
  **Constraint:** Goal is executing the `## Plan` exactly. NO deviation. If issues arise, trigger error handling or revert phase.

RULE_WF_PHASE_VALIDATE:
  **Constraint:** Goal is verifying implementation against `## Plan` and requirements using tools. NO new implementation.

RULE_WF_TRANSITION_01:
  **Trigger:** Explicit user command (`@analyze`, `@blueprint`, `@construct`, `@validate`).
  **Action:** Update `State.Phase` accordingly. Log phase change.

RULE_WF_TRANSITION_02:
  **Trigger:** AI determines current phase constraint prevents fulfilling user request OR error handling dictates phase change (e.g., RULE_ERR_HANDLE_TEST_01).
  **Action:** Log the reason. Update `State.Phase` (e.g., to `BLUEPRINT_REVISE`). Set `State.Status` appropriately (e.g., `NEEDS_PLAN_APPROVAL`). Report to user.

RULE_ITERATE_01: # Triggered by RULE_MEM_READ_STM_01 when State.Status == READY and State.CurrentItem == null, or after VALIDATE phase completion.
  **Trigger:** `State.Status == READY` and `State.CurrentItem == null` OR after `VALIDATE` phase completion.
  **Action:**
    1. Check `## Items` section for more items.
    2. If more items:
    3. Set `State.CurrentItem` to the next item.
    4. Clear `## Log`.
    5. Set `State.Phase = ANALYZE`, `State.Status = READY`.
    6. Log "Starting processing item [State.CurrentItem]".
    7. If no more items:
    8. Trigger `RULE_ITERATE_02`.

RULE_ITERATE_02:
  **Trigger:** `RULE_ITERATE_01` determines no more items.
  **Action:**
    1. Set `State.Status = COMPLETED_ITERATION`.
    2. Log "Tokenization iteration completed."

**# --- Initialization & Resumption Rules ---**

RULE_INIT_01:
  **Trigger:** AI session/task starts AND `workflow_state.md` is missing or empty.
  **Action:**
    1. Create `workflow_state.md` with default structure.
    2. Read `project_config.md` (prompt user if missing).
    3. Set `State.Phase = ANALYZE`, `State.Status = READY`.
    4. Log "Initialized new session."
    5. Prompt user for the first task.

RULE_INIT_02:
  **Trigger:** AI session/task starts AND `workflow_state.md` exists.
  **Action:**
    1. Read `project_config.md`.
    2. Read existing `workflow_state.md`.
    3. Log "Resumed session."
    4. Check `State.Status`: Handle READY, COMPLETED, BLOCKED_*, NEEDS_*, IN_PROGRESS appropriately (prompt user or report status).

RULE_INIT_03:
  **Trigger:** User confirms continuation via RULE_INIT_02 (for IN_PROGRESS state).
  **Action:** Proceed with the next action based on loaded state and rules.

**# --- Memory Management Rules ---**

RULE_MEM_READ_LTM_01:
  **Trigger:** Start of a new major task or phase.
  **Action:** Read `project_config.md`. Log action.
RULE_MEM_READ_STM_01:
  **Trigger:** Before *every* decision/action cycle.
  **Action:**
    1. Read `workflow_state.md`.
    2. If `State.Status == READY` and `

## CHANGELOG

### v1.1.0 (2024-06-09)
- 백워드 호환되는 기능 추가 및 개선 (MINOR)
- 백테스팅 엔진이 score(시그널)를 weight(비중)로 바로 반영하도록 구조 변경 (부분매수/부분매도/비중조절 전략 지원)
- 트레이딩뷰 스타일 plot에 포지션(비중) 시계열 별도 시각화(plot_position_weight) 추가
- 매수/매도 마커, 포지션 시각화 등 plot 개선
- 전략명/파일명 매핑 버그, 트레이드 마커 표시 버그 등 다수 버그 픽스

### v1.0.0 (2024-06-01)
- 최초 릴리즈 (백테스팅/포워드테스트, 기본 plot, 카드 기반 전략 등)
