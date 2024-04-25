from flask import Blueprint, request, make_response, jsonify, redirect, render_template
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
    context = dict()
    context["amount_of_community_users"] = 25
    context["amount_of_total_items"] = 100

    match request.method:
        case "GET":
            return render_template("register.html", **context)

        case "POST":
            data: dict[str, str | None] = request.form.to_dict()

            if not data.get("login").strip() or not data.get("password").strip():
                context["error"] = "Missing fields (login or password)"
                return render_template("register.html", **context)

            # сохраняем аватарку, если есть
            if avatar := request.files.get("avatar"):
                global counter_for_unique_avatar_name

                counter_for_unique_avatar_name += 1
                c = counter_for_unique_avatar_name

                request.files["avatar"].save(filename := f"./db/avatars/{c}_img_{avatar.filename}")
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
    context = dict()
    context["amount_of_community_users"] = 25
    context["amount_of_total_items"] = 100

    match request.method:
        case "GET":
            return render_template("login.html", **context)

        case "POST":
            data: dict = request.form.to_dict()

            if not data.get("login").strip() or not data.get("password").strip():
                context["error"] = "Missing fields (login or password)"
                return render_template("login.html", **context)

            db_session = create_session()
            user = db_session.query(User).filter(User.username == data.get("login")).first()
            if user is None:
                context["error"] = "User not found"
                return render_template("login.html", **context)

            if not bcrypt.check_password_hash(user.password, data.get("password")):
                context["error"] = "Incorrect password"
                return render_template("login.html", **context)

            # данные, которые будем хранить в JWT-токене
            user_jwt_data = {
                "id": user.id,
                "login": user.username
            }

            response = redirect("/")
            response.set_cookie("token", create_jwt(identity=user_jwt_data))

            return response
