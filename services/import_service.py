import json
from app import db
from models import Kanji, Word, Grammar, Example, WordKanji, WordGrammar, GrammarUsage

# ===========================
# HELPER FUNCTIONS
# ===========================

def load_json(file_path):
    """Load JSON file"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_text_json_lines(file_path):
    """
    Mỗi dòng trong file là 1 JSON object
    """
    with open(file_path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                print(f"❌ JSON error at line {line_no}: {e}")


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

        kanji = Kanji.query.filter_by(character=char).first()
        if not kanji:
            kanji = Kanji(character=char)
            db.session.add(kanji)

        # Readings
        kanji.onyomi = ",".join(k.get("on", []))
        kanji.kunyomi = ",".join(k.get("kun", []))
        kanji.hanviet = k.get("ah")

        # Meanings
        meanings = k.get("m", {})
        kanji.meaning_en = meanings.get("en")
        kanji.meaning_vi = meanings.get("vi")

        # Metadata
        kanji.strokes = int(k["s"]) if k.get("s") else None
        kanji.frequency = int(k["f"]) if k.get("f") else None

        # Examples
        kanji.examples = k.get("e")

    db.session.commit()    
    print(f"Imported {len(kanji_list)} Kanji.")


# ===========================
# IMPORT VOCABULARY
# ===========================
def import_vocab(file_path):
    for v in load_text_json_lines(file_path):

        # ===========================
        # WORD TEXT
        # ===========================
        word_text = None

        if v.get("k_ele"):
            word_text = v["k_ele"][0].get("keb", [None])[0]
        if not word_text and v.get("r_ele"):
            word_text = v["r_ele"][0].get("reb", [None])[0]

        if not word_text:
            continue

        word = get_or_create_word(word_text)

        # ===========================
        # FURIGANA
        # ===========================
        readings = []
        for r in v.get("r_ele", []):
            if r.get("reb"):
                readings.append(r["reb"][0])

        word.furigana = " : ".join(readings) if readings else None

        # ===========================
        # POS
        # ===========================
        pos_set = set()
        for s in v.get("sense", []):
            for p in s.get("pos", []):
                pos_set.add(p)

        word.pos = ",".join(pos_set) if pos_set else None

        # ===========================
        # MEANINGS (EN + VI)
        # ===========================
        meanings = []
        for s in v.get("sense", []):
            for g in s.get("gloss", []):
                en = g.get("en")
                vi = g.get("vi")
                if en and vi:
                    meanings.append(f"{en} ({vi})")
                elif en:
                    meanings.append(en)
                elif vi:
                    meanings.append(vi)

        word.meanings = "; ".join(meanings)

        # ===========================
        # LEVEL (chưa có → None)
        # ===========================
        word.level = None

        # ===========================
        # EXAMPLES
        # ===========================
        for s in v.get("sense", []):
            for ex in s.get("example", []):
                jp = ex.get("ex_sent", [{}])[0].get("_")
                trans = ""

                # bản dịch EN / VI
                if len(ex.get("ex_sent", [])) > 1:
                    trans_obj = ex["ex_sent"][1].get("_", {})
                    if isinstance(trans_obj, dict):
                        trans = trans_obj.get("vi") or trans_obj.get("en")

                if jp:
                    example = Example(
                        word=word,
                        sentence=jp,
                        translation=trans,
                        source="JMdict"
                    )
                    db.session.add(example)

    db.session.commit()
    print("Import words completed.")


# ===========================
# IMPORT GRAMMAR
# ===========================
def import_grammar(file_path):
    grammar_list = load_json(file_path)

    for g in grammar_list.values():  # vì không lấy key
        pattern = g.get("g")
        if not pattern:
            continue

        # ===== Grammar =====
        grammar = Grammar.query.filter_by(pattern=pattern).first()
        if not grammar:
            grammar = Grammar(
                pattern=pattern,
                meaning=g.get("m", ""),
                level=f"N{g.get('n')}" if g.get("n") else None
            )
            db.session.add(grammar)
            db.session.flush()  # lấy grammar.id

        # ===== Grammar Usage =====
        for u in g.get("u", []):
            usage_pattern = u.get("s")

            usage = GrammarUsage(
                grammar_id=grammar.id,
                pattern=usage_pattern,
                meaning=u.get("m", ""),
                explanation=u.get("e", ""),
                h_note=u.get("h", ""),
                note=u.get("n", "")
            )
            db.session.add(usage)
            db.session.flush()  # lấy usage.id

            # ===== Examples =====
            for ex in u.get("ex", []):
                sentence = ex.get("s")
                if not sentence:
                    continue

                example = Example(
                    grammar_usage_id=usage.id,
                    sentence=sentence,
                    translation=ex.get("m", ""),
                    furigana=ex.get("t", ""),
                    source="data"
                )
                db.session.add(example)

    db.session.commit()
    print("Import grammar completed.")


# ===========================
# MAIN IMPORT FUNCTION
# ===========================
def run_import(kanji_file, vocab_file, grammar_file):
    print("Starting import...")
    # import_kanji(kanji_file)
    import_vocab(vocab_file)
    # import_grammar(grammar_file)
    print("All data imported successfully!")


# run_import(
#     kanji_file="data/kanji.json",
#     vocab_file="data/vocab.json",
#     grammar_file="data/grammar.json")
