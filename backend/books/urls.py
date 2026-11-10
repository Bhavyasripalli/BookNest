
from django.urls import path
from . import views

urlpatterns = [
    # Display books
    path('books/', views.book_list, name='book_list'),

    # Place customer orders
    path('orders/', views.create_order, name='create_order'),

    # Customer registration
    path('signup/', views.signup, name='signup'),

    # Customer login
    path('login/', views.customer_login, name='customer_login'),
]
