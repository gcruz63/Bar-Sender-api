from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    account_type = models.ForeignKey('AccountType', on_delete=models.CASCADE)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=300)
