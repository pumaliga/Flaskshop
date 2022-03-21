from flask import Flask


# login_manager.login_view = 'auth.login'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'app/uploads'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key'


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/main')

    from app.views import views
    app.register_blueprint(views)

    return app


