import streamlit as st
from cards_parser import cards_from_yaml
from report.plot import plot_performance
import pandas as pd
from main_cards_runner import run_card_result

## 출력용 헬퍼 함수들 ##
def to_utc_ts(val):
    ts = pd.to_datetime(val)
    if ts.tzinfo is None:
        ts = ts.tz_localize('UTC')
    else:
        ts = ts.tz_convert('UTC')
    return ts

def format_period(period):
    # 리스트면 각 원소를 변환해서 'YYYY-MM-DD ~ YYYY-MM-DD'로 합침
    if isinstance(period, list) and len(period) == 2:
        def to_str(x):
            if isinstance(x, (int, float)) and x > 1e10:
                return pd.to_datetime(x, unit='ms').strftime('%Y-%m-%d')
            return str(x)
        return f"{to_str(period[0])} ~ {to_str(period[1])}"
    return str(period)

st.set_page_config(page_title="카드 기반 자동 백/포워드테스트", layout="wide")
st.title("🃏 카드 기반 자동 백테스트/포워드테스트 + 실시간 시그널")


## 화면 구성 ##
st.sidebar.write("버전: 1.0.0")

## 카드 목록 표시 ##
cards = cards_from_yaml()
df = pd.DataFrame(cards)
if 'backtest_period' in df.columns:
    df['backtest_period'] = df['backtest_period'].apply(format_period)
st.write("## Cards (전략/옵션/기간/엔진)")
st.dataframe(df)

## 전체 카드 실행 ##
if st.button("전체 카드 실행"):
    for card in cards:
        st.subheader(f"카드: {card['id']} ({card['strategy']})")
        result = run_card_result(card)
        # 백테스트
        st.write("### 백테스트")
        metrics_bt = result['backtest']['metrics']
        trades_bt = result['backtest']['trades']
        st.write("지표:", metrics_bt)
        st.write("트레이드 수:", len(trades_bt))
        st.plotly_chart(plot_performance(result['backtest']['results']['equity']), use_container_width=True)
        # 실시간 시그널
        st.write("### 실시간 시그널")
        realtime_signal = float(result.get('realtime_signal', None)) if result.get('realtime_signal', None) is not None else None
        if realtime_signal == 1:
            st.success("💚 [매수 시그널] 지금 매수!")
        elif realtime_signal == -1:
            st.error("❤️ [매도 시그널] 지금 매도!")
        elif realtime_signal == 0:
            st.info("💤 [관망 시그널] 지금은 관망!")
        elif isinstance(realtime_signal, float) and 0 < realtime_signal < 1:
            st.success(f"🟢 [비중 매수] 현재 비중: {realtime_signal:.2f} ({realtime_signal*100:.0f}%) 매수 상태")
        else:
            st.warning("시그널 없음/계산 불가!") 