from flask import session, flash, render_template, request, redirect
from app import app, db
from models import Article, Word, WordOccurrence, User


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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            flash("Đăng nhập thành công!")
            return redirect("/")
        flash("Sai username hoặc password")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Đã đăng xuất")
    return redirect("/")
