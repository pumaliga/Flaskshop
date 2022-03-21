from flask import Blueprint, render_template

views = Blueprint("views", __name__)


@views.route('/')
def main():
    return render_template('about.html')