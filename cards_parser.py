import yaml
import re

def cards_from_md(md_path="workflow_state.md"):
    """
    workflow_state.md에서 Cards 섹션만 파싱해서 리스트(dict)로 반환
    """
    with open(md_path, encoding="utf-8") as f:
        text = f.read()
    # Cards 섹션 추출 (```yaml ... ``` 블록)
    m = re.search(r"## Cards\s*```yaml\n(.*?)```", text, re.DOTALL)
    if not m:
        raise ValueError("Cards 섹션을 찾을 수 없습니다!")
    cards_yaml = m.group(1)
    cards = yaml.safe_load(cards_yaml)
    return cards

def cards_from_yaml(path='cards/cards.yaml'):
    with open(path, 'r') as f:
        cards = yaml.safe_load(f)
    return cards

if __name__ == "__main__":
    cards = cards_from_md()
    for card in cards:
        print(card) 