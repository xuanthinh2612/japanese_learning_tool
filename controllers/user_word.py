from flask import render_template, request, redirect
from app import app, db
from models import Article, Word, WordOccurrence, User, LearningItem
from controllers.helper import extract_words
from flask import g, session, jsonify


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


# Tra từ API
@app.route("/api/word/<word>", methods=["GET", "POST"])
def get_word(word):
    word_obj = Word.query.filter_by(word=word).first_or_404()  # tìm theo column 'word'
    examples = [{"sentence": e.sentence, "translation": e.translation} for e in word_obj.examples]
    return jsonify({
        "id": word_obj.id,
        "word": word_obj.word,
        "furigana": word_obj.furigana,
        "pos": word_obj.pos,
        "meanings": word_obj.meanings,
        "examples": examples
    })