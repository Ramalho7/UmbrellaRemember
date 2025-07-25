from models.model import User

def email_exists(session, email):
    return session.query(User).filter_by(email=email).first() is not None