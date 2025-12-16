from app import db

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

    occurrences = db.relationship("WordOccurrence", back_populates="word")


class WordOccurrence(db.Model):
    __tablename__ = "word_occurrences"

    word_id = db.Column(db.Integer, db.ForeignKey("words.id"), primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), primary_key=True)
    count = db.Column(db.Integer)

    word = db.relationship("Word", back_populates="occurrences")
    article = db.relationship("Article", back_populates="occurrences")
