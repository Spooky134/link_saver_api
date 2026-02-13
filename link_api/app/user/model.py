from datetime import datetime
from sqlalchemy import Column, Enum, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from sqlalchemy import Column, Integer, Table, ForeignKey
from app.core.database import Base


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))

    links: Mapped[list["LinkModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    collections: Mapped[list["CollectionModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )