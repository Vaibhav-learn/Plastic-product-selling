from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class Area(Base):
    __tablename__ = "areas"
    #name of the table

    id: Mapped[int] = mapped_column(
        primary_key = True
    )
    #ensuring each area has unique id

    name : Mapped[str] = mapped_column(
        String(100),
        unique = True,
        nullable = False
    )
    #adding the name on the area

    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default = lambda : datetime.now(timezone.utc),
        nullable = False
    )
    # time when the record was created
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable = False
    )

    users = relationship("User", back_populates="area")