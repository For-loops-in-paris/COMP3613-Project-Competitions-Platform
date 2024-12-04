from flask_login import login_user, login_manager, logout_user, LoginManager, current_user
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from flask import redirect, flash, request
from functools import wraps

from App.models import User, Student, Moderator

def jwt_authenticate(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    return create_access_token(identity=username)
  return None

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_student(id):
        return Student.query.get(id)

    return login_manager

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        user = User.query.filter_by(username=identity).one_or_none()
        if user:
            return user.id
        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    return jwt

def moderator_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Moderator):
            flash("Moderator role required")
            return redirect(request.referrer)
        return func(*args, **kwargs)
    return wrapper


