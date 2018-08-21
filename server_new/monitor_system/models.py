from monitor_system import db
from werkzeug.security import generate_password_hash
import pymysql
from sqlalchemy.schema import ForeignKeyConstraint
pymysql.install_as_MySQLdb()


class Organisation(db.Model):
    __tablename__ = 'organisations'

    # id = db.Column(db.Integer, )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), nullable=False, unique=True, index=True)
    # This is a one-to-many relationship
    # A organisation can have many instruments
    instrument = db.relationship('Instrument', backref='Organisation', lazy='dynamic')
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.png')

    def __init__(self, name):
        self.name = name




class Instrument(db.Model):
    __tablename__ = 'instruments'

    #organisation ID and instrument name are composite primary key
    o_id = db.Column(db.Integer,db.ForeignKey('organisations.id'), primary_key=True, nullable=False)
    name = db.Column(db.VARCHAR(128), primary_key=True, nullable=False)
    # pwd = db.Column(db.VARCHAR(16),nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)

    samples = db.relationship('Sample', backref='Instrument', lazy='dynamic')
    def __init__(self,o_id, name, password):
        self.o_id = o_id
        self.name = name
        self.password_hash = generate_password_hash(password)

    # def __init__(self, name, organ_name):
    #     self.name = name
    #     self.organ_name = organ_name


class Sample(db.Model):
    __tablename__ = 'samples'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text,nullable=False)

    o_id = db.Column(db.Integer)
    instrument = db.Column(db.VARCHAR(128))
    __table_args__ = (ForeignKeyConstraint([o_id, instrument],
                                           [Instrument.o_id, Instrument.name]),
                      {})
    # o_id = relationship("Instrument", foreign_keys=[o_id])
    # instrument = relationship("Instrument", foreign_keys=[instrument])
    actual_start = db.Column(db.DateTime, nullable=False)
    actual_end = db.Column(db.DateTime, nullable=False)
    length = db.Column(db.Text)


    def __init__(self, o_id, name, instrument, actual_start, actual_end,length):
        self.o_id = o_id
        self.name = name
        self.instrument = instrument
        self.actual_start = actual_start
        self.actual_end = actual_end
        self.length = length
