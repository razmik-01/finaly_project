from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.timezone import now, timedelta


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=15, unique=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    email_verification_expires = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    def generate_verification_code(self):
        self.email_verification_code = get_random_string(length=6, allowed_chars='1234567890')
        self.email_verification_expires = now() + timedelta(minutes=30)
        self.save()


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    image = models.ImageField(upload_to='products/', verbose_name="Image", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date added")

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.quantity})"


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart_items = models.JSONField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'