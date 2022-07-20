import os
import logging
import pickle
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from django_app.celery import app, redis_instance
from ..models import SheetRow

logger = logging.getLogger('error')


@app.task()
def update_database():
    try:
        dataframe = pickle.loads(redis_instance.get('sheet_dataframe'))
        dataframe = prepare_dataframe(dataframe)
        currency = pickle.loads(redis_instance.get('currency')) if redis_instance.get('currency') else 1
        dataframe_to_db(dataframe, currency)
    except Exception as error:
        print(error)
        logger.info(f'{error}')
        logger.error(f'{error}')


def prepare_dataframe(dataframe):
    dataframe = dataframe.rename(
        columns={
            '№': 'sheet_id',
            'заказ №': 'order_num',
            'стоимость,$': 'cost',
            'срок поставки': 'delivery_time',
        }
    )

    dataframe['sheet_id'] = dataframe['sheet_id'].astype(int)
    dataframe['order_num'] = dataframe['order_num'].astype(int)
    dataframe['cost'] = dataframe['cost'].astype(int)
    dataframe['delivery_time'] = pd.to_datetime(dataframe['delivery_time'], infer_datetime_format=True)

    return dataframe


def dataframe_to_db(dataframe, currency):
    for index, row in dataframe.iterrows():
        sheet = SheetRow.objects.filter(sheet_id=row.sheet_id).first()
        if sheet:
            data = {
                'order_num': row.order_num,
                'cost': row.cost,
                'delivery_time': row.delivery_time,
                'cost_in_rur': row.cost * currency
            }
            SheetRow.objects.filter(sheet_id=row.sheet_id).update(**data)
        else:
            data = {
                'sheet_id': row.sheet_id,
                'order_num': row.order_num,
                'cost': row.cost,
                'cost_in_rur': row.cost * currency,
                'delivery_time': row.delivery_time,
            }
            SheetRow.objects.create(**data)
