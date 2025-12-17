from app import db
# CREATE DATABASE japanese_vocab CHARACTER SET utf8mb4;
from werkzeug.security import generate_password_hash, check_password_hash


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    source = db.Column(db.String(50))
    content = db.Column(db.Text)

    occurrences = db.relationship("WordOccurrence", back_populates="article")


class Word(db.Model):
    __tablename__ = "words"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), unique=True)
    pos = db.Column(db.String(50))
    furigana = db.Column(db.String(100))
    meanings = db.Column(db.String(256))
    level = db.Column(db.String(10))

    occurrences = db.relationship("WordOccurrence", back_populates="word")
    examples = db.relationship("Example", back_populates="word", cascade="all, delete-orphan")
    learning_items = db.relationship("LearningItem", back_populates="word", uselist=True, cascade="all, delete-orphan")
    

class WordOccurrence(db.Model):
    __tablename__ = "word_occurrences"

    word_id = db.Column(db.Integer, db.ForeignKey("words.id"), primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), primary_key=True)
    count = db.Column(db.Integer)

    word = db.relationship("Word", back_populates="occurrences")
    article = db.relationship("Article", back_populates="occurrences")

class Example(db.Model):
    __tablename__ = "examples"

    id = db.Column(db.Integer, primary_key=True)

    word_id = db.Column(
        db.Integer,
        db.ForeignKey("words.id"),
        nullable=False
    )

    sentence = db.Column(db.Text, nullable=False)

    translation = db.Column(db.Text)      # nghĩa tiếng Việt / Anh
    source = db.Column(db.String(50))     # NHK / movie / meeting / manual
    level = db.Column(db.String(10))      # N3 / N2 / N1 (optional)

    word = db.relationship(
        "Word",
        back_populates="examples"
    )

    # Thêm example
    # word = Word.query.filter_by(word="円高ドル安").first()

    # ex = Example(
    #     word_id=word.id,
    #     sentence="円高ドル安が進んでいます。",
    #     translation="Đồng yên mạnh lên, đô la yếu đi.",
    #     source="NHK"
    # )

    # db.session.add(ex)
    # db.session.commit()


class LearningItem(db.Model):
    __tablename__ = "learning_items"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey("words.id"), nullable=False)

    # learning: đang học reviewing: đang ôn mastered: đã thuộc dropped: bỏ học ❌
    status = db.Column(db.String(20), default="learning") 
    added_at = db.Column(db.DateTime, server_default=db.func.now())
    last_reviewed_at = db.Column(db.DateTime)
    review_count = db.Column(db.Integer, default=0)
    dropped_at = db.Column(db.DateTime)
    drop_reason = db.Column(db.String(255))

    word = db.relationship("Word", back_populates="learning_items")
    user = db.relationship("User", back_populates="learning_items")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")  # ⚡ "user" hoặc "admin"

    learning_items = db.relationship("LearningItem", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
