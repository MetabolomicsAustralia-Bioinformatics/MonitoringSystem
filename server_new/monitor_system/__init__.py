# import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
# from monitor_system.models import Organisation, Instrument, Sample
import pymysql
pymysql.install_as_MySQLdb()
from flask_login import LoginManager
from flask_script import Manager


app = Flask(__name__)

# Often people will also separate these into a separate config.py file
app.config['SECRET_KEY'] = 'mysecretkey'
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1025@localhost:3306/monitoring_system'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://giuuhvimvuhrot:7592aee111ef95e22a60c960d02ff83ea391a4f7943c47fb2143557983337d38@ec2-50-17-194-186.compute-1.amazonaws.com:5432/dfnrndu27hlrd3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.create_all()
Migrate(app,db)


###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()




manager = Manager(app)
manager.add_command('db', MigrateCommand)
# We can now pass in our app to the login manager
# login_manager.init_app(app)

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