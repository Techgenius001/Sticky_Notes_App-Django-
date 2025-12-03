# Project Structure

## Directory Layout

```
stickynotes/               # Django project root
├── manage.py              # Django management script
├── db.sqlite3             # SQLite database file
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment configuration (Render/Heroku)
│
├── stickynotes/          # Main project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # Root URL configuration
│   ├── wsgi.py           # WSGI application entry point
│   └── asgi.py           # ASGI application entry point
│
├── notes/                # Main application (sticky notes)
│   ├── models.py         # Note model definition
│   ├── views.py          # View functions (auth + CRUD)
│   ├── urls.py           # App-specific URL patterns
│   ├── admin.py          # Django admin configuration
│   ├── apps.py           # App configuration
│   ├── tests.py          # Test cases
│   └── migrations/       # Database migrations
│
├── templates/            # HTML templates (project-level)
│   ├── base.html         # Base template with header/styling
│   ├── auth/             # Authentication templates
│   │   ├── login.html
│   │   └── signup.html
│   └── notes/            # Notes app templates
│       └── dashboard.html
│
├── static/               # Static files (CSS, JS, images)
│   └── .gitkeep
│
└── venv/                 # Virtual environment (not in version control)
```

## Architecture Patterns

### URL Routing

- Root URLs defined in `stickynotes/urls.py`
- App URLs included from `notes/urls.py`
- All note-related routes prefixed under root path

### Views

- Function-based views (not class-based)
- Use `@login_required` decorator for protected views
- Use `@require_POST` for state-changing operations
- Return `JsonResponse` for AJAX endpoints
- Return `redirect` after POST operations (PRG pattern)

### Models

- Single `Note` model with user foreign key
- Uses Django's built-in `AUTH_USER_MODEL`
- Includes position (x, y), size (width, height), and metadata fields
- Color choices defined as model constants

### Templates

- Extend from `base.html` for consistent layout
- Use Django template tags (`{% url %}`, `{% csrf_token %}`, etc.)
- JavaScript embedded in `{% block extra_body %}` for page-specific logic
- Tailwind utility classes for styling

### Frontend Interactions

- Vanilla JavaScript for drag-and-drop and resize functionality
- AJAX requests for position/size updates (auto-save)
- CSRF token handling via cookie extraction
- Modal-based editing interface

## Conventions

- Use `related_name` on foreign keys for reverse lookups
- Type hints on view functions (`HttpRequest`, `HttpResponse`)
- Ordering defined in model `Meta` class
- Static configuration in `settings.py` (no environment-specific files in repo)
