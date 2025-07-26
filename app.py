from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from models.model import User, engine, City, State
from sqlalchemy.orm import sessionmaker, joinedload
from dotenv import load_dotenv
from datetime import datetime
import os
from utils.email_exists import email_exists
from utils.login_verify import login_verify
from models.get_user_by_id import get_user_by_id
from models.update_user import update_user


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

@app.route("/update")
def editUserPage():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db_session = DBSession()
    cities = db_session.query(City).options(joinedload(City.state)).order_by(City.city_name).all()
    user = db_session.query(User).options(joinedload(User.city).joinedload(City.state)).get(session['user_id'])
    db_session.close()
    return render_template('editUserPage.html',user=user, cities=cities)

@app.route("/updateUser", methods=["POST"])
def updateUser():
    name = request.form['name']
    email = request.form['email'].strip()
    city_id = request.form['city_id']
    db_session = DBSession()
    update_user(db_session, session['user_id'], name=name, email=email, city_id=city_id)
    db_session.close()
    flash("Dados atualizados com sucesso!", "success")
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db_session = DBSession()
    user = db_session.query(User).options(joinedload(User.city).joinedload(City.state).joinedload(State.country)).get(session['user_id'])
    db_session.close()
    return render_template('profile.html', user=user)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email'].strip()
        password = request.form['password']
        db_session = DBSession()
        user = login_verify(db_session, email, password)
        db_session.close()
        if user:
            session['user_id'] = user.id
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('profile'))
        else:
            flash("Email ou senha inválidos", "error")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
