from flask import render_template, request, redirect
from app import app, db
from models import User, Kanji, UserKanji
from controllers.helper import extract_words
from flask import g, session, jsonify
from sqlalchemy import case


message = {"searched": "Đã tra", "added": "Đã thêm", "learning": "Đang học", "reviewing": "Đang ôn tập", "mastered": "Đã thuộc", "dropped": "Đã bỏ"}
allowed = ["added", "learning", "reviewing", "mastered", "dropped"]

@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = User.query.get(user_id) if user_id else None


@app.route("/kanji", methods=["GET"])
def get_all_kanji():
    page = request.args.get("page", 1, type=int)
    per_page = 10   # 60 kanji / page (hợp lý cho grid)

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
    user_kanji = None
    if g.user:
        user_kanji = UserKanji.query.filter_by(user_id=g.user.id, kanji_id=kanji_id).first()

    if user_kanji:
        btn_data = {
            'disabled_flg': user_kanji.status in allowed,
            'display_text': message[user_kanji.status]
            }
    else:
        btn_data = {
            'disabled_flg': False,
            'display_text': "⭐ Thêm vào danh sách học"
            }

    return render_template(
        "kanji_detail.html",
        kanji=kanji,
        none_display_flg=True,
        btn_data=btn_data
    )


@app.route("/api/add-kanji/<int:kanji_id>", methods=["POST"])
def add_kanji(kanji_id):
    if g.user is None:
        return {"message": "Vui lòng đăng nhập", "success": False}, 401

    user_kanji = UserKanji.query.filter_by(user_id=g.user.id, kanji_id=kanji_id).first()

    if user_kanji:
        return {"message": "đã có trong danh sách", "success": False}

    item = UserKanji(
        user_id=g.user.id,
        kanji_id=kanji_id,
        status="added"
    )
    
    db.session.add(item)
    db.session.commit()

    return {"message": "Đã thêm vào danh sách", "success": True, "item_id": item.id}


# API to extract kanji from text
@app.route("/api/kanji", methods=["GET"])
def api_get_all_kanji():
    page = request.args.get("page", 1, type=int)
    per_page = 60  # 60 Kanji mỗi trang (có thể điều chỉnh tùy theo yêu cầu)

    pagination = Kanji.query.order_by(
        case((Kanji.frequency == None, 1), else_=0),
        Kanji.frequency.asc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    kanji_list = [
        {
            "id": kanji.id,
            "character": kanji.character,
            "level": kanji.level,
            "hanviet": kanji.hanviet,
            "meaning_vi": kanji.meaning_vi,
            "onyomi": kanji.onyomi,
            "kunyomi": kanji.kunyomi,
            "frequency": kanji.frequency
        }
        for kanji in pagination.items
    ]

    return jsonify({
        "kanji_list": kanji_list,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    })


@app.route("/api/kanji/<int:kanji_id>", methods=["GET"])
def api_kanji_detail(kanji_id):
    kanji = Kanji.query.get_or_404(kanji_id)
    user_kanji = None
    if g.user:
        user_kanji = UserKanji.query.filter_by(user_id=g.user.id, kanji_id=kanji_id).first()

    if user_kanji:
        btn_data = {
            'disabled_flg': user_kanji.status in allowed,
            'display_text': message[user_kanji.status]
        }
    else:
        btn_data = {
            'disabled_flg': False,
            'display_text': "⭐ Thêm vào danh sách học"
        }

    kanji_detail = {
        "id": kanji.id,
        "character": kanji.character,
        "onyomi": kanji.onyomi,
        "kunyomi": kanji.kunyomi,
        "meaning_vi": kanji.meaning_vi,
        "examples": kanji.examples.split(' ') if kanji.examples else [],
        "btn_data": btn_data
    }

    return jsonify(kanji_detail)
