# import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from monitor_system.models import Organisation, Instrument, Sample
import pymysql
pymysql.install_as_MySQLdb()
from flask_login import LoginManager


app = Flask(__name__)

# Often people will also separate these into a separate config.py file
app.config['SECRET_KEY'] = 'mysecretkey'
# basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1025@localhost:3306/monitoring_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)
db.create_all()

###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "admin.login"





from monitor_system.core.views import core
from monitor_system.error_pages.handlers import error_pages
from monitor_system.admin.views import admin
# from monitor_system.admin.adminMonitor import adminMonitor


app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(admin,url_prefix="/admin")
# app.register_blueprint(adminMonitor)