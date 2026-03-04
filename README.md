# GoStuds Backend Intern Assignment

## Project Creation System (Django + DRF + JWT)

This project implements a **backend-only Project Creation System** using **Django and Django REST Framework**.

It allows authenticated users to:

* Create projects
* View their own projects
* Update projects
* Delete projects

The system uses **JWT authentication** and enforces **strict ownership permissions** so that only the project creator can modify their project.

The backend follows **clean RESTful API design, modular architecture, and secure authentication practices**.

This assignment simulates a **real production backend feature used in GoStuds**. 

---

# Tech Stack

| Technology            | Purpose                |
| --------------------- | ---------------------- |
| Django                | Core backend framework |
| Django REST Framework | API layer              |
| SimpleJWT             | JWT authentication     |
| SQLite                | Development database   |
| Pillow                | Image field support    |
| uv                    | Environment management |
| Postman               | API testing            |

---

# Project Architecture

The project follows a **modular Django app structure** separating authentication and business logic. 

```
Assesment/
│
├── ProjectCreationSystem/
│   ├── settings.py
│   ├── urls.py
│
├── users/
│   ├── models.py
│   ├── backends.py
│   ├── serializers.py
│   ├── views.py
│
├── projects/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│
├── manage.py
└── README.md
```

### App Responsibilities

**users**

* Custom user model
* Authentication logic
* Email/username login

**projects**

* Project CRUD APIs
* Permission enforcement
* Business logic

This separation ensures **clean architecture and scalability**.

---

# Setup Instructions

## 1️⃣ Clone Repository

```
git clone https://github.com/Proxpekt/Backend-Intern-Assignment-GoStuds
cd Assesment
```

---

# 2️⃣ Create Virtual Environment

This project uses **uv**.

```
uv venv
```

Activate environment.

### Windows

```
.venv\Scripts\activate
```

### Mac/Linux

```
source .venv/bin/activate
```

---

# 3️⃣ Install Dependencies

```
uv pip install django
uv pip install djangorestframework
uv pip install djangorestframework-simplejwt
uv pip install pillow
```

---

# 4️⃣ Run Migrations

```
python manage.py makemigrations
python manage.py migrate
```

---

# 5️⃣ Create Superuser

```
python manage.py createsuperuser
```

---

# 6️⃣ Run Server

```
python manage.py runserver
```

Server runs at:

```
http://127.0.0.1:8000
```

---

# Database Schema

## Custom User Model

A **custom authentication system** was implemented using:

* `AbstractBaseUser`
* `PermissionsMixin`
* `BaseUserManager`

This provides full control over authentication and allows login using **username OR email**. 

### User Model Fields

| Field            | Type                                     | Description                                                                       | Usage                                                                                                                |
| ---------------- | ---------------------------------------- | --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **username**     | `CharField (unique)`                     | A unique identifier chosen by the user.                                           | Used as the primary login identity (`USERNAME_FIELD`) and to uniquely identify users within the system.              |
| **email**        | `EmailField (unique)`                    | User's email address. Must be unique across the system.                           | Used for authentication (login via email is supported), communication, and account identification.                   |
| **full_name**    | `CharField`                              | Stores the complete name of the user.                                             | Used for displaying user information in profiles, project ownership, and admin panels.                               |
| **avatar**       | `ImageField`                             | Optional profile picture uploaded by the user.                                    | Used for profile display in UI clients or dashboards. Requires **Pillow** for image handling.                        |
| **password**     | `Hashed Password (CharField internally)` | Securely stored hashed password generated using Django’s password hashing system. | Used for user authentication. Raw passwords are never stored — they are hashed using `set_password()` before saving. |
| **is_active**    | `BooleanField`                           | Indicates whether the user account is active.                                     | Inactive users cannot authenticate or access the system. Useful for suspending accounts without deleting them.       |
| **is_staff**     | `BooleanField`                           | Determines whether the user has access to the Django admin interface.             | Admin users can manage models and data through `/admin`.                                                             |
| **joining_date** | `DateTimeField`                          | Timestamp recording when the user account was created.                            | Used for auditing, analytics, and user activity tracking. Often set automatically using `auto_now_add=True`.         |

---

### Project Model Fields

