from . import db
from flask_login import UserMixin
from sqlalchemy import func


#establishing one to many relationship

class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    note=db.Column(db.String(150))
    data=db.Column(db.String(50000))
    date=db.Column(db.DateTime(timezone=True),server_default=func.now())
    user_id =db.Column(db.Integer,db.ForeignKey('user.id'))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150))
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    notes = db.relationship('Note')


 
