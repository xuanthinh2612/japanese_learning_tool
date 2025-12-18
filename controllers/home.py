from flask import render_template, request, redirect
from app import app, db
from models import Article, Word, WordOccurrence, LearningItem
from flask import g, session
from models import User


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = User.query.get(user_id) if user_id else None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/top-words")
def top_words():
    words_data = []
    for w, freq, word_id in (
        db.session.query(
            Word.word,
            db.func.sum(WordOccurrence.count).label("freq"),
            Word.id
        )
        .join(WordOccurrence)
        .group_by(Word.id, Word.word)
        .order_by(db.desc("freq"))
        .limit(5000)
        .all()
    ):
        li_status = None
        if g.user:
            item = LearningItem.query.filter_by(user_id=g.user.id, word_id=word_id).first()
            li_status = item.status if item else None
        words_data.append((w, freq, word_id, li_status))

    return render_template("top_words.html", words=words_data)
