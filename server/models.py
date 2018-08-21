import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# This grabs our directory
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1025@localhost:3306/demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

##create our db
##pass the app into SQLAlchemy
db = SQLAlchemy(app)
Migrate(app, db)


# class Organisation(db.Model):
#     __tablename__ = 'organisations'
#
#     # id = db.Column(db.Integer, )
#     o_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.VARCHAR, nullable=False, unique=True)
#     # This is a one-to-many relationship
#     # A organisation can have many instruments
#     instrument = db.relationship('Instrument', backref='organisation', lazy='dynamic')
#
#
#     def __init__(self, name):
#         self.name = name

    # def __repr__(self):
    #     if self.owner:
    #         return "Puppy name is {self.name} and owner is {self.owner.name}"
    #     else:
    #         return "Puppy name is {self.name} and has no owner assigned yet."

class Instrument(db.Model):
    __tablename__ = 'instruments'

    #organisation ID and instrument name are composite primary key
    # o_id = db.Column(db.Integer,db.ForeignKey('organisations.o_id'), primary_key=True)
    name = db.Column(db.VARCHAR(128), primary_key=True)
    # pwd = db.Column(db.VARCHAR(16),nullable=False)

    samples = db.relationship('Sample', backref='Instrument', lazy='dynamic')
    def __init__(self, name):
        self.name = name

    # def __init__(self, name, organ_name):
    #     self.name = name
    #     self.organ_name = organ_name


class Sample(db.Model):
    __tablename__ = 'samples'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    o_id = db.Column(db.Integer,db.ForeignKey('instruments.o_id'))
    instrument = db.Column(db.VARCHAR(128), db.ForeignKey('instruments.name'))
    actual_start = db.Column(db.DateTime)
    actual_end = db.Column(db.DateTime)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    length = db.Column(db.Text)


    def __init__(self,o_id, name, instrument, actual_start, actual_end, start, end, length):
        self.o_id = o_id
        self.name = name
        self.instrument = instrument
        self.actual_start = actual_start
        self.actual_end = actual_end
        self.start = start
        self.end = end
        self.length = length
