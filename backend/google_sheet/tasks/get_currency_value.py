import os
import logging
import pickle
import requests
import datetime
from bs4 import BeautifulSoup
from django_app.celery import app, redis_instance

logger = logging.getLogger('error')


@app.task()
def get_currency_value():
    try:
        date_for_link = datetime.date.today()
        url = os.getenv('CURRENCY_LINK') + f'{date_for_link.day}/{date_for_link.month}/{date_for_link.year}'
        result = requests.get(url)
        content = result.content
        soup = BeautifulSoup(content, 'xml')
        currency = list(filter(lambda x: 'USD' in str(x), soup.find_all('Valute')))[0]
        currency = str(currency).split('Value')[1]
        currency = float(str(currency).replace('/', '').replace('>', '').replace('<', '').replace(',', '.'))
        redis_instance.set('currency', pickle.dumps(currency))
    except Exception as error:
        print(error)
        logger.info(f'{error}')
        logger.error(f'{error}')
