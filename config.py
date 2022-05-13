import os


class Config:
    """Parent Config Class """
    SECRET_KEY = os.urandom(234102)
    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "cirusamuels@gmail.com"
    MAIL_PASSWORD = "Ninja102"
    
    # simple mde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True



class ProdConfig(Config):
    """Production Config Class"""


class DevConfig(Config):
    """Developement Config"""
    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig
}
