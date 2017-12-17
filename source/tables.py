from flask_table import Table, Col, DatetimeCol


class UserTable(Table):
    id = Col('Id')
    name = Col('Name')
    registered_on = DatetimeCol('Registered on', datetime_format='dd-MM-YY hh:mm:ss')


class ObservationGroupTable(Table):
    id = Col("Id")
    type = Col("Type")
    value = Col("Value")
    unit = Col("Unit")
