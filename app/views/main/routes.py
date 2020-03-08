from flask import render_template, request, Blueprint, jsonify
from flask_login import login_required, current_user

from app.views.main.main import *
from app.views.users.routes import users

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('landing/landing.html')


@main.route("/dashboard", methods=['GET', 'POST'])
# @login_required
def dashboard():
    countries_min = CountriesMinDataParser()
    deaths = DeathsDataParser()
    demographics = DemographicsDataParser()
    updates = UpdatesDataParser()

    countries_data = countries_min.get_countries()
    deaths_data = deaths.get_deaths()
    demographics_data = demographics.get_demographics()
    updates_data = updates.get_updates()

    return render_template('dashboard/coronavirus/dashboard.html', data=updates_data, username=current_user.username,
                           avatar=current_user.image_file, demographics=demographics_data, deaths=deaths_data, countries=countries_data)


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
    print(countries_data)

    return render_template('dashboard/coronavirus/countries.html', countries=countries_data, username=current_user.username,
                           avatar=current_user.image_file,)


@main.route('/maps')
def maps():
    return render_template('dashboard/coronavirus/maps.html', username=current_user.username, avatar=current_user.image_file,)


@main.route("/predictions", methods=['GET', 'POST'])
@login_required
def coronavirus_predictions():
    deaths_predicted = start('deaths', 10, train=False)
    cases_predicted = start('cases', 10, train=False)
    return render_template('dashboard/coronavirus/predictions.html', deaths=deaths_predicted, cases=cases_predicted,
                           username=current_user.username, avatar=current_user.image_file,)


@main.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')


@main.route("/test", methods=['GET', 'POST'])
@login_required
def test():
    return render_template('test.html')


@main.route("/api/predict/deaths", methods=['GET', 'POST'])
@login_required
def test_deaths():
    cases = start('deaths', 10, train=False)
    return jsonify(cases)


@main.route("/api/predict/cases", methods=['GET', 'POST'])
@login_required
def test_cases():
    cases = start('cases', 10, train=False)
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
