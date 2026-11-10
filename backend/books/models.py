from django.db import models


class Book(models.Model):

    CATEGORY_CHOICES = [
        ('children', "Children's Books"),
        ('fiction', 'Fiction & Novels'),
        ('educational', 'Educational'),
        ('technology', 'Programming & Technology'),
        ('competitive', 'Competitive Exams'),
        ('motivational', 'Motivation & Personal Growth'),
    ]

    FORMAT_CHOICES = [
        ('physical', 'Physical Book'),
        ('free_ebook', 'Free eBook'),
        ('premium_ebook', 'Premium eBook'),
    ]

    title = models.CharField(max_length=200)

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    book_format = models.CharField(
        max_length=20,
        choices=FORMAT_CHOICES
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    description = models.TextField(blank=True)

    image = models.CharField(max_length=255, blank=True)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.book.title
