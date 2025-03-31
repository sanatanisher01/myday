# Deployment Guide for MyDay Website

## Prerequisites

1. PythonAnywhere account (https://www.pythonanywhere.com/)
2. Git installed on your local machine
3. SSH keys configured for PythonAnywhere

## Deployment Steps

1. **Create a PythonAnywhere Account**
   - Go to https://www.pythonanywhere.com/
   - Sign up for a new account
   - Choose the free tier (BASIC) which is sufficient for this website

2. **Prepare Your Code**
   - Ensure all migrations are created and applied locally
   - Run `python manage.py collectstatic` locally to ensure all static files are present

3. **Upload Code to PythonAnywhere**
   - Log in to your PythonAnywhere account
   - Go to "Files" -> "Bash Console"
   - Clone your repository:
     ```bash
     git clone https://github.com/yourusername/myday.git
     cd myday
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure PythonAnywhere**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Select "Python 3.12" (or the latest Python version)
   - Choose "Manual configuration"
   - Click "Next"

6. **Configure Virtual Environment**
   - Go to "Virtualenvs" tab
   - Create a new virtual environment
   - Select Python 3.12
   - Click "Create virtualenv"

7. **Configure Web App**
   - Go to "Web" tab
   - Click on your domain name
   - In "Source code", enter the path to your project
   - In "WSGI configuration file", enter the path to your wsgi.py
   - Click "Reload" to apply changes

8. **Set Up Database**
   - Go to "Databases" tab
   - Create a new PostgreSQL database
   - Update your settings.py with the database credentials

9. **Final Steps**
   - Run migrations:
     ```bash
     python manage.py migrate
     ```
   - Collect static files:
     ```bash
     python manage.py collectstatic --noinput
     ```
   - Create a superuser:
     ```bash
     python manage.py createsuperuser
     ```

10. **Test Your Website**
    - Visit your domain (yourusername.pythonanywhere.com)
    - Test all major functionality
    - Check that static files are loading correctly

## Troubleshooting

1. **Static Files Not Loading**
   - Ensure STATIC_ROOT is set correctly in settings.py
   - Run `python manage.py collectstatic` again
   - Check permissions on static files directory

2. **Database Connection Issues**
   - Verify database credentials in settings.py
   - Check if database is running
   - Verify database permissions

3. **Application Not Starting**
   - Check PythonAnywhere error logs
   - Verify wsgi.py configuration
   - Check for syntax errors in settings.py
