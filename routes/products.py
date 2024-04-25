from flask import Blueprint, request, make_response, jsonify

from data.db_session import create_session
from data.products import Product


blueprint = Blueprint(
    "products",
    __name__,
    template_folder="templates"
)


@blueprint.route("/all_products", methods=["GET"])
def get_all_products():
    db_session = create_session()
    products = db_session.query(Product).all()

    # TODO: страница со всеми продуктами (одна страница для всех роутов)
    return make_response(jsonify({"products": products}), 200)


@blueprint.route("/products_by_data", methods=["GET"])
def login():
    all_found_products = []

    keywords = request.args.get("data").strip(",.;:").split()
    db_session = create_session()

    # добавляем найденные товары
    for keyword in keywords:
        rows = db_session.query(Product).filter(Product.name.like(f"%{keyword}%")).all()
        all_found_products.extend(rows)

    # TODO: страница со всеми найденными продуктами (одна страница для всех роутов)
    return make_response(jsonify({"products": all_found_products}), 200)
