import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import pytest
from cards_parser import cards_from_yaml
from main_cards_runner import get_strategy_func, get_realtime_signal

def test_realtime_signal_only():
    cards = cards_from_yaml()
    assert len(cards) > 0, '카드가 하나도 없으면 테스트 못한다!'
    for card in cards:
        print(f"\n=== 카드: {card['id']} ===")
        print(f"전략: {card['strategy']}")
        print(f"심볼: {card['symbol']}")
        print(f"타임프레임: {card['timeframe']}")
        strategy_func = get_strategy_func(card['strategy'])
        sig = get_realtime_signal(card, strategy_func)
        print(f"실시간 시그널: {sig}")
        # None이면 패스, 아니면 타입/값 체크
        if sig is not None:
            assert isinstance(sig, (int, float)), f'실시간 시그널 타입 이상함: {sig}'
            if isinstance(sig, int):
                assert sig in [-1, 0, 1], f'실시간 시그널 int값 이상함: {sig}'
            elif isinstance(sig, float):
                assert -1 <= sig <= 1, f'실시간 시그널 float값 이상함: {sig}' 