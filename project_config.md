# Project Configuration (LTM)

## Core Goal

암호화폐 트레이딩 전략을 robust하게 백테스트하고, 실시간 시그널을 제공하며, 결과를 시각화 및 분석할 수 있는 시스템 구축.
데이터는 CCXT, mcp 등에서 자동으로 불러오고, 전략은 파이썬 함수로 등록/수정/삭제 가능.
누적수익률, 연별수익률, 연율화수익률, MDD, 샤프, 변동성 등 주요 지표와, 크립토 퀀트 회사에서 쓰는 리포트까지 제공.

## Tech Stack

*   **Backend/엔진:** Python 3.10+, pandas, numpy, ccxt, mcp(optional), backtrader, backtesting.py, empyrical, pyfolio
*   **Frontend/UI:** Streamlit, Plotly, Matplotlib
*   **Testing:** pytest
*   **Lint/Format:** black, flake8

## Critical Patterns & Conventions

*   전략은 /strategies 폴더에 파이썬 함수로 저장
*   데이터는 /data 폴더에 CSV/Parquet로 저장
*   리포트/시각화는 /report 폴더
*   커밋 메시지는 Conventional Commits
*   모든 주요 지표는 empyrical/pyfolio로 계산

## Key Constraints

*   거래소 API rate limit, 데이터 품질 체크
*   전략별 파라미터화 지원
*   결과 리포트는 웹에서 바로 확인 가능해야 함
*   확장성(새 전략/지표/거래소 쉽게 추가)

## Tokenization Settings

*   **Estimation Method:** Character-based
*   **Characters Per Token (Estimate):** 4

## Version

*   **Current Version:** 1.0.0
