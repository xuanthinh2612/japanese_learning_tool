from flask import render_template, request, redirect, flash
from app import app, db
from models import Article, Word, WordOccurrence, LearningItem, WordForm, WordSense, WordGloss, Grammar, Kanji, WordReading
from flask import g, session, jsonify
from models import User
from services import run_import
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
from sqlalchemy import or_


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = User.query.get(user_id) if user_id else None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/top-words")
def top_words():
    # run_import()
    
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
    
    

@app.route("/my-words")
def my_learning():
    if g.user is None:
        flash("Vui lòng đăng nhập")
        return redirect("/login")

    return render_template("my_learning.html")
    

@app.route("/my-grammars")
def my_grammars():
    if g.user is None:
        flash("Vui lòng đăng nhập")
        return redirect("/login")

    return render_template("my_learning.html")
    

@app.route("/my-kanji")
def my_kanji():
    if g.user is None:
        flash("Vui lòng đăng nhập")
        return redirect("/login")

    return render_template("my_learning.html")

    


def display_word(word: Word):
    if word.forms:
        return word.forms[0].form
    if word.readings:
        return word.readings[0].reading
    return ""


@app.route("/search/<key>", methods=["POST"])
def search(key):
    if g.user is None:
        flash("Vui lòng đăng nhập")
        return redirect("/login")

    return render_template("my_learning.html")


@app.route("/api/search-suggest", methods=["POST"])
def search_suggest():
    data = request.get_json()
    keyword = data.get("keyword")

    words = (
        db.session.query(Word)
        .outerjoin(WordForm)
        .outerjoin(WordSense)
        .outerjoin(WordReading)
        .outerjoin(WordGloss)
        .filter(
            or_(
                WordForm.form.like(f"%{keyword}%"),
                WordGloss.means_vi.like(f"%{keyword}%"),
                WordReading.reading.like(f"%{keyword}%"),
            )
        )
        .distinct()
        .limit(10)
        .all()
    )

    kanji_list = (
        Kanji.query
        .filter(
            or_(
                Kanji.character.like(f"%{keyword}%"),
                Kanji.onyomi.like(f"%{keyword}%"),
                Kanji.kunyomi.like(f"%{keyword}%"),
                Kanji.hanviet.like(f"%{keyword}%"),
                Kanji.meaning_vi.like(f"%{keyword}%"),
            )
        )
        .limit(10)
        .all()
    )

    grammars = (
        Grammar.query
        .filter(
            or_(
                Grammar.pattern.like(f"%{keyword}%"),
                Grammar.meaning.like(f"%{keyword}%"),
            )
        )
        .limit(10)
        .all()
    )

    return jsonify({
        "success": True,
        "words": uniformDataWord(words),
        "kanji_list": uniformDataKanji(kanji_list),
        "grammars": uniformDataGrammar(grammars)
        })

def uniformDataWord(words):
    words_data = []
    for w in words:
        if w.forms and w.senses:
            words_data.append({
                "form":w.forms[0].form, 
                "means_vi":w.senses[0].glosses[0].means_vi
                })

    return words_data

def uniformDataKanji(kanji_list):
    kanji_list_data = [{"id": k.id, "character": k.character, "means_vi": k.meaning_vi} for k in kanji_list]
    return kanji_list_data

def uniformDataGrammar(grammars):
    grammar_data = [{"id": g.id, "pattern": g.pattern, "meaning": g.meaning} for g in grammars]
    return grammar_data