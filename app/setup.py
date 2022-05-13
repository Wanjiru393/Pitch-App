

def create_db():
    from . import db
    from . import pitch, user
    db.create_all()
    print('db created')
