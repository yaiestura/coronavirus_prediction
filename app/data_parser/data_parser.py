from bs4 import BeautifulSoup
from datetime import datetime

import requests
import json
import math
import csv
import re


class DataParser:

    BASE_URL = 'https://www.worldometers.info/coronavirus'

    def save_data_to_file(self, filename, data):
        data_to_save = []

        for i in range(0, len(data)):
            data_to_save.append([i, data[i]])

        with open('datasets/' + filename, 'w', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerows(data_to_save)

    def get_dataset_file_name(self, dataset_prefix, dataset_date=''):
        filename = dataset_prefix + '_dataset_'
        if dataset_date == '':
            filename += datetime.today().strftime('%Y-%m-%d')
        else:
            filename += dataset_date

        filename += '.csv'

        return filename

    def scrape_table():
        pass
        # rewrite method


class DeathsDataParser(DataParser):

    def __init__(self):
        super()

    def get_deaths(self):

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
            total_data.append([value.replace(',', '') for value in columns if value])

        deaths_today = soup.select('.maincounter-number span')[0].text.strip().replace(',', '')
        today_date = re.sub(r'\d+', str(int(re.findall(r'\d+', total_data[0][0])[0]) + 1), total_data[0][0])
        deaths_diff = int(deaths_today) - int(total_data[0][1])
        deaths_growth = f'{math.floor(deaths_diff * 100 / int(deaths_today))}%'

        total_data.insert(0, [ today_date, deaths_today, str(deaths_diff), deaths_growth ])

        table_daily = soup.select('.table-responsive')[1].find('table')
        table_body_daily = table_daily.find('tbody')

        daily_rows = table_body_daily.find_all('tr')

        for row in daily_rows:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            daily_data.append([value.replace(',', '') for value in columns if value])

        return {'total_deaths': total_data, 'daily_deaths': daily_data}


class CountriesDataParser(DataParser):

    def __init__(self):
        super()

    def get_countries_minimal(self):

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
            data_countries.append([value.replace(',', '') for value in columns if value])

        return data_countries

    def get_countries_advanced(self):

        url= DataParser.BASE_URL + '/' + '#countries'
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        table_countries = soup.select('#main_table_countries_div')[0].find('table')
        table_body_countries = table_countries.find('tbody')

        rows_countries = table_body_countries.find_all('tr')

        data_countries = []

        for row in rows_countries:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            data_countries.append([value.replace(',', '') for value in columns if value])
        return data_countries[:-1]

    def get_countries(self):
        return {'countries_minimal_table': self.get_countries_minimal(),
                'countries_extended_table': self.get_countries_advanced(),
                'countries_affected': len(self.get_countries_minimal()) }


class UpdatesDataParser(DataParser):

    def __init__(self):
        super()

    def get_updates(self):

        url = DataParser.BASE_URL
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        updates_data, cases_data = [], []

        statistics = soup.select('.maincounter-number')
        
        active_cases = soup.select('.panel-body')[0].find('div', {'class': 'panel_front'})
        closed_cases = soup.select('.panel-body')[1].find('div', {'class': 'panel_front'})
        active_conditions = soup.select('.panel-body')[0].find_all('span', {'class': 'number-table'})

        active_plot_data = soup.select('.panel-body')[0].find('script', type="text/javascript").text
        x_axis_act = list(json.loads(re.search(r'categories: (.+?)}, yAxis', active_plot_data)[1]))
        y_axis_act = list(json.loads(re.search(r'data: (.+?) }', active_plot_data)[1]))

        closed_plot_data = soup.select('.panel-body')[1].find('script', type="text/javascript").text
        x_axis_cl = list(json.loads(re.search(r'categories: (.+?) }, yAxis', closed_plot_data)[1]))
        y_axis_cl = re.findall(r'data: (.+?) }', closed_plot_data)

        cases_plot_data = soup.find('div', {'id': 'coronavirus-cases-log'}).find_next('script', type="text/javascript").text
        x_axis_cases = list(json.loads(re.search(r'categories: (.+?) }, yAxis', cases_plot_data)[1]))
        y_axis_cases = list(json.loads(re.search(r'data: (.+?) }', cases_plot_data)[1]))

        today_date = re.sub(r'\d+', str(int(re.findall(r'\d+', x_axis_cases[-1])[0]) + 1).zfill(2), x_axis_cases[-1])

        x_axis_cases.append(today_date)
        y_axis_cases.append(int(statistics[0].text.strip().replace(',', '')))

        for item in soup.find('div', {'id': 'innercontent'}).find_next('ul').find_all('li'):
            updates_data.append([item.text.replace('[source]', "").strip(), item.find_next('a')['href']])

        return { 'total_cases': statistics[0].text.strip().replace(',', ''),
                'total_deaths': statistics[1].text.strip().replace(',', ''),
                'total_recovered': statistics[2].text.strip().replace(',', ''),
                'active_cases': active_cases.find('div', {'class': 'number-table-main'}).text.strip().replace(',', ''),
                'closed_cases': closed_cases.find('div', {'class': 'number-table-main'}).text.strip().replace(',', ''),
                'mild_condition': active_conditions[0].text.strip().replace(',', ''),
                'critical_condition': active_conditions[1].text.strip().replace(',', ''),
                'cases_plot': [ x_axis_cases, y_axis_cases ],
                'active_cases_plot': [ x_axis_act, y_axis_act ],
                'closed_cases_plot': [ x_axis_cl,  
                                       list(json.loads(y_axis_cl[0])),  
                                       list(json.loads(y_axis_cl[1])) 
                                     ],
                'updates_data': list(updates_data) }


class DemographicsDataParser(DataParser):

    def __init__(self):
        super()

    def get_demographics(self):

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
            age_data.append([value.replace(',', '') for value in columns if value])

        for row in sex_rows:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            sex_data.append([value.replace(',', '') for value in columns if value])

        for row in conditions_rows:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            conditions_data.append([value.replace(',', '') for value in columns if value])

        return { 'death_rate_by_age': age_data, 'death_rate_by_sex': sex_data,
                 'pre_existing_conditions': conditions_data }
