import csv
import sys
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import List, Optional


FAQ_FILE = Path(__file__).with_name("faq.csv")


@dataclass
class FAQItem:
    question: str
    answer: str


def load_faq(path: Path = FAQ_FILE) -> List[FAQItem]:
    if not path.exists():
        raise FileNotFoundError(
            f"FAQファイルが見つかりません: {path}. READMEの手順に従って用意してください。"
        )

    items: List[FAQItem] = []
    with path.open(encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = row.get("question", "").strip()
            answer = row.get("answer", "").strip()
            if question and answer:
                items.append(FAQItem(question=question, answer=answer))
    if not items:
        raise ValueError("FAQデータが空です。CSVに質問と回答を追加してください。")
    return items


def find_best_match(user_question: str, faq_items: List[FAQItem]) -> FAQItem:
    normalized_input = user_question.strip().lower()
    best_item: Optional[FAQItem] = None
    best_score = -1.0

    for item in faq_items:
        score = SequenceMatcher(None, normalized_input, item.question.lower()).ratio()
        if score > best_score:
            best_score = score
            best_item = item

    if best_item is None:
        raise ValueError("FAQが読み込めていません。")
    return best_item


def main():
    faq_items = load_faq()

    if len(sys.argv) > 1:
        user_question = " ".join(sys.argv[1:])
    else:
        user_question = input("質問を入力してください: ")

    best_item = find_best_match(user_question, faq_items)

    print("\n--- 最も近いFAQ ---")
    print(f"Q: {best_item.question}")
    print(f"A: {best_item.answer}")


if __name__ == "__main__":
    main()
