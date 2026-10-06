from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import ( Boolean, DateTime,
                        Enum as SQLEnum,
                        ForeignKey,
                        String)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class UserRole(str, Enum):
    ADMIN ="admin"
    OFFICE_WORKER = "oworker"
    Worker = "worker"

class Department(str, Enum):
    OPERATIONS ="operation"
    HR ="hr"
    FINANCE ="finance"


class User(Base):

    __tablename__ = "users"
    id: Mapped[int] = mapped_column( primary_key = True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        unique = True,
        nullable = False
    )
    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable = True
    )
    login_id: Mapped[str] = mapped_column(
        String(50),
        unique = True,
        nullable = False,
        index = True
    )
    password_hash : Mapped[str] = mapped_column(
        String(255),
        nullable =False
    )

    must_change_password: Mapped[bool] = mapped_column( Boolean, default = True, nullable = False)

    role : Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name ="user_role"),
        nullable=False
    )
    department: Mapped[Department | None] = mapped_column(
        SQLEnum(Department, name = "user_department"),
        nullable = True
    )
    area_id: Mapped[int | None] = mapped_column(
        ForeignKey("areas.id"),
        nullable =True
    )

    is_active: Mapped[bool] = mapped_column( Boolean, default = True, nullable = False)

    created_by: Mapped[int | None] = mapped_column( ForeignKey("users.id"), nullable = True)

    created_at: Mapped[datetime] = mapped_column(DateTime)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default = lambda: datetime.now(timezone.utc),
        onupdate= lambda : datetime.now(timezone.utc),
        nullable = False
    )

    area = relationship("Area", back_populates= "users")

    created_by_user = relationship("User", remote_side=[id], foreign_keys=[created_by],
                                back_populates = "created_users")

    created_users = relationship("User", foreign_keys = [created_by], back_populates="created_by_user")