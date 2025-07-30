from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.model import User, City, State
from sqlalchemy.orm import sessionmaker, joinedload
from models.model import engine
import os

DBSession = sessionmaker(bind=engine)

user_bp = Blueprint('user', __name__, template_folder=os.path.abspath('templates/user'))

@user_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db_session = DBSession()
    user = db_session.query(User).options(joinedload(User.city).joinedload(City.state).joinedload(State.country)).get(session['user_id'])
    db_session.close()
    return render_template('profile.html', user=user)