from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import DateTime, Enum as SQLEnum, Float, ForeignKey, String, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
class StoreStatus(str, Enum):
    PENDING = "pending"
    APPROVED ="approved"
    Rejected = "rejected"

class Store(Base):
    __tablename__ = "store"
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(150), nullable = False)

    owner_name: Mapped[str] = mapped_column(String(100), nullable = False)
    phone: Mapped[str] = mapped_column(String(13), nullable = False)
    alternate_phone: Mapped[str] = mapped_column(String(13), nullable = False)
    address: Mapped[str | None] = mapped_column(Text, nullable = True)

    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable = False)
    pincode: Mapped[str] = mapped_column(String(6), nullable = False)
    gst_number : Mapped[str | None] = mapped_column(str(20), nullable=True)
    notes : Mapped[str | None] = mapped_column(Text, nullable= True)
    area_id: Mapped[int] = mapped_column(ForeignKey("areas_id"), nullable = False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    status : Mapped[StoreStatus] = mapped_column(SQLEnum(StoreStatus, name="store_status"),
                                                    default=StoreStatus.PENDING, nullable = False)

    reviewed_by : Mapped[int | None] = mapped_column(ForeignKey("user.id"), nullable = True)

    review_note : Mapped[str | None] = mapped_column(Text, nullable = True)
    reviewed_at : Mapped[datetime | None] = mapped_column(DateTime(timezone = True), nullable = True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default = lambda : datetime.now(timezone.utc),
                                                    nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone = True),
                                                default=lambda: datetime.now(timezone.utc),
                                                onupdate=lambda: datetime.now(timezone.utc),
                                                nullable=False)

    area = relationship("Area")
    creator = relationship("User", foreign_keys= created_by)
    reviewer = relationship("User", foreign_keys=reviewed_by)