from backend import db, course_today
from datetime import datetime


class Result(db.Model):
    _table_name = 'results'
    id = db.Column(db.Integer, primary_key=True)
    row_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer)
    dollar_price = db.Column(db.Integer)
    rubble_price = db.Column(db.Float)
    delivery_time = db.Column(db.Date)

    def __init__(self, **kwargs):
        date_str = kwargs['срок поставки'].replace('.', '/')
        self.delivery_time = datetime.strptime(date_str, '%d/%M/%Y').date()
        self.id = kwargs['id']
        self.row_id = kwargs['№']
        self.order_id = kwargs['заказ №']
        self.dollar_price = kwargs['стоимость,$']
        self.calculate_dollar(self.dollar_price)

    def __repr__(self):
        return f'<id {self.id}>'

    def calculate_dollar(self, dollar):
        print(course_today)

