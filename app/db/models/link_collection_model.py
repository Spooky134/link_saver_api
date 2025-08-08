from sqlalchemy import Column, Integer, Table, ForeignKey
from app.config.database import Base


link_collection = Table(
    'link_collection',
    Base.metadata,
    Column('link_id', Integer, ForeignKey('links.id'), primary_key=True),
    Column('collection_id', Integer, ForeignKey('collections.id'), primary_key=True),
    # Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
)