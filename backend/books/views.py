
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.db import transaction

from .models import Book, Order, OrderItem


# 1. DISPLAY ALL BOOKS
@require_GET
def book_list(request):
    books = Book.objects.filter(is_available=True)

    data = []

    for book in books:
        data.append({
            "id": book.id,
            "title": book.title,
            "category": book.category,
            "format": book.book_format,
            "price": float(book.price),
            "description": book.description,
            "image": book.image,
        })

    return JsonResponse(data, safe=False)


# 2. CREATE ORDER
@csrf_exempt
@require_POST
def create_order(request):
    try:
        data = json.loads(request.body)

        customer_name = data.get("customer_name", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        address = data.get("address", "").strip()
        items = data.get("items", [])

        if not customer_name or not email or not phone or not address:
            return JsonResponse(
                {"error": "Please fill in all customer details."},
                status=400
            )

        if not items:
            return JsonResponse(
                {"error": "Your cart is empty."},
                status=400
            )

        with transaction.atomic():
            order_items = []
            total_amount = 0

            for item in items:
                book = Book.objects.get(
                    id=item["id"],
                    is_available=True
                )

                quantity = int(item["quantity"])

                if quantity < 1:
                    raise ValueError("Invalid quantity.")

                if book.book_format == "premium_ebook":
                    if data.get("payment_confirmed") is not True:
                        return JsonResponse(
                            {"error": "Payment confirmation is required."},
                            status=400
                        )

                total_amount += book.price * quantity

                order_items.append({
                    "book": book,
                    "quantity": quantity,
                    "price": book.price
                })

            order = Order.objects.create(
                customer_name=customer_name,
                email=email,
                phone=phone,
                address=address,
                total_amount=total_amount
            )

            for item in order_items:
                OrderItem.objects.create(
                    order=order,
                    book=item["book"],
                    quantity=item["quantity"],
                    price=item["price"]
                )

        return JsonResponse({
            "message": "Order placed successfully!",
            "order_id": order.id,
            "total_amount": float(total_amount)
        })

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid request data."},
            status=400
        )

    except (KeyError, ValueError) as error:
        return JsonResponse(
            {"error": str(error)},
            status=400
        )

    except Book.DoesNotExist:
        return JsonResponse(
            {"error": "Book not found."},
            status=404
        )


# 3. CUSTOMER SIGNUP
@csrf_exempt
@require_POST
def signup(request):
    try:
        data = json.loads(request.body)

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")

        if not name or not email or not password:
            return JsonResponse(
                {"error": "Please fill in all fields."},
                status=400
            )

        if len(password) < 6:
            return JsonResponse(
                {"error": "Password must contain at least 6 characters."},
                status=400
            )

        if User.objects.filter(username=email).exists():
            return JsonResponse(
                {"error": "This email is already registered."},
                status=400
            )

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        return JsonResponse({
            "message": "Account created successfully!"
        })

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid request data."},
            status=400
        )


# 4. CUSTOMER LOGIN
@csrf_exempt
@require_POST
def customer_login(request):
    try:
        data = json.loads(request.body)

        email = data.get("email", "").strip()
        password = data.get("password", "")

        if not email or not password:
            return JsonResponse(
                {"error": "Enter your email and password."},
                status=400
            )

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            auth_login(request, user)

            return JsonResponse({
                "message": "Login successful!",
                "name": user.first_name
            })

        return JsonResponse(
            {"error": "Invalid email or password."},
            status=401
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid request data."},
            status=400
        )
