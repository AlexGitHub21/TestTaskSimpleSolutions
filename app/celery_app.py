from celery import Celery
from dotenv import load_dotenv
import os


load_dotenv()

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

celery_app = Celery("celery_worker", broker=f'{CELERY_BROKER_URL}', backend=CELERY_RESULT_BACKEND, include=["app.tasks"])

celery_app.conf.update(timezone="UTC",
        beat_schedule={
        'fetch_prices_every_minute': {
            'task': 'app.tasks.fetch_prices',
            'schedule': 60.0,
        }})