import re
import string
from typing import Optional

POSITIVE_WORDS = {
    "dobr", "świet", "super", "faj", "spoko", "pozytyw", "ok", "zadowol", "motyw", "relaks", "luz"
}
NEGATIVE_WORDS = {
    "stres", "zmęczen", "znuż", "słab", "smut", "zaniepokoj", "przeciąż", "problem", "trudn", "niepewn"
}
TOPIC_KEYWORDS = {
    "stres": ["stres", "naprężen", "nerw", "presja"],
    "egzaminy": ["egzam", "kolokwi", "test", "zaliczen", "sprawdzian"],
    "organizacja": ["plan", "termin", "godzin", "zajęć", "organiz"],
    "relacje": ["przyjaź", "koleż", "znajom", "zespół", "współpraca"],
    "motywacja": ["motyw", "chęć", "zapał", "ambicj", "energia"]
}


def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.replace("ż", "z").replace("ź", "z").replace("ć", "c")
    text = text.replace("ś", "s").replace("ń", "n")
    text = text.replace("ą", "a").replace("ę", "e").replace("ł", "l")
    text = text.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    return text


def detect_sentiment(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    text = normalize_text(text)
    tokens = text.split()
    positive = sum(1 for token in tokens if any(token.startswith(word) for word in POSITIVE_WORDS))
    negative = sum(1 for token in tokens if any(token.startswith(word) for word in NEGATIVE_WORDS))
    if positive > negative:
        return "positive"
    if negative > positive:
        return "negative"
    if positive == negative and positive > 0:
        return "neutral"
    return "neutral"


def extract_keywords(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    text = normalize_text(text)
    tokens = set(text.split())
    found = set()
    for label, patterns in TOPIC_KEYWORDS.items():
        for pattern in patterns:
            if any(token.startswith(pattern) for token in tokens):
                found.add(label)
                break
    if not found:
        return None
    return ", ".join(sorted(found))
