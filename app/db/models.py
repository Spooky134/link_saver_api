from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

link_collection = Table(
    'link_collection',
    Base.metadata,
    Column('link_id', Integer, ForeignKey('links.id'), primary_key=True),
    Column('collection_id', Integer, ForeignKey('collections.id'), primary_key=True)
)


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=True)
    url = Column(String(500), unique=True, nullable=False)
    description = Column(String(500), nullable=True)
    image = Column(String(500), nullable=True)
    link_type = Column(String(20), nullable=True)
    time_create = Column(DateTime, default=datetime.now)
    time_update = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    collections = relationship(
        "Collection",
        secondary=link_collection,
        back_populates="links"
    )

    # # Для связи многие-ко-многим с коллекциями
    # collections = relationship("Collection", secondary=link_collection, back_populates="links")

class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    description = Column(String(500), nullable=True)
    time_create = Column(DateTime, default=datetime.now)
    time_update = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    links = relationship(
        "Link",
        secondary=link_collection,
        back_populates="collections",
    )

# class Collection(models.Model):
#       user = models.ForeignKey(User, on_delete=models.CASCADE)
#       name = models.CharField(max_length=30, unique=True)
#       description = models.CharField(max_length=60, blank=True)
#       time_create = models.DateTimeField(auto_now_add=True)
#       time_update = models.DateTimeField(auto_now=True)

#       def __str__(self) -> str:
#             return self.name


# class Link(models.Model):
#       user = models.ForeignKey(User, on_delete=models.CASCADE)
#       title = models.CharField(max_length=100)
#       description = models.CharField(max_length=400)
#       url = models.URLField()
#       image = models.ImageField(upload_to=user_derictory_path, blank=True)
#       link_type = models.CharField(max_length=10)
#       time_create = models.DateTimeField(auto_now_add=True)
#       time_update = models.DateTimeField(auto_now=True)
#       collection = models.ManyToManyField(Collection)

#       class Meta:
#             constraints = [
#                   models.UniqueConstraint(fields=['user', 'url'], name='unique_user_url')
#                   ]
      
#       def user_derictory_path(self, instance, name):
#             current_date = datetime.date.today()
#             date_string = current_date.strftime("/%Y%m%d/")
#             return f'user_{instance.user.id}/{date_string}/{name}'

#       def __str__(self) -> str:
#             return self.title