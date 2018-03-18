from flask_table import Table, Col, DatetimeCol


class UserTable(Table):
    id = Col('Id')
    name = Col('Name')
    registered_on = DatetimeCol('Registered on', datetime_format='dd-MM-YY hh:mm:ss')


class MeasurementsTable(Table):
    id = Col("Id")
    timestamp = DatetimeCol('Time', datetime_format='dd-MM-YY hh:mm:ss')
    device_name = Col("Device")
    type = Col("Type")
    value = Col("Value")
    unit = Col("Unit")
