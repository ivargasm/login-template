from fastapi import APIRouter, Depends, HTTPException, Request, Response, BackgroundTasks
from fastapi.responses import JSONResponse
import jwt
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User, Role
from app.schemas import ForgotPasswordRequest, ResetPasswordRequest, UserCreate, UserLogin, UserResponse
from app.services.auth import create_reset_token, decode_access_token, decode_reset_token, hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.crud import get_user_by_email, get_role_by_name, update_user_password
from app.services.email import send_reset_email

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Registro de usuario con rol
@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Buscar si el rol "user" ya existe, si no, asignarlo
    role = get_role_by_name(db, "user")
    if not role:
        raise HTTPException(status_code=500, detail="Rol por defecto no encontrado")

    nuevo_usuario = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        username=user_data.username,
        role_id=role.id
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return UserResponse(
        id=nuevo_usuario.id,
        username=nuevo_usuario.username,
        email=nuevo_usuario.email,
        role=nuevo_usuario.role.name  # ✅ Convertimos el objeto Role a string
    )

# Login de usuario
@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):

    usuario = db.query(User).filter(User.email == user_data.email).first()
    if not usuario or not verify_password(user_data.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    access_token = create_access_token(data={"sub": usuario.email})

    response = Response()
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # 🔥 Evita acceso con JavaScript
        secure=True,  # 🔒 Solo se envía por HTTPS
        samesite="Lax",  # ⚠️ Ajusta según necesidad "Lax" para desarrollo, "None" para producción
    )
    return response

@router.get("/me", response_model=UserResponse)
def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No autenticado")

    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Token inválido")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = db.query(User).filter(User.email == email).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return UserResponse(
        id=usuario.id,
        username=usuario.username,
        email=usuario.email,
        role=usuario.role.name  # ✅ Convertimos el objeto Role a string
    )


# Obtener usuario admin
def get_admin_user(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado, solo administradores")
    return user

# cerra sesión
@router.post("/logout")
def logout(response: Response):
    response = JSONResponse(content={"message": "Logout exitoso"})
    response.delete_cookie("access_token")
    return response


@router.post("/forgot-password")
def forgot_password(email: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    print("Email recibido:", email)
    user = get_user_by_email(db, email.email)

    if not user:
        return {"message": "Si el correo está registrado, recibirás un enlace para restablecer tu contraseña."}

    reset_token = create_reset_token(email.email)

    # Enviar email en segundo plano para no bloquear la respuesta de la API
    background_tasks.add_task(send_reset_email, email.email, reset_token)

    return {"message": "Se ha enviado un enlace de recuperación a tu correo."}


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    email = decode_reset_token(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")

    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    hashed_password = hash_password(request.new_password)
    update_user_password(db, user, hashed_password)

    return {"message": "Contraseña restablecida correctamente"}


