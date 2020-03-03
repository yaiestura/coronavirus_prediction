import requests
from bs4 import BeautifulSoup
from datetime import datetime
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


class CasesDataParser(DataParser):

    DATASET_PREFIX = 'cases'

    def __init__(self):
        super()

    def get_cases(self):
        data = self.get_table_content('coronavirus-cases', '.table-responsive', 2)

        return list(reversed(data))


class DeathsDataParser(DataParser):

    DATASET_PREFIX = 'deaths'

    def __init__(self):
        super()

    def get_deaths(self):

        url = DataParser.BASE_URL + '/' + 'coronavirus-death-toll'
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        data = []

        table = soup.select('.table-responsive')[0].find('table')
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')

        for row in rows:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            data.append([value.replace(',', '') for value in columns if value]) # Get rid of empty values

        deaths_today = soup.select('.maincounter-number span')[0].text.strip().replace(',', '')
        today_date = re.sub(r'\d+', str(int(re.findall(r'\d+', data[0][0])[0]) + 1), data[0][0])
        deaths_diff = int(deaths_today) - int(data[0][1])
        deaths_growth = f'{math.floor(deaths_diff * 100 / int(deaths_today))}%'

        data.insert(0, [ today_date, deaths_today, str(deaths_diff), deaths_growth ])

        return list(data)


class CountriesDataParser(DataParser):

    DATASET_PREFIX = 'countries'

    def __init__(self):
        super()

    def get_countries_minimal(self):

        url = DataParser.BASE_URL + '/' + 'countries-where-coronavirus-has-spread/'
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        table = soup.select('.table-responsive')[0].find('table')
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')

        data = []

        for row in rows:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            data.append([value.replace(',', '') for value in columns if value])

        return data

    def get_countries_advanced(self):

        url= DataParser.BASE_URL + '/' + '#countries'
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        table = soup.select('#main_table_countries_div')[0].find('table')
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')

        data = []

        for row in rows:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            data.append([value.replace(',', '') for value in columns if value])
        return data[:-1]

    def get_countries(self):
        return {'countries_minimal_table': self.get_countries_minimal(),
                'countries_extended_table': self.get_countries_advanced(),
                'countries_affected': len(self.get_countries_minimal()) }


class UpdatesDataParser(DataParser):

    DATASET_PREFIX = 'updates'

    def __init__(self):
        super()

    def get_updates(self):

        url = DataParser.BASE_URL
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        data = []

        for item in soup.find('div', {'id': 'innercontent'}).find_next('ul').find_all('li'):
            data.append([item.text.replace('[source]', "").strip(), item.find_next('a')['href']])

        return list(data)


class DemographicsDataParser(DataParser):

    DATASET_PREFIX = 'demographics'

    def __init__(self):
        super()

    def get_demographics(self):

        url = DataParser.BASE_URL + '/' + 'coronavirus-age-sex-demographics/'
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        table_age = soup.select('.table-responsive')[0].find('table')
        table_body_age = table_age.find('tbody')

        rows_age = table_body_age.find_all('tr')[1:]

        table_sex = soup.select('.table-responsive')[2].find('table')
        table_body_sex = table_sex.find('tbody')

        rows_sex = table_body_sex.find_all('tr')[1:]
        print(rows_sex)

        table_conditions = soup.select('.table-responsive')[3].find('table')
        table_body_conditions = table_conditions.find('tbody')

        rows_conditions = table_body_conditions.find_all('tr')[1:]

        data_age, data_sex, data_conditions = [], [], []

        for row in rows_age:
            columns = row.find_all('td')[0].contents + row.find_all('td')[-1].contents
            columns = [value.text.strip() for value in columns]
            data_age.append([value.replace(',', '') for value in columns if value])

        for row in rows_sex:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            data_sex.append([value.replace(',', '') for value in columns if value])

        for row in rows_conditions:
            columns = row.find_all('td')
            columns = [value.text.strip() for value in columns]
            data_conditions.append([value.replace(',', '') for value in columns if value])

        return {'death_rate_by_age': data_age, 'death_rate_by_sex': data_sex,
                'pre_existing_conditions': data_conditions }
