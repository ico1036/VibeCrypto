# Crypto Trading Backtest & Forwardtest System

이 프로젝트는 암호화폐 트레이딩 전략을 robust하게 백테스트/포워드테스트하고, 결과를 시각화 및 분석할 수 있는 시스템이다. 데이터는 CCXT, mcp 등에서 자동으로 불러오고, 전략은 파이썬 함수로 등록/수정/삭제 가능하다. 주요 성능지표와 크립토 퀀트 회사에서 쓰는 리포트까지 제공한다.

## 주요 기능
- 거래소 데이터 자동 다운로드 (CCXT, mcp)
- 전략 등록/수정/삭제 (파이썬 함수 기반)
- 백테스트/포워드테스트 엔진 (Backtrader/Backtesting.py)
- 성능지표: 누적수익률, 연별수익률, 연율화수익률, MDD, Sharpe, 변동성 등
- 시각화: 누적수익률 그래프, 연도별 바차트, 드로우다운, 히트맵 등
- Streamlit 웹 UI: 전략 선택, 파라미터 입력, 결과 리포트/그래프 확인

## 폴더 구조
```
/data         # 시세 데이터 저장
/strategies   # 트레이딩 전략 파이썬 파일
/backtest     # 백테스트/포워드테스트 엔진
/report       # 리포트/시각화 코드
app.py        # Streamlit 메인 앱
```

## 설치 및 실행법
```bash
# 의존성 설치
pip install -r requirements.txt

# Streamlit 앱 실행
streamlit run app.py
```

## 예시 코드/스크린샷
(추후 추가)

## 주요 의존성
- python 3.10+
- pandas, numpy
- ccxt, mcp
- backtrader, backtesting.py
- empyrical, pyfolio
- streamlit, plotly, matplotlib

## 기여 방법
- PR/이슈 환영
- 전략/지표/시각화 추가 자유롭게 제안
# VibeCrypto
