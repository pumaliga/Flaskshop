from flask import render_template, request, flash, redirect, url_for

from app.main import main
from app.main.auth import logged_in_admin
from app.models.tabs import session, Types
from werkzeug.utils import secure_filename



@main.route('/')
@logged_in_admin
def index():
    return render_template('index.html')


@main.route('create/category', methods=["GET", "POST"])
@logged_in_admin
def create_category():
    if request.method == "POST":
        name = request.form['name']

        with session() as s:
            categories = Types(name=name)
            s.add(categories)
            s.commit()

        return redirect(url_for('main.index'))

    return render_template('add/categories.html')


@main.route('create/model', methods=["GET", "POST"])
@logged_in_admin
def create_model():
    if request.method == "POST":
        data = request.form
        print(data)


    with session() as s:
        categories = s.query(Types).all()

    return render_template('add/add_model.html', categories=categories)
