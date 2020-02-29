from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)