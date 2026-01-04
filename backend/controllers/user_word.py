from flask import render_template, request, redirect
from app import app, db
from models import Article, Word, WordOccurrence, User, LearningItem, WordForm, WordReading, WordSense
from controllers.helper import extract_words
from flask import g, session, jsonify, flash
from sqlalchemy.orm import joinedload
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity
)


message = {"searched": "Đã tra", "added": "Đã thêm", "learning": "Đang học", "reviewing": "Đang ôn tập", "mastered": "Đã thuộc", "dropped": "Đã bỏ"}
allowed = ["added", "learning", "reviewing", "mastered", "dropped"]


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
        return {"message": "Từ đã có trong danh sách", "success": False}

    item = LearningItem(
        user_id=g.user.id,
        word_id=word_id,
        status="added"
    )
    db.session.add(item)
    db.session.commit()

    return {"message": "Đã thêm vào danh sách", "success": True, "item_id": item.id}


@app.route("/update_learning_status/<int:word_id>", methods=["POST"])
def update_learning_status(word_id):
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
    
    if new_status not in allowed:
        return {"message": "Trạng thái không hợp lệ", "success": False}

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
    
    user_word = None
    if g.user:
        user_word = LearningItem.query.filter_by(user_id=g.user.id, word_id=word_obj.id).first()
    if user_word:
        btn_data = {
            'disabled_flg': user_word.status in allowed,
            'display_text': message[user_word.status]
            }
    else:
        btn_data = {
            'disabled_flg': False,
            'display_text': "⭐ Thêm vào danh sách học"
            }


    return render_template(
        "word_detail.html",
        word=word_obj,
        articles=articles,
        word_text=word,
        btn_data=btn_data
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
    

@app.route("/api/add_to_learning/<int:word_id>", methods=["POST"])
def api_add_to_learning(word_id):
    if g.user is None:
        return jsonify(
            {
                "success": False,
                "status": "error",
                "message": "Bạn chưa login"
             }
        ), 401

    item = LearningItem.query.filter_by(
        user_id=g.user.id,
        word_id=word_id
    ).first()

    if item:
        return jsonify(
            {
                "success": False,
                "status": "error",
                "message": "Từ đã có trong danh sách"
             }
        )

    item = LearningItem(
        user_id=g.user.id,
        word_id=word_id,
        status="added"
    )
    db.session.add(item)
    db.session.commit()

    return jsonify(
        {
            "success": True,
            "status": "ok",
            "message": "Đã thêm vào danh sách",
            "item_id": item.id
         }
    )


@app.route("/api/word-detail/<word_text>", methods=["GET"])
def api_word_detail(word_text):
    # 1. Lấy từ chính từ database
    word_obj = (
        Word.query
        .join(WordForm)
        .filter(WordForm.form == word_text)
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

    # 2. Lấy bài viết liên quan
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

    # 3. Kiểm tra trạng thái của từ trong danh sách học của người dùng
    user_word = None
    if g.user:
        user_word = LearningItem.query.filter_by(user_id=g.user.id, word_id=word_obj.id).first()
    if user_word:
        btn_data = {
            'disabled_flg': user_word.status in allowed,
            'display_text': message[user_word.status]
        }
    else:
        btn_data = {
            'disabled_flg': False,
            'display_text': "⭐ Thêm vào danh sách học"
        }

    # 4. Trả về dữ liệu dạng JSON
    return jsonify({
        'forms': [form.form for form in word_obj.forms],
        'readings': [reading.reading for reading in word_obj.readings],
        'senses': [
            {
                'pos': sense.pos,
                'meanings': {
                    'vi': [g.means_vi for g in sense.glosses if g.means_vi]
                },
                'examples': [{'sentence': ex.sentence, 'translation_vi': ex.translation_vi} for ex in sense.examples]
            } for sense in word_obj.senses
        ],
        'articles': [
            {
                'title': title,
                'source': source,
                'content': content,
                'count': count
            } for title, source, content, count in articles
        ],
        'btn_data': btn_data
    })
    

@app.route("/api/my-words", methods=["GET"])
@jwt_required()
def api_my_words():
    username = get_jwt_identity()

    if username is None:
        return jsonify(
            {
                "success": False,
                "status": "error",
                "message": "Bạn chưa login"
             }
        )

    user = User.query.filter_by(username=username).first()
    
    status = request.args.get("status", "learning")
    page = request.args.get("page", 1, type=int)
    per_page = 50
    pagination = (
        LearningItem.query
        .filter_by(user_id=user.id, status=status)
        .join(Word)
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    
    print(len(pagination.items))
    
    return jsonify({
        "success": True,
        "words": 
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
    
    
@app.route("/api/update-word-status/<int:word_id>", methods=["POST"])
@jwt_required()
def update_word_status(word_id):
    username = get_jwt_identity()
    
    if username is None:
        return {"message": "Vui lòng đăng nhập", "success": False}, 401

    user = User.query.filter_by(username=username).first()
    
    item = LearningItem.query.filter_by(
        user_id=user.id,
        word_id=word_id
    ).first()
        
    if not item:
        return {"message": "Từ chưa có trong danh sách học", "success": False}

    data = request.get_json()
    new_status = data.get("status")
    
    if new_status not in allowed:
        return {"message": "Trạng thái không hợp lệ", "success": False}

    item.status = new_status
    db.session.commit()

    return {
        "message": f"Đã thêm vào → {message.get(new_status)}",
        "success": True
    }
