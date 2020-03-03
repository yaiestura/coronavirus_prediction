from flask import render_template, request, Blueprint, jsonify
from flask_login import login_required
from app.data_parser.data_parser import CasesDataGrabber, DeathsDataGrabber, UpdatesDataGrabber

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


@main.route("/test_deaths", methods=['GET', 'POST'])
@login_required
def test_deaths():
    cases = CasesDataGrabber()
    deaths = DeathsDataGrabber()
    return jsonify(deaths.get_deaths())


@main.route("/test_news", methods=['GET', 'POST'])
@login_required
def test_news():
    updates = UpdatesDataGrabber()
    return jsonify(updates.get_updates())


@main.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')
