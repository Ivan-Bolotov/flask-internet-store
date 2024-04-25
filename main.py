from datetime import timedelta

from flask import Flask, render_template, make_response
from flask_bcrypt import Bcrypt
import flask_jwt_simple as jwt

from data import db_session
from routes import reg_and_auth, products, about
from routes.funcs.funcs import get_amount_of_users, get_amount_of_products

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
    context["amount_of_community_users"] = get_amount_of_users()
    context["amount_of_total_items"] = get_amount_of_products()
    return render_template("index.html", **context)


@app.errorhandler(404)
def not_found(_):
    context = dict()
    context["amount_of_community_users"] = 25
    context["amount_of_total_items"] = 100

    return make_response(render_template("errors/404.html", **context), 404)


if __name__ == '__main__':
    # Подключение к БД
    db_session.global_init("db/main_db.db")

    # Маршрутизация
    app.register_blueprint(reg_and_auth.blueprint)
    app.register_blueprint(products.blueprint)
    app.register_blueprint(about.blueprint)

    # Запуск
    app.run(host="0.0.0.0", port=8080, debug=True)
