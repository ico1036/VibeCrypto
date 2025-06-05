import ccxt
import pandas as pd
from datetime import datetime, timezone, date

def to_timestamp(dt):
    # 문자열이면 datetime으로 변환
    if isinstance(dt, str):
        dt = pd.to_datetime(dt)
    # date 타입이면 datetime으로 변환
    if isinstance(dt, date) and not isinstance(dt, datetime):
        dt = datetime(dt.year, dt.month, dt.day)
    # tzinfo 붙이기
    if getattr(dt, 'tzinfo', None) is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)

def download_ohlcv(symbol: str, timeframe: str, since: str, until: str, exchange_name: str = 'binance'):
    """
    CCXT를 이용한 OHLCV 데이터 다운로드 함수 (기본 binance)
    :param symbol: 예) 'BTC/USDT'
    :param timeframe: 예) '1h', '4h', '1d'
    :param since: 시작일 (ISO str)
    :param until: 종료일 (ISO str)
    :param exchange_name: 거래소명
    :return: pd.DataFrame
    """
    exchange = getattr(ccxt, exchange_name)()
    since_ts = to_timestamp(since)
    until_ts = to_timestamp(until)
    all_ohlcv = []
    limit = 1000
    now = since_ts
    while now < until_ts:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=now, limit=limit)
        if not ohlcv:
            break
        all_ohlcv += ohlcv
        last = ohlcv[-1][0]
        if last == now:
            break
        now = last + 1
        if last >= until_ts:
            break
    df = pd.DataFrame(all_ohlcv, columns=["datetime", "open", "high", "low", "close", "volume"])
    df["datetime"] = pd.to_datetime(df["datetime"], unit="ms", utc=True)
    df = df.set_index("datetime")
    df = df[df.index <= pd.to_datetime(until, utc=True)]
    return df 