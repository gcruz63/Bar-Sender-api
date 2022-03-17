from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    store = models.ForeignKey(
        "Store", on_delete=models.CASCADE, related_name='products')
    price = models.FloatField(validators=[
        MinValueValidator(0.00), MaxValueValidator(10000.00)])
    description = models.TextField()
    quantity = models.IntegerField()
    image_path = models.ImageField(upload_to='products', height_field=None,
                                   width_field=None, max_length=None, null=True, blank=True)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name='products')

    def save(self, *args, **kwargs):
        self.clean_fields()
        super().save(*args, **kwargs)

    @property
    def number_purchased(self):
        """Returns the number of times product shows up on completed orders
        """
        return self.orders.exclude(payment_type=None).count()

    def __str__(self):
        return self.name
