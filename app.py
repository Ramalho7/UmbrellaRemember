from flask import Flask, render_template, request, redirect, url_for
from models.model import User, engine, City, State
from sqlalchemy.orm import sessionmaker, joinedload
from dotenv import load_dotenv
import os

app=Flask(__name__)

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
    email = request.form['email']
    city_id = request.form['city_id']
    password = request.form['password']
    session = Session()
    new_user = User(name=name, email=email, city_id=city_id, password=password)
    session.add(new_user)
    session.commit()
    session.close()
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    return render_template('profile.html')
