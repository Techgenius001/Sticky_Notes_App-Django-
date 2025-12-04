# Deployment Guide for Midnight Notes

## 🚀 Deploy to Render

### Prerequisites

- GitHub account
- Render account (free tier available at https://render.com)

### Step 1: Render Setup

1. **Create New Web Service**

   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select this repository

2. **Configure Service**

   ```
   Name: midnight-notes (or your choice)
   Region: Choose closest to you
   Branch: main
   Runtime: Python 3

   Build Command:
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

   Start Command:
   gunicorn stickynotes.wsgi
   ```

3. **Set Environment Variables**

   Add these in the "Environment" section:

   | Key              | Value                        |
   | ---------------- | ---------------------------- |
   | `SECRET_KEY`     | Generate using command below |
   | `DEBUG`          | `False`                      |
   | `ALLOWED_HOSTS`  | `your-app-name.onrender.com` |
   | `PYTHON_VERSION` | `3.11.0`                     |

4. **Generate SECRET_KEY**

   Run locally to generate a secure key:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first deployment
   - Your app will be live at `https://your-app-name.onrender.com`

### Step 2: Post-Deployment (Optional)

**Create Admin User:**

1. Go to Render dashboard → Your service → "Shell" tab
2. Run: `python manage.py createsuperuser`
3. Access admin at: `https://your-app-name.onrender.com/admin/`

### Important Notes

⚠️ **Database Persistence**: The free tier uses ephemeral storage. Your SQLite database will reset on each deployment. For persistent data:

- Upgrade to a paid Render plan, or
- Use an external PostgreSQL database

✅ **User Signup**: Users can create accounts at `/signup/`

📊 **Monitoring**: Check the "Logs" tab in Render for debugging

🌐 **Custom Domain**: Available with paid plans

## Local Development

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Run development server
python manage.py runserver

# Access at http://localhost:8000
```

## Environment Variables Reference

- `SECRET_KEY`: Django secret key (required in production)
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames
- `PYTHON_VERSION`: Python version for Render (3.11.0 recommended)
