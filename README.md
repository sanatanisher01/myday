# MyDay - Event Memory Management Platform

MyDay is a modern, fully animated web platform for managing and sharing event memories such as weddings, birthdays, anniversaries, and college events.

## Features

- User authentication and dashboard
- Admin dashboard for content management
- Event and sub-event organization
- Review system for events
- Responsive design for all devices
- Smooth animations and transitions

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, GSAP, FontAwesome
- **Backend**: Django (Python), SQLite (dev)/PostgreSQL (prod), Django REST Framework
- **Deployment**: Render, Heroku/DigitalOcean, Cloudflare CDN

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd myday_project
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the site at http://127.0.0.1:8000/

## Deployment on Render

This project is configured for easy deployment on Render.com. Follow these steps to deploy:

### Option 1: Deploy using render.yaml (Recommended)

1. Fork or clone this repository to your GitHub account
2. Sign up for a [Render account](https://render.com/)
3. Create a new "Blueprint" on Render and connect your GitHub repository
4. Render will automatically detect the `render.yaml` file and set up your web service and PostgreSQL database
5. Click "Apply" to start the deployment process

### Option 2: Manual Deployment

1. Sign up for a [Render account](https://render.com/)
2. Create a new PostgreSQL database in your Render dashboard
3. Create a new Web Service and connect your GitHub repository
4. Configure the following settings:
   - **Environment**: Python
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn myday.wsgi:application`
5. Add the following environment variables:
   - `DEBUG`: False
   - `SECRET_KEY`: (generate a secure random key)
   - `DATABASE_URL`: (copy from your Render PostgreSQL database)
   - `ALLOWED_HOSTS`: yourapp.onrender.com
   - `RENDER_EXTERNAL_HOSTNAME`: yourapp.onrender.com

### Important Notes

- The first deployment may take up to 5-10 minutes as Render builds your application
- Static files are handled by WhiteNoise, so no additional configuration is needed
- Media files (user uploads) will not persist on Render's free tier. For production, configure cloud storage like AWS S3

## Project Structure

```
myday_project/
├── myday/           (Django project)
├── events/          (Django app)
├── static/          
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
└── requirements.txt
```

## Development Team

- [Developer Name]

## License

This project is licensed under the MIT License - see the LICENSE file for details.
