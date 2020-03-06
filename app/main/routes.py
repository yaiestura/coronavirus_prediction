from flask import render_template, request, Blueprint, jsonify
from flask_login import login_required

from app.main.main import *

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('landing/landing.html')


@main.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():

    countries_min = CountriesMinDataParser()
    deaths = DeathsDataParser()
    demographics = DemographicsDataParser()
    updates = UpdatesDataParser()      

    countries_data = countries_min.get_countries()
    deaths_data = deaths.get_deaths()
    demographics_data = demographics.get_demographics()
    updates_data = updates.get_updates()

    return render_template('dashboard/coronavirus/dashboard.html', data=updates_data,
        demographics=demographics_data, deaths=deaths_data, countries=countries_data)


@main.route("/test", methods=['GET', 'POST'])
@login_required
def test():
    return render_template('test.html')


@main.route("/deaths", methods=['GET', 'POST'])
@login_required
def api_deaths():
    deaths = DeathsDataParser()
    return jsonify(deaths.get_deaths())


@main.route("/api/predict/cases", methods=['GET', 'POST'])
@login_required
def api_pred_cases():
    cases = start(10, train=False)
    return jsonify(cases)


@main.route("/api/countries_min", methods=['GET', 'POST'])
@login_required
def api_countries_min():
    countries = CountriesMinDataParser()
    return jsonify(countries.get_countries())


@main.route("/api/countries_adv", methods=['GET', 'POST'])
@login_required
def api_countries_adv():
    countries = CountriesAdvDataParser()
    return jsonify(countries.get_countries())



@main.route("/api/updates", methods=['GET', 'POST'])
@login_required
def api_updates():
    updates = UpdatesDataParser()
    return jsonify(updates.get_updates())


@main.route("/api/demographics", methods=['GET', 'POST'])
@login_required
def api_demographics():
    demographics = DemographicsDataParser()
    return jsonify(demographics.get_demographics())


@main.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')
