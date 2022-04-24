from models import *

def Reset_DB():
    db.drop_all()
    db.create_all()

def admin_create():
    t_us = User(
        firstname = "qwerty",
        lastname = "qwerty",
        email = "qwerty@qwe.qw",
        role = "admin"
    )
    t_us.set_password("admin")
    t_us.pin = "admin"
    db.session.add(t_us)
    db.session.commit()

#Reset_DB()
# admin_create()