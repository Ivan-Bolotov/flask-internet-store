from flask import Blueprint, render_template
from routes.funcs.funcs import *


blueprint = Blueprint(
    "about",
    __name__,
    template_folder="templates"
)


@blueprint.route("/about", methods=["GET"])
def about():
    context = dict()
    context["amount_of_community_users"] = get_amount_of_users()
    context["amount_of_total_items"] = get_amount_of_products()

    return render_template("about.html", **context)
