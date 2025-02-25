from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.utils.timezone import now
from .models import CustomUser, Product
from .utils import send_verification_email


def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_email_verified:
            login(request, user)

            return redirect("home")
        else:
            return render(request, "shop/login.html", {"error": "Неверный email или пароль, или email не подтверждён."})

    return render(request, "shop/login.html")


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        phone = request.POST["phone"]
        username = request.POST["username"]

        user = CustomUser.objects.create_user(
            username=username, email=email, phone_number=phone, password=password
        )
        user.generate_verification_code()
        send_verification_email(user)

        return redirect("verify_email")
    return render(request, "shop/register.html")


def verify_email(request):
    if request.method == "POST":
        email = request.POST["email"]
        code = request.POST["code"]
        user = CustomUser.objects.filter(email=email).first()

        if user and user.email_verification_code == code and now() <= user.email_verification_expires:
            user.is_email_verified = True
            user.email_verification_code = None
            user.email_verification_expires = None
            user.save()
            login(request, user)
            return redirect("home")

        return render(request, "shop/verify_email.html", {"error": "Неверный или просроченный код"})

    return render(request, "shop/verify_email.html")


def home(request):
    products = Product.objects.all()  # Получаем все товары
    return render(request, 'shop/home.html', {'products': products, 'user': request.user})


def custom_logout(request):
    logout(request)
    return redirect("home")
