from models.model import User
from models.check_password import check_password
from sqlalchemy.orm import Session

def login_verify(session: Session, email: str, password: str):
    user = session.query(User).filter_by(email=email).first()
    if user and check_password(user, password):
        return user
    return None