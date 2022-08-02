from backend import app, db, sched, gsheet
import pandas as pd
from backend.tasks import TestTable
from backend.models import Result


if __name__ == '__main__':
    db.init_app(app)
    test = TestTable()
    sched.add_job(test.compare_data, 'interval', seconds=5)
    sched.start()
    app.run(host='0.0.0.0', debug=False)


def migrate():
     wks = gsheet.get_worksheet_by_id(0)
     records_data = wks.get_all_records()
     records_df = pd.DataFrame.from_dict(records_data)
     filter_data = records_df.to_dict('index')
     attrs = {}
     for data in filter_data:
          #iter rows
          attrs['id'] = data + 1
          for key in filter_data[data].keys():
               attrs[key] = filter_data[data][key]
          result = Result(**attrs)
          db.session.add(result)
     return db.session.commit()