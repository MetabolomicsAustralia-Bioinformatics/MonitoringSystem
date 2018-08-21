# import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from monitor_system.models import Organisation, Instrument, Sample
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)

# Often people will also separate these into a separate config.py file
app.config['SECRET_KEY'] = 'mysecretkey'
# basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1025@localhost:3306/monitoring_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)
db.create_all()

from monitor_system.core.views import core
from monitor_system.error_pages.handlers import error_pages
from monitor_system.admin.views import admin


app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(admin,url_prefix="/admin")
