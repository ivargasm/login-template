import logging
from app.db import SessionLocal
from app.models import Role

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_default_roles() -> None:
    db = SessionLocal()
    try:
        # Revisa si los roles base existen
        roles_to_seed = ["admin", "user"]
        
        for role_name in roles_to_seed:
            existing_role = db.query(Role).filter(Role.name == role_name).first()
            if not existing_role:
                logger.info(f"Role '{role_name}' no existe. Creándolo...")
                new_role = Role(name=role_name)
                db.add(new_role)
            else:
                logger.info(f"Role '{role_name}' ya existe.")
        
        db.commit()
        logger.info("Roles inicializados correctamente.")
    except Exception as e:
        logger.error(f"Error insertando roles: {e}")
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_default_roles()
