from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from events.models import Event, SubEvent, Review, Booking, UserProfile
from django.core.files.base import ContentFile
import datetime
import random
import os

class Command(BaseCommand):
    help = 'Create sample data for the MyDay website'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpassword'
            )
            self.stdout.write(self.style.SUCCESS('Created superuser: admin'))
        else:
            admin = User.objects.get(username='admin')
        
        # Create regular users
        users = []
        for i in range(1, 6):
            if not User.objects.filter(username=f'user{i}').exists():
                user = User.objects.create_user(
                    username=f'user{i}',
                    email=f'user{i}@example.com',
                    password=f'password{i}',
                    first_name=f'User{i}',
                    last_name=f'Surname{i}'
                )
                
                # Update profile information
                profile = user.profile
                profile.phone = f'+1 555-{i}00-{i}000'
                profile.date_of_birth = timezone.now() - datetime.timedelta(days=365*30)
                profile.bio = f'This is the bio for User{i}'
                profile.address = f'{i}23 Main St'
                profile.city = 'New York'
                profile.state = 'NY'
                profile.country = 'USA'
                profile.postal_code = f'1000{i}'
                profile.save()
                
                self.stdout.write(self.style.SUCCESS(f'Created user: user{i}'))
                users.append(user)
            else:
                users.append(User.objects.get(username=f'user{i}'))
        
        # Create event categories
        event_data = [
            {
                'name': 'Wedding',
                'description': 'Capture every moment of your special day with our premium wedding photography and videography services. Our experienced team will create beautiful memories that last a lifetime.',
                'image_name': 'wedding.jpg',
            },
            {
                'name': 'Birthday',
                'description': 'Make your birthday celebration truly special with our birthday event services. From cake smash sessions for little ones to elaborate themed parties for adults, we cover it all.',
                'image_name': 'birthday.jpg',
            },
            {
                'name': 'Anniversary',
                'description': 'Celebrate your relationship milestones with our anniversary event packages. Whether it\'s your first or fiftieth, we\'ll help you commemorate your special journey together.',
                'image_name': 'anniversary.jpg',
            },
            {
                'name': 'Corporate',
                'description': 'Elevate your corporate events with our professional services. From team-building activities to annual conferences, we ensure your company events are memorable and productive.',
                'image_name': 'corporate.jpg',
            },
            {
                'name': 'Graduation',
                'description': 'Mark this important achievement with our graduation event services. We offer photography, venue decoration, and complete event management for this milestone.',
                'image_name': 'graduation.jpg',
            }
        ]
        
        events = []
        for idx, data in enumerate(event_data, 1):
            event, created = Event.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                }
            )
            
            if created:
                # Dummy image since we don't have actual images
                event.image.save(data['image_name'], ContentFile(''), save=True)
                self.stdout.write(self.style.SUCCESS(f'Created event: {data["name"]}'))
            events.append(event)
        
        # Create sub-events for each event category
        subevent_data = [
            # Wedding sub-events
            {
                'event': events[0],
                'name': 'Photography Package',
                'description': 'Complete wedding day coverage with 2 photographers, 8 hours of coverage, and all digital images.',
                'price': 2500.00,
            },
            {
                'event': events[0],
                'name': 'Videography Package',
                'description': 'Full wedding film including ceremony, speeches, and first dance with professional editing.',
                'price': 3000.00,
            },
            {
                'event': events[0],
                'name': 'Photo + Video Bundle',
                'description': 'Our most popular package combining photography and videography at a special price.',
                'price': 4800.00,
            },
            
            # Birthday sub-events
            {
                'event': events[1],
                'name': 'Kids Birthday Party',
                'description': 'Complete kids birthday package including photography, decorations, and entertainment.',
                'price': 800.00,
            },
            {
                'event': events[1],
                'name': 'Adult Birthday Celebration',
                'description': 'Elegant adult birthday package with professional photography and event coordination.',
                'price': 1200.00,
            },
            {
                'event': events[1],
                'name': 'Milestone Birthday Special',
                'description': 'Celebrate milestone birthdays (30, 40, 50, etc.) with our premium package.',
                'price': 1800.00,
            },
            
            # Anniversary sub-events
            {
                'event': events[2],
                'name': 'Silver Anniversary Package',
                'description': 'Celebrate 25 years together with our special Silver Anniversary package.',
                'price': 1500.00,
            },
            {
                'event': events[2],
                'name': 'Golden Anniversary Package',
                'description': 'Mark 50 years of marriage with our exceptional Golden Anniversary celebration.',
                'price': 2000.00,
            },
            {
                'event': events[2],
                'name': 'Vow Renewal Ceremony',
                'description': 'Renew your wedding vows with a beautiful ceremony and professional photography.',
                'price': 2800.00,
            },
            
            # Corporate sub-events
            {
                'event': events[3],
                'name': 'Corporate Team Building',
                'description': 'Boost team morale and collaboration with our corporate team building events.',
                'price': 3500.00,
            },
            {
                'event': events[3],
                'name': 'Annual Conference',
                'description': 'Full service annual conference planning and execution for up to 200 attendees.',
                'price': 5000.00,
            },
            {
                'event': events[3],
                'name': 'Product Launch Event',
                'description': 'Make a splash with your new product launch with our comprehensive event package.',
                'price': 4000.00,
            },
            
            # Graduation sub-events
            {
                'event': events[4],
                'name': 'Graduation Photography',
                'description': 'Professional graduation photography package including individual and group portraits.',
                'price': 600.00,
            },
            {
                'event': events[4],
                'name': 'Graduation Party',
                'description': 'Complete graduation party planning and execution for the graduate and guests.',
                'price': 1200.00,
            },
            {
                'event': events[4],
                'name': 'Graduation Video Memoir',
                'description': 'Professional video compilation of the graduation journey, ceremony, and celebration.',
                'price': 900.00,
            },
        ]
        
        subevents = []
        for data in subevent_data:
            subevent, created = SubEvent.objects.get_or_create(
                event=data['event'],
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'price': data['price'],
                }
            )
            
            if created:
                # Dummy image since we don't have actual images
                subevent.image.save(f"{data['name'].lower().replace(' ', '_')}.jpg", ContentFile(''), save=True)
                self.stdout.write(self.style.SUCCESS(f'Created subevent: {data["name"]}'))
            subevents.append(subevent)
        
        # Create reviews
        review_texts = [
            "Absolutely amazing service! Exceeded all our expectations.",
            "Great experience from start to finish. Highly recommend!",
            "Professional team that went above and beyond for our event.",
            "Good service but a bit pricey for what you get.",
            "Fantastic quality and attention to detail. Will use again!",
            "The team was so helpful and made our day special.",
            "Couldn't have asked for better service. Thank you!",
            "Slightly disappointed with communication, but the end result was good.",
            "Outstanding work! The photos/videos are beautiful.",
            "The entire process was smooth and stress-free. Love the results!"
        ]
        
        for event in events:
            # Create 2-4 reviews for each event
            for _ in range(random.randint(2, 4)):
                user = random.choice(users)
                
                # Skip if user already reviewed this event
                if Review.objects.filter(user=user, event=event).exists():
                    continue
                
                review = Review.objects.create(
                    user=user,
                    event=event,
                    rating=random.randint(3, 5),  # Mostly positive reviews
                    comment=random.choice(review_texts),
                )
                self.stdout.write(self.style.SUCCESS(f'Created review for {event.name} by {user.username}'))
        
        # Create bookings
        for user in users:
            # Create 1-3 bookings for each user
            for _ in range(random.randint(1, 3)):
                subevent = random.choice(subevents)
                
                # Skip if user already booked this subevent
                if Booking.objects.filter(user=user, subevent=subevent).exists():
                    continue
                
                # Create either an upcoming, past, or cancelled booking
                booking_type = random.choice(['upcoming', 'past', 'cancelled'])
                
                if booking_type == 'upcoming':
                    booking_date = timezone.now() + datetime.timedelta(days=random.randint(1, 60))
                    status = 'confirmed'
                elif booking_type == 'past':
                    booking_date = timezone.now() - datetime.timedelta(days=random.randint(1, 60))
                    status = 'completed'
                else:  # cancelled
                    booking_date = timezone.now() + datetime.timedelta(days=random.randint(1, 60))
                    status = 'cancelled'
                
                booking = Booking.objects.create(
                    user=user,
                    subevent=subevent,
                    booking_date=booking_date,
                    booking_time=timezone.now().time(),
                    guests=random.randint(2, 10),
                    notes=f"Special request from {user.username} for {subevent.name}" if random.choice([True, False]) else "",
                    total_amount=subevent.price * random.randint(2, 10),
                    status=status,
                    cancellation_reason="Customer changed plans" if status == 'cancelled' else None,
                )
                self.stdout.write(self.style.SUCCESS(f'Created {status} booking for {user.username}'))
        
        self.stdout.write(self.style.SUCCESS('Sample data creation completed successfully!'))
