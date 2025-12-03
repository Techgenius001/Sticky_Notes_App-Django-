## Midnight Sticky Notes (Django)

Dark, minimalist sticky-notes board with free-form drag-and-drop canvas, built with Django and Tailwind (via CDN).

### Features
- **User accounts**: Django auth signup, login, logout
- **Dashboard**: Midnight Productivity dark theme (Inter + Roboto)
- **Sticky notes**:
  - Title, content, color, tags
  - Position (x, y) on a free-form board
  - Size (width, height) with drag-to-resize
  - Last edited timestamp
- **Interactions**:
  - Drag notes anywhere on the canvas
  - Resize from bottom-right corner
  - View/update via modal
  - Add/delete notes

### Running locally

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

### Deployment (Render outline)
- **Environment**: Python 3.x
- **Start command**: `gunicorn stickynotes.wsgi`
- **Build command**: `pip install -r requirements.txt && python manage.py migrate`
- Ensure `ALLOWED_HOSTS` and `DEBUG` are configured via env vars in `stickynotes/settings.py` for production.


