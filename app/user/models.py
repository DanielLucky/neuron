from sqlalchemy import Column, Integer, String, DateTime, func

from database.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


