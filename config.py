import os


class Config:
    '''
    Parent config class
    '''
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = 'SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = 'postgresql://fkjcprkpdmtgke:3da620cc3546cef8066ff0bd1335445ece84cb858b5344919318c4bd121df546@ec2-107-22-238-112.compute-1.amazonaws.com:5432/d6ab7t3gmljed8'

    # SQLALCHEMY_DATABASE_URI = os.environ.get(
    #     'DATABASE_URL').replace("://", "ql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Mail confugurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SUBJECT_PREFIX = 'PITCH APP!'
    SENDER_EMAIL = 'cirusamuels@gmail.com'

    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):
    '''
    Production  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''


SQLALCHEMY_DATABASE_URI = 'postgresql://fkjcprkpdmtgke:3da620cc3546cef8066ff0bd1335445ece84cb858b5344919318c4bd121df546@ec2-107-22-238-112.compute-1.amazonaws.com:5432/d6ab7t3gmljed8'


# SQLALCHEMY_DATABASE_URI = os.environ.get(
#     'DATABASE_URL').replace("://", "ql://", 1)


DEBUG = True


class TestConfig(Config):
    '''
    Test
    '''


SQLALCHEMY_DATABASE_URI = 'postgresql://fkjcprkpdmtgke:3da620cc3546cef8066ff0bd1335445ece84cb858b5344919318c4bd121df546@ec2-107-22-238-112.compute-1.amazonaws.com:5432/d6ab7t3gmljed8'

# SQLALCHEMY_DATABASE_URI = os.environ.get(
#     'DATABASE_URL').replace("://", "ql://", 1)


class DevConfig(Config):
    '''
    Development  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''


SQLALCHEMY_DATABASE_URI= 'postgresql://fkjcprkpdmtgke:3da620cc3546cef8066ff0bd1335445ece84cb858b5344919318c4bd121df546@ec2-107-22-238-112.compute-1.amazonaws.com:5432/d6ab7t3gmljed8'

# SQLALCHEMY_DATABASE_URI = os.environ.get(
#     'DATABASE_URL').replace("://", "ql://", 1)


config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'test': TestConfig,
}
