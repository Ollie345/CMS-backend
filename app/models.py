# STAGE ONE: DATABASE SETUP

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from . import db

app = Flask(__name__)
db = SQLAlchemy()  # DATABASE OBJECT


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    # This is a relationship field
    role = db.relationship('UserRole', backref='users')

    def __init__(self, username, email, password, role_id):
        self.role_id = role_id
        self.username = username
        self.email = email
        self.password = password

    @property
    def is_superadmin(self):
        return self.role.role_name == 'Super Admin'

    @property
    def is_subadmin(self):
        return self.role.role_name == 'Sub Admin'

    def has_role(self, role_name):
        return self.role.role_name == role_name
# DATABASE MODEL FOR USER AND ROLE CHECK FUNCTIONS


class UserRole(db.Model):
    __tablename__ = 'roles'  # SPECIFY THE TABLE NAME TO MATCH THE FORIEGN KEY REFERENCE
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)
    role_desc = db.Column(db.String(200))

    def __init__(self, role_name, role_desc):
        self.role_name = role_name
        self.role_desc = role_desc
# DATABASE MODEL FOR USER ROLE

# CREATING A RELATIONSHIP BETWEEEN THE USER AND USER ROLE
        super_admin_role = UserRole.query.filter_by(
            role_name='Super Admin').first()
        user = User(username='superadmin', email='superadmin@example.com',
                    password='secret', role_id=super_admin_role.id)
        db.session.add(user)
        db.session.commit()
        # SUPER ADMIN IS ALREADY CREATED HERE

# CREATING ROLES IN THE DATABASE
        sub_admin_role = UserRole(
            role_name='Sub Admin', role_desc='This user can manage certain aspects of the site')
        visitor_role = UserRole(
            role_name='Visitor', role_desc='This user can only view and interact with this site but cannot make changes')

        db.session.add(sub_admin_role)
        db.session.add(visitor_role)
        db.session.commit()


class Content(db.Model):
    """Content table for storing blog posts"""
    __tablename__ = "content"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.String(300))
    author = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    imagepath = db.Column(db.String(255))

    def __init__(self, title, content, author, timetstamp, imagepath):
        self.title = title
        self.content = content
        self.author = author
        self.timestamp = timetstamp
        self.imagepath = imagepath
# DATABASE MODEL FOR CONTENT


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
