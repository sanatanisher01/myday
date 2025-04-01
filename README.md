# MyDay - Event Memory Management Platform

MyDay is a modern, fully animated web platform for managing and sharing event memories such as weddings, birthdays, anniversaries, and college events.

## Features

- User authentication and dashboard
- Admin dashboard for content management
- Event and sub-event organization
- Review system for events
- Responsive design for all devices
- Smooth animations and transitions
- Booking system with address and mobile number verification
- Real-time statistics and dashboard metrics

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, GSAP, FontAwesome
- **Backend**: Django (Python), SQLite (dev)/PostgreSQL (prod), Django REST Framework
- **Deployment**: Render, Heroku/DigitalOcean, Cloudflare CDN

## Live Demo

Visit the live demo at: [https://myday-events.onrender.com](https://myday-events.onrender.com)

## Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/myday.git
   cd myday
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Run migrations
   ```
   python manage.py migrate
   ```

4. Start the development server
   ```
   python manage.py runserver
   ```

## Deployment

This project is configured for easy deployment on Render.com:

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Set the build command to `./build.sh`
5. Set the start command to `gunicorn myday.wsgi --log-file -`

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
