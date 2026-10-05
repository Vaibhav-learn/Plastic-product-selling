from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import ( Boolean, DateTime,
                        Enum as SQLEnum,
                        ForeignKey,
                        String)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class USER_ROLE(str, Enum):
    ADMIN ="admin"
    OFFICE_WORKER = "oworker"
    Worker = "worker"

class DEPARTMENT(str, Enum):
    OPERATIONS ="operation"
    HR ="hr"
    FINANCE ="finance"


