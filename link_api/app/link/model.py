from datetime import datetime
from typing import Optional

from sqlalchemy import Enum, String, DateTime, UniqueConstraint, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.link.enum import LinkType
from sqlalchemy import Column, Integer, Table, ForeignKey, Text
from app.core.database import Base


class LinkModel(Base):
    __tablename__ = "link"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(1024))
    title: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_url: Mapped[Optional[str]] = mapped_column(String(1024))
    link_type: Mapped[LinkType] = mapped_column(
        Enum(LinkType, native_enum=True),
        default=LinkType.WEBSITE,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        onupdate=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True)

    user: Mapped["UserModel"] = relationship(back_populates="links")
    collections: Mapped[list["CollectionModel"]] = relationship(
        secondary="link_collection",
        back_populates="links"
    )

    __table_args__ = (
        UniqueConstraint("user_id", "url", name="unique_user_link_url"),
    )


    def __str__(self):
        return f"{self.url}"