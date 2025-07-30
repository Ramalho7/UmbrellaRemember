from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.model import User
from utils.login_verify import login_verify
from sqlalchemy.orm import sessionmaker
from models.model import engine
import os

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
        if user:
            session['user_id'] = user.id
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('user.profile'))
        else:
            flash("Email ou senha inválidos", "error")
            return redirect(url_for('login'))
    return render_template('login.html')

@auth_bp.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect('/')