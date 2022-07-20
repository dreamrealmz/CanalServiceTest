import os
import pickle
from datetime import timedelta
from redis import StrictRedis
from telegram.ext import Updater, CallbackContext

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')

redis_instance = StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
)

bot = Updater(token=TOKEN, use_context=True)
dp = bot.dispatcher
jq = bot.job_queue


def callback(context: CallbackContext):
    try:
        report = pickle.loads(redis_instance.get('orders_to_report'))
        if report:
            report_text = ',\n'.join([str(item) for item in report])
            context.bot.send_message(chat_id=CHAT_ID,
                                     text=f'orders rancid {report_text}')
            redis_instance.set('reported_orders', pickle.dumps(report))
    except Exception as error:
        print(error)


callback = jq.run_repeating(callback, interval=timedelta(seconds=60), first=timedelta(seconds=10))

if __name__ == '__main__':
    bot.start_polling()
    bot.idle()
