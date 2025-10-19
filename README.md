Task Manager API

A Django REST Framework backend API for managing tasks. Users can create, update, delete, and mark tasks as complete or incomplete. The API supports categories, task history, collaborative tasks, filters, sorting, and notifications for due tasks.

Table of Contents

Features

Getting Started

Installation

API Endpoints

Authentication

Notifications

Filters and Sorting

Deployment

License

Features

CRUD operations for Tasks

CRUD operations for Users

Task attributes: Title, Description, Due Date, Priority, Status, Completed timestamp

Task Ownership: users can only manage their own tasks

Task Categories and Recurring Tasks

Collaborative Tasks: share tasks with other users

Task History tracking

Notifications for tasks due within 24 hours

Filters: Status, Priority, Due Date

Ordering: Due Date, Priority

RESTful API design with proper HTTP methods and error handling

Getting Started
Requirements

Python 3.11+

Django 5.2+

Django REST Framework

django-filter

Installation

# Clone the repo

git clone https://github.com/Faithy-dev/task-manager-api.git
cd task-manager-api

# Create virtual environment

python3 -m venv venv
source venv/bin/activate # Mac/Linux

# venv\Scripts\activate # Windows

# Install dependencies

pip install -r requirements.txt

# Run migrations

python manage.py makemigrations
python manage.py migrate

# Create superuser

python manage.py createsuperuser

# Run the server

python manage.py runserver

API Endpoints

Public API root:

GET /

Users:

/api/users/

Tasks:

/api/tasks/

Categories:

/api/categories/

Task History:

/api/task-history/

Authentication (Login/Logout):

/api-auth/login/
/api-auth/logout/

Authentication

The API requires login to access tasks and perform CRUD operations.

You can use Django session authentication at /api-auth/login/.

Users can only manage tasks they own.

Notifications

Console-based notifications for tasks due in the next 24 hours:

python manage.py send_notifications

Filters and Sorting

Filter by status, priority, due_date:

/api/tasks/?status=pending&priority=high&due_date=2025-10-20

Sort by due_date or priority:

/api/tasks/?ordering=due_date
/api/tasks/?ordering=-priority

Deployment
Heroku
heroku login
heroku create task-manager-api
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser

PythonAnywhere

Push code to PythonAnywhere, configure virtualenv, run migrations, and create superuser.

License

This project is for educational purposes (Capstone Project).
