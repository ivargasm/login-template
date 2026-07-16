#!/bin/bash

# Asegurar que el script se detenga si algo falla
set -e

echo "⏳ Esperando a que la base de datos esté lista..."
# uv run python -c "from app.db import engine; engine.connect()" podria ser usado aquí si se necesita esperar.

echo "⚙️  Creando schema de la base de datos si no existe..."
uv run python -m app.pre_start

echo "🔄 Ejecutando migraciones de Alembic..."
uv run alembic upgrade head

echo "🌱 Sembrando roles por defecto en la base de datos..."
uv run python -m app.seed_roles

echo "🚀 Iniciando servidor FastAPI..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
