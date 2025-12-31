from flask import session, flash, render_template, request, redirect, jsonify
from app import app, db
from models import Article, Word, WordOccurrence, User
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Username đã tồn tại")
            return redirect("/register")

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        flash("Đăng ký thành công!")
        return redirect("/login")
    return render_template("register.html")


@app.route("/api/login", methods=["POST"])
def login_api():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    
    print(username)
    print(password)
    if not user or not user.check_password(password):
        print("sai mk")
        return jsonify({"msg": "Sai tài khoản hoặc mật khẩu"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route("/api/profile", methods=["GET"])
@jwt_required()
def profile():
    user = get_jwt_identity()
    return jsonify(user=user)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Đã đăng xuất")
    return redirect("/")
