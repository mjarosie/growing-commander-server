from flask import render_template, request, url_for, flash, redirect
from flask_login import login_user, logout_user, login_required
from .. import app

from models import User, Measurement
from forms import LoginForm
from tables import UserTable, ObservationGroupTable


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate():
            login_user(form.user)
            flash("Successfully logged in as %s." % form.user.name, "success")
            return redirect(url_for("overview"))
    else:
        form = LoginForm()
    return render_template("login_page.html", form=form)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/overview')
@login_required
def overview():
    return render_template('homepage.html')


@app.route('/users')
@login_required
def users():
    all_users = User.query.order_by(User.registered_on.desc()).all()
    table = UserTable(all_users, border=True)
    return render_template('users.html', table=table)


@app.route('/measures')
@login_required
def measures():
    tables = []
    measurements = Measurement.query.all()
    tables.append(ObservationGroupTable(measurements, border=True))
    return render_template('measures.html', tables=tables)


@app.route('/commands')
@login_required
def commands():
    return render_template('homepage.html')