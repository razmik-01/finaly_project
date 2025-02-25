from django.urls import path
from .views import register, verify_email, user_login, home, custom_logout
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views

urlpatterns = [
                  path('', home, name='home'),
                  path("login/", user_login, name="login"),
                  path('logout/', custom_logout, name='custom_logout'),
                  path("register/", register, name="register"),
                  path("verify_email/", verify_email, name="verify_email"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
