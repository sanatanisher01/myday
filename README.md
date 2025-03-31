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
- **Deployment**: Heroku/DigitalOcean, Cloudflare CDN

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
