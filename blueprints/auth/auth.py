from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.model import User
from utils.login_verify import login_verify
from sqlalchemy.orm import sessionmaker
from models.model import engine
import os
from flask_login import login_user, logout_user

DBSession = sessionmaker(bind=engine)

auth_bp = Blueprint('auth', __name__, template_folder=os.path.abspath('templates/auth'))

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email'].strip()
        password = request.form['password']
        db_session = DBSession()
        user = login_verify(db_session, email, password, User)
        db_session.close()
        if not user:
            flash("Email ou senha inválidos", "error")
            return redirect(url_for('auth.login'))
        login_user(user)
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for('user.profile'))
            
    return render_template('login.html')

@auth_bp.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect('/')