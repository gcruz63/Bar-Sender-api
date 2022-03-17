from django.db import models


class AccountType(models.Model):
    label = models.CharField(max_length=50)

