import re 
import unicodedata

def remove_emoji_and_icons(text: str) -> str:
    # Remove all characters that are symbols, pictographs, or other non-text elements
    cleaned = ''.join(ch for ch in text if unicodedata.category(ch)[0] != 'So')
    
    # Also remove remaining emoji using regex ranges for emoji unicode blocks
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & pictographs
        "\U0001F680-\U0001F6FF"  # Transport & map symbols
        "\U0001F700-\U0001F77F"  # Alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002600-\U000026FF"  # Misc symbols
        "\U00002700-\U000027BF"  # Dingbats
        "\U0001F1E6-\U0001F1FF"  # Flags
        "\U0001FA70-\U0001FAFF"  # Extended pictographs
        "\U0001F018-\U0001F270"  # Various symbols
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    cleaned = emoji_pattern.sub(' ', cleaned)

    # Normalize whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def remove_chinese(text: str) -> str:
    # Remove all CJK (Chinese, Japanese, Korean) ideographs
    return re.sub(r'[\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF]+', '', text)

_whitespace_re = re.compile(r"\s+")
# Regex that matches nearly all non-alphanumeric symbols
_duplicate_symbols_re = re.compile(r'([\[\]\(\)\{\}\<\>\=\+\-\_\&\\\/\*\!\?\:\;\|\,\.~#@\$%\^])\1+')
def clean_text(s: str) -> str:
    s = s.replace("\r", " ").replace("\n", " ").replace("﻿", "")
    s = unicodedata.normalize("NFKC", s)  # "F U L L W I D T H" to "FULLWIDTH"
    s = _whitespace_re.sub(" ", s) # "This  is  a   test." to "This is a test."
    s = _duplicate_symbols_re.sub(r'\1', s)  # "Hello!!!!!!!!!!" to "Hello!"
    s = re.sub(r'([?!.,;:])(?=\w)', r'\1',s)  # "2018?Nhổ" to "2018? Nhổ"

    # Remove Chinese characters
    s = remove_chinese(s)

    # Duplicate specific symbols removal
    s = re.sub(r'_{2,}', '_', s)
    s = re.sub(r'\*{2,}', '*', s)
    s = re.sub(r'\-{2,}', '-', s)
    s = re.sub(r'\.{4,}', '.', s)
    s = re.sub(r'\,{2,}', ',', s)
    s = remove_emoji_and_icons(s)
    s = re.sub(r"\'", '', s)
    s = re.sub(r"\"", '', s)
    s = re.sub(r"\"""", '', s)
    s = re.sub(r'\;{2,}', ',', s)
    s = re.sub(r'\:{2,}', ',', s)
    
    return s.strip()