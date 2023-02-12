from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class NewUser(models.Model):
    UserName = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    confirmPassword = models.CharField(max_length=50)

    REQUIRED_FIELDS = ['username', 'email', 'password']
    USERNAME_FIELD = 'username'


class NewProduct(models.Model):
    itemClass = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    model = models.CharField(max_length=50, null=False, blank=False)
    quantity = models.PositiveIntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)], blank=False)
    price_per_piece = models.PositiveIntegerField(null=False, blank=False)
    stock_date = models.DateField(auto_now_add=True)
    ready_to_load = models.BooleanField(default=False)

    def __str__(self):
        return self.itemClass + ", " + self.name + ", " + self.model + ", " + str(self.quantity) + ", " + \
               str(self.price_per_piece) + ", " + str(self.stock_date)
