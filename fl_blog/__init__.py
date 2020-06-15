from flask import Flask
from flask_bootstrap import Bootstrap
#from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from fl_blog.config import config
from flask_login import LoginManager

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
# The login_view attribute of the LoginManager object sets the endpoint for the login page.
# Flask-Login will redirect to the login page when an anonymous user tries to access a protected page.
# Because the login route is inside a blueprint, it needs to be prefixed with the blueprint name.
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    #mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from fl_blog.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # The url_prefix argument in the blueprint registration is optional. When used, all the routes
    # defined in the blueprint will be registered with the given prefix, in this case /auth.
    # For example, the /login route will be registered as /auth/login,
    # and the fully qualified URL under the development web server then becomes http://localhost:5000/auth/login.
    from fl_blog.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app
