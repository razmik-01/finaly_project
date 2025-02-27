from django.urls import path
from .views import (register, verify_email, user_login, home, custom_logout, add_to_cart,
                    cart_view, remove_from_cart, checkout_view, profile_view)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views

urlpatterns = [
                  path('', home, name='home'),
                  path("login/", user_login, name="login"),
                  path('logout/', custom_logout, name='custom_logout'),
                  path("register/", register, name="register"),
                  path("verify_email/", verify_email, name="verify_email"),
                  path('cart/', cart_view, name='cart'),
                  path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
                  path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
                  path('checkout/', checkout_view, name='checkout'),
                  path('profile/', profile_view, name='profile')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
