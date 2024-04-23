from flask import Blueprint, request, make_response, jsonify
import flask_bcrypt as bcrypt

from data.db_session import create_session
from data.users import User

blueprint = Blueprint(
    "registration_and_authorisation",
    __name__,
    template_folder="templates"
)


@blueprint.route("/register", methods=["POST"])
def register():
    json_data: dict = request.json
    if json_data.get("login") is None or json_data.get("password") is None:
        return make_response(jsonify({"error": "Missing fields (login and password)"}), 400)

    new_user = User(username=json_data.get("login"),
                    password=bcrypt.generate_password_hash
                    (json_data.get("password")).decode("utf-8"))

    db_session = create_session()
    db_session.add(new_user)
    db_session.commit()

    return make_response(jsonify({"result": "OK"}), 200)


@blueprint.route("/login", methods=["POST"])
def login():
    json_data: dict = request.json
    if json_data.get("login") is None or json_data.get("password") is None:
        return make_response(jsonify({"error": "Missing fields (login and password)"}), 400)

    new_user = User(username=json_data.get("login"),
                    password=json_data.get("password"))

    db_session = create_session()
    db_session.add(new_user)
    db_session.commit()

    print(json_data)
    return make_response(jsonify({"result": "OK"}), 200)


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@blueprint.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({"error": "Bad Request"}), 400)
