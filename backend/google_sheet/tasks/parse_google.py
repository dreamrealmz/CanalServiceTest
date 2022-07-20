import os
import pandas as pd
import logging
import pickle
from django_app.celery import app, redis_instance


logger = logging.getLogger('error')


@app.task()
def parse_google():
    try:
        google_sheet_link = os.getenv('GOOGLE_SHEET_LINK')
        url = google_sheet_link.replace('/edit#gid=', '/export?format=csv&gid=')
        redis_instance.set('sheet_dataframe', pickle.dumps(pd.read_csv(url)))
    except Exception as error:
        print(error)
        logger.info(f'{error}')
        logger.error(f'{error}')
