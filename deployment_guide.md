# Deployment Guide: ServiceNow CSA Platform

This document outlines the steps required to move the application from development to a production environment.

## 1. Environment Configuration
Update the following settings in `servicenow_csa/settings.py` for production:

```python
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-production-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com', 'your-app-name.herokuapp.com', 'localhost']
```

## 2. Static and Media Files
In production, Django does not serve static files by itself. Use a service like **WhiteNoise** or an Nginx reverse proxy.

### Step-by-Step for WhiteNoise:
1. Install WhiteNoise: `pip install whitenoise`
2. Add to `MIDDLEWARE` in `settings.py` (right after SecurityMiddleware):
   ```python
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware', # Add this
       ...
   ]
```
3. Run collection command:
   ```powershell
   python manage.py collectstatic
   ```

## 3. Database
While the project uses SQLite for simplicity, it is recommended to use **PostgreSQL** for production.

## 4. Hosting Recommendations

### Option A: Render / Heroku (Easiest)
- **Render**: Free tier available, handles SSL and static files automatically if configured.
- **Heroku**: Paid tiers, very robust for Django.

### Option B: PythonAnywhere
- Dedicated Python hosting with a free tier.
- Easy setup for Django apps.

### Option C: DigitalOcean / AWS (Advanced)
- Full control via Virtual Private Servers (Droplets/EC2).
- Requires setting up Nginx and Gunicorn.

## 5. Pre-deployment Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Run `python manage.py migrate` on the production server
- [ ] Create a superuser on the production server
- [ ] Set up environment variables for the `SECRET_KEY`
