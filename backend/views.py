from backend import app, db, celery
from .models import Result
from backend import gsheet
import pandas as pd
from backend import celery
from celery import task

# @app.route('/')
# def params():
#      wks = gsheet.get_worksheet_by_id(0)
#      records_data = wks.get_all_records()
#      records_df = pd.DataFrame.from_dict(records_data)
#      filter_data = records_df.to_dict('index')
#      attrs = {}
#      for data in filter_data:
#           #iter row tables
#           attrs['id'] = data + 1
#           for key in filter_data[data].keys():
#                #iter column of row
#                attrs[key] = filter_data[data][key]
#           result = Result(**attrs)
#           # db.session.add(result)
#           # db.session.commit()
#      print(Result.query.all())
#      return 'hello'

@app.route('/')
def route():
     bg_task.delay()
     return 'hi'


@celery.task()
def bg_task():
     print('asdasd')
     return 'xz'