from datetime import datetime
from growing_commander_server import db
from growing_commander_server.models import User, Measurement

if __name__ == '__main__':
    db.create_all()
    user = User(
        name='admin',
        password='admin',
        is_admin=True
    )
    db.session.add(user)
    db.session.commit()

    measurement_1 = Measurement(datetime.now(), "DHT11", "temperature", 25.7, "C")
    measurement_2 = Measurement(datetime.now(), "DHT11", "humidity", 29, "%")
    db.session.add(measurement_1)
    db.session.add(measurement_2)
    db.session.commit()
