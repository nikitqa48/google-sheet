import gspread
from flask import Flask
from sqlalchemy import create_engine
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from cbr import get_exchange_rates
from celery import Celery
import os
from dotenv import load_dotenv


load_dotenv()

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_BACKEND_URL"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app = Flask('kanalservis')
#app init
app.config.update(
    CELERY_BROKER_URL=os.environ.get("CELERY_BROKER_URL"),
    CELERY_BACKEND_URL=os.environ.get("CELERY_BACKEND_URL"),
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    CELERY_IMPORTS=('tasks', )
)


celery = make_celery(app)

engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])

gc = gspread.service_account(filename='backend/credentials.json')
#connect to google sheets

gsheet = gc.open_by_key(os.environ['GSHEET_FILE_KEY'])
#open google worksheets

today = date.today()
date_now = today.strftime('%d/%m/%Y"').replace('/', '.')
course_today = get_exchange_rates(date_now, symbols=['USD', 'RUB'])

db = SQLAlchemy(app)
#db init


from backend import views, models

db.create_all()