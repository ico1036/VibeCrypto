import pandas as pd
import numpy as np

def rolling_vwap_channel_strategy(
    data,
    anchor_period=24,      # 몇 캔들마다 anchor를 새로 잡을지 (예: 24=1일)
    vwap_amount=100,       # 동시에 굴릴 VWAP 개수
    percentiles=(20, 50, 80),  # 채널 백분위수
    source_col='close',    # VWAP 계산 기준
):
    """
    롤링 VWAP 채널 전략
    - 여러 anchor에서 VWAP을 굴리고, 각 시점마다 VWAP 값들의 백분위수로 채널을 그림
    - 가격이 하단 채널(20%) 아래면 매수, 상단(80%) 위면 매도, 아니면 관망
    """
    df = data.copy()
    n = len(df)
    vwap_matrix = np.full((n, vwap_amount), np.nan)
    anchors = [i for i in range(0, n, anchor_period)]
    for idx, anchor in enumerate(anchors[-vwap_amount:]):
        price = df[source_col].values
        vol = df['volume'].values
        cum_vol = np.cumsum(vol[anchor:])
        cum_pv = np.cumsum(price[anchor:] * vol[anchor:])
        vwap = cum_pv / cum_vol
        vwap_matrix[anchor:, idx] = vwap
    # 각 시점별로 VWAP 값들의 백분위수 계산
    channel = {}
    for p in percentiles:
        channel[p] = np.nanpercentile(vwap_matrix, p, axis=1)
        df[f'vwap_p{p}'] = channel[p]
    # 시그널: close < 하단 → 매수(1), close > 상단 → 매도(-1), 아니면 관망(0)
    lower = df[f'vwap_p{percentiles[0]}']
    upper = df[f'vwap_p{percentiles[-1]}']
    close = df[source_col]
    signal = np.where(close < lower, 1, np.where(close > upper, -1, 0))
    # 마지막 값만 파이썬 int로 반환
    return pd.Series([int(signal[-1])], index=[df.index[-1]]) 