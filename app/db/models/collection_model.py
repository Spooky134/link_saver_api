from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from app.config.database import Base
from sqlalchemy.orm import relationship
from app.db.models.link_collection_model import link_collection


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    description = Column(String(500), nullable=True)
    time_create = Column(DateTime, default=datetime.now)
    time_update = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    links = relationship(
        "Link",
        secondary=link_collection,
        back_populates="collections",
    )


    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # # Уникальность имени коллекции для пользователя
    # __table_args__ = (
    #     UniqueConstraint('name', 'user_id', name='unique_collection_name_per_user'),
    # )
    
    # # Связи
    # owner = relationship("User", back_populates="collections")