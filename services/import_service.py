import json
from app import db
from models import Kanji, Word, Grammar, Example, WordExample, WordForm, WordGloss, WordReading, WordSense, Article

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
        # WORD (entry)
        # ===========================
        ent_seq = v.get("ent_seq", [None])[0]
        if not ent_seq:
            continue

        # tránh import trùng
        word = Word.query.filter_by(ent_seq=ent_seq).first()
        if word:
            continue

        word = Word(ent_seq=ent_seq)
        db.session.add(word)

        # ===========================
        # WORD FORMS (k_ele)
        # ===========================
        for k in v.get("k_ele", []):
            for keb in k.get("keb", []):
                form = WordForm(
                    word=word,
                    form=keb,
                    priority=",".join(k.get("ke_pri", [])) if k.get("ke_pri") else None
                )
                db.session.add(form)

        # ===========================
        # WORD READINGS (r_ele)
        # ===========================
        for r in v.get("r_ele", []):
            for reb in r.get("reb", []):
                reading = WordReading(
                    word=word,
                    reading=reb,
                    info=",".join(r.get("re_inf", [])) if r.get("re_inf") else None,
                    priority=",".join(r.get("re_pri", [])) if r.get("re_pri") else None
                )
                db.session.add(reading)

        # ===========================
        # WORD SENSES
        # ===========================
        for s in v.get("sense", []):

            sense = WordSense(
                word=word,
                pos=",".join(s.get("pos", [])) if s.get("pos") else None,
                misc=",".join(s.get("misc", [])) if s.get("misc") else None,
                antonym=",".join(s.get("ant", [])) if s.get("ant") else None,
                xref=",".join(s.get("xref", [])) if s.get("xref") else None
            )
            db.session.add(sense)

            # ===========================
            # GLOSSES
            # ===========================
            for g in s.get("gloss", []):
                db.session.add(
                    WordGloss(
                        sense=sense,
                        means_vi=g.get("vi"),
                        means_en=g.get("en")
                    )
                )

            # ===========================
            # EXAMPLES
            # ===========================
            for ex in s.get("example", []):
                ex_text = ex.get("ex_text", [None])[0]

                jp = None
                en = None
                vi = None

                for sent in ex.get("ex_sent", []):
                    if sent.get("$", {}).get("xml:lang") == "jpn":
                        jp = sent.get("_")
                    elif sent.get("$", {}).get("xml:lang") == "eng":
                        data = sent.get("_")
                        if isinstance(data, dict):
                            en = data.get("en")
                            vi = data.get("vi")

                if jp:
                    example = WordExample(
                        sense=sense,
                        ex_text=ex_text,
                        sentence=jp,
                        translation_en=en,
                        translation_vi=vi
                    )
                    db.session.add(example)

    db.session.commit()
    print("Import vocabulary completed.")


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
# def run_import():
def run_import(kanji_file, vocab_file, grammar_file):
    print("Starting import...")
    # import_kanji(kanji_file)
    # import_vocab(vocab_file)
    # import_grammar(grammar_file)
    # articles = Article.query.all()
    # for a in articles:
    #     db.session.delete(a)

    # words = Word.query.all()
    # for a in words:
    #     db.session.delete(a)

    db.session.commit()
    print("All data imported successfully!")


if __name__ == "__main__":
    from app import app

    with app.app_context():
        # run_import(
        #     kanji_file="data/kanji.json",
        #     vocab_file="data/vocab.json",
        #     grammar_file="data/grammar.json")
        db.session.query(Article).delete()
        db.session.commit()
