

def create_db():
    from run import *
    # from . import db
    # from . import pitch, user
    db.create_all()
    print('db created')
