import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'mail.socialdroid.io')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    MAIL_USE_TLS = False
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 1)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[Socialdroid.io]'
    MAIL_SENDER = 'Socialdroid <support@socialdroid.io>'
    ADMIN = os.environ.get('ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE_PAGINATION = 50

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_DEBUG=True
    TEMPLATES_AUTO_RELOAD=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': ProductionConfig
}
