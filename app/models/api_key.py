from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from datetime import datetime

from app.core.database import Base


class APIKey(Base):

    __tablename__ = "api_keys"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    developer_email = Column(
        String,
        nullable=False
    )

    hashed_key = Column(
        String,
        unique=True,
        nullable=False
    )

    tier = Column(
        String,
        default="free"
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )