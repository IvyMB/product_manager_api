import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = os.getenv('DEV_DATABASE_URL')


class TestingConfig(Config):
    DEBUG = True
    MONGO_URI = os.getenv('TEST_DATABASE_URL')


class ProductionConfig(Config):
    DEBUG = False
    MONGO_URI = os.getenv('PROD_DATABASE_URL')


config_options = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)
