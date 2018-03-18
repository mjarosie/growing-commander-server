from flask import render_template, request, url_for, flash, redirect, Blueprint
from flask_login import login_user, logout_user, login_required

from growing_commander_server.forms import LoginForm
from growing_commander_server.models import User, Measurement
from growing_commander_server.tables import UserTable, MeasurementsTable

app_blueprint = Blueprint('app_blueprint', __name__)


@app_blueprint.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate():
            login_user(form.user)
            flash("Successfully logged in as %s." % form.user.name, "success")
            return redirect(url_for("app_blueprint.overview"))
    else:
        form = LoginForm()
    return render_template("login_page.html", form=form)


@login_required
@app_blueprint.route("/logout/")
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('app_blueprint.login'))


@app_blueprint.route('/overview')
@login_required
def overview():
    return render_template('homepage.html')


@app_blueprint.route('/users')
@login_required
def users():
    all_users = User.query.order_by(User.registered_on.desc()).all()
    table = UserTable(all_users, border=True)
    return render_template('users.html', table=table)


@app_blueprint.route('/measures')
@login_required
def measures():
    tables = []
    measurements = Measurement.query.all()
    tables.append(MeasurementsTable(measurements, border=True))
    return render_template('measures.html', tables=tables)


@app_blueprint.route('/commands')
@login_required
def commands():
    return render_template('api_overview.html')
