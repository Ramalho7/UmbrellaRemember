from typing import Optional, Type
from models.model import User
from models.check_password import check_password
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

def login_verify(session: Session, email: str, password: str, user_model: Type[User]) -> Optional[User]:
    try:
        user = session.query(user_model).filter_by(email=email).first()
        if user and check_password(user, password):
            return user
        return None
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return None