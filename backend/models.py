from backend import db, course_today
from datetime import datetime


class Result(db.Model):
    _table_name = 'results'
    id = db.Column(db.Integer, primary_key=True)
    row_id = db.Column(db.String(80))
    order_id = db.Column(db.String(80))
    dollar_price = db.Column(db.String(80))
    rubble_price = db.Column(db.Float)
    delivery_time = db.Column(db.String(80))

    def __init__(self, **kwargs):

        self.delivery_time = kwargs.get('срок поставки')
        self.id = kwargs.get('id')
        self.row_id = kwargs.get('№')
        self.order_id = kwargs.get('заказ №')
        if type(kwargs['стоимость,$']) is int:
            self.dollar_price = kwargs.get('стоимость,$')
            self.rubble_price = self.calculate_dollar()

    def __repr__(self):
        return f'<id {self.id}>'

    def calculate_dollar(self):
        return course_today[0]['rate'] * self.dollar_price

    @property
    def serialize(self):
        return {
            'id': self.id,
            'row_id': self.id,
            'order_id': self.order_id,
            'dollar_price': self.dollar_price,
            'rubble_price': self.rubble_price,
            'data': self.delivery_time
        }

    def update_time(self, date):
        date_str = date.replace('.', '/')
        return datetime.strptime(date_str, '%d/%M/%Y').date()

