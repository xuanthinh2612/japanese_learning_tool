from flask import render_template, request, redirect
from app import app, db
from models import Article, Word, WordOccurrence, User, LearningItem, WordForm, WordReading, WordSense
from controllers.helper import extract_words
from flask import g, session, jsonify, flash
from sqlalchemy.orm import joinedload


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = User.query.get(user_id) if user_id else None


@app.route("/add_to_learning/<int:word_id>", methods=["POST"])
def add_to_learning(word_id):
    if g.user is None:
        return {"message": "Vui lòng đăng nhập", "success": False}, 401

    item = LearningItem.query.filter_by(
        user_id=g.user.id,
        word_id=word_id
    ).first()

    if item:
        return {"message": "Từ đã có trong danh sách học", "success": False}

    item = LearningItem(
        user_id=g.user.id,
        word_id=word_id,
        status="learning"
    )
    db.session.add(item)
    db.session.commit()

    return {"message": "Đã thêm vào danh sách học", "success": True, "item_id": item.id}


@app.route("/update_learning_status/<int:word_id>", methods=["POST"])
def update_learning_status(word_id):
    message = {"learning": "Đang học", "reviewing": "Đang học", "mastered": "Đã thuộc", "dropped": "Đã bỏ"}
    if g.user is None:
        return {"message": "Vui lòng đăng nhập", "success": False}, 401

    item = LearningItem.query.filter_by(
        user_id=g.user.id,
        word_id=word_id
    ).first()
        
    if not item:
        return {"message": "Từ chưa có trong danh sách học", "success": False}

    data = request.get_json()
    new_status = data.get("status")

    print(new_status)
    
    allowed = ["learning", "reviewing", "mastered", "dropped"]
    if new_status not in allowed:
        return {"message": "Trạng thái không hợp lệ", "success": False}


    print(new_status)
    item.status = new_status
    db.session.commit()

    return {
        "message": f"Đã thêm vào → {message.get(new_status)}",
        "success": True
    }


@app.route("/word/<word>")
def word_detail(word):
    # 1. Lấy word chính
    word_obj = (
        Word.query
        .join(WordForm)
        .filter(WordForm.form == word)
        .options(
            joinedload(Word.forms),
            joinedload(Word.readings),
            joinedload(Word.senses)
                .joinedload(WordSense.glosses),
            joinedload(Word.senses)
                .joinedload(WordSense.examples),
        )
        .first_or_404()
    )

    # 2. Lấy article context
    articles = (
        db.session.query(
            Article.title,
            Article.source,
            Article.content,
            WordOccurrence.count
        )
        .join(WordOccurrence)
        .filter(WordOccurrence.word_id == word_obj.id)
        .limit(1)
        .all()
    )

    return render_template(
        "word_detail.html",
        word=word_obj,
        articles=articles,
        word_text=word
    )


# API Search 
@app.route("/api/word/<keyword>", methods=["GET"])
def get_word(keyword):
    from sqlalchemy import or_

    word_obj = (
        Word.query
        .outerjoin(WordForm)
        .outerjoin(WordReading)
        .filter(
            or_(
                WordForm.form == keyword,
                WordReading.reading == keyword
            )
        )
        .first_or_404()
    )

    # forms
    forms = [f.form for f in word_obj.forms]

    # readings
    readings = [r.reading for r in word_obj.readings]

    # senses
    senses = []
    for s in word_obj.senses:
        senses.append({
            "pos": s.pos,
            "misc": s.misc,
            "antonym": s.antonym,
            "xref": s.xref,
            "meanings": {
                "en": [g.means_en for g in s.glosses if g.means_en],
                "vi": [g.means_vi for g in s.glosses if g.means_vi],
            },
            "examples": [
                {
                    "sentence": e.sentence,
                    "translation_en": e.translation_en,
                    "translation_vi": e.translation_vi
                }
                for e in s.examples
            ]
        })

    return jsonify({
        "id": word_obj.id,
        "ent_seq": word_obj.ent_seq,
        "forms": forms,
        "readings": readings,
        "senses": senses
    })


@app.route("/api/my_learning")
def api_my_learning():
    
    if g.user is None:
        return jsonify(
            {
                "success": False,
                "status": "error",
                "message": "Bạn chưa login"
             }
        )

    status = request.args.get("status", "learning")
    page = request.args.get("page", 1, type=int)
    per_page = 50
    pagination = (
        LearningItem.query
        .filter_by(user_id=g.user.id, status=status)
        .join(Word)
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    
    return jsonify({
        "success": True,
        "data": 
            [
            {
                "word_id": i.word.id,
                "status": i.status,
                "word": i.word.forms[0].form,
            }
            for i in pagination.items
            ],
            "pagination": {
                "page": pagination.page,
                "pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
                "total": pagination.total
            }
        })