from sqlalchemy import select
from app.core.config import settings
from app.core.database import SessionLocal

from app.core.security import hash_password
from app.models.user import User, UserRole

def create_initial_admin():
    db = SessionLocal()

    try:
        statement = select(User).where(
            User.login_id == settings.INITIAL_ADMIN_LOGIN_ID
        )
        existing_admin = db.scalar(statement)

        if existing_admin is not None:
            print("Initial admin already exists.")
            return

        password_hash = hash_password(
            settings.INITIAL_ADMIN_PASSWORD
        )

        admin = User(
            name = settings.INITIAL_ADMIN_NAME,
            phone = settings.INITIAL_ADMIN_PHONE,
            email = None,
            login_id = settings.INITIAL_ADMIN_LOGIN_ID,
            password_hash = password_hash,
            must_change_password = False,

            role = UserRole.ADMIN,
            department = None,
            area_id = None,
            is_active = True,
            created_by= None,
        )
        db.add(admin)
        db.commit()
        print("Initial admin created successfully.")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_initial_admin()