from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def get_password_encrypted(password):
    return pwd_context.hash(password)