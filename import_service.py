import json
from app import db
from models import Kanji, Word, Grammar, Example, WordKanji, WordGrammar

# ===========================
# HELPER FUNCTIONS
# ===========================

def load_json(file_path):
    """Load JSON file"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_or_create_word(word_text):
    """Lấy Word nếu đã có, nếu chưa thì tạo mới"""
    word = Word.query.filter_by(word=word_text).first()
    if not word:
        word = Word(word=word_text)
        db.session.add(word)
        db.session.flush()
    return word


def get_or_create_kanji(char):
    """Lấy Kanji nếu đã có, nếu chưa thì tạo mới"""
    kanji = Kanji.query.filter_by(character=char).first()
    if not kanji:
        kanji = Kanji(character=char)
        db.session.add(kanji)
        db.session.flush()
    return kanji


def get_or_create_grammar(pattern):
    """Lấy Grammar nếu đã có, nếu chưa thì tạo mới"""
    grammar = Grammar.query.filter_by(pattern=pattern).first()
    if not grammar:
        grammar = Grammar(pattern=pattern)
        db.session.add(grammar)
        db.session.flush()
    return grammar


# ===========================
# IMPORT KANJI
# ===========================
def import_kanji(file_path):
    kanji_list = load_json(file_path)

    for k in kanji_list:
        char = k.get("k")
        if not char:
            continue

        kanji = get_or_create_kanji(char)
        kanji.onyomi = ",".join(k.get("on", []))
        kanji.kunyomi = ",".join(k.get("kun", []))
        kanji.meaning = k.get("m", {}).get("en", "")
        kanji.strokes = int(k.get("s", 0))
        kanji.frequency = int(k.get("f", 0)) if k.get("f") else None

    db.session.commit()
    print(f"Imported {len(kanji_list)} Kanji.")


# ===========================
# IMPORT VOCABULARY
# ===========================
def import_vocab(file_path):
    vocab_list = load_json(file_path)

    for v in vocab_list:
        # Lấy hoặc tạo Word
        word_text = v.get("k_ele", [{}])[0].get("keb", [None])[0] \
                    or v.get("r_ele", [{}])[0].get("reb", [None])[0]
        if not word_text:
            continue

        word = get_or_create_word(word_text)

        # Furigana
        readings = [r.get("reb", [])[0] for r in v.get("r_ele", []) if r.get("reb")]
        word.furigana = ",".join(readings) if readings else None

        # Meanings
        senses = v.get("sense", [])
        meanings = []
        for s in senses:
            glosses = s.get("gloss", [])
            for g in glosses:
                meanings.append(g.get("en"))
        word.meanings = "; ".join(filter(None, meanings))

        # TODO: level (nếu có)
        word.level = None

        # Examples
        for s in senses:
            for ex in s.get("example", []):
                sentence = ex.get("ex_text", [None])[0]
                translation = ex.get("ex_sent", [None])[0].get("_", "") if ex.get("ex_sent") else ""
                if sentence:
                    example = Example(
                        word=word,
                        sentence=sentence,
                        translation=translation
                    )
                    db.session.add(example)

    db.session.commit()
    print(f"Imported {len(vocab_list)} Words.")


# ===========================
# IMPORT GRAMMAR
# ===========================
def import_grammar(file_path):
    grammar_list = load_json(file_path)

    for g in grammar_list:
        pattern = g.get("g")
        if not pattern:
            continue

        grammar = get_or_create_grammar(pattern)
        grammar.meaning = g.get("m", "")
        # level nếu có
        # grammar.level = g.get("level", None)

        # Examples
        for u in g.get("u", []):
            for ex in u.get("ex", []):
                sentence = ex.get("s")
                translation = ex.get("m", "")
                if sentence:
                    example = Example(
                        grammar=grammar,
                        sentence=sentence,
                        translation=translation
                    )
                    db.session.add(example)

    db.session.commit()
    print(f"Imported {len(grammar_list)} Grammar patterns.")


# ===========================
# MAIN IMPORT FUNCTION
# ===========================
def run_import(kanji_file, vocab_file, grammar_file):
    print("Starting import...")
    import_kanji(kanji_file)
    import_vocab(vocab_file)
    import_grammar(grammar_file)
    print("All data imported successfully!")


run_import(
    kanji_file="data/kanji.json",
    vocab_file="data/vocab.json",
    grammar_file="data/grammar.json"
)
