import logging
import pickle
import datetime
from django_app.celery import app, redis_instance
from ..models import SheetRow

logger = logging.getLogger('error')


@app.task()
def notify_orders():
    try:
        sheets_to_update = redis_instance.get('reported_orders')
        if sheets_to_update:
            sheets_to_update = pickle.loads(redis_instance.get('reported_orders'))
            SheetRow.objects.filter(order_num__in=sheets_to_update).update(informed_about_rancid=True)

        sheets = [order['order_num'] for order in SheetRow.objects.filter(
            delivery_time__lte=datetime.datetime.now(),
            informed_about_rancid=False,
        ).order_by('delivery_time').values('order_num')]
        redis_instance.set('orders_to_report', pickle.dumps(sheets))

    except Exception as error:
        print(error)
        logger.info(f'{error}')
        logger.error(f'{error}')
