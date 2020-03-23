import requests
import csv
from datetime import datetime
from cachetools import cached, TTLCache
from app.api.utils.utils import *

BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-%s.csv';

@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def get_data(category):

    category = category.lower().capitalize();

    request = requests.get(BASE_URL % category)
    text    = request.text

    data = list(csv.DictReader(text.splitlines()))

    locations = []

    for item in data:
        history = dict(filter(lambda element: is_date(element[0]), item.items()))

        country = item['Country/Region']

        latest = list(history.values())[-1];

        locations.append({
            'country':  country,
            'country_code': country_code(country),
            'province': item['Province/State'],

            'coordinates': {
                'lat':  item['Lat'],
                'long': item['Long'],
            },

            'history': history,

            'latest': int(latest or 0),
        })

    # Latest total.
    latest = sum(map(lambda location: location['latest'], locations))

    # Return the final data.
    return {
        'locations': locations,
        'total': latest,
        'last_updated': datetime.utcnow(),
    }