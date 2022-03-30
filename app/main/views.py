import os

from flask import render_template, request, flash, redirect, url_for

from app import UPLOAD_FOLDER
from app.main import main
from app.main.auth import logged_in_admin
from app.models.tabs import session, Types, Models, Images



@main.route('/')
@logged_in_admin
def index():
    with session() as s:
        categories = s.query(Types).all()
    return render_template('index.html', categories=categories)


@main.route('/category/<int:id>', methods=["GET"])
def show_category(id):
    with session() as s:
        data_img = {}
        filter_models = s.query(Models).filter(Models.types_id==id).all()
        for i in filter_models:
            id_img = i.id
            img = s.query(Images).filter(Images.model_id==id_img).first()
            data_img[id_img] = img.name

    return render_template('category.html', models=filter_models, data_img=data_img)


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
        category = data.get('select-category')
        name = data.get('name')
        desc = data.get('description')
        season = data.get('select-season')
        available = data.get('available')
        price = data.get('price')
        files = request.files.getlist('files')

        with session() as s:
            model = Models(types_id=category, name=name, descriptions=desc,
                           season=season, available=available, price=price)
            s.add(model)

            for file in files:
                img = Images(name=file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))
                model.model_img.append(img)
                s.add(img)

            s.commit()

    with session() as s:
        categories = s.query(Types).all()

    return render_template('add/add_model.html', categories=categories)
