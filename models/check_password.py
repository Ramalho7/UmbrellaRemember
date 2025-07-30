from models.model import ph

def check_password(self, password_plain):
    try:
        return ph.verify(self.password, password_plain)
    except Exception:
        return False