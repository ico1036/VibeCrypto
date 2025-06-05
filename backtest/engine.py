import pandas as pd
import numpy as np

def run_backtest(data: pd.DataFrame, strategy_func, params: dict, lookback: int, initial_capital: float = 1.0, position_transform=None):
    """
    날짜별로 lookback window를 전략에 넣고, 전략이 스코어 벡터를 반환하는 time-driven 백테스터
    :param data: 시세 데이터 (index: 날짜, columns: 종목별 'close' 등)
    :param strategy_func: 전략 함수 (window_df, **params) -> (종목수,) 스코어 벡터
    :param params: 전략 파라미터 dict
    :param lookback: lookback 기간 (int)
    :param initial_capital: 초기 자본금
    :param position_transform: 스코어 → 포지션 변환 함수 (None이면 top1 long)
    :return: 결과(수익률 시계열, 트레이드 내역 등)
    """
    dates = data.index
    tickers = [col for col in data.columns if col.endswith('close')]
    n_assets = len(tickers)
    positions = []
    scores = []
    for i in range(lookback, len(dates)):
        window = data.iloc[i-lookback:i]
        score = strategy_func(window, **params)  # (n_assets,) shape
        scores.append(score)
        # 스코어 → 포지션 변환 (예: top1 long, 나머지 0)
        if position_transform is not None:
            pos = position_transform(score)
        else:
            pos = np.zeros(n_assets)
            if np.any(~np.isnan(score)):
                idx = np.nanargmax(score)
                pos[idx] = 1.0
        positions.append(pos)
    # 포지션 DataFrame 만들기
    pos_df = pd.DataFrame(positions, index=dates[lookback:], columns=tickers)
    # 수익률 계산
    ret_df = data[tickers].pct_change().iloc[lookback:]
    strat_ret = (pos_df.shift(1).fillna(0) * ret_df).sum(axis=1)
    print(f"[DEBUG-pos_df] {pos_df.head(10)} ... tail={pos_df.tail(10)}")
    print(f"[DEBUG-ret_df] {ret_df.head(10)} ... tail={ret_df.tail(10)}")
    print(f"[DEBUG-strat_ret] {strat_ret.head(10)} ... tail={strat_ret.tail(10)}")
    equity = initial_capital * (1 + strat_ret).cumprod()
    # 트레이드 내역 (진입/청산 기록)
    trades = []
    prev_pos = np.zeros(n_assets)
    entry_price = [None]*n_assets
    entry_time = [None]*n_assets
    for date, pos in pos_df.iterrows():
        price = data.loc[date, tickers].values
        delta = pos.values - prev_pos
        for j in range(n_assets):
            if delta[j] > 0:
                trades.append({'시점': date, '종목': tickers[j], '구분': '진입/증액', '비중변화': delta[j], '가격': price[j]})
                if entry_price[j] is None:
                    entry_price[j] = price[j]
                    entry_time[j] = date
            elif delta[j] < 0:
                trades.append({'시점': date, '종목': tickers[j], '구분': '청산/감소', '비중변화': delta[j], '가격': price[j]})
                if pos[j] == 0 and entry_price[j] is not None:
                    trades.append({'시점': date, '종목': tickers[j], '구분': '완전청산', '비중변화': -prev_pos[j], '진입일': entry_time[j], '진입가': entry_price[j], '청산가': price[j], '수익률': price[j]/entry_price[j]-1})
                    entry_price[j] = None
                    entry_time[j] = None
        prev_pos = pos.values.copy()
    trades_df = pd.DataFrame(trades)
    result = {
        'equity': equity,
        'positions': pos_df,
        'scores': pd.DataFrame(scores, index=dates[lookback:], columns=tickers),
        'trades': trades_df
    }
    return result

def run_backtest_cpp(data, strategy_func, params, initial_capital=1.0):
    """
    C++ fast 백테스터 dummy (실제 구현은 pybind11 등으로 래핑)
    """
    print("[C++] Fast 백테스터로 실행! (dummy)")
    return run_backtest(data, strategy_func, params, use_fast_backtest_yn=0, initial_capital=initial_capital) 