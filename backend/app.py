from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_cors import CORS


app = Flask(__name__)
CORS(app) # Thêm cho JWT

app.config["JWT_SECRET_KEY"] = "super-secret-key" # Thêm cho JWT
jwt = JWTManager(app) # Thêm cho JWT

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
