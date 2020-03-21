from flask import render_template, request, Blueprint, jsonify
from flask_login import login_required, current_user

from app.views.main.main import *

from app.views.users.routes import users

import requests

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('landing/landing.html')


@main.route("/live", methods=['GET', 'POST'])
@login_required
def monitor():

    url = 'https://media-cdn.factba.se/rss/json/coronavirus.json'

    r = requests.get(url=url)
    data = r.json()

    metrics = data['world']
    countries = sorted(data['countries'], key=lambda item: (data['countries'][item]['cases']), reverse=True)
    countries = [data['countries'][item] for item in countries if data['countries'][item]['iso3166-2']]

    cases = CasesDataParser()
    cases_data = cases.get_cases()

    return render_template('dashboard/coronavirus/monitor.html', metrics=metrics, countries=countries,
                           username=current_user.username, avatar=current_user.image_file, cases=cases_data)


@main.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    countries_adv = CountriesAdvDataParser()
    deaths = DeathsDataParser()
    demographics = DemographicsDataParser()
    updates = UpdatesDataParser()
    tests = TestsDataParser()

    countries_data = countries_adv.get_countries()
    deaths_data = deaths.get_deaths()
    demographics_data = demographics.get_demographics()
    updates_data = updates.get_updates()
    tests_data = tests.get_testing()
    print(tests_data)

    return render_template('dashboard/coronavirus/dashboard.html', data=updates_data, username=current_user.username,
                           avatar=current_user.image_file, demographics=demographics_data, deaths=deaths_data,
                           countries=countries_data, tests=tests_data)


@main.route("/news", methods=['GET', 'POST'])
@login_required
def news():
    news = NewsDataParser()
    news_data = news.get_news_updates()

    return render_template('dashboard/coronavirus/news.html', news=news_data['news'], updated=news_data['last_updated'], 
                            username=current_user.username, avatar=current_user.image_file,)


@main.route("/countries", methods=['GET', 'POST'])
@login_required
def countries():
    countries = CountriesAdvDataParser()
    countries_data = countries.get_countries()

    return render_template('dashboard/coronavirus/countries.html', countries=countries_data, username=current_user.username,
                           avatar=current_user.image_file,)


@main.route("/countries/<string:country>", methods=['GET', 'POST'])
@login_required
def single_country(country):
    country_data = SingleCountryParser()
    data = country_data.get_country_data(country)

    population_data = {
        "China": { 'population': '1,439,323,776', 'density': 153, 'land': '9,388,211' },
        "South Korea": { 'population': '51,269,185', 'density': 527, 'land': '97,230' },
        "United States": { 'population': '331,002,651', 'density': 36, 'land': '9,147,420' },
        "United Kingdom": { 'population': '67,886,011', 'density': 281, 'land': '241,930' },
        "Iran": { 'population': '83,992,949', 'density': 52, 'land': '1,628,550' },
        "Italy": { 'population': '60,461,826', 'density': 206, 'land': '294,140' },
        "France": { 'population': '65,273,511', 'density': 119, 'land': '547,557' },
        "Spain": { 'population': '46,754,778', 'density': 94, 'land': '498,800' },
        "Germany": { 'population': '83,783,942', 'density': 153, 'land': '348,560' },
        "Canada": { 'population': '37,742,154', 'density': 4, 'land': '9,093,510' },
        "Australia": { 'population': '25,499,884', 'density': 3, 'land': '7,682,300' },
        "Switzerland": { 'population': '8,654,622', 'density': 219, 'land': '39,516' },

    }

    return render_template('dashboard/coronavirus/country.html', data=data, population=population_data,
                           username=current_user.username, avatar=current_user.image_file)

@main.route('/maps')
@login_required
def maps():
    return render_template('dashboard/coronavirus/maps.html', username=current_user.username, avatar=current_user.image_file,)


@main.route("/predictions", methods=['GET', 'POST'])
@login_required
def predictions():
    deaths_predicted = start('deaths', 10, train=False)
    cases_predicted = start('cases', 10, train=False)
    print(cases_predicted)
    return render_template('dashboard/coronavirus/predictions.html', deaths=deaths_predicted, cases=cases_predicted,
                           username=current_user.username, avatar=current_user.image_file,)


@main.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')


@main.route("/api/predict/deaths", methods=['GET', 'POST'])
@login_required
def test_deaths():
    cases = start('deaths', 10, train=True)
    return jsonify(cases)


@main.route("/api/predict/cases", methods=['GET', 'POST'])
@login_required
def test_cases():
    cases = start('cases', 10, train=True)
    return jsonify(cases)


@main.route('/api/csse/data')
def csse_data():
    confirmed = get_data('confirmed')
    deaths    = get_data('deaths')
    recovered = get_data('recovered')

    return jsonify({
        'confirmed': confirmed,
        'deaths':    deaths,
        'recovered': recovered,
    })


@main.route("/api/deaths", methods=['GET', 'POST'])
@login_required
def api_deaths():
    deaths = DeathsDataParser()
    return jsonify(deaths.get_deaths())


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


@main.route("/api/news", methods=['GET', 'POST'])
@login_required
def api_news():
    news = NewsDataParser()
    return jsonify(news.get_news_updates())


@main.route("/api/demographics", methods=['GET', 'POST'])
@login_required
def api_demographics():
    demographics = DemographicsDataParser()
    return jsonify(demographics.get_demographics())


@main.route("/api/cases", methods=['GET', 'POST'])
@login_required
def api_cases():
    cases = CasesDataParser()
    return jsonify(cases.get_cases())


@main.route("/api/tests", methods=['GET', 'POST'])
@login_required
def api_tests():
    tests = TestsDataParser()
    return jsonify(tests.get_testing())


@main.route("/api/countries/<string:country>", methods=['GET', 'POST'])
@login_required
def api_single_country(country):
    country_data = SingleCountryParser()
    return jsonify(country_data.get_country_data(country))
