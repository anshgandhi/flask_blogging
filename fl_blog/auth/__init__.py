from flask import Blueprint

# By storing the blueprint templates in their own subdirectory,
# there is no risk of naming collisions with the main blueprint
# or any other blueprints that will be added in the future.
auth = Blueprint('auth', __name__)

from fl_blog.auth import views