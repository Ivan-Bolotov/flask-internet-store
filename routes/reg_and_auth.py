from flask import Blueprint, request, make_response, jsonify, redirect
from flask_jwt_simple import create_jwt
import flask_bcrypt as bcrypt

from data.db_session import create_session
from data.users import User


blueprint = Blueprint(
    "registration_and_authorisation",
    __name__,
    template_folder="templates"
)

counter_for_unique_avatar_name = 1_000_000


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    match request.method:
        case "GET":
            pass  # TODO: возвращаем страницу регистрации с формой
        case "POST":
            data: dict[str, str | None] = request.form.to_dict()

            if not data.get("login").strip() or not data.get("password").strip():
                pass  # TODO: возвращаем эту же страницу с ошибкой ввода
                # return make_response(jsonify({"error": "Missing fields (login and password)"}), 400)

            # сохраняем аватарку, если есть
            if avatar := data.get("avatar").strip():
                global counter_for_unique_avatar_name

                counter_for_unique_avatar_name += 1
                c = counter_for_unique_avatar_name

                request.files["avatar"].save(filename := f"/db/avatars{c}_img_{avatar}")
                data["avatar"] = filename
            else:
                data["avatar"] = None

            userdata = {
                "username": data.get("login"),
                "password": bcrypt.generate_password_hash
                (data.get("password")).decode("utf-8"),
                "about": data.get("about"),
                "email": data.get("email"),
            }

            if data["avatar"] is not None:
                userdata["avatar"] = data["avatar"]

            # создаём нового пользователя
            new_user = User(**userdata)

            db_session = create_session()
            db_session.add(new_user)  # добавляем нового пользователя
            db_session.commit()

            return redirect(location="/login")  # редиректим на строницу авторизации


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    match request.method:
        case "GET":
            pass  # TODO: возвращаем страницу авторизации с формой
        case "POST":
            data: dict = request.form.to_dict()

            if data.get("login") is None or data.get("password") is None:
                pass  # TODO: возвращаем эту же страницу с ошибкой ввода
                # return make_response(jsonify({"error": "Missing fields (login and password)"}), 400)

            db_session = create_session()
            user = db_session.query(User).filter(User.username == data.get("login")).first()
            if user is None:
                pass  # TODO: страница ошибки авторизации
                # return make_response(jsonify({"error": "There is no such a user"}), 401)

            if not bcrypt.check_password_hash(user.password, data.get("password")):
                pass  # TODO: страница ошибки ввода пароля (один тип страницы ошибок)
                # return make_response(jsonify({"error": "Wrong password"}), 401)

            # данные, которые будем хранить в JWT-токене
            user_jwt_data = {
                "id": user.id,
                "login": user.username
            }

            # TODO: редиректим на главную, но с JWT-токеном
            # return make_response(jsonify({"token": create_jwt(identity=user_jwt_data)}), 200)
