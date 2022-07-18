import json

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, LargeBinary,  func
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base


class Picture(Base):
    __tablename__ = "picture"

    id = Column(Integer, primary_key=True)
    id_slack = Column(String(length=36), nullable=True)
    picture = Column(LargeBinary, nullable=True)
    picture_path = Column(String(255), nullable=True)  # TODO:изменить на false
    format = Column(String(length=10), nullable=True)

    quality = Column(Integer, nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    def to_json(self):
        data = {
            'id': str(self.id_slack),
            'format': self.format,
            'quality': self.quality,
            'width': self.width,
            'height': self.height,
            'created_at': str(self.created_at)
        }
        return json.dumps(data)
