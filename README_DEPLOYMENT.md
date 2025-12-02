# Haramaya Health Center - Render Deployment Guide

## Prerequisites
- GitHub account
- Render account (free tier available at render.com)
- Git installed locally

## Step-by-Step Deployment Instructions

### 1. Prepare Your Code

Make sure all files are committed:
```bash
git init
git add .
git commit -m "Initial commit for deployment"
```

### 2. Push to GitHub

Create a new repository on GitHub, then:
```bash
git remote add origin https://github.com/YOUR_USERNAME/haramaya-health-center.git
git branch -M main
git push -u origin main
```

### 3. Deploy on Render

#### Option A: Using render.yaml (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml` and create:
   - Web Service (Django app)
   - PostgreSQL Database

#### Option B: Manual Setup

1. **Create PostgreSQL Database:**
   - Click "New" → "PostgreSQL"
   - Name: `haramaya-health-db`
   - Plan: Free
   - Click "Create Database"
   - Copy the "Internal Database URL"

2. **Create Web Service:**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** haramaya-health-center
     - **Environment:** Python 3
     - **Build Command:** `./build.sh`
     - **Start Command:** `gunicorn health_center.wsgi:application`
   
3. **Add Environment Variables:**
   - `PYTHON_VERSION`: `3.12.0`
   - `DATABASE_URL`: (paste the Internal Database URL from step 1)
   - `SECRET_KEY`: (generate a random string)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app-name.onrender.com`

### 4. Make build.sh Executable

Before pushing, make sure build.sh is executable:
```bash
chmod +x build.sh
git add build.sh
git commit -m "Make build.sh executable"
git push
```

### 5. Deploy

Render will automatically:
1. Install dependencies from `requirements.txt`
2. Run `collectstatic` to gather static files
3. Run database migrations
4. Start the application with Gunicorn

### 6. Create Superuser

After deployment, access the Render Shell:
1. Go to your web service dashboard
2. Click "Shell" tab
3. Run:
```bash
python manage.py createsuperuser
```

### 7. Access Your Application

Your app will be available at:
```
https://your-app-name.onrender.com
```

Admin panel:
```
https://your-app-name.onrender.com/admin
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Random 50-character string |
| `DEBUG` | Debug mode | `False` for production |
| `DATABASE_URL` | PostgreSQL connection | Auto-set by Render |
| `ALLOWED_HOSTS` | Allowed domains | `your-app.onrender.com` |
| `PYTHON_VERSION` | Python version | `3.12.0` |

## Troubleshooting

### Static Files Not Loading
```bash
python manage.py collectstatic --no-input
```

### Database Connection Issues
- Verify `DATABASE_URL` is set correctly
- Check PostgreSQL database is running

### Application Errors
- Check logs in Render dashboard
- Verify all environment variables are set
- Ensure `DEBUG=False` in production

## Local Development

To run locally with production-like settings:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```
DEBUG=True
SECRET_KEY=your-local-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run server:
```bash
python manage.py runserver
```

## Updating Your Deployment

To deploy updates:
```bash
git add .
git commit -m "Your update message"
git push
```

Render will automatically redeploy your application.

## Free Tier Limitations

Render free tier includes:
- 750 hours/month of runtime
- App sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- 512 MB RAM
- Shared CPU

For production use, consider upgrading to a paid plan.

## Support

For issues:
- Check Render logs
- Review Django error messages
- Consult Render documentation: https://render.com/docs

## Security Notes

- Never commit `.env` file
- Keep `SECRET_KEY` secure
- Always use `DEBUG=False` in production
- Regularly update dependencies
- Monitor application logs
