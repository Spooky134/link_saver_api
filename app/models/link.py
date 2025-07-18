


# class Collection(models.Model):
#       user = models.ForeignKey(User, on_delete=models.CASCADE)
#       name = models.CharField(max_length=30, unique=True)
#       description = models.CharField(max_length=60, blank=True)
#       time_create = models.DateTimeField(auto_now_add=True)
#       time_update = models.DateTimeField(auto_now=True)

#       def __str__(self) -> str:
#             return self.name


class Link(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      title = models.CharField(max_length=100)
      description = models.CharField(max_length=400)
      url = models.URLField()
      image = models.ImageField(upload_to=user_derictory_path, blank=True)
      link_type = models.CharField(max_length=10)
      time_create = models.DateTimeField(auto_now_add=True)
      time_update = models.DateTimeField(auto_now=True)
      collection = models.ManyToManyField(Collection)

      class Meta:
            constraints = [
                  models.UniqueConstraint(fields=['user', 'url'], name='unique_user_url')
                  ]
      
      def user_derictory_path(self, instance, name):
            current_date = datetime.date.today()
            date_string = current_date.strftime("/%Y%m%d/")
            return f'user_{instance.user.id}/{date_string}/{name}'

      def __str__(self) -> str:
            return self.title