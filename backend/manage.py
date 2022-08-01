from backend import app, db

if __name__ == '__main__':
    db.init_app(app)
    app.run(host='0.0.0.0')