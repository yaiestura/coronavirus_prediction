from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    ctx = app.app_context()
    ctx.push()

    db.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    migrate = Migrate(app, db)

    from app.views.users.routes import users
    from app.views.main.routes import main
    from app.views.posts.routes import posts
    from app.views.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app
