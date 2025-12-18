# CREATE DATABASE japanese_vocab CHARACTER SET utf8mb4;
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


# ==================================================
# USER
# ==================================================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user") # role "admin" or "user"

    learning_items = db.relationship(
        "LearningItem",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ==================================================
# ARTICLE (giữ nguyên)
# ==================================================
class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    source = db.Column(db.String(50))
    content = db.Column(db.Text)

    occurrences = db.relationship(
        "WordOccurrence",
        back_populates="article",
        cascade="all, delete-orphan"
    )


# ==================================================
# WORD (Vocabulary)
# ==================================================
class Word(db.Model):
    __tablename__ = "words"

    id = db.Column(db.Integer, primary_key=True)

    word = db.Column(db.String(100), unique=True, nullable=False)
    furigana = db.Column(db.String(100))
    pos = db.Column(db.String(50))
    meanings = db.Column(db.Text)
    level = db.Column(db.String(10))  # N5–N1

    examples = db.relationship(
        "Example",
        back_populates="word",
        cascade="all, delete-orphan"
    )

    kanji = db.relationship(
        "Kanji",
        secondary="word_kanji",
        back_populates="words"
    )

    grammar = db.relationship(
        "Grammar",
        secondary="word_grammar",
        back_populates="words"
    )

    learning_items = db.relationship(
        "LearningItem",
        back_populates="word",
        cascade="all, delete-orphan"
    )

    occurrences = db.relationship(
        "WordOccurrence",
        back_populates="word",
        cascade="all, delete-orphan"
    )

# ==================================================
# KANJI
# ==================================================
class Kanji(db.Model):
    __tablename__ = "kanji"

    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.String(1), unique=True, nullable=False)

    onyomi = db.Column(db.String(255))
    kunyomi = db.Column(db.String(255))
    meaning = db.Column(db.Text)

    strokes = db.Column(db.Integer)
    frequency = db.Column(db.Integer)
    jlpt_level = db.Column(db.String(5))

    words = db.relationship(
        "Word",
        secondary="word_kanji",
        back_populates="kanji"
    )


# ==================================================
# GRAMMAR
# ==================================================
class Grammar(db.Model):
    __tablename__ = "grammar"

    id = db.Column(db.Integer, primary_key=True)

    pattern = db.Column(db.String(100), unique=True, nullable=False)
    meaning = db.Column(db.Text)
    explanation = db.Column(db.Text)
    level = db.Column(db.String(10))  # N5–N1

    examples = db.relationship(
        "Example",
        back_populates="grammar",
        cascade="all, delete-orphan"
    )

    words = db.relationship(
        "Word",
        secondary="word_grammar",
        back_populates="grammar"
    )


# ==================================================
# EXAMPLE (dùng chung cho Word & Grammar)
# ==================================================
class Example(db.Model):
    __tablename__ = "examples"

    id = db.Column(db.Integer, primary_key=True)

    word_id = db.Column(db.Integer, db.ForeignKey("words.id"), nullable=True)
    grammar_id = db.Column(db.Integer, db.ForeignKey("grammar.id"), nullable=True)

    sentence = db.Column(db.Text, nullable=False)
    translation = db.Column(db.Text)
    source = db.Column(db.String(50)) # NHK / movie / meeting / manual
    level = db.Column(db.String(10))

    word = db.relationship("Word", back_populates="examples")
    grammar = db.relationship("Grammar", back_populates="examples")


# ==================================================
# ASSOCIATION TABLES
# ==================================================
class WordKanji(db.Model):
    __tablename__ = "word_kanji"

    word_id = db.Column(
        db.Integer,
        db.ForeignKey("words.id"),
        primary_key=True
    )

    kanji_id = db.Column(
        db.Integer,
        db.ForeignKey("kanji.id"),
        primary_key=True
    )


class WordGrammar(db.Model):
    __tablename__ = "word_grammar"

    word_id = db.Column(
        db.Integer,
        db.ForeignKey("words.id"),
        primary_key=True
    )

    grammar_id = db.Column(
        db.Integer,
        db.ForeignKey("grammar.id"),
        primary_key=True
    )


# ==================================================
# ARTICLE WORD OCCURRENCE
# ==================================================
class WordOccurrence(db.Model):
    __tablename__ = "word_occurrences"

    word_id = db.Column(
        db.Integer,
        db.ForeignKey("words.id"),
        primary_key=True
    )

    article_id = db.Column(
        db.Integer,
        db.ForeignKey("articles.id"),
        primary_key=True
    )

    count = db.Column(db.Integer, default=1)

    word = db.relationship("Word")
    article = db.relationship("Article")


# ==================================================
# LEARNING / SRS
# ==================================================
class LearningItem(db.Model):
    __tablename__ = "learning_items"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    word_id = db.Column(
        db.Integer,
        db.ForeignKey("words.id"),
        nullable=False
    )

    # learning: đang học reviewing: đang ôn mastered: đã thuộc dropped: bỏ học ❌
    status = db.Column(db.String(20), default="learning")
    added_at = db.Column(db.DateTime, server_default=db.func.now())
    last_reviewed_at = db.Column(db.DateTime)
    review_count = db.Column(db.Integer, default=0)
    dropped_at = db.Column(db.DateTime)
    drop_reason = db.Column(db.String(255))

    user = db.relationship("User", back_populates="learning_items")
    word = db.relationship("Word", back_populates="learning_items")
