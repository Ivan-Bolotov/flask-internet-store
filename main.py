from datetime import timedelta

from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_jwt_simple import JWTManager

from data import db_session
from routes import reg_and_auth

app = Flask(__name__)

app.bcrypt = Bcrypt()

app.config["JWT_SECRET_KEY"] = "secret-key"
app.config["JWT_EXPIRES"] = timedelta(hours=24)
app.config["JWT_IDENTITY_CLAIM"] = "username"
app.config["JWT_HEADER_NAME"] = "token"
app.jwt = JWTManager(app)


@app.route("/", methods=['POST'])
def index():
    # user = User()
    # user.name = "Пользователь 1"
    # user.about = "биография пользователя 1"
    # user.email = "email@email.ru"
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()

    context = dict()
    context["title"] = "Main Page"
    return render_template("topper.html", **context)


if __name__ == '__main__':
    # Подключение к БД
    db_session.global_init("db/main_db.db")

    # Маршрутизация
    app.register_blueprint(reg_and_auth.blueprint)

    # Запуск
    app.run(host="0.0.0.0", port=8080, debug=True)
