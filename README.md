# Person Management

## Overview
This is a Django REST API project that manages **Person** entities, allowing authentication and role-based access control. The system supports person-based authentication with **Admin** and **Guest** roles, along with custom permissions.

---

## Features
- **Person Entity**: Includes `first_name`, `last_name`, `email`, `phone_number`, `date_of_birth`, `age`, `username`, and `password`.
- **Authentication**: Utilizes Django’s built-in session authentication system.
- **Role-Based Access**:
  - `Admin`: Full CRUD access.
  - `Guest`: Can only filter/search persons.
- **RESTful API**:
  - CRUD operations for `Person` (Admin-only with pagination).
  - Search API for filtering people by `first_name`, `last_name`, and `age` (Admin & Guest with pagination).
- **Custom Exception Handling**: Graceful error handling with meaningful responses.
- **Pagination Support**: Default pagination of 10 records per page.
- **Logging Support**: Integrated logging for better debugging and monitoring.
- **Docker & Docker Compose Support**: To simplify project setup.
- **Management Command**: Auto-create **Admin** and **Guest** persons.

---

## Installation

### **1. Clone the Repository**
```
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```
---
### Setup Using Virtual Env
### **2. Create a Virtual Environment**
```
python -m venv venv
source venv/bin/activate
```

### **3. Install Dependencies**
```
pip install -r requirements.txt
```

### **4. Apply Migrations**
```
python manage.py migrate
```

### **5. Create Admin and Guest Persons**
```
python manage.py create_person
```

### **6. Run the Development Server**
#### **Debug is `True`**
```
python manage.py runserver
```
#### **Debug is `False`** (To serve `staticfiles` appropriately)
```
python manage.py runserver --insecure
```

Now, the API is available at: **`http://127.0.0.1:8000/api/`**

---

### Setup Using Docker & Docker Compose
`Dockerfile` and `docker-compose.yml` files are included for easy setup.


### **2. Build and Start the Application**
```
docker-compose up --build
```

### **3. Stop the Application**
```
docker-compose down
```
---

## API Endpoints

### **Authentication**
| Method | Endpoint | Description       |
|--------|---------|-------------------|
| POST   | `/api/login/` | Login a person    |
| POST   | `/api/logout/` | Logout the person |

### **Person API**
| Method | Endpoint                                             | Role | Description                                   |
|--------|------------------------------------------------------|------|-----------------------------------------------|
| GET    | `/api/person/`                                       | Admin | List all persons (Paginated)                  |
| POST   | `/api/person/`                                       | Admin | Create a new person                           |
| GET    | `/api/person/{id}/`                                  | Admin | Retrieve a specific person                    |
| PATCH  | `/api/person/{id}/`                                  | Admin | Update a person                               |
| DELETE | `/api/person/{id}/`                                  | Admin | Delete a person                               |
| GET    | `/api/person/filter-people/?first_name=nevil&age=29` | Admin, Guest | Search people by first_name / last_name / age |

---

## **Permissions & Roles**
| Role | Access                        |
|------|-------------------------------|
| Admin | Full CRUD access              |
| Guest | Can only filter/search people |

---

## **Environment Variables (.env)**
Create a `.env` file at the same location as `.env.example` and add:
```
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## **Logging Configuration**
The application includes structured logging for better debugging and monitoring.
### Check your logs inside the `logs/` directory,
- `django.log` → General Logs (INFO, DEBUG, WARNING)
- `errors.log` → Captures only ERROR messages


### **Log Levels**:
- DEBUG: Detailed information for diagnosing problems.
- INFO: Confirmation that things are working as expected.
- WARNING: An indication of potential issues.
- ERROR: A more serious problem that has prevented part of the application from functioning.

Logging is configured in `settings.py`.

---

## **Running Tests**
To run unit tests, execute:
```
python manage.py test
```

---

