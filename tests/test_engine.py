import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import pandas as pd
from backtest.data_loader import download_ohlcv
from backtest.engine import run_backtest
from strategies.sma_cross import sma_cross_strategy
from report.metrics import calc_metrics

# 실제 데이터로 테스트

def main():
    symbol = 'BTC/USDT'
    timeframe = '1h'
    since = '2023-01-01'
    until = '2023-01-10'
    print(f"실제 데이터 다운로드: {symbol} {timeframe} {since}~{until}")
    data = download_ohlcv(symbol, timeframe, since, until, exchange_name='binance')
    print(f"데이터 shape: {data.shape}")
    # run_backtest에 맞게 컬럼명 맞추기 (단일 종목)
    data = data.rename(columns={col: f'btc_{col}' for col in data.columns})
    lookback = 24
    params = {'fast': 8, 'slow': 24}
    def strategy_wrapper(window, fast, slow):
        # run_backtest는 score(weight)로 바로 사용하므로 float만 반환
        sig = sma_cross_strategy(window.rename(columns={f'btc_close': 'close'}), fast=fast, slow=slow)
        return sig.iloc[-1]
    result = run_backtest(
        data,
        strategy_func=strategy_wrapper,
        params=params,
        lookback=lookback,
        initial_capital=1.0
    )
    print('Equity:')
    print(result['equity'].head())
    print('\nPositions:')
    print(result['positions'].head())
    print('\nTrades:')
    print(result['trades'].head())
    print('\nMetrics:')
    print(calc_metrics(result['equity']))

    # 실시간 시그널 테스트 (가장 최근 100개 데이터로)
    print('\n[실시간 시그널 테스트]')
    recent = data.tail(lookback)
    realtime_signal = strategy_wrapper(recent, **params)
    print(f'실시간 시그널: {realtime_signal}')

if __name__ == '__main__':
    main() 