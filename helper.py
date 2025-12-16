from janome.tokenizer import Tokenizer
from collections import Counter

tokenizer = Tokenizer()

def extract_words(text):
    results = []
    for token in tokenizer.tokenize(text):
        pos = token.part_of_speech.split(",")[0]
        base = token.base_form

        if pos in ["名詞", "動詞", "形容詞", "副詞"] and len(base) > 1:
            results.append((base, pos))

    return Counter(results)

# from janome.tokenizer import Tokenizer
# from collections import Counter, defaultdict

# STOP_WORDS = {
#     "する", "ある", "いる", "こと", "もの", "これ", "それ", "ため", "よう", "ところ", "とき"
# }

# tokenizer = Tokenizer()

# def extract_words(texts):
#     article_word_freqs = []

#     for text in texts:
#         words = []
#         tokens = tokenizer.tokenize(text)

#         for token in tokens:
#             base = token.base_form

#             # split an toàn
#             pos_parts = token.part_of_speech.split(",")
#             pos_main = pos_parts[0] if len(pos_parts) > 0 else "*"
#             pos_sub = pos_parts[1] if len(pos_parts) > 1 else "*"

#             # bỏ từ rỗng hoặc stop word
#             if base == "*" or base in STOP_WORDS:
#                 continue

#             # chỉ giữ content words
#             if pos_main in ["名詞", "動詞", "形容詞", "副詞"]:
#                 article_word_freqs.append((base, pos_main))


#     # tổng hợp across articles
#     return Counter(article_word_freqs)
