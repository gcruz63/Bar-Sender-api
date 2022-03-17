from django.db import models
from Bar_Sender_api.models.my_user import MyUser


class Store(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    my_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
