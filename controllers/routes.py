from flask import render_template, request, redirect
from app import app, db
from models import Article, Word, WordOccurrence, LearningItem
from controllers.helper import extract_words
from flask import g, session
from models import User

@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = User.query.get(user_id) if user_id else None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_article():
    if request.method == "POST":
        article = Article(
            title=request.form["title"],
            source=request.form["source"],
            content=request.form["content"]
        )
        db.session.add(article)
        db.session.commit()

        word_counts = extract_words(article.content)

        for (word_text, pos), count in word_counts.items():
            word = Word.query.filter_by(word=word_text).first()
            if not word:
                word = Word(word=word_text, pos=pos)
                db.session.add(word)
                db.session.commit()

            occ = WordOccurrence.query.filter_by(
                word_id=word.id,
                article_id=article.id
            ).first()
            
            if occ:
                occ.count += count
            else:
                occ = WordOccurrence(
                    word_id=word.id,
                    article_id=article.id,
                    count=count
                )
            db.session.add(occ)

        db.session.commit()
        return redirect("/")

    return render_template("add_article.html")


@app.route("/word/<word>")
def word_detail(word):
    data = (
        db.session.query(
            Article.title,
            Article.source,
            Article.content,
            WordOccurrence.count
        )
        .join(WordOccurrence)
        .join(Word)
        .filter(Word.word == word)
        .all()
    )
    return render_template("word.html", word=word, articles=data, current_source="daily")
