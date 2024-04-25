from flask import Blueprint, render_template


blueprint = Blueprint(
    "about",
    __name__,
    template_folder="templates"
)


@blueprint.route("/about", methods=["GET"])
def about():
    context = dict()
    context["amount_of_community_users"] = 25
    context["amount_of_total_items"] = 100

    return render_template("about.html", **context)
