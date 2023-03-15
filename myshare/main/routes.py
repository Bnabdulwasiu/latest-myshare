from flask import render_template, request, Blueprint
from myshare.models import Link
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
@login_required
def home():
    page = request.args.get("page", 1, type=int)
    links = Link.query.order_by(Link.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", links=links)

@main.route("/about")
def about():
    return render_template("about.html", title="About")
