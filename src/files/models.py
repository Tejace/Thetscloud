from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    ForeignKey,
    DateTime,
)
from sqlalchemy.sql import func

from src.utils.db import Base


class FileModel(Base):
    __tablename__ = "file_table"

    id = Column(Integer, primary_key=True, autoincrement=True)

    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), unique=True, nullable=False)

    content_type = Column(String(100), nullable=True)
    size = Column(BigInteger, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("user_table.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )