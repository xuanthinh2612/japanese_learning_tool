from flask import render_template, request, redirect
from app import app, db
from models import Article, Word, WordOccurrence, User, LearningItem
from helper import extract_words
from flask import g, session


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

@app.route("/my_learning")
def my_learning():
    if g.user is None:
        flash("Vui lòng đăng nhập")
        return redirect("/login")

    items = LearningItem.query.filter_by(user_id=g.user.id).join(Word).all()
    return render_template("my_learning.html", items=items)


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

    allowed = ["learning", "reviewing", "mastered", "dropped"]
    if new_status not in allowed:
        return {"message": "Trạng thái không hợp lệ", "success": False}

    item.status = new_status
    db.session.commit()

    return {
        "message": f"Đã chuyển trạng thái → {new_status}",
        "success": True
    }


@app.route("/top-words")
def top_words():
    words_data = []
    for w, freq, word_id in (
        db.session.query(
            Word.word,
            db.func.sum(WordOccurrence.count).label("freq"),
            Word.id
        )
        .join(WordOccurrence)
        .group_by(Word.id, Word.word)
        .order_by(db.desc("freq"))
        .limit(5000)
        .all()
    ):
        li_status = None
        if g.user:
            item = LearningItem.query.filter_by(user_id=g.user.id, word_id=word_id).first()
            li_status = item.status if item else None
        words_data.append((w, freq, word_id, li_status))

    return render_template("top_words.html", words=words_data)

