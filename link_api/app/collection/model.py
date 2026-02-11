from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base


class Collection(Base):
    __tablename__ = "collection"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[int] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        onupdate=text("TIMEZONE('utc', CURRENT_TIMESTAMP)")
    )

    links = relationship(
        "Link",
        secondary="link_collection",
        back_populates="collections",
    )

    def __str__(self):
        return f"{self.name}"

    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # # Уникальность имени коллекции для пользователя
    # __table_args__ = (
    #     UniqueConstraint('name', 'user_id', name='unique_collection_name_per_user'),
    # )

    # # Связи
    # owner = relationship("User", back_populates="collections")