from flask_sqlalchemy import SQLAlchemy
from monitor_system.models import Admin
from monitor_system import db,app
from werkzeug.security import check_password_hash

db.create_all()

admin = Admin(email='abc@gmail.com',username='abc', password='123')
db.session.add(admin)
db.session.commit()