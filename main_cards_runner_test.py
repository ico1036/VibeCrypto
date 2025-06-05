import pytest
from cards_parser import cards_from_yaml
from main_cards_runner import run_card_result

def test_realtime_signal():
    cards = cards_from_yaml()
    assert len(cards) > 0, '카드가 하나도 없으면 테스트 못한다!'
    for card in cards:
        result = run_card_result(card)
        sig = result['realtime_signal']
        # None이면 패스, 아니면 타입/값 체크
        if sig is not None:
            assert isinstance(sig, (int, float)), f'실시간 시그널 타입 이상함: {sig}'
            # int면 -1, 0, 1 중 하나거나, float면 0~1 사이
            if isinstance(sig, int):
                assert sig in [-1, 0, 1], f'실시간 시그널 int값 이상함: {sig}'
            elif isinstance(sig, float):
                assert -1 <= sig <= 1, f'실시간 시그널 float값 이상함: {sig}' 