import importlib
from cards_parser import cards_from_yaml
from backtest.data_loader import download_ohlcv
from backtest.engine import run_backtest
from report.metrics import calc_metrics
import pandas as pd

def to_utc_ts(val):
    ts = pd.to_datetime(val)
    if ts.tzinfo is None:
        ts = ts.tz_localize('UTC')
    else:
        ts = ts.tz_convert('UTC')
    return ts

def get_strategy_func(strategy_name):
    mod = importlib.import_module(f"strategies.{strategy_name.lower()}")
    func = [v for k, v in vars(mod).items() if k.lower().startswith(strategy_name.lower())][0]
    return func

def main():
    cards = cards_from_yaml()
    for card in cards:
        run_card_result(card)

def run_card_result(card):
    """
    카드 1개 실행 결과를 dict로 반환 (UI에서 import해서 쓸 수 있게)
    """
    all_start = card['backtest_period'][0]
    all_end = card['backtest_period'][1]
    data = download_ohlcv(symbol=card['symbol'], timeframe=card['timeframe'], since=all_start, until=all_end)
    # 단일 종목이면 컬럼명을 'close'로 통일
    if len(data.columns) == 1 or (len(data.columns) <= 5 and 'close' in data.columns[0]):
        data = data.rename(columns={col: 'close' for col in data.columns})
    strategy_func = get_strategy_func(card['strategy'])
    lookback = card.get('lookback', 300)
    # 백테스트
    bt_start = to_utc_ts(card['backtest_period'][0])
    bt_end = to_utc_ts(card['backtest_period'][1])
    data_bt = data[(data.index >= bt_start) & (data.index <= bt_end)]
    results_bt = run_backtest(data_bt, strategy_func, card['params'], lookback, initial_capital=1.0)
    trades_bt = results_bt['trades']
    metrics_bt = calc_metrics(results_bt['equity'])
    # 실시간 시그널
    import datetime
    now = pd.Timestamp.utcnow()
    tf_map = {'1m': 1, '5m': 5, '15m': 15, '30m': 30, '1h': 60, '4h': 240, '1d': 1440}
    tf_min = tf_map.get(card['timeframe'], 60)
    since = now - pd.Timedelta(minutes=200*tf_min)
    data_live = download_ohlcv(card['symbol'], card['timeframe'], since, now)
    if len(data_live.columns) == 1 or (len(data_live.columns) <= 5 and 'close' in data_live.columns[0]):
        data_live = data_live.rename(columns={col: 'close' for col in data_live.columns})
    print(f"[DEBUG-data_live] {data_live.head()} ... tail={data_live.tail()}")
    signal_series = strategy_func(data_live, **card['params'])
    print(f"[DEBUG-signal_series] {signal_series[:5]} ... tail={signal_series[-5:]}")
    last_signal = signal_series.iloc[-1] if hasattr(signal_series, 'iloc') and not signal_series.empty else None
    return {
        'card': card,
        'backtest': {'results': results_bt, 'trades': trades_bt, 'metrics': metrics_bt},
        'realtime_signal': last_signal,
    }

if __name__ == "__main__":
    main() 