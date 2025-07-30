from models.model import ph
def set_password(self, password_plain):
    self.password = ph.hash(password_plain)