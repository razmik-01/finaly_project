from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Product)
# Register your models here.
