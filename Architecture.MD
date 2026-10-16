
# Architecture Documentation

## 1. Overview

books_api is a RESTful API built with Django and Django REST Framework for managing book records.

The application follows Django's project-and-app structure:

> <br>django_api/ contains the Django project configuration and URL routing.
> <br>app/ contains the book domain model and REST API implementation.
> <br>Django REST Framework provides serializers, viewsets, and API routing.
> <br>The database stores book records through Django's ORM.
> <br>Docker and Gunicorn provide the containerized application runtime.

Technology stack - Component Technology:
> <br>Programming language-	Python
> <br>Web framework-	Django
> <br>REST API-	Django REST Framework
> <br>Data access-	Django ORM
> <br>Database-	PostgreSQL configured for live deployment; SQLite database file also present (for local testing)
> <br>Application server-	Gunicorn
> <br>Static file handling-	WhiteNoise dependency
> <br>Containerization-	Docker
> <br>Public Repository- Github Repo
> <br>Public container hub- Github  Package
> <br>App local/test environment- LinuxMint
> <br>App live deployment- Render Cloud
> <br>Database live deployment- AWS-RDS
> <br> Automation tool used for live database setup- Terraform

The exact installed versions are defined in requirements.txt. 

## 2. Directory Structure

The following tree represents the repository structure identified during review. Some directories may contain additional files not listed here.

books_api/
<br>├── app/
<br>│   ├── models.py          # Book data model
<br>│   ├── serializers.py     # Book API serialization
<br>│   ├── views.py           # API request handling
<br>│   └── urls.py            # API route registration
<br>│
<br>├── django_api/
<br>│   ├── settings.py        # Django application settings
<br>│   ├── urls.py            # Root URL configuration
<br>│   ├── wsgi.py            # WSGI application entry point
<br>│   └── ...
<br>│
<br>├── staticfiles/           # Static files directory
<br>├── .venv/                 # Local Python virtual environment
<br>├── Dockerfile             # Container build and startup configuration
<br>├── manage.py              # Django management entry point
<br>├── requirements.txt       # Python dependencies
<br>├── db.sqlite3             # SQLite database file
<br>├── README.md              # Project documentation
<br>├── books_api_ui.png       # Project image
<br>└── ARCHITECTURE.md        # Architecture documentation

Key responsibilities - File or directory	Responsibility
><br>manage.py-	Executes Django management commands and identifies the settings module.
><br>django_api/settings.py-	Configures installed applications, middleware, database access, static files, and security settings.
><br>django_api/urls.py-	Defines the root URL routes and connects the API URL configuration.
><br>django_api/wsgi.py-	Exposes the WSGI application for compatible application servers.
><br>app/models.py-	Defines the Book model.
><br>app/serializers.py-	Converts book model instances to and from API representations.
><br>app/views.py-	Implements book operations through a Django REST Framework viewset.
><br>app/urls.py-	Registers the book API routes.
><br>requirements.txt-	Lists the Python packages required by the application.
><br>Dockerfile-	Defines the container image and application startup command.

Repository add-ons: .venv/ is generally a local development artifact and is committed for local testing.

## 3. Application Architecture
3.1 Component diagram

The application uses Django URL routing and Django REST Framework's viewset and serializer abstractions to expose the Book model through an HTTP API.

flowchart TD
    Client["API Client Browser, Postman, or Application"]

    subgraph Django["Django Application"]
        RootURL["django_api/urls.py<br/>Root URL Configuration"]
        AppURL["app/urls.py<br/>API Router"]
        View["app/views.py<br/>BookViewSet"]
        Serializer["app/serializers.py<br/>BookSerializer"]
        Model["app/models.py<br/>Book Model"]
    end

    Database[("Configured Database<br/>PostgreSQL (live env) or SQLite (local/test env)")]

    Client -->|"HTTP Request"| RootURL
    RootURL -->|"/api/"| AppURL
    AppURL --> View
    View --> Serializer
    View --> Model
    Model <-->|"Django ORM"| Database
    Serializer -->|"Serialized Response"| View
    View -->|"HTTP Response"| Client


The diagram represents the logical request flow. The serializer handles conversion and validation of API data, while the model and Django ORM provide database access. The live database backend is postgresql while the local database is sqlite.

3.2 Request lifecycle

A typical API request follows these steps:

><br>An API client sends an HTTP request to an endpoint under /api/.
><br>Django's root URL configuration delegates the request to the books application's URL configuration.
><br>The router resolves the endpoint to BookViewSet.
><br>he viewset executes the requested operation, such as listing, creating, retrieving, updating, or deleting a book.
><br>The serializer validates incoming data or converts model instances into API response data.
><br>Django's ORM reads or modifies the configured database.
><br>Django REST Framework returns an HTTP response to the client.

3.3 Architectural responsibilities

The application separates routing, request handling, serialization, and persistence:
><br>Routing layer: maps HTTP paths to API views.
><br>View layer: coordinates CRUD operations and HTTP responses.
><br>Serialization layer: validates and represents book data.
><br>Model layer: defines the structure of book records.
><br>Persistence layer: stores and retrieves records through Django's ORM.

The current implementation uses a model viewset rather than a separate service layer. A dedicated service layer is not necessary for a small CRUD API unless the business logic becomes more complex.

## 4. Data Model
4.1 Book entity

The Book model defines the core data managed by the API:
><br>Field	Type	Description
><br>id	Auto-generated primary key	Unique identifier for a book.
><br>title	CharField(max_length=200)	Title of the book.
><br>author	CharField(max_length=100)	Name of the author.
><br>publish_date	DateField, nullable	Publication date, when available.

The serializer exposes id, title, author, and publish_date.

