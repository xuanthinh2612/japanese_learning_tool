from flask import render_template, request, redirect
from app import app, db
from models import Article, Word, WordOccurrence, LearningItem
from .helper import extract_words, extract_full_words
from flask import g, session
from models import User, WordForm


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = User.query.get(user_id) if user_id else None


@app.route("/add-article", methods=["GET", "POST"])
def add_article():
    if request.method == "POST":
        article_content = request.form["content"].strip()
        article = Article(
            title=request.form["title"],
            source=request.form["source"],
            content=extract_full_words(article_content)
        )
        db.session.add(article)
        db.session.commit()

        word_counts = extract_words(article_content)

        for (word_text, pos), count in word_counts.items():
            word = (Word.query
                .join(WordForm)
                .filter(WordForm.form == word_text)
                .first()
                )

            if not word:
                continue
            
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

@app.route("/articles", methods=["GET"])
def get_article_list():
    article_list = Article.query.all()
    return render_template("article_list.html", article_list=article_list)


@app.route("/article/<int:article_id>", methods=["GET"])
def get_article(article_id):
    article= Article.query.fiter_by(id=article_id).all()
    return render_template("article_detail.html", article=article)