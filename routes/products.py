from flask import Blueprint, request, render_template

from data.db_session import create_session
from data.products import Product
from routes.funcs.funcs import get_amount_of_users, get_amount_of_products

blueprint = Blueprint(
    "products",
    __name__,
    template_folder="templates"
)

context = dict()
context["amount_of_community_users"] = get_amount_of_users()
context["amount_of_total_items"] = get_amount_of_products()


@blueprint.route("/all_products", methods=["GET"])
def get_all_products():
    db_session = create_session()
    products = db_session.query(Product).all()

    return render_template("products.html", products=products, **context)


@blueprint.route("/products_by_data", methods=["GET"])
def products_by_data():
    all_found_products = []

    keywords = request.args.get("data").strip(",.;:").split()
    db_session = create_session()

    # добавляем найденные товары
    for keyword in keywords:
        rows = db_session.query(Product).filter(Product.name.like(f"%{keyword}%")).all()
        all_found_products.extend(rows)

    return render_template("products.html", products=all_found_products, **context)


@blueprint.route("/sneakers", methods=["GET"])
def get_sneakers_products():
    data = request.args.get("data")

    db_session = create_session()
    products = (db_session.query(Product)
                .filter(Product.category == "sneakers")
                .filter(Product.name.like(f"%{data}%")))

    return render_template("products.html", products=products, **context)


@blueprint.route("/rackets", methods=["GET"])
def get_rackets_products():
    data = request.args.get("data")

    db_session = create_session()
    products = (db_session.query(Product)
                .filter(Product.category == "rackets")
                .filter(Product.name.like(f"%{data}%")))

    return render_template("products.html", products=products, **context)


@blueprint.route("/balls", methods=["GET"])
def get_balls_products():
    data = request.args.get("data")

    db_session = create_session()
    products = (db_session.query(Product)
                .filter(Product.category == "balls")
                .filter(Product.name.like(f"%{data}%")))

    return render_template("products.html", products=products, **context)


@blueprint.route("/clothes", methods=["GET"])
def get_clothes_products():
    data = request.args.get("data")

    db_session = create_session()
    products = (db_session.query(Product)
                .filter(Product.category == "clothes")
                .filter(Product.name.like(f"%{data}%")))

    return render_template("products.html", products=products, **context)


@blueprint.route("/new", methods=["GET"])
def get_new_products():
    db_session = create_session()
    products = (db_session.query(Product)
                .filter(Product.tag == "new"))

    return render_template("products.html", products=products, **context)


@blueprint.route("/popular", methods=["GET"])
def get_popular_products():
    db_session = create_session()
    products = (db_session.query(Product)
                .filter(Product.tag == "popular"))

    return render_template("products.html", products=products, **context)
