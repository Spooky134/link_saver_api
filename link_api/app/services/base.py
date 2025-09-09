from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.enums import LinkType
from app.db.repositories.link import LinkRepository
from app.db.repositories.collection import CollectionRepository
from link_api.app.db.models.link import Link
from app.api.schemas.link import LinkCreate, LinkUpdate
# from ..exceptions import NotFoundError, ValidationError
# from app.utils.parser import LinkInfoParser
from pydantic import BaseModel, Field, HttpUrl, field_validator
from app.exceptions.exceptions import ValidationError, NotFoundError
from asyncio import to_thread



class BaseService:
    def __init__(self, db: AsyncSession):
        pass
