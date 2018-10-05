from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import pymysql

pymysql.install_as_MySQLdb()
from flask_login import LoginManager
from flask_script import Manager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1025@localhost:3306/monitoring_system'
# app.config[
#     'SQLALCHEMY_DATABASE_URI'] = 'postgres://bwjfnaecequqzs:0dd9b73c304d36c46629fc9036e3486d89c03f589203742976a3b7f18992a0d3@ec2-23-23-253-106.compute-1.amazonaws.com:5432/d7j1q5eatac7m0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.create_all()
Migrate(app, db)

#########################
#### LOGIN CONFIGS ######
#########################

login_manager = LoginManager()
login_manager.init_app(app)
# Tell users what view to go to when they need to login.
login_manager.login_view = "admin.login"

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from monitor_system.core.views import core
from monitor_system.error_pages.handlers import error_pages
from monitor_system.admin.views import admin

# register flask blueprint
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(admin, url_prefix="/admin")
