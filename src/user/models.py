from sqlalchemy import Column, String, Integer, DateTime, Boolean
from src.utils.db import Base


class UserModel(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key = True, autoincrement=True)
    name = Column(String(255))
    username = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255))