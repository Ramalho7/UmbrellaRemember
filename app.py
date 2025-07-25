from flask import Flask, render_template, request, redirect, url_for, flash
from models.model import User, engine, City, State
from sqlalchemy.orm import sessionmaker, joinedload
from dotenv import load_dotenv
from datetime import datetime
import os
from utils.email_exists import email_exists

load_dotenv()

app=Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_secret_key")

Session = sessionmaker(bind=engine)

@app.route('/', methods=["GET","POST"])
def index_page():
    session = Session()
    cities = session.query(City).options(joinedload(City.state)).order_by(City.city_name).all()
    session.close()
    return render_template('index.html', cities=cities)

@app.route('/register', methods=["POST"])
def registerUser():
    name = request.form['name']
    email = request.form['email'].strip()
    city_id = request.form['city_id']
    password = request.form['password']
    session = Session()
    if email_exists(session, email):
        session.close()
        flash("E-mail já cadastrado!", "error")
        return redirect(url_for('index_page'))
    new_user = User(name=name, email=email, city_id=city_id)
    new_user.set_password(password)
    session.add(new_user)
    session.commit()
    session.close()
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == "__main__":
    app.run(debug=True)
