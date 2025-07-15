from datetime import datetime
from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db import Base
from app.config import SCHEMA

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # Ejemplo: "user", "admin"

    users = relationship("User", back_populates="role")  # Relación inversa

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("login.roles.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())  # Fecha de creación
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Última actualización

    role = relationship("Role")  # Relación con la tabla de roles