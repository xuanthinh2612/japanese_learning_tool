from flask import render_template, request, redirect
from app import app, db
from models import Article, Word, WordOccurrence, User, LearningItem, Kanji
from controllers.helper import extract_words
from flask import g, session, jsonify
from sqlalchemy import case


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = User.query.get(user_id) if user_id else None


@app.route("/kanji", methods=["GET"])
def get_all_kanji():
    page = request.args.get("page", 1, type=int)
    per_page = 60   # 60 kanji / page (hợp lý cho grid)

    pagination = Kanji.query.order_by(
        case((Kanji.frequency == None, 1), else_=0),
        Kanji.frequency.asc()
        ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template(
        "list_kanji.html",
        Kanji_list=pagination.items,
        pagination=pagination
    )


@app.route("/kanji/<int:kanji_id>", methods=["GET"])
def kanji_detail(kanji_id):
    kanji = Kanji.query.get_or_404(kanji_id)

    return render_template(
        "kanji_detail.html",
        kanji=kanji,
        none_display_flg=True,
    )
