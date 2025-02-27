from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import CustomUser, Product, Cart, Order
from .utils import send_verification_email
from .forms import UserProfileForm


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
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products, 'user': request.user})


def custom_logout(request):
    logout(request)
    return redirect("home")


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('home')


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_cost = sum(item.total_price() for item in cart_items)

    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_cost': total_cost})


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


@login_required
def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_cost = sum(item.total_price() for item in cart_items)

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            cart_items=[{'product_id': item.product.id, 'quantity': item.quantity} for item in cart_items],
            total_cost=total_cost
        )

        cart_items.delete()

        return redirect('home')

    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items,
        'total_cost': total_cost
    })


def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if 'password' in request.POST and request.POST['password']:
                user.set_password(request.POST['password'])
                user.save()
                update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'shop/profile.html', {'form': form})
