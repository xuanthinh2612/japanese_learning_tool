from flask import render_template, request, redirect, jsonify, flash
from app import app, db
from models import Grammar, UserGrammar
from flask import g, session
from models import User
from services import run_import


message = {"searched": "Đã tra", "added": "Đã thêm", "learning": "Đang học", "reviewing": "Đang ôn tập", "mastered": "Đã thuộc", "dropped": "Đã bỏ"}
allowed = ["added", "learning", "reviewing", "mastered", "dropped"]

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
    
    user_grammar = None
    if g.user:
        user_grammar = UserGrammar.query.filter_by(user_id=g.user.id, grammar_id=grammar_id).first()
    if user_grammar:
        btn_data = {
            'disabled_flg': user_grammar.status in allowed,
            'display_text': message[user_grammar.status]
            }
    else:
        btn_data = {
            'disabled_flg': False,
            'display_text': "⭐ Thêm vào danh sách học"
            }

    return render_template("grammar_detail.html", 
                           grammar=grammar,
                           none_display_flg=True,
                           btn_data=btn_data)


@app.route("/api/add-grammar/<int:grammar_id>", methods=["POST"])
def add_grammar(grammar_id):
    if g.user is None:
        return {"message": "Vui lòng đăng nhập", "success": False}, 401

    user_grammar = UserGrammar.query.filter_by(user_id=g.user.id, grammar_id=grammar_id).first()

    if user_grammar:
        return {"message": "đã có trong danh sách", "success": False}

    item = UserGrammar(
        user_id=g.user.id,
        grammar_id=grammar_id,
        status="added"
    )
    
    db.session.add(item)
    db.session.commit()

    return {"message": "Đã thêm vào danh sách", "success": True, "item_id": item.id}

# API endpoints
@app.route("/api/grammar", methods=["GET"])
def get_grammar_list():
    page = request.args.get("page", 1, type=int)
    per_page = 60

    pagination = Grammar.query.order_by(Grammar.level, Grammar.id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    result = [{"id": g.id, "pattern": g.pattern, "meaning": g.meaning, "level": g.level} for g in pagination.items]
    return jsonify({"grammar_list": result, "pagination": {"pages": pagination.pages, "current_page": pagination.page}})

@app.route("/api/grammar/<int:grammar_id>", methods=["GET"])
def get_grammar_detail(grammar_id):
    grammar = Grammar.query.get_or_404(grammar_id)
    
    user_grammar = None
    if g.user:
        user_grammar = UserGrammar.query.filter_by(user_id=g.user.id, grammar_id=grammar_id).first()

    if user_grammar:
        btn_data = {
            'disabled_flg': user_grammar.status in allowed,
            'display_text': message[user_grammar.status]
        }
    else:
        btn_data = {
            'disabled_flg': False,
            'display_text': "⭐ Thêm vào danh sách học"
        }

    grammar_data = {
        "id": grammar.id,
        "pattern": grammar.pattern,
        "meaning": grammar.meaning,
        "level": grammar.level,
        "usages": [
            {
                "pattern": usage.pattern,
                "meaning": usage.meaning,
                "explanation": usage.explanation,
                "examples": [{"sentence": ex.sentence, "furigana": ex.furigana, "translation": ex.translation} for ex in usage.examples]
            }
            for usage in grammar.usages
        ]
    }

    return jsonify({"grammar": grammar_data, "btn_data": btn_data})

# @app.route("/api/add-grammar/<int:grammar_id>", methods=["POST"])
# def add_grammar(grammar_id):
#     if g.user is None:
#         return jsonify({"message": "Vui lòng đăng nhập", "success": False}), 401

#     user_grammar = UserGrammar.query.filter_by(user_id=g.user.id, grammar_id=grammar_id).first()

#     if user_grammar:
#         return jsonify({"message": "Đã có trong danh sách", "success": False})

#     item = UserGrammar(
#         user_id=g.user.id,
#         grammar_id=grammar_id,
#         status="added"
#     )
    
#     db.session.add(item)
#     db.session.commit()

#     return jsonify({"message": "Đã thêm vào danh sách", "success": True, "item_id": item.id})

