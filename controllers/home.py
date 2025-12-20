from flask import render_template, request, redirect
from app import app, db
from models import Article, Word, WordOccurrence, LearningItem
from flask import g, session
from models import User
from services import run_import
from sqlalchemy.orm import joinedload


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = User.query.get(user_id) if user_id else None


@app.route("/")
def index():
    # run_import(
    #     kanji_file="data/kanji.json",
    #     vocab_file="data/vocab.json",
    #     grammar_file="data/grammar.json")

    return render_template("index.html")


@app.route("/top-words")
def top_words():
    words_data = []

    results = (
        db.session.query(
            Word,
            db.func.sum(WordOccurrence.count).label("freq")
        )
        .join(WordOccurrence)
        .options(
            joinedload(Word.forms),
            joinedload(Word.readings)
        )
        .group_by(Word.id)
        .order_by(db.desc("freq"))
        .limit(5000)
        .all()
    )

    for word, freq in results:
        li_status = None
        if g.user:
            item = LearningItem.query.filter_by(
                user_id=g.user.id,
                word_id=word.id
            ).first()
            li_status = item.status if item else None

        words_data.append({
            "text": display_word(word),
            "freq": freq,
            "word_id": word.id,
            "learning_status": li_status
        })

    return render_template("top_words.html", words=words_data)

def display_word(word: Word):
    if word.forms:
        return word.forms[0].form
    if word.readings:
        return word.readings[0].reading
    return ""