import wtforms
from wtforms import validators
from source.models import User


class LoginForm(wtforms.Form):
    name = wtforms.StringField("Name", validators=[validators.DataRequired()])
    password = wtforms.PasswordField("Password", validators=[validators.DataRequired()])

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        self.user = User.authenticate(self.name.data, self.password.data)
        if not self.user:
            self.name.errors.append("Invalid email or password.")
            return False
        return True
