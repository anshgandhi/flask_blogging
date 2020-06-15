from werkzeug.security import generate_password_hash, check_password_hash
from fl_blog import db
from flask_login import UserMixin
from fl_blog import login_manager

# To be able to work with the application’s User model, the Flask-Login extension requires it
# to implement a few common properties and methods.
# These properties and methods can be implemented directly in the model class, but as an easier
# alternative Flask-Login provides a UserMixin class that has default implementations that are appropriate for most cases.
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


# The login_manager.user_loader decorator is used to register the function with Flask-Login,
# which will call it when it needs to retrieve information about the logged-in user.
# The user identifier will be passed as a string, so the function converts it to an integer before
# it passes it to the Flask-SQLAlchemy query that loads the user. The return value of the function
# must be the user object, or None if the user identifier is invalid or any other error occurred.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 
