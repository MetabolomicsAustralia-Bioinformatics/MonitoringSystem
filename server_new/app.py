from monitor_system import app
from monitor_system.models import Organisation, Instrument, Sample
from monitor_system import db


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
