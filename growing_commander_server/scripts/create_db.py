from datetime import datetime
from source.main import db
from source.models import User, ObservationGroup, Measurement

if __name__ == '__main__':
    db.create_all()
    user = User(
        name='admin',
        password='admin',
        is_admin=True
    )
    db.session.add(user)
    db.session.commit()

    user = User(
        name='admin',
        password='admin',
        is_admin=True
    )
    db.session.add(user)
    db.session.commit()

    obs_group_1 = ObservationGroup(datetime(2017, 6, 25, 17, 15), datetime(2017, 6, 25, 17, 20))
    db.session.add(obs_group_1)
    db.session.commit()

    measurement_1 = Measurement("temperature", 25.7, "C", obs_group_1.id)
    measurement_2 = Measurement("humidity", 29, "%", obs_group_1.id)
    db.session.add(measurement_1)
    db.session.add(measurement_2)
    db.session.commit()
