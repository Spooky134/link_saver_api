from pydantic import BaseModel

class Collection(BaseModel):
    pass

# class Collection(models.Model):
#       user = models.ForeignKey(User, on_delete=models.CASCADE)
#       name = models.CharField(max_length=30, unique=True)
#       description = models.CharField(max_length=60, blank=True)
#       time_create = models.DateTimeField(auto_now_add=True)
#       time_update = models.DateTimeField(auto_now=True)

#       def __str__(self) -> str:
#             return self.name