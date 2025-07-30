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
from models.set_password import set_password
from blueprints.user import user_bp
from blueprints.auth import auth_bp


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

DBSession = sessionmaker(bind=engine)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/', methods=["GET","POST"])
def index_page():
    session = DBSession()
    cities = session.query(City).options(joinedload(City.state)).order_by(City.city_name).all()
    session.close()
    return render_template('index.html', cities=cities)

if __name__ == "__main__":
    app.run(debug=True)
