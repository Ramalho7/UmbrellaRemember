from models.model import User
from sqlalchemy.orm import Session

def login_verify(session: Session, email: str, password: str):
    user = session.query(User).filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None