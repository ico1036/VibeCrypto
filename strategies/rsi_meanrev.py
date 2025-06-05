import pandas as pd

def rsi_meanrev_strategy(data, rsi_period=14, rsi_thresh=30):
    """
    RSI mean reversion 전략 (비중 기반)
    :param data: pd.DataFrame, columns=['open', 'high', 'low', 'close', ...]
    :param rsi_period: RSI 계산 기간
    :param rsi_thresh: 진입 임계값
    :return: (1,) shape 벡터 (마지막 시점 값)
    """
    df = data.copy()
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(rsi_period).mean()
    avg_loss = loss.rolling(rsi_period).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    rsi = 100 - (100 / (1 + rs))
    df['rsi'] = rsi
    # rsi가 rsi_thresh보다 낮을수록 비중↑
    signal = ((rsi_thresh - df['rsi']) / rsi_thresh).clip(0, 1).fillna(0)
    # 마지막 시점 값만 벡터로 반환
    return pd.Series([signal.iloc[-1]], index=[df.index[-1]]) 