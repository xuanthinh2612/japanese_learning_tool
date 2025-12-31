from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:1010@localhost/japanese_vocab"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --- Secret key để session/flash ---
app.secret_key = "secret-key"  # ⚡ Thay bằng chuỗi dài và khó đoán

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # <<< Dùng để chạy migration

from controllers import *
from models import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
