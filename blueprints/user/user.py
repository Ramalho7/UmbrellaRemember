from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models.model import User, City, State
from sqlalchemy.orm import sessionmaker, joinedload
from models.model import engine
import os
from utils.set_password import set_password
from utils.email_exists import email_exists
from models.update_user import update_user
from flask_login import current_user, login_required, login_user

DBSession = sessionmaker(bind=engine)

user_bp = Blueprint('user', __name__, template_folder=os.path.abspath('templates/user'))

@user_bp.route('/profile')
@login_required
def profile():
    db_session = DBSession()
    user = db_session.query(User).options(joinedload(User.city).joinedload(City.state).joinedload(State.country)).get(current_user.id)
    db_session.close()
    return render_template('profile.html', user=user)

@user_bp.route("/register")
def registerPage():
    db_session = DBSession()
    cities = db_session.query(City).options(joinedload(City.state)).order_by(City.city_name).all()
    return render_template('register.html', cities=cities)

@user_bp.route("/registeruser", methods=["POST"])
def registeruser():
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
    set_password(new_user, password)
    db_session.add(new_user)
    db_session.commit()
    login_user(new_user)
    db_session.close()
    flash("Cadastro realizado com sucesso!", "success")
    return redirect(url_for('user.profile'))

@user_bp.route("/edituser")
@login_required
def editUserPage():
    db_session = DBSession()
    cities = db_session.query(City).options(joinedload(City.state)).order_by(City.city_name).all()
    user = db_session.query(User).options(joinedload(User.city).joinedload(City.state)).get(current_user.id)
    db_session.close()
    return render_template('editUserPage.html',user=user, cities=cities)

@user_bp.route("/updateuser", methods=["POST"])
@login_required
def updateUser():
    name = request.form['name']
    email = request.form['email'].strip()
    city_id = request.form['city_id']
    db_session = DBSession()
    update_user(db_session, current_user.id, name=name, email=email, city_id=city_id)
    db_session.close()
    flash("Dados atualizados com sucesso!", "success")
    return redirect(url_for('user.profile'))

@user_bp.route("/deleteAccount", methods=["POST"])
@login_required
def deleteAccount():
    db_session = DBSession()
    user = db_session.query(User).get(current_user.id)
    if user:
        db_session.delete(user)
        db_session.commit()
        session.clear()
        flash("Conta excluída com sucesso!", "success")
    db_session.close()
    return redirect(url_for('index_page'))
