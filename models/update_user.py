from sqlalchemy import update
from models.model import User

def update_user(session, user_id, **kwargs):
    session.query(User).filter_by(id=user_id).update(kwargs)
    session.commit()

