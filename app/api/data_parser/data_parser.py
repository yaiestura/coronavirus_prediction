from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import requests
import json
import math
import csv
import re


class DataParser:
    BASE_URL = 'https://www.worldometers.info/coronavirus'

    @staticmethod
    def save_data_to_file(filename, data):
        data_to_save = []

        for i in range(0, len(data)):
            data_to_save.append([i, data[i]])

        with open('datasets/' + filename, 'w', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerows(data_to_save)

    @staticmethod
    def get_dataset_file_name(dataset_prefix, dataset_date=''):
        filename = dataset_prefix + '_dataset_'
        if dataset_date == '':
            filename += datetime.today().strftime('%Y-%m-%d')
        else:
            filename += dataset_date

        filename += '.csv'

        return filename

    @staticmethod
    def create_date_axis_forward(dataset):

        january = datetime(2020, 1, 22)
        date_list = [int(datetime.timestamp(january + timedelta(days=x)) * 1000) for x in range(len(dataset))]

        return list(date_list)

    @staticmethod
    def create_date_axis(dataset):

        yesterday = datetime.now() - timedelta(days=1)
        date_list = [int(datetime.timestamp(yesterday - timedelta(days=x)) * 1000) for x in range(len(dataset))]

        return date_list[::-1]

    def scrape_table(self):
        pass
        # rewrite method


class DeathsDataParser(DataParser):

    def __init__(self):
        super()

    @staticmethod
    def get_deaths():

        url = DataParser.BASE_URL + '/' + 'coronavirus-death-toll'
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        total_data, daily_data = [], []

        table_total = soup.select('.table-responsive')[0].find('table')
        table_body_total = table_total.find('tbody')

        total_rows = table_body_total.find_all('tr')

        for row in total_rows:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            total_data.append([value.replace(',', '') for value in columns])

        deaths_today = soup.select('.maincounter-number span')[0].text.strip().replace(',', '')
        today_date = re.sub(r'\d+', str(int(re.findall(r'\d+', total_data[0][0])[0]) + 1), total_data[0][0])
        deaths_diff = int(deaths_today) - int(total_data[0][1])
        deaths_growth = f'{math.floor(deaths_diff * 100 / int(deaths_today))}%'

        total_data.insert(0, [today_date, deaths_today, str(deaths_diff), deaths_growth])

        table_daily = soup.select('.table-responsive')[1].find('table')
        table_body_daily = table_daily.find('tbody')

        daily_rows = table_body_daily.find_all('tr')

        for row in daily_rows:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            daily_data.append([value.replace(',', '') for value in columns])

        return {'total_deaths': total_data, 'daily_deaths': daily_data}


class CountriesMinDataParser(DataParser):

    def __init__(self):
        super()

    @staticmethod
    def get_countries_minimal():

        url = DataParser.BASE_URL + '/' + 'countries-where-coronavirus-has-spread/'
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        table_countries = soup.select('.table-responsive')[0].find('table')
        table_body_countries = table_countries.find('tbody')

        rows_countries = table_body_countries.find_all('tr')

        data_countries = []

        for row in rows_countries:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            data_countries.append([value.replace(',', '') for value in columns])

        return data_countries

    def get_countries(self):
        return {'countries_min_data': self.get_countries_minimal(),
                'countries_affected': len(self.get_countries_minimal())}

class CountriesAdvDataParser(DataParser):

    def __init__(self):
        super()

    @staticmethod
    def get_countries_advanced():

        url = DataParser.BASE_URL + '/' + '#countries'
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        table_countries = soup.find('table', {'id': 'main_table_countries_today'})
        table_body_countries = table_countries.find('tbody')

        rows_countries = table_body_countries.find_all('tr')

        data_countries = []

        for row in rows_countries:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            data_countries.append([value.replace(',', '') for value in columns])
        return data_countries[:-1]

    def get_countries(self):
        return {'countries_adv_data': self.get_countries_advanced(),
                'countries_affected': len(self.get_countries_advanced())}


class UpdatesDataParser(DataParser):

    def __init__(self):
        super()

    @staticmethod
    def get_updates():
        url = DataParser.BASE_URL
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        cases_data = []

        statistics = soup.select('.maincounter-number')

        active_cases = soup.select('.panel-body')[0].find('div', {'class': 'panel_front'})
        closed_cases = soup.select('.panel-body')[1].find('div', {'class': 'panel_front'})
        active_conditions = soup.select('.panel-body')[0].find_all('span', {'class': 'number-table'})

        active_plot_data = soup.select('.panel-body')[0].find('script', type="text/javascript").text
        x_axis_act = list(json.loads(re.search(r'categories:(.+?)},yAxis', re.sub('\s+','',active_plot_data))[1]))
        y_axis_act = list(json.loads(re.search(r'data:(.+?)}', re.sub('\s+','',active_plot_data))[1]))

        closed_plot_data = soup.select('.panel-body')[1].find('script', type="text/javascript").text
        x_axis_cl = list(json.loads(re.search(r'categories:(.+?)},yAxis', re.sub('\s+','',closed_plot_data))[1]))
        y_axis_cl = re.findall(r'data:(.+?)}', re.sub('\s+','',closed_plot_data))

        cases_plot_data = soup.find('div', {'id': 'coronavirus-cases-log'}).find_next('script',
                                                                                      type="text/javascript").text
        x_axis_cases = list(json.loads(re.search(r'categories:(.+?)},yAxis', re.sub('\s+','',cases_plot_data))[1]))
        y_axis_cases = list(json.loads(re.search(r'data:(.+?)}', re.sub('\s+','',cases_plot_data))[1]))

        today_date = re.sub(r'\d+', str(int(re.findall(r'\d+', x_axis_cases[-1])[0]) + 1).zfill(2), x_axis_cases[-1])

        x_axis_cases.append(today_date)
        y_axis_cases.append(int(statistics[0].text.strip().replace(',', '')))

        return {'total_cases': statistics[0].text.strip().replace(',', ''),
                'total_deaths': statistics[1].text.strip().replace(',', ''),
                'total_recovered': statistics[2].text.strip().replace(',', ''),
                'active_cases': active_cases.find('div', {'class': 'number-table-main'}).text.strip().replace(',', ''),
                'closed_cases': closed_cases.find('div', {'class': 'number-table-main'}).text.strip().replace(',', ''),
                'mild_condition': active_conditions[0].text.strip().replace(',', ''),
                'critical_condition': active_conditions[1].text.strip().replace(',', ''),
                'cases_plot': [x_axis_cases, y_axis_cases],
                'active_cases_plot': [x_axis_act, y_axis_act],
                'closed_cases_plot': [x_axis_cl,
                                      list(json.loads(y_axis_cl[0])),
                                      list(json.loads(y_axis_cl[1]))
                                      ],
                'last_updated': soup.find('div', {'id': 'page-top'}).find_next('div').text }


class CasesDataParser(DataParser):

    def __init__(self):
        super()

    @staticmethod
    def get_cases():
        url = DataParser.BASE_URL
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        cases_data = []

        statistics = soup.select('.maincounter-number')

        cases_plot_data = soup.find('div', {'id': 'coronavirus-cases-log'}).find_next('script',
                                                                                      type="text/javascript").text
        y_axis_cases = list(json.loads(re.search(r'data:(.+?)}', re.sub('\s+','',cases_plot_data))[1]))
        x_axis_cases = DataParser.create_date_axis(y_axis_cases)

        return {
            'cases_data': list(zip(x_axis_cases, y_axis_cases)),
        }



class NewsDataParser(DataParser):

    def __init__(self):
        super()

    @staticmethod
    def get_news_updates():

        url = DataParser.BASE_URL + '/' + '#news'
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        news = []

        print(soup.find_all('div', {'class': 'news_post'}))

        for item in soup.find_all('div', {'class': 'news_post'}):
            news.append([item.text.replace('[source]', "").strip(), item.find_next('a')['href']])


        return { 'news': list(news),
            'last_updated': soup.find('div', {'id': 'page-top'}).find_next('div').text
        }

class DemographicsDataParser(DataParser):

    def __init__(self):
        super()

    @staticmethod
    def get_demographics():

        url = DataParser.BASE_URL + '/' + 'coronavirus-age-sex-demographics/'
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        table_age = soup.select('.table-responsive')[0].find('table')
        table_body_age = table_age.find('tbody')

        age_rows = table_body_age.find_all('tr')[1:]

        table_sex = soup.select('.table-responsive')[2].find('table')
        table_body_sex = table_sex.find('tbody')

        sex_rows = table_body_sex.find_all('tr')[1:]

        table_conditions = soup.select('.table-responsive')[3].find('table')
        table_body_conditions = table_conditions.find('tbody')

        conditions_rows = table_body_conditions.find_all('tr')[1:]

        age_data, sex_data, conditions_data = [], [], []

        for row in age_rows:
            columns = row.find_all('td')[0].contents + row.find_all('td')[-1].contents
            columns = [value.text.strip() for value in columns]
            age_data.append([value.replace(',', '').replace(' years old', '') for value in columns if value])

        for row in sex_rows:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            sex_data.append([value.replace(',', '') for value in columns if value])

        for row in conditions_rows:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            conditions_data.append([value.replace(',', '').replace('%', '') for value in columns if value])

        return {'death_rate_by_age': age_data, 'death_rate_by_sex': sex_data,
                'pre_existing_conditions': conditions_data}

class TestsDataParser(DataParser):

    def __init__(self):
        super()

    @staticmethod
    def get_testing():

        url = DataParser.BASE_URL + '/' + 'covid-19-testing/'
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        tests_table = soup.select('.table-responsive')[0].find('table')
        tests_table_body = tests_table.find('tbody')

        tests_rows = tests_table_body.find_all('tr')[1:]

        tests_data = []

        for row in tests_rows:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            tests_data.append([value.replace(',', '') for value in columns[:-1]])

        return { 'tests_data': tests_data }


class SingleCountryParser(DataParser):

    def __init__(self):
        super()

    @staticmethod
    def get_country_data(country):

        url = DataParser.BASE_URL + f'/country/{country}/'
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        country = soup.find('div', {'style': 'text-align:center;width:100%'}).find_next('h1').text

        flag = soup.find('div', {'style': 'text-align:center;width:100%'}).find_next('img')['src']

        statistics = soup.select('.maincounter-number')

        scripts = soup.find_all('script')

        cases_data = [script.text for script in scripts if 'coronavirus-cases-linear' in str(script)][0]

        y_axis_cases = list(json.loads(re.search(r'data:(.+?)}]', re.sub('\s+','',cases_data))[1]))
        x_axis_cases = DataParser.create_date_axis(y_axis_cases)

        daily_cases_data = [script.text for script in scripts if 'graph-cases-daily' in str(script)][0]
        y_axis_daily = list(json.loads(re.search(r'data:(.+?)}]', re.sub('\s+','',daily_cases_data))[1]))
        x_axis_daily = DataParser.create_date_axis(y_axis_daily)

        active_cases_data = [script.text for script in scripts if 'graph-active-cases-total' in str(script)][0]
        y_axis_active = list(json.loads(re.search(r'data:(.+?)}]', re.sub('\s+','',active_cases_data))[1]))
        x_axis_active = DataParser.create_date_axis(y_axis_active)

        total_deaths_data = [script.text for script in scripts if 'coronavirus-deaths-linear' in str(script)][0]
        y_axis_deaths = list(json.loads(re.search(r'data:(.+?)}', re.sub('\s+','',total_deaths_data))[1]))
        x_axis_deaths = DataParser.create_date_axis(y_axis_deaths)

        daily_deaths_data = [script.text for script in scripts if 'graph-deaths-daily' in str(script)][0]
        y_axis_daily_deaths = list(json.loads(re.search(r'data:(.+?)}', re.sub('\s+','',daily_deaths_data))[1]))
        x_axis_daily_deaths = DataParser.create_date_axis(y_axis_daily_deaths)

        closed_cases_data = [script.text for script in scripts if 'deaths-cured-outcome' in str(script)][0]
        y_axis_closed_fat = list(json.loads(re.findall(r'data:(.+?)}', re.sub('\s+','',closed_cases_data))[0]))
        y_axis_closed_rec = list(json.loads(re.findall(r'data:(.+?)}', re.sub('\s+','',closed_cases_data))[1]))
        x_axis_closed = DataParser.create_date_axis(y_axis_closed_fat)

        last_updated = soup.find('div', {'id': 'page-top'}).find_next('div').text

        link = DataParser.BASE_URL
        new_query = requests.get(link)

        world_share = BeautifulSoup(new_query.content, 'html.parser').select('.maincounter-number')

        return {
            'country': country.strip(),
            'flag': 'https://www.worldometers.info' + flag,
            'total_cases': list(zip(x_axis_cases, y_axis_cases)),
            'daily_cases': list(zip(x_axis_daily, y_axis_daily)),
            'active_cases': list(zip(x_axis_active, y_axis_active)),
            'closed_cases': list(zip(x_axis_closed, y_axis_closed_fat, y_axis_closed_rec)),
            'total_deaths': list(zip(x_axis_deaths, y_axis_deaths)),
            'daily_deaths': list(zip(x_axis_daily_deaths, y_axis_daily_deaths)),
            'cases_now': statistics[0].text.strip().replace(',', ''),
            'deaths_now': statistics[1].text.strip().replace(',', ''),
            'recovered_now': statistics[2].text.strip().replace(',', ''),
            'cases_world': world_share[0].text.strip().replace(',', ''),
            'deaths_world': world_share[1].text.strip().replace(',', ''),
            'last_updated': last_updated
        }


class MainStatsDataParser(DataParser):

    def __init__(self):
        super()

    @staticmethod
    def get_stats():
        url = DataParser.BASE_URL
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        cases_data = []

        statistics = soup.select('.maincounter-number')

        return {
            'total_cases': statistics[0].text.strip().replace(',', ''),
            'total_deaths': statistics[1].text.strip().replace(',', ''),
            'total_recovered': statistics[2].text.strip().replace(',', '')
        }

