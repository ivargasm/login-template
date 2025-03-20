from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from sqlalchemy.orm import Session

from app.routes import auth

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],  # Orígenes permitidos (Frontend)
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Métodos permitidos (GET, POST, etc.)
    allow_headers=["*"],  # Encabezados permitidos
)


app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])



@app.get("/")
def read_root():
    return {"message": "Login"}