4.2 Persistence

The Django ORM maps the Book model to a database table. Database schema changes should be managed through Django migrations.

For example:

python manage.py makemigrations
python manage.py migrate


The migration commands above describe the standard Django workflow. Run them in the intended environment after confirming the database connection and reviewing any pending migrations.

## 5. REST API Endpoints

The root URL configuration delegates /api/ requests to app.urls. The books URL configuration uses Django REST Framework's DefaultRouter to register the BookViewSet.

The following endpoints are the standard routes generated by that configuration.

Method	Endpoint	Description
><br>GET	/api/books/	List books.
><br>POST	/api/books/	Create a book.
><br>GET	/api/books/{id}/	Retrieve a book by ID.
><br>PUT	/api/books/{id}/	Replace a book's fields.
><br>PATCH	/api/books/{id}/	Partially update a book.
><br>DELETE	/api/books/{id}/	Delete a book.

Confirm the exact router registration and any custom actions in app/urls.py and app/views.py before treating this table as an exhaustive API specification.

5.1 Example request: create a book
POST /api/books/
Content-Type: application/json

{
  "title": "Example Book",
  "author": "Example Author",
  "publish_date": "2024-01-15"
}


The example illustrates the serializer's exposed fields. Actual validation requirements and response status codes depend on the model, serializer, and viewset configuration.

5.2 Example request: list books
GET /api/books/


The endpoint returns a serialized representation of the books available through the configured database.

5.3 Example request: retrieve a book
GET /api/books/1/


Replace 1 with the ID of the desired record.

5.4 Example request: update a book
PATCH /api/books/1/
Content-Type: application/json

{
  "title": "Updated Book Title"
}


A partial update changes only the submitted fields, subject to serializer validation.

5.5 Example request: delete a book
DELETE /api/books/1/


This requests deletion of the specified book. The operation's availability to unauthenticated or authenticated clients depends on the configured API permissions.

## 6. Database Configuration
6.1 Database backends

The repository contains a db.sqlite3 file for locally testing the aps, while the PostgreSQL configurations points to a live database.

Django migrations should be applied locally after database connection has been configured to point to the sqlite file.

Database backups, retention, and recovery procedures is managed separately in production environment.

## 7. Deployment Architecture
7.1 Container startup

The repository includes a Dockerfile that uses Python 3.10, installs Python dependencies, copies the application into the image, and starts Gunicorn with three workers.

The intended logical runtime is:

flowchart TD
    Build["Docker Build"]
    Image["Container Image<br/>Python 3.10 + Dependencies"]
    Runtime["Container Runtime"]
    Gunicorn["Gunicorn<br/>3 Workers"]
    Django["Django WSGI Application"]
    DB[("Configured Database")]
    Client["API Client"]

    Build --> Image
    Image --> Runtime
    Runtime --> Gunicorn
    Gunicorn --> Django
    Client -->|"HTTP Request"| Django
    Django <-->|"ORM Queries"| DB
    Django -->|"HTTP Response"| Client


This diagram describes runtime architecture of this repo.

7.2 Port configuration

The reviewed Dockerfile exposes port 8000, while the Gunicorn command binds to port 8002 (this is intentional and can be reconfigured locally as required).

## 8. Security Considerations

The following settings deserve particular attention before deployment:

Allowed hosts

The reviewed settings use a wildcard for ALLOWED_HOSTS. Replace this with an explicit list of trusted hostnames for each deployment environment.

API permissions

The ModelViewSet exposes create, update, and delete operations. Authentication and permission classes requires additional configuration before exposing the API for final production.

Dependency management

Review requirements.txt with additonal configurations regularly for compatibility, security updates, and unnecessary packages. Pin dependencies and test updates before deploying them.

## 9. Development Workflow

A typical local development workflow is:
><br>Create and activate a Python virtual environment.
><br>Install the dependencies listed in requirements.txt.
><br>Configure the database and other required environment variables.
><br>Apply database migrations.
><br>Start the Django development server.
><br>Exercise the API endpoints.
><br>Run automated tests before committing changes.

Typical commands:
><br>python -m venv .venv
><br>source .venv/bin/activate
><br>pip install -r requirements.txt
><br>python manage.py migrate
><br>python manage.py runserver

The activation command shown here is for a Linux environment. Windows uses a different virtual-environment activation command.

The development server's default address is generally http://127.0.0.1:8000/. The API is expected under /api/, subject to the project's URL configuration.

## 10. Known Limitations and Items to Verify

This documentation is based on the published repository files. The following should be reviewed before deploying to a target live / prod environment:
><br>The exact contents of nested directories and any additional modules not listed in the directory tree.
><br>The active database backend (postgresql in this case) and the committed SQLite database file (for local testing).
><br>The exact serializer validation rules and required fields.
><br>API authentication, permissions, pagination, filtering, and custom actions.
><br>The preferred container listening port and external port mapping.
><br>Static-file collection and serving behavior in production.
><br>The presence and coverage of automated tests.

These points should be checked before redeploying to a target live environment.

## 11. Summary

books_api is organized as a small Django REST Framework application. The root project configuration delegates API requests to the books application, which uses a model viewset, serializer, and Django ORM to implement book CRUD operations.

The existing structure is suitable for a simple API. The additional priority improvements include:
><br>apply the appropriate cnfiguration for the final prod database.
><br>add automated API tests.

This application, after containerization build has been:
1. Pushed to a public container registry (Github).
2. Deployed successfully to a PaaS cloud platform (Render).
3. The live database has also been successfully deployed to a cloud relational database instance (AWS-RDS).
4. The active url of this application will be temporarily available on the README.MD file, on this same repository.

This document will be updated as the API grows or its deployment architecture changes.