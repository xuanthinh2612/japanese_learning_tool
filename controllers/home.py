from flask import render_template, request, redirect, flash
from app import app, db
from models import Article, Word, WordOccurrence, LearningItem
from flask import g, session
from models import User
from services import run_import
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func


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
    page = request.args.get("page", 1, type=int)
    per_page = 30   # hiển thị rất nhiều từ / page

    query = (
        db.session.query(
            Word,
            func.sum(WordOccurrence.count).label("freq")
        )
        .join(WordOccurrence)
        .options(
            joinedload(Word.forms),
            joinedload(Word.readings)
        )
        .group_by(Word.id)
        .order_by(func.sum(WordOccurrence.count).desc())
    )

    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    words_data = []

    for word, freq in pagination.items:
        li_status = None
        if g.user:
            item = LearningItem.query.filter_by(
                user_id=g.user.id,
                word_id=word.id
            ).first()
            li_status = item.status if item else None

        words_data.append({
            "id": word.id,
            "text": display_word(word),
            "freq": freq,
            "status": li_status
        })

    return render_template(
        "top_words.html",
        words=words_data,
        pagination=pagination
    )
    
    

@app.route("/my_learning")
def my_learning():
    if g.user is None:
        flash("Vui lòng đăng nhập")
        return redirect("/login")

    # items = LearningItem.query.filter_by(user_id=g.user.id).join(Word).all()
    # items = (
    #     db.session.query(LearningItem)
    #     .filter_by(user_id=g.user.id, status=status)
    #     .all()
    # )

    # data = [
    #     {
    #         "word_id": i.word.id,
    #         "word": i.word.forms[0].form,
    #     }
    #     for i in items
    # ]
    
    return render_template("my_learning.html")

    


def display_word(word: Word):
    if word.forms:
        return word.forms[0].form
    if word.readings:
        return word.readings[0].reading
    return ""