# helper.py
from collections import Counter
from sudachipy import dictionary, tokenizer as sudachi_tokenizer
import re


tokenizer = dictionary.Dictionary(dict="full").create()

# các POS nên BỎ (trợ từ, lịch sự…)
STOP_POS = {"助詞", "助動詞", "補助記号", "記号"}
KEEP_POS = {"名詞", "動詞", "形容詞", "形状詞"}
COMMON_JUNK = {"もの", "こと", "ところ", "よう", "ため", "％", "し"}
AUX_VERBS = {"する", "なる", "ある", "いる", "できる"}

def extract_words(text: str):
    """
    return:
      { (word, pos): count }
    """
    tokens = tokenizer.tokenize(
        text,
        sudachi_tokenizer.Tokenizer.SplitMode.C
    )

    words = []

    for t in tokens:
        pos1, pos2 = t.part_of_speech()[0], t.part_of_speech()[1]
        surface = t.surface()

        # bỏ rác
        if pos1 in STOP_POS:
            continue

        # chỉ giữ loại cần
        if pos1 not in KEEP_POS:
            continue

        # bỏ số (39, 155, 2025, 1.17...)
        if pos1 == "名詞" and pos2 == "数詞":
            continue


        if re.fullmatch(r"[0-9０-９]+([.,．][0-9０-９]+)?", t.surface()):
            continue

        # 4️⃣ bỏ ngày / tháng / năm
        if surface.endswith(("日", "月", "年")) and surface[:-1].isdigit():
            continue

        # 5️⃣ bỏ tiền tệ
        if surface.endswith(("円", "銭", "ドル", "ユーロ")):
            continue

        if surface in COMMON_JUNK:
            continue

        if pos1 == "動詞" and surface in AUX_VERBS:
            continue

        words.append((surface, pos1))

    return Counter(words)
