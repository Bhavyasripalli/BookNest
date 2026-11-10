# BookNest – Online Bookstore

**Tagline:** Read • Dream • Grow

## Project Description
BookNest is a simple online bookstore developed as part of the CodeAlpha internship project. It allows users to browse books, search by title, filter by category, add books to a shopping cart, and place orders.

## Technologies Used
- HTML
- CSS
- JavaScript
- Python
- Django
- SQLite Database

## Features
- User registration and login
- Book listings from the database
- Search and category filters
- Shopping cart
- Checkout and order processing
- Django Admin for managing books and orders

## Book Categories
- Children's Books
- Fiction & Novels
- Educational
- Programming & Technology
- Competitive Exams
- Motivation & Personal Growth

## How to Run the Project

### 1. Start the Django Backend
Open a terminal:

```powershell
cd backend
python manage.py runserver
```

### 2. Start the Frontend
Open another terminal in the main BookNest folder:

```powershell
python -m http.server 5500
```

### 3. Open the Website
Visit:

http://127.0.0.1:5500/index.html

### Django Admin
http://127.0.0.1:8000/admin/

## Note
This project uses a local development server and SQLite database. Payment processing is a demonstration and does not collect real payments.

## Developed For
CodeAlpha Internship – Task 1: Simple E-commerce Store