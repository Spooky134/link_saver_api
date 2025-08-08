from datetime import datetime
from sqlalchemy import Column, Enum, Integer, String, DateTime, ForeignKey, UniqueConstraint
from app.config.database import Base
from sqlalchemy.orm import relationship
from app.api.schemas.enums import LinkType
from app.db.models.link_collection_model import link_collection



class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=True)
    url = Column(String(500), unique=True, nullable=False)
    description = Column(String(500), nullable=True)
    image = Column(String(500), nullable=True)
    link_type = Column(Enum(LinkType), nullable=True)
    time_create = Column(DateTime, default=datetime.now)
    time_update = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    collections = relationship(
        "Collection",
        secondary=link_collection,
        back_populates="links"
    )

    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # # Уникальность URL в рамках одного пользователя
    # __table_args__ = (
    #     UniqueConstraint('url', 'user_id', name='unique_link_per_user'),
    # )

    # owner = relationship("User", back_populates="links")
