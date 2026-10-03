from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    supplier = models.ForeignKey("Supplier",on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100,unique = True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100,unique = True)
    contact_email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name