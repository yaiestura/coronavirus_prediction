class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    GOOGLE_CLIENT_ID = '557601922567-85lqa1rjlr710l70ag092lqncf4m2pjt.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = 'dQ_SHXPavROnzAwhfV4UXdUt'
    GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'

    HOME_VIEW = 'main.home'
    DASHBOARD_VIEW = 'main.dashboard'
    REGISTER_VIEW = 'users.register'
    LOGIN_VIEW = 'users.login'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'NONE'
    MAIL_PASSWORD = 'NONE'
