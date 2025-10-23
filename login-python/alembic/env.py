from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.db import Base, engine
from app.config import DATABASE_URL, SCHEMA

# Importa tus modelos aquí
from app.models import Role, User  # Asegúrate de importar todos los modelos

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Obtener la URL de la base de datos desde variables de entorno
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def include_name(name, type_, parent_names):
    """
    Filtra los objetos de la base de datos para que Alembic solo
    considere aquellos dentro del esquema 'contracts'.
    """
    if type_ == "schema":
        # Incluye solo el esquema 'contracts' en la comparación
        return name in [SCHEMA]
    else:
        # Para todos los demás objetos (tablas, índices, etc.),
        # solo los incluye si pertenecen al esquema 'contracts'.
        return parent_names.get("schema_name") in [SCHEMA]


def run_migrations_offline():
    """Ejecuta migraciones en modo offline."""
    # url = config.get_main_option("sqlalchemy.url")
    context.configure(
        # url=url,
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,  # Asegúrate de incluir todos los esquemas
        version_table_schema=SCHEMA,  # Especificar el esquema donde está la tabla de versiones de Alembic
        include_name=include_name
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Ejecuta migraciones en modo online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,  # Asegúrate de incluir todos los esquemas
            version_table_schema=SCHEMA,  # Especificar el esquema donde está la tabla de versiones de Alembic
            include_name=include_name
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
