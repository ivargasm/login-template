from sqlalchemy.orm import Session
from app.models import User, Role
from app.schemas import ForgotPasswordRequest, UserCreate
from app.services.auth import hash_password

def get_user_by_email(db: Session, email: ForgotPasswordRequest):
    """ Obtiene un usuario por su email """
    return db.query(User).filter(User.email == email).first()

def get_role_by_name(db: Session, role_name: str):
    """ Obtiene un rol por su nombre """
    return db.query(Role).filter(Role.name == role_name).first()

def create_user(db: Session, user: UserCreate, role_name: str = "user"):
    """ Crea un nuevo usuario con un rol determinado """
    hashed_password = hash_password(user.password)

    # Buscar si el rol existe, si no, asignar "user" por defecto
    role = get_role_by_name(db, role_name)
    if not role:
        role = get_role_by_name(db, "user")

    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        username=user.username,
        role_id=role.id  # Ahora asignamos el ID del rol
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_password(db: Session, user: User, new_hashed_password: str):
    user.hashed_password = new_hashed_password
    db.commit()
    db.refresh(user)
