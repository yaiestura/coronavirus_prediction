from flask import render_template, request, Blueprint
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('landing/landing.html')

@main.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html')

@main.route("/test", methods=['GET', 'POST'])
@login_required
def test():
    return render_template('test.html')

@main.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')
