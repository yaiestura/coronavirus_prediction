from app import create_app, db
from datetime import datetime

app = create_app()

def _jinja2_filter_datetime(date):
    return datetime.utcfromtimestamp(date / 1000).strftime('%d-%m-%Y')

app.jinja_env.filters['datetime'] = _jinja2_filter_datetime

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)
