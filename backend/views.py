from backend import app, db
from .models import Result
from flask import jsonify


@app.route('/')
def route():
     queryset = Result.query.all()
     return jsonify(json_list=[i.serialize for i in queryset])

