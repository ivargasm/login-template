from datetime import datetime, timedelta
import bcrypt
import jwt
from app.config import SECRET_KEY, SESSION_EXPIRE_MINUTES

# Clave secreta para firmar los tokens
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = SESSION_EXPIRE_MINUTES
RESET_PASSWORD_EXPIRE_MINUTES = 30  # Token válido por 30 minutos

# Eliminar passlib ya que falla con bcrypt >= 4.0
def hash_password(password: str) -> str:
    """Genera un hash seguro de la contraseña."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña ingresada coincide con el hash almacenado."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Genera un token JWT con expiración."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=RESET_PASSWORD_EXPIRE_MINUTES)
    return jwt.encode({"sub": email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str)->dict:
    """Decodifica el JWT y devuelve el payload o lanza una excepción si el token no es válido."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Token inválido")
    
def decode_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # Retorna el email si es válido
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None