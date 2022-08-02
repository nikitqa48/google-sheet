from backend import gsheet, db
from backend.models import Result
import pandas as pd

wks = gsheet.get_worksheet_by_id(0)


class TestTable:

    def __init__(self):
        self.data = wks.get_all_records()

    def compare_data(self):
        updated_data = wks.get_all_records()
        if self.data != updated_data:
            data = self.data
            self.data = updated_data
            data_frame = pd.DataFrame(data)
            update_data_frame = pd.DataFrame(updated_data)
            compared_frames = self.compare_frames(data_frame, update_data_frame)
            if compared_frames['create'].empty and not compared_frames['remove'].empty:
                return self.remove_table(compared_frames['remove'].index.values.tolist())
            return self.update_or_create_db(compared_frames['create'])

    def update_or_create_db(self, data):
        dict = data.to_dict('index')
        for item in dict:
            result = Result.query.get(item+1)
            if result is not None:
                result = Result.query.get(item+1)
                result.dollar_price = dict[item].get('стоимость,$')
                result.rubble_price = result.calculate_dollar()
                result.order_id = dict[item].get('заказ №')
                result.row_id = dict[item].get('№')
                result.delivery_time = dict[item].get('срок поставки')
            else:
                dict[item]['id'] = item + 1
                result = Result(**dict[item])
            db.session.add(result)
        return db.session.commit()

    def remove_table(self, values):
        try:
            for id in values:
                result = Result.query.get(id+1)
                db.session.delete(result)
                return db.session.commit()
        except:
            pass

    def compare_frames(self, data_frame, updated_frame):
        """ return list id values rows
            for remove and create or update"""
        create = data_frame.merge(
            updated_frame, indicator=True, how='right'
        ).loc[lambda x: x['_merge'] != 'both']
        remove = data_frame.merge(
            updated_frame, indicator=True, how='left'
        ).loc[lambda x: x['_merge'] != 'both']
        return {
            'create': create,
            'remove': remove
        }
