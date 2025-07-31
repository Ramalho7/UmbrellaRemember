from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from models.model import User, engine, City, State
from sqlalchemy.orm import sessionmaker, joinedload
from dotenv import load_dotenv
from datetime import datetime
import os
from utils.email_exists import email_exists
from utils.login_verify import login_verify
from models.update_user import update_user
from utils.set_password import set_password
from blueprints.user import user_bp
from blueprints.auth import auth_bp
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

DBSession = sessionmaker(bind=engine)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login'

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(auth_bp, url_prefix='/auth')

@lm.user_loader
def user_loarder(id):
    db_session = DBSession()
    user = db_session.query(User).get(int(id))
    db_session.close()
    return user

@app.route('/', methods=["GET","POST"])
def index_page():
    dbsession = DBSession()
    cities = dbsession.query(City).options(joinedload(City.state)).order_by(City.city_name).all()
    dbsession.close()
    return render_template('index.html', cities=cities)

if __name__ == "__main__":
    app.run(debug=True)
