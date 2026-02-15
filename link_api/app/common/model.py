from sqlalchemy import Column, Integer, Table, ForeignKey
from app.core.database import Base


link_collection = Table(
    'link_collection',
    Base.metadata,
    Column('link_id', Integer,ForeignKey('link.id', ondelete="CASCADE"), primary_key=True),
    Column('collection_id', Integer,ForeignKey('collection.id', ondelete="CASCADE"),  primary_key=True)
)