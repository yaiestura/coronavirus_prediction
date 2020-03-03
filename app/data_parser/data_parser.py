import requests
from bs4 import BeautifulSoup
from datetime import datetime
import math
import csv
import re

class DataGrabber:

    TARGET_DOMAIN = "https://www.worldometers.info/coronavirus"

    def save_data_to_file(self, filename, data):
        data_to_save = []


        for i in range(0, len(data)):
            data_to_save.append([i, data[i]])

        with open("datasets/" + filename, 'w', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerows(data_to_save)

    def get_dataset_file_name(self, dataset_prefix, dataset_date=""):
        filename = dataset_prefix + "_dataset_"

        if dataset_date == "":
            filename += datetime.today().strftime('%Y-%m-%d')
        else:
            filename += dataset_date

        filename += ".csv"

        return filename


class CasesDataGrabber(DataGrabber):
    DATASET_PREFIX = "cases"

    def __init__(self):
        super()

    def grab_data(self):
        data = self.get_cases()
        filename = self.get_dataset_file_name()

        self.save_data_to_file(filename, data)

    def get_cases(self):
        data = self.get_table_content("coronavirus-cases", ".table-responsive", 2)

        return list(reversed(data))

    def get_dataset_file_name(self, dataset_date=""):
        return super().get_dataset_file_name(CasesDataGrabber.DATASET_PREFIX, dataset_date=dataset_date)


class DeathsDataGrabber(DataGrabber):

    DATASET_PREFIX = "deaths"

    def __init__(self):
        super()

    def grab_data(self):
        data = self.get_deaths()
        filename = self.get_dataset_file_name()

        self.save_data_to_file(filename, data)

    def get_deaths(self):

        url = DataGrabber.TARGET_DOMAIN + '/' + 'coronavirus-death-toll'
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


    def get_dataset_file_name(self, dataset_date=""):
        return super().get_dataset_file_name(DeathsDataGrabber.DATASET_PREFIX, dataset_date=dataset_date)


class CountriesDataGrabber(DataGrabber):
    DATASET_PREFIX = "countries"

    def __init__(self):
        super()

    def grab_data(self):
        data = self.get_countries()
        filename = self.get_dataset_file_name()

        self.save_data_to_file(filename, data)


class UpdatesDataGrabber(DataGrabber):
    DATASET_PREFIX = "updates"

    def __init__(self):
        super()

    def grab_data(self):
        data = self.get_updates()
        filename = self.get_dataset_file_name()
        self.save_data_to_file(filename, data)

    def get_updates(self):

        url = DataGrabber.TARGET_DOMAIN
        r = requests.get(url)
        content = r.content

        soup = BeautifulSoup(content, 'html.parser')

        data = []

        for item in soup.find('div', {'id': 'innercontent'}).find_next("ul").find_all('li'):
            data.append([item.text.replace("[source]", "").strip(), item.find_next('a')['href']])

        return list(data)

    def get_dataset_file_name(self, dataset_date=""):
        return super().get_dataset_file_name(UpdatesDataGrabber.DATASET_PREFIX, dataset_date=dataset_date)
