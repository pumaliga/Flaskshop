from functools import wraps
from flask import session as ses_admin, redirect, url_for, request, render_template

from app.main import main


def logged_in_admin(function):
    """DECORATOR FOR CHECKING LOGGED IN ADMIN"""

    @wraps(function)
    def wrap(*args, **kwargs):
        if ses_admin.get('logged_in_admin'):
            ses_admin['logged_in_admin'] = True
            return function(*args, **kwargs)
        return redirect(url_for('main.login'))

    return wrap


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == '1':
            ses_admin['logged_in_admin'] = True
            return redirect(url_for('main.index'))
    return render_template('login.html')


@main.route('/logout')
def logout():
    ses_admin.pop('logged_in_admin', None)
    return redirect(url_for('main.login'))
