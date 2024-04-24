from datetime import timedelta

from flask import Flask, render_template
from flask_bcrypt import Bcrypt
import flask_jwt_simple as jwt

from data import db_session
from routes import reg_and_auth

app = Flask(__name__)

app.bcrypt = Bcrypt()

app.config["JWT_SECRET_KEY"] = "secret-key"
app.config["JWT_EXPIRES"] = timedelta(hours=24)
app.config["JWT_IDENTITY_CLAIM"] = "username"
app.config["JWT_HEADER_NAME"] = "token"
app.jwt = jwt.JWTManager(app)


@app.route("/")
def index():
    context = dict()
    context["amount_of_community_users"] = 25
    context["amount_of_total_items"] = 100
    return render_template("index.html", **context)


if __name__ == '__main__':
    # Подключение к БД
    db_session.global_init("db/main_db.db")

    # Маршрутизация
    app.register_blueprint(reg_and_auth.blueprint)

    # Запуск
    app.run(host="0.0.0.0", port=8080, debug=True)
