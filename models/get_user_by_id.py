from models.model import User
from sqlalchemy.orm import Session

def get_user_by_id(session, user_id):
    return session.query(User).get(user_id)