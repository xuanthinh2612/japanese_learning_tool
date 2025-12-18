from flask import render_template, request, redirect
from app import app, db
from models import Article, Word, WordOccurrence, LearningItem, Grammar
from flask import g, session
from models import User
from services import run_import


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = User.query.get(user_id) if user_id else None


@app.route("/grammar")
def grammar_list():
    page = request.args.get("page", 1, type=int)
    per_page = 40

    pagination = Grammar.query.order_by(Grammar.level, Grammar.id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template(
        "grammar_list.html",
        grammar_list=pagination.items,
        pagination=pagination
    )


@app.route("/grammar/<int:grammar_id>")
def grammar_detail(grammar_id):
    grammar = Grammar.query.get_or_404(grammar_id)
    return render_template("grammar_detail.html", grammar=grammar)
