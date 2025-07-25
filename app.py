from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from models.model import User, engine, City, State
from sqlalchemy.orm import sessionmaker, joinedload
from dotenv import load_dotenv
from datetime import datetime
import os
from utils.email_exists import email_exists
from utils.login_verify import login_verify
from utils.get_user_by_id import get_user_by_id


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

DBSession = sessionmaker(bind=engine)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/', methods=["GET","POST"])
def index_page():
    session = DBSession()
    cities = session.query(City).options(joinedload(City.state)).order_by(City.city_name).all()
    session.close()
    return render_template('index.html', cities=cities)

@app.route('/register', methods=["POST"])

def registerUser():
    name = request.form['name']
    email = request.form['email'].strip()
    city_id = request.form['city_id']
    password = request.form['password']
    db_session = DBSession()
    if email_exists(db_session, email):
        db_session.close()
        flash("E-mail já cadastrado!", "error")
        return redirect(url_for('index_page'))
    new_user = User(name=name, email=email, city_id=city_id)
    new_user.set_password(password)
    db_session.add(new_user)
    db_session.commit()
    user_id = new_user.id
    db_session.close()
    session['user_id'] = user_id
    return redirect(url_for('profile'))

@app.route('/profile')

def profile():
    session_db = DBSession()
    user = get_user_by_id(session_db, session['user_id'])
    session_db.close()
    return render_template('profile.html', user=user)

@app.route('/login', methods=["GET", "POST"])

def login():
    if request.method == "POST":
        email = request.form['email'].strip()
        password = request.form['password']
        session_db = DBSession()
        user = login_verify(session_db, email, password)
        session_db.close()
        if user:
            session['user_id'] = user.id
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('profile'))
        else:
            flash("Email ou senha inválidos", "error")
            return redirect(url_for('login'))
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
