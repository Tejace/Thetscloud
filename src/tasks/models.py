from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from src.utils.db import Base


class TaskModel(Base):
    __tablename__ = "test_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    desctiption = Column(String(50))
    completed = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("user_table.id", ondelete="CASCADE"))