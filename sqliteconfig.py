from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
import configparser

sqlite_config = configparser.ConfigParser()
sqlite_config.read("config/general_config.conf")
class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(app, options)
        options["pool_pre_ping"] = True

class Config:
    SECRET_KEY = 'hard to guess string'#not sure what's this for
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = False
    # database = 'demo_web_crawler'
    database = sqlite_config["sqlite"]["database"]
    # CHARSET = 'utf8mb4'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(database)


config = {
    'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    # 'production': ProductionConfig,
    'default': DevelopmentConfig
}