| Field           | Type                   | Description                                                                             | Usage                                                                                                                                                                                                     |
| --------------- | ---------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **title**       | `CharField`            | The name of the project. Limited to a defined maximum length (commonly 255 characters). | Used as the primary identifier for the project in listings, searches, and API responses. A uniqueness constraint with the creator prevents duplicate titles for the same user.                            |
| **description** | `TextField`            | A detailed explanation of the project including its purpose, goals, or specifications.  | Allows users to store extended information about the project. Displayed when retrieving project details through the API.                                                                                  |
| **status**      | `Enum (TextChoices)`   | Indicates the current state of the project: `active` or `inactive`.                     | Helps categorize projects based on their lifecycle state. Useful for filtering projects or tracking whether a project is currently active.                                                                |
| **duration**    | `PositiveIntegerField` | Represents the expected duration of the project in months.                              | Used to estimate project timelines. Validation ensures the value is positive (e.g., minimum of 1 month).                                                                                                  |
| **creator**     | `ForeignKey(User)`     | References the user who created the project.                                            | Establishes ownership of the project. Used for permission checks so that only the creator can update or delete the project. Also enables querying all projects created by a user (`user.projects.all()`). |
| **created_at**  | `DateTimeField`        | Automatically stores the timestamp when the project was created.                        | Useful for auditing, sorting projects by creation date, and displaying when a project was first added. Typically implemented using `auto_now_add=True`.                                                   |
| **updated_at**  | `DateTimeField`        | Automatically updates whenever the project is modified.                                 | Tracks the last modification time of the project, useful for version tracking, activity logs, and UI updates. Implemented using `auto_now=True`.                                                          |

---

# Relationship

```
User (1) ------ (Many) Projects
```

A user can create **multiple projects**.

Reverse relation:

```
user.projects.all()
```

---

# Database Constraints

### Unique Constraint

```
(title, creator)
```

This prevents a user from creating **duplicate projects with the same title**.

### Database Index

```
(status, creator)
```

Improves performance when filtering projects by:

* status
* creator
* both

---

# Authentication System

Authentication is implemented using **JWT tokens**.

Library used:

```
djangorestframework-simplejwt
```

---

# Authentication Flow

1️⃣ User logs in

```
POST /api/token/
```

Response:

```
access_token
refresh_token
```

2️⃣ Client sends token with requests

```
Authorization: Bearer <access_token>
```

3️⃣ Protected APIs verify JWT.

---

# Logout

Logout is implemented by **blacklisting refresh tokens**.

```
POST /api/logout/
```

User sends refresh token and it becomes invalid.

---

# API Endpoints

## Authentication APIs

| Method | Endpoint              | Description          |
| ------ | --------------------- | -------------------- |
| POST   | `/api/token/`         | Login                |
| POST   | `/api/token/refresh/` | Refresh access token |
| POST   | `/api/logout/`        | Logout               |

---

## Project APIs

| Method | Endpoint              | Description                    |
| ------ | --------------------- | ------------------------------ |
| POST   | `/api/projects/`      | Create project                 |
| GET    | `/api/projects/`      | List logged-in user's projects |
| GET    | `/api/projects/{id}/` | Retrieve project               |
| PUT    | `/api/projects/{id}/` | Update project                 |
| PATCH  | `/api/projects/{id}/` | Partial update                 |
| DELETE | `/api/projects/{id}/` | Delete project                 |

---

# Permission Logic

Custom permission class implemented:

```
IsCreatorOrReadOnly
```

Rules enforced:

| Action | Permission          |
| ------ | ------------------- |
| Create | Authenticated users |
| View   | Only own projects   |
| Update | Only creator        |
| Delete | Only creator        |

---

### Ownership Check

```
request.user == project.creator
```

If another user tries to update/delete:

```
403 Forbidden
```

---

# Filtering Logic

Users **only see their own projects**.

Example logic in viewset:

```
queryset = Project.objects.filter(creator=request.user)
```

This ensures complete **data isolation between users**.

---

# Validation Rules

* `duration >= 1`
* `status ∈ {active, inactive}`
* `title + creator` must be unique

---

# Example API Usage

## Create Project

Request

```
POST /api/projects/
```

Body

```
{
"title": "Traffic Optimization AI",
"description": "Smart signal control",
"status": "active",
"duration": 6
}
```

Response

```
{
"id": 1,
"title": "Traffic Optimization AI",
"description": "Smart signal control",
"status": "active",
"duration": 6,
"creator": 2,
"created_at": "2026-03-04T10:21:10Z"
}
```

---

# Example Authorization Header

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

# Testing

All APIs were tested using **Postman**.

Demonstration includes:

* Login
* JWT authentication
* Create project
* List projects
* Update project
* Delete project
* Logout

---

## Postman Collection

A ready-to-use Postman collection is included.

File:
postman/Assesment.postman_collection.json

Import it into Postman to test all APIs instantly.

---

# Design Decisions

### Custom User Model

Implemented instead of Django default for flexibility and scalable authentication.

### JWT Authentication

Chosen because:

* Stateless
* Suitable for REST APIs
* Scalable for microservices

### Separate Django Apps

* users → authentication
* projects → domain logic

Improves maintainability.

### Database Constraints

Used to prevent duplicate project titles per user.

---

# Author

**Aayush Saxena**

Backend Intern Assignment – GoStuds
