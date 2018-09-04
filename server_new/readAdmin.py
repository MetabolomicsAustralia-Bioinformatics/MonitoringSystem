import os
from monitor_system.models import Admin
from monitor_system import db


path = os.path.abspath('admin.txt')

with open(path, 'r') as f:
    lines = f.readlines()
    last_line = lines[-1]
    line = last_line.split(':')
    name = line[0].strip()
    email = line[1].strip()
    pwd = line[2].strip()
    admin = Admin(email=email, username=name, password=pwd)
    db.session.add(admin)
    db.session.commit()
    print("complete")



f.close()