import plotly.graph_objs as go
import pandas as pd
import numpy as np

def plot_performance(equity_curve: pd.Series):
    """
    누적수익률 곡선 시각화 (plotly)
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=equity_curve.index, y=equity_curve.values, mode="lines", name="누적수익률"))
    fig.update_layout(title="누적수익률 곡선", xaxis_title="날짜", yaxis_title="자산")
    return fig

def plot_candles_with_trades(ohlcv_df, positions=None, trades=None):
    """
    캔들스틱 + 포지션(롱/숏/관망) + 매수/매도 마커 + 스크롤/줌 지원
    ohlcv_df: DataFrame (index=datetime, columns=[open, high, low, close, volume])
    positions: Series or DataFrame (index=datetime, 값: 1/0/-1 등)
    trades: DataFrame (columns: 시점, 가격, 구분 등)
    """
    fig = go.Figure()
    # 1. 캔들스틱
    fig.add_trace(go.Candlestick(
        x=ohlcv_df.index,
        open=ohlcv_df['open'],
        high=ohlcv_df['high'],
        low=ohlcv_df['low'],
        close=ohlcv_df['close'],
        name='캔들'
    ))
    # 2. 포지션 상태 마커 (롱/숏/관망)
    if positions is not None:
        if isinstance(positions, pd.DataFrame):
            pos_series = positions.iloc[:, 0]
        else:
            pos_series = positions
        color_map = {1: 'green', -1: 'red', 0: 'gray'}
        colors = pos_series.map(lambda x: color_map.get(np.sign(x), 'gray'))
        fig.add_trace(go.Scatter(
            x=pos_series.index,
            y=ohlcv_df.loc[pos_series.index, 'close'],
            mode='markers',
            marker=dict(color=colors, size=8, opacity=0.5),
            name='포지션'
        ))
        # 비중(포지션) 시계열 추가 (보조 y축)
        fig.add_trace(go.Scatter(
            x=pos_series.index,
            y=pos_series.values,
            mode='lines',
            name='포지션 비중',
            yaxis='y2',
            line=dict(color='purple', width=2, dash='dot')
        ))
    # 3. 매수/매도 마커
    if trades is not None and not trades.empty:
        # 매수: '진입', '증액' 포함 / 매도: '청산', '감소', '완전청산' 포함 (대소문자 무시)
        buy_trades = trades[trades['구분'].str.contains('진입|증액', case=False, na=False)]
        sell_trades = trades[trades['구분'].str.contains('청산|감소', case=False, na=False)]
        fig.add_trace(go.Scatter(
            x=buy_trades['시점'],
            y=buy_trades['가격'],
            mode='markers',
            marker=dict(symbol='triangle-up', color='blue', size=12),
            name='매수'
        ))
        fig.add_trace(go.Scatter(
            x=sell_trades['시점'],
            y=sell_trades['가격'],
            mode='markers',
            marker=dict(symbol='triangle-down', color='red', size=12),
            name='매도'
        ))
    # 5. 레이아웃: 보조 y축 추가
    fig.update_layout(
        xaxis_rangeslider_visible=True,
        title="캔들+포지션+트레이드뷰+비중",
        xaxis_title="날짜",
        yaxis_title="가격",
        yaxis2=dict(
            title="포지션 비중",
            overlaying='y',
            side='right',
            range=[-1, 1]
        )
    )
    return fig

def plot_position_weight(positions):
    """
    포지션(비중)만 별도로 예쁘게 시각화 (라인+영역, 보라색, y축 -1~1)
    positions: Series or DataFrame (index=datetime, 값: -1~1)
    """
    if isinstance(positions, pd.DataFrame):
        pos_series = positions.iloc[:, 0]
    else:
        pos_series = positions
    fig = go.Figure()
    # 영역그래프
    fig.add_trace(go.Scatter(
        x=pos_series.index,
        y=pos_series.values,
        mode='lines',
        fill='tozeroy',
        line=dict(color='rgba(128,0,255,0.2)', width=0),
        name='비중 영역',
        hoverinfo='skip',
        showlegend=False
    ))
    # 라인그래프
    fig.add_trace(go.Scatter(
        x=pos_series.index,
        y=pos_series.values,
        mode='lines',
        line=dict(color='purple', width=3),
        name='포지션 비중',
        hovertemplate='날짜: %{x}<br>비중: %{y:.2f}<extra></extra>'
    ))
    fig.update_layout(
        title='포지션(비중) 시계열',
        xaxis_title='날짜',
        yaxis_title='비중',
        yaxis=dict(range=[-1, 1]),
        template='plotly_white',
        height=350
    )
    return fig

# TODO: 연별수익률, 드로우다운 등 추가 