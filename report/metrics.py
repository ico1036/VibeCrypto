import numpy as np
import pandas as pd

# 누적수익률
def cum_returns_final(equity_curve):
    return equity_curve.iloc[-1] / equity_curve.iloc[0] - 1

# 연율화수익률 (CAGR)
def annual_return(equity_curve, freq='daily'):
    n = len(equity_curve)
    if n < 2:
        return np.nan
    dt = (equity_curve.index[-1] - equity_curve.index[0]).days
    if dt == 0:
        return np.nan
    years = dt / 365.25
    total_return = equity_curve.iloc[-1] / equity_curve.iloc[0]
    return total_return ** (1/years) - 1

# MDD (최대 낙폭)
def max_drawdown(equity_curve):
    roll_max = equity_curve.cummax()
    drawdown = equity_curve / roll_max - 1
    return drawdown.min()

# 샤프지수 (무위험수익률 0 가정)
def sharpe_ratio(equity_curve, freq='daily'):
    ann_ret = annual_return(equity_curve, freq)
    ann_vol = annual_volatility(equity_curve, freq)
    if ann_vol == 0:
        return np.nan
    return ann_ret / ann_vol

# 연율화 변동성
def annual_volatility(equity_curve, freq='daily'):
    ret = equity_curve.pct_change().dropna()
    std = ret.std()
    ann_factor = {'daily': np.sqrt(252), 'hourly': np.sqrt(252*24), '1h': np.sqrt(252*24), '4h': np.sqrt(252*6), '1d': np.sqrt(252)}
    factor = ann_factor.get(freq, np.sqrt(252))
    return std * factor

def calc_metrics(equity_curve: pd.Series, freq: str = 'daily'):
    """
    주요 성능지표 계산 (누적수익률, 연별수익률, 연율화수익률, MDD, Sharpe, 변동성 등)
    :param equity_curve: 자산 곡선 (pd.Series)
    :param freq: 빈도 ('daily', 'hourly' 등)
    :return: dict
    """
    print(f"[METRICS DEBUG] equity_curve head: {equity_curve.head(10)} tail: {equity_curve.tail(10)}")
    metrics = {
        '누적수익률': float(cum_returns_final(equity_curve)),
        '연율화수익률': float(annual_return(equity_curve, freq)),
        'MDD': float(max_drawdown(equity_curve)),
        'Sharpe': float(sharpe_ratio(equity_curve, freq)),
        '변동성': float(annual_volatility(equity_curve, freq)),
        # '연별수익률': ...
    }
    return metrics 