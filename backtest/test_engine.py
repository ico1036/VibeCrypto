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
        # run_backtest는 (n_assets,) 벡터를 기대하므로, 시리즈를 벡터로 변환
        sig = sma_cross_strategy(window.rename(columns={f'btc_close': 'close'}), fast=fast, slow=slow)
        return [sig.iloc[-1]]
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

if __name__ == '__main__':
    main() 