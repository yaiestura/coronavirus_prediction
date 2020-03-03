from flask import render_template, request, Blueprint, jsonify
from flask_login import login_required

from app.data_parser.data_parser import ( CasesDataParser, DeathsDataParser,
    UpdatesDataParser, CountriesDataParser, DemographicsDataParser )

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
    deaths = DeathsDataParser()
    return jsonify(deaths.get_deaths())


@main.route("/test_countries", methods=['GET', 'POST'])
@login_required
def test_countries():
    countries = CountriesDataParser()
    return jsonify(countries.get_countries())


@main.route("/test_news", methods=['GET', 'POST'])
@login_required
def test_news():
    updates = UpdatesDataParser()
    return jsonify(updates.get_updates())


@main.route("/test_demographics", methods=['GET', 'POST'])
@login_required
def test_demographics():
    demographics = DemographicsDataParser()
    return jsonify(demographics.get_demographics())


@main.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')
