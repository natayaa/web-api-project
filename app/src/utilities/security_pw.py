from passlib.context import CryptContext

class SecurityPassword:
    def __init__(self):
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, password, hashed_password):
        return self.password_context.verify(password, hashed_password)