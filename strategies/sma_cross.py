import pandas as pd

def sma_cross_strategy(data, fast=20, slow=60):
    """
    단순 이동평균 크로스오버 전략 (비중 기반)
    :param data: pd.DataFrame, columns=['open', 'high', 'low', 'close', ...]
    :param fast: 빠른 이동평균 기간
    :param slow: 느린 이동평균 기간
    :return: (1,) shape 벡터 (마지막 시점 값)
    """
    df = data.copy()
    df['fast_ma'] = df['close'].rolling(fast).mean()
    df['slow_ma'] = df['close'].rolling(slow).mean()
    spread = df['fast_ma'] - df['slow_ma']
    # spread가 0보다 크면 매수, spread가 클수록 비중↑
    max_abs = spread.abs().max() if spread.abs().max() != 0 else 1
    signal = (spread / max_abs).clip(0, 1).fillna(0)
    # 마지막 시점 값만 벡터로 반환
    return pd.Series([signal.iloc[-1]], index=[df.index[-1]]) 