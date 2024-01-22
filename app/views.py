# --------ROUTES AND VALIDATION CHECKS--------


# from app import Bcrypt
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, abort, current_app
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .auth import auth_blueprint, LoginForm, CreateSubAdminForm, AssignRoleForm
from .models import User, db
from app import db
from .extensions import db
from .bcrypt import generate_password_hash, check_password_hash


@auth_blueprint.route("/")
def index():
    return render_template("index.html")
# ROUTE FOR THE HOME PAGE


@auth_blueprint.route("/admin", methods=['GET', 'POST'])
def admin():
    return render_template(('admin_dashborad.html'))
# ROUTE FOR THE ADMIN PAGE


@auth_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            if user.is_superadmin or user.is_subadmin:
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('admin'))
            else:
                flash('Only super admins and sub admins can log in', 'danger')
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)


# bcrypt = current_app.Bcrypt

# ROUTE FOR ADMIN DASHBOARD UPON LOGIN AND VALIDATION


@auth_blueprint.route('/logout')
def logout_request():
    logout_user()
    return redirect(url_for('login'))
# LOGOUT USER FUNCTION


@auth_blueprint.route("/create-sub-admin", methods=['GET', 'POST'])
def create_sub_admin():
    if not current_user.is_superadmin:
        flash('You do not have permission to create sub admin', 'danger')
        return redirect(url_for('index'))

    form = CreateSubAdminForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_sub_admin = User(username=form.username.data,
                             password=hashed_password, is_superadmin=False)
        db.session.add(new_sub_admin)
        db.session.commit()
        flash('New Sub Admin Created!', 'success')
        return redirect(url_for('index'))

    return render_template('create_sub_admin.html', form=form)
# ROUTE FOR CREATION OF SUB ADMIN


@auth_blueprint.route("/assign-role", methods=['GET', 'POST'])
def assign_role():
    form = AssignRoleForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.user.data).first()
        if user:
            user.role = form.role.data
            db.session.commit()
            flash('Role assigned successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('User not found', 'danger')
    return render_template('assign_role.html', form=form)
# ROUTE FOR HANDLING FORM SUBMISSION AND ROLE ASSIGNMENT

# --------ROUTES AND VALIDATION CHECKS--------
