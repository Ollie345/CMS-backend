from app.views import views_blueprint
from app.auth import auth_blueprint
from flask import Flask
from .extensions import db
from flask_login import LoginManager

app = Flask(__name__)  # INSTANCE OF THE APP


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Oregunwa_19@localhost/users'
# app.config['SECRET_KEY'] = 'thisisasecretkey'
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


app.register_blueprint(auth_blueprint)
app.register_blueprint(views_blueprint)

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
