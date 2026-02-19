from datetime import datetime
from sqlalchemy import String, DateTime, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        onupdate=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
    )

    links: Mapped[list["LinkModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    collections: Mapped[list["CollectionModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )