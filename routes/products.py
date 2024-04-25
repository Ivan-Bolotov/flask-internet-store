from flask import Blueprint, request, render_template

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

    return render_template("products.html", products=products)


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
    return render_template("products.html", products=all_found_products)
