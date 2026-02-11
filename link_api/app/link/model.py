from datetime import datetime
from sqlalchemy import Column, Enum, Integer, String, DateTime, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.link.enum import LinkType
from sqlalchemy import Column, Integer, Table, ForeignKey
from app.core.database import Base


class Link(Base):
    __tablename__ = "link"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=True)
    url: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    image: Mapped[str] = mapped_column(String(500), nullable=True)
    link_type: Mapped[LinkType] = mapped_column(
        Enum(LinkType, native_enum=True),
        default=LinkType.WEBSITE,
        nullable=True,
        index=True
    )

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

    collections = relationship(
        "Collection",
        secondary="link_collection",
        back_populates="links"
    )

    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # # Уникальность URL в рамках одного пользователя
    # __table_args__ = (
    #     UniqueConstraint('url', 'user_id', name='unique_link_per_user'),
    # )

    # owner = relationship("User", back_populates="links")

    def __str__(self):
        return f"{self.url}"



link_collection = Table(
    'link_collection',
    Base.metadata,
    Column('link_id', Integer, ForeignKey('link.id'), primary_key=True),
    Column('collection_id', Integer, ForeignKey('collection.id'), primary_key=True),
    # Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
)