from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    text,
    Text,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base
from app.link.model import LinkModel
from app.user.model import UserModel


class CollectionModel(Base):
    __tablename__ = "collection"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        onupdate=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), index=True
    )

    user: Mapped["UserModel"] = relationship(back_populates="collections")

    links: Mapped[list["LinkModel"]] = relationship(
        secondary="link_collection",
        back_populates="collections",
    )

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="unique_user_collection_name"),
    )

    def __str__(self):
        return f"{self.name}"
