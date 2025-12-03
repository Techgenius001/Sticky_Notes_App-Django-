# Technology Stack

## Backend

- **Framework**: Django 5.2.9
- **Database**: SQLite3 (default, suitable for development and small deployments)
- **Python Version**: Python 3.x
- **WSGI Server**: Gunicorn (for production deployment)

## Frontend

- **CSS Framework**: Tailwind CSS (via CDN)
- **Fonts**: Inter (primary), Roboto (alternative) via Google Fonts
- **JavaScript**: Vanilla JS (no framework dependencies)
- **Templates**: Django template engine

## Deployment

- Configured for Render deployment
- Environment variables for production: `ALLOWED_HOSTS`, `DEBUG`

## Common Commands

### Development Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Unix/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

### Database Management

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

### Production

```bash
# Start with Gunicorn
gunicorn stickynotes.wsgi
```

## Dependencies

Minimal dependency footprint - only Django is required (see `requirements.txt`)
