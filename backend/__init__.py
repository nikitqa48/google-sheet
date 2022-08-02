import gspread
from flask import Flask
from sqlalchemy import create_engine
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from cbr import get_exchange_rates
import os
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask('kanalservis')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
sched = BackgroundScheduler(daemon=True)

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