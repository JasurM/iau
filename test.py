from models import *

def Reset_DB():
    db.drop_all()
    db.create_all()

Reset_DB()