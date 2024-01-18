# STAGE TWO: USER AUTHENTICATION

from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from .models import User, UserRole, db

auth_blueprint = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.login_view = "login"


# Decorator that tells Flask-Login to use this function to reload the user object
@login_manager.user_loader
# Function that takes a user ID as input
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------ALL FORMS----------


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=5, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")
# LOGIN FORM CLASS


class CreateSubAdminForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=5, max=20)])
    role = SelectField('Role', choices=[('sub admin', 'Sub Admin')])
    submit = SubmitField('Create Sub Admin')
# CREATE SUB ADMIN FORM CLASS


class AssignRoleForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=5, max=20)])
    role = SelectField(
        'Role', choices=[('admin', 'Admin'), ('subadmin', 'Sub Admin')])
    assign = SubmitField()

# --------ALL FORMS----------
