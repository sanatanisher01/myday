from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Avg, Count, Sum, Q, Min
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from rest_framework import viewsets, permissions

from .models import Event, SubEvent, Review, Booking, UserProfile, ContactMessage, User, GalleryItem, SubEventCategory, CartItem, UserMessage
from .serializers import EventSerializer, SubEventSerializer, ReviewSerializer
from .forms import ReviewForm, BookingForm, EventForm, SubEventForm, GalleryItemForm, SubEventCategoryForm, UserMessageForm

def is_admin(user):
    """Check if user is an admin"""
    return user.is_superuser

# Public views
def home(request):
    """Home page / landing page view"""
    events = Event.objects.all()
    top_rated_events = Event.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:4]
    recent_reviews = Review.objects.all().order_by('-created_at')[:6]
    
    context = {
        'events': events,
        'top_rated_events': top_rated_events,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'events/home.html', context)

def event_list(request):
    """List all event categories"""
    # Get the search parameter from the request
    search_query = request.GET.get('search', '')
    sort_param = request.GET.get('sort', '-created_at')  # Default sort by newest
    
    # Start with all events
    events_queryset = Event.objects.all().prefetch_related('subevents')
    
    # Apply search filter if provided
    if search_query:
        events_queryset = events_queryset.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Apply sorting
    if sort_param:
        if sort_param == '-reviews':
            # Handle special case for sorting by reviews
            events_queryset = events_queryset.annotate(
                avg_rating=Avg('reviews__rating'),
                review_count=Count('reviews')
            ).order_by('-avg_rating')
        else:
            events_queryset = events_queryset.order_by(sort_param)
    
    # Annotate with ratings and price information
    events = events_queryset.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews'),
        min_price=Min('subevents__price')
    )
    
    # Get categories for filter dropdown
    categories = Event.objects.all()
    
    context = {
        'events': events,
        'categories': categories
    }
    
    return render(request, 'events/event_list.html', context)

def event_detail(request, slug):
    """Show details of a specific event category and its sub-events"""
    event = get_object_or_404(Event, slug=slug)
    subevents = event.subevents.all()
    reviews = event.reviews.all()
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'event': event,
        'subevents': subevents,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'events/event_detail.html', context)

def subevent_detail(request, event_slug, subevent_slug):
    """Show details of a specific sub-event"""
    event = get_object_or_404(Event, slug=event_slug)
    subevent = get_object_or_404(SubEvent, slug=subevent_slug, event=event)
    
    # Handle booking form
    if request.method == 'POST' and request.user.is_authenticated:
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.subevent = subevent
            booking.save()
            messages.success(request, "Booking created successfully!")
            return redirect('user_bookings')
    else:
        form = BookingForm()
        
    context = {
        'event': event,
        'subevent': subevent,
        'booking_form': form,
    }
    return render(request, 'events/subevent_detail.html', context)

# User dashboard views
@login_required
def user_dashboard(request):
    """User dashboard view"""
    user_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')[:5]
    upcoming_bookings = Booking.objects.filter(
        user=request.user,
        booking_date__gte=timezone.now().date(),
        status__in=['pending', 'confirmed']
    ).order_by('booking_date', 'booking_time')[:3]
    
    # Get user messages
    all_user_messages = UserMessage.objects.filter(user=request.user)
    user_messages = all_user_messages.order_by('-created_at')[:5]
    unread_count = all_user_messages.filter(is_read=False).count()
    
    context = {
        'user_bookings': user_bookings,
        'upcoming_bookings': upcoming_bookings,
        'user_messages': user_messages,
        'unread_count': unread_count,
    }
    return render(request, 'events/user/dashboard.html', context)

@login_required
def user_bookings(request):
    """View function for displaying user's bookings."""
    # Get current date for comparison
    today = timezone.now().date()
    
    # Get all bookings for the current user
    all_bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    
    # Split bookings by status
    upcoming_bookings = all_bookings.filter(
        Q(status='pending') | Q(status='confirmed'),
        booking_date__gte=today
    )
    
    past_bookings = all_bookings.filter(
        Q(status='confirmed'),
        booking_date__lt=today
    )
    
    cancelled_bookings = all_bookings.filter(status='cancelled')
    
    # Add a status_color property to each booking for badge styling
    for booking in all_bookings:
        if booking.status == 'pending':
            booking.status_color = 'pending'
        elif booking.status == 'confirmed':
            if booking.booking_date < today:
                booking.status_color = 'completed'
            else:
                booking.status_color = 'confirmed'
        elif booking.status == 'cancelled':
            booking.status_color = 'cancelled'
        
        # Check if the booking has a review
        booking.has_review = Review.objects.filter(user=request.user, event=booking.subevent.event).exists()
    
    context = {
        'all_bookings': all_bookings,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'cancelled_bookings': cancelled_bookings,
    }
    
    return render(request, 'events/user/bookings.html', context)

@login_required
def cancel_booking(request, booking_id):
    """View function to handle booking cancellation."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Check if booking can be cancelled
    if booking.status not in ['pending', 'confirmed']:
        messages.error(request, "This booking cannot be cancelled.")
        return redirect('user_bookings')
    
    if request.method == 'POST':
        # Update booking status
        booking.status = 'cancelled'
        
        # Get cancellation reason and notes
        reason = request.POST.get('reason')
        notes = request.POST.get('notes', '')
        
        # Store cancellation details
        booking.cancellation_reason = reason
        booking.notes = f"{booking.notes}\n\nCancellation notes: {notes}" if booking.notes else f"Cancellation notes: {notes}"
        booking.save()
        
        messages.success(request, "Your booking has been successfully cancelled.")
        
        # Send notification or email about cancellation
        # notify_booking_cancellation(booking)  # Placeholder for notification system
        
        return redirect('user_bookings')
    
    # If not POST, redirect to bookings page
    return redirect('user_bookings')

@login_required
def user_profile(request):
    """User profile page"""
    if request.method == 'POST':
        # Get profile data from form
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        date_of_birth = request.POST.get('date_of_birth', None)
        bio = request.POST.get('bio', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        country = request.POST.get('country', '')
        
        # Update user data
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        # Update or create user profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.phone = phone
        
        if date_of_birth:
            profile.date_of_birth = date_of_birth
            
        profile.bio = bio
        profile.address = address
        profile.city = city
        profile.state = state
        profile.zip_code = zip_code
        profile.country = country
        
        # Handle avatar upload
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        # Handle avatar removal
        if request.POST.get('remove_avatar') == 'true':
            # Delete the old image file if it exists
            if profile.avatar:
                if os.path.isfile(profile.avatar.path):
                    os.remove(profile.avatar.path)
            profile.avatar = None
        
        profile.save()
        
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('user_profile')
    
    # Get statistics for the user
    bookings_count = Booking.objects.filter(user=request.user).count()
    completed_bookings_count = Booking.objects.filter(
        user=request.user,
        booking_date__lt=timezone.now().date(),
        status='confirmed'
    ).count()
    reviews_count = Review.objects.filter(user=request.user).count()
    
    # Placeholder for saved events (if you implement this feature later)
    saved_events_count = 0
    
    context = {
        'bookings_count': bookings_count,
        'completed_bookings_count': completed_bookings_count,
        'reviews_count': reviews_count,
        'saved_events_count': saved_events_count,
    }
    
    return render(request, 'events/user/profile.html', context)

@login_required
def user_settings(request):
    """User settings page for account preferences and security."""
    if request.method == 'POST' and 'email' in request.POST:
        # Handle account preferences update
        user = request.user
        user.email = request.POST.get('email')
        user.save()
        
        # Update profile settings if UserProfile exists
        if hasattr(user, 'profile'):
            user.profile.marketing_emails = 'marketing_emails' in request.POST
            user.profile.save()
        
        messages.success(request, "Account preferences updated successfully!")
        return redirect('user_settings')
    
    context = {}
    return render(request, 'events/user/settings.html', context)

@login_required
def change_password(request):
    """Handle password change requests."""
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if current password is correct
        if not request.user.check_password(current_password):
            messages.error(request, 'Your current password is incorrect.')
            return redirect('user_settings')
        
        # Check if new passwords match
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('user_settings')
        
        # Check password complexity
        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('user_settings')
        
        # Update password
        request.user.set_password(new_password)
        request.user.save()
        
        # Update user's session to prevent automatic logout
        update_session_auth_hash(request, request.user)
        
        messages.success(request, 'Your password has been changed successfully.')
        return redirect('user_settings')
    
    return redirect('user_settings')

@login_required
def update_notification_settings(request):
    """Update user notification preferences."""
    if request.method == 'POST':
        user_profile = request.user.profile
        
        # Email notifications
        user_profile.email_notifications = 'email_booking_confirmations' in request.POST
        user_profile.email_promotions = 'email_promotions' in request.POST
        user_profile.email_system_updates = 'email_system_updates' in request.POST
        
        # SMS notifications
        user_profile.sms_notifications = 'sms_booking_alerts' in request.POST
        
        user_profile.save()
        
        messages.success(request, 'Notification preferences updated successfully.')
        return redirect('user_settings')
    
    return redirect('user_settings')

@login_required
def update_privacy_settings(request):
    """Update user privacy settings."""
    if request.method == 'POST':
        user_profile = request.user.profile
        
        # Profile visibility
        visibility = request.POST.get('profile_visibility', 'private')
        if visibility in ['public', 'limited', 'private']:
            user_profile.profile_visibility = visibility
        
        # Data preferences
        user_profile.allow_data_collection = 'allow_data_collection' in request.POST
        user_profile.allow_third_party_sharing = 'allow_third_party_sharing' in request.POST
        
        user_profile.save()
        
        messages.success(request, 'Privacy settings updated successfully.')
        return redirect('user_settings')
    
    return redirect('user_settings')

@login_required
def setup_2fa(request):
    """Set up two-factor authentication."""
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        
        # This is a placeholder. In a real implementation, you would verify the code
        # against a generated secret and enable 2FA if valid.
        if verification_code and len(verification_code) == 6 and verification_code.isdigit():
            user_profile = request.user.profile
            user_profile.two_factor_enabled = True
            user_profile.save()
            
            messages.success(request, 'Two-factor authentication has been enabled for your account.')
        else:
            messages.error(request, 'Invalid verification code. Please try again.')
            
        return redirect('user_settings')
    
    return redirect('user_settings')

@login_required
def delete_account(request):
    """Handle account deletion requests."""
    if request.method == 'POST':
        delete_confirmation = request.POST.get('delete_confirmation')
        password = request.POST.get('password')
        feedback = request.POST.get('feedback', '')
        
        # Verify confirmation text and password
        if delete_confirmation != 'DELETE':
            messages.error(request, 'Please type DELETE to confirm account deletion.')
            return redirect('user_settings')
        
        if not request.user.check_password(password):
            messages.error(request, 'Incorrect password. Account deletion cancelled.')
            return redirect('user_settings')
        
        # Store feedback if provided (optional implementation)
        if feedback:
            # Save feedback to a deletion feedback model or send to admin
            pass
        
        # Delete user account
        user = request.user
        logout(request)  # Log the user out first
        user.delete()    # Then delete the account
        
        messages.success(request, 'Your account has been permanently deleted.')
        return redirect('home')
    
    return redirect('user_settings')

@login_required
def user_messages(request):
    """User messages view"""
    user_messages = UserMessage.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark all messages as read if requested
    if request.method == 'POST' and 'mark_all_read' in request.POST:
        user_messages.filter(is_read=False).update(is_read=True)
        messages.success(request, "All messages marked as read.")
        return redirect('user_messages')
    
    context = {
        'user_messages': user_messages,
    }
    return render(request, 'events/user/messages.html', context)

@login_required
def mark_message_read(request, message_id):
    """Mark a message as read"""
    message = get_object_or_404(UserMessage, id=message_id, user=request.user)
    message.is_read = True
    message.save()
    return redirect('user_messages')

def contact(request):
    """Contact page with form for user inquiries."""
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        agree_tos = request.POST.get('agree_tos', '') == 'on'
        
        # Validate form inputs
        if not all([name, email, subject, message, agree_tos]):
            messages.error(request, 'Please fill in all required fields and agree to the privacy policy.')
            return redirect('contact')
        
        try:
            # Save contact message to database
            contact_message = ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            
            # Send notification email to admin (this would be implemented with actual email sending logic)
            # send_admin_notification(contact_message)
            
            # Optionally send confirmation email to user
            # send_confirmation_email(email, name)
            
            messages.success(request, 
                'Thank you for contacting us! Your message has been received. '
                'We will get back to you within 24 hours.')
        except Exception as e:
            # Log the error
            print(f"Error processing contact form: {str(e)}")
            messages.error(request, 
                'There was an error processing your request. '
                'Please try again or contact us directly at support@mydayevents.com.')
    
    return render(request, 'events/contact.html')

def manager_login(request):
    """Manager login view with specific credentials"""
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        
        # Check for hardcoded manager credentials
        if mobile == '8630500821' and password == 'Aryan@010':
            # First try to find a user with this phone in UserProfile
            try:
                user_profile = UserProfile.objects.get(phone=mobile)
                user = user_profile.user
            except UserProfile.DoesNotExist:
                # Look for an existing manager user
                try:
                    user = User.objects.get(username='manager')
                    # Update the profile with the phone number
                    try:
                        user_profile = UserProfile.objects.get(user=user)
                        user_profile.phone = mobile
                        user_profile.save()
                    except UserProfile.DoesNotExist:
                        # Create a profile for the existing manager
                        user_profile = UserProfile.objects.create(
                            user=user,
                            phone=mobile
                        )
                except User.DoesNotExist:
                    # Create a new manager user if it doesn't exist
                    user = User.objects.create_user(
                        username='manager',
                        email='manager@example.com',
                        password=password
                    )
                    user.is_staff = True
                    user.save()
                    
                    # Create profile for the manager
                    user_profile = UserProfile.objects.create(
                        user=user,
                        phone=mobile
                    )
            
            # Log the user in
            login(request, user)
            messages.success(request, "Welcome, Manager!")
            return redirect('manager_dashboard')
        else:
            messages.error(request, "Invalid manager credentials")
    
    return render(request, 'events/manager/login.html')

# Admin dashboard views
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard view with overview and statistics."""
    # Get counts for statistics
    total_events = Event.objects.count()
    total_bookings = Booking.objects.count()
    total_users = User.objects.count()
    
    # Calculate total revenue
    total_revenue = Booking.objects.filter(status='confirmed').aggregate(
        total=Sum('subevent__price')
    )['total'] or 0
    
    # Get recent bookings
    recent_bookings = Booking.objects.select_related('user', 'subevent').order_by('-created_at')[:5]
    for booking in recent_bookings:
        booking.total_amount = booking.subevent.price

    # Get unread messages count
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    
    # Get pending bookings count
    pending_bookings = Booking.objects.filter(status='pending').count()
    
    # Get recent messages
    recent_messages = ContactMessage.objects.all().order_by('-created_at')[:5]
    
    context = {
        'total_events': total_events,
        'total_bookings': total_bookings,
        'total_users': total_users,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
        'unread_messages': unread_messages,
        'pending_bookings': pending_bookings,
        'recent_messages': recent_messages,
        'today': datetime.now().date(),
    }
    
    return render(request, 'events/admin/dashboard.html', context)

@user_passes_test(is_admin)
def admin_events(request):
    """Admin events management page"""
    events = Event.objects.all()
    subevents = SubEvent.objects.all()
    
    # Handle event form
    if request.method == 'POST':
        if 'event_form' in request.POST:
            event_form = EventForm(request.POST, request.FILES)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, "Event added successfully!")
                return redirect('admin_events')
        elif 'subevent_form' in request.POST:
            subevent_form = SubEventForm(request.POST, request.FILES)
            if subevent_form.is_valid():
                subevent_form.save()
                messages.success(request, "Sub-event added successfully!")
                return redirect('admin_events')
    else:
        event_form = EventForm()
        subevent_form = SubEventForm()
    
    context = {
        'events': events,
        'subevents': subevents,
        'event_form': event_form,
        'subevent_form': subevent_form,
    }
    return render(request, 'events/admin/events.html', context)

@user_passes_test(is_admin)
def admin_bookings(request):
    """Admin bookings management page"""
    bookings = Booking.objects.all().order_by('-created_at')
    context = {'bookings': bookings}
    return render(request, 'events/admin/bookings.html', context)

@user_passes_test(is_admin)
def admin_reviews(request):
    """Admin reviews management page"""
    reviews = Review.objects.all().order_by('-created_at')
    context = {'reviews': reviews}
    return render(request, 'events/admin/reviews.html', context)

@user_passes_test(is_admin)
def admin_users(request):
    """Admin user management page"""
    users = User.objects.all().select_related('profile').order_by('-date_joined')
    
    # Handle user status changes if submitted
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        
        if user_id and action:
            try:
                user = User.objects.get(id=user_id)
                
                if action == 'activate':
                    user.is_active = True
                    messages.success(request, f"User {user.username} has been activated.")
                elif action == 'deactivate':
                    user.is_active = False
                    messages.success(request, f"User {user.username} has been deactivated.")
                elif action == 'make_staff':
                    user.is_staff = True
                    messages.success(request, f"{user.username} has been given staff permissions.")
                elif action == 'remove_staff':
                    user.is_staff = False
                    messages.success(request, f"Staff permissions removed from {user.username}.")
                
                user.save()
            except User.DoesNotExist:
                messages.error(request, "User not found.")
    
    context = {
        'users': users
    }
    return render(request, 'events/admin/users.html', context)

@user_passes_test(is_admin)
def admin_add_user(request):
    """Handle adding a new user from the admin panel"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        is_staff = request.POST.get('is_staff') == 'on'
        
        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' is already taken.")
            return redirect('admin_users')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, f"Email '{email}' is already registered.")
            return redirect('admin_users')
        
        # Create the new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Set staff status if checked
        if is_staff:
            user.is_staff = True
            user.save()
            
        # Create user profile
        UserProfile.objects.create(user=user)
            
        messages.success(request, f"User '{username}' has been created successfully.")
        return redirect('admin_users')
        
    # If not POST, redirect to users page
    return redirect('admin_users')

# Manager views
def manager_login(request):
    """Manager login view with specific credentials"""
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        
        # Check for hardcoded manager credentials
        if mobile == '8630500821' and password == 'Aryan@010':
            # First try to find a user with this phone in UserProfile
            try:
                user_profile = UserProfile.objects.get(phone=mobile)
                user = user_profile.user
            except UserProfile.DoesNotExist:
                # Look for an existing manager user
                try:
                    user = User.objects.get(username='manager')
                    # Update the profile with the phone number
                    try:
                        user_profile = UserProfile.objects.get(user=user)
                        user_profile.phone = mobile
                        user_profile.save()
                    except UserProfile.DoesNotExist:
                        # Create a profile for the existing manager
                        user_profile = UserProfile.objects.create(
                            user=user,
                            phone=mobile
                        )
                except User.DoesNotExist:
                    # Create a new manager user if it doesn't exist
                    user = User.objects.create_user(
                        username='manager',
                        email='manager@example.com',
                        password=password
                    )
                    user.is_staff = True
                    user.save()
                    
                    # Create profile for the manager
                    user_profile = UserProfile.objects.create(
                        user=user,
                        phone=mobile
                    )
            
            # Log the user in
            login(request, user)
            messages.success(request, "Welcome, Manager!")
            return redirect('manager_dashboard')
        else:
            messages.error(request, "Invalid manager credentials")
    
    return render(request, 'events/manager/login.html')

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def manager_dashboard(request):
    """Manager dashboard with overview of site data"""
    # Count statistics for dashboard
    event_count = Event.objects.count()
    subevent_count = SubEvent.objects.count()
    booking_count = Booking.objects.count()
    user_count = User.objects.filter(is_staff=False, is_superuser=False).count()
    
    # Recent items
    recent_bookings = Booking.objects.all().order_by('-created_at')[:5]
    recent_events = Event.objects.all().order_by('-created_at')[:5]
    recent_users = User.objects.filter(is_staff=False, is_superuser=False).order_by('-date_joined')[:5]
    
    # Calculate revenue
    total_revenue = Booking.objects.filter(status='confirmed').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    context = {
        'event_count': event_count,
        'subevent_count': subevent_count,
        'booking_count': booking_count,
        'user_count': user_count,
        'recent_bookings': recent_bookings,
        'recent_events': recent_events,
        'recent_users': recent_users,
        'total_revenue': total_revenue,
    }
    
    return render(request, 'events/manager/dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def manager_events(request):
    """Manager events management page"""
    events = Event.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        # Handle creating new event
        if 'create_event' in request.POST:
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Event created successfully!")
                return redirect('manager_events')
        
        # Handle updating event
        elif 'update_event' in request.POST:
            event_id = request.POST.get('event_id')
            event = get_object_or_404(Event, id=event_id)
            form = EventForm(request.POST, request.FILES, instance=event)
            if form.is_valid():
                form.save()
                messages.success(request, "Event updated successfully!")
                return redirect('manager_events')
        
        # Handle deleting event
        elif 'delete_event' in request.POST:
            event_id = request.POST.get('event_id')
            event = get_object_or_404(Event, id=event_id)
            event_name = event.name
            event.delete()
            messages.success(request, f"Event '{event_name}' deleted successfully!")
            return redirect('manager_events')
    else:
        form = EventForm()
    
    context = {
        'events': events,
        'form': form,
    }
    
    return render(request, 'events/manager/events.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def manager_subevents(request, event_id=None):
    """Manager subevents management page"""
    event = None
    if event_id:
        event = get_object_or_404(Event, id=event_id)
        subevents = SubEvent.objects.filter(event=event).order_by('-created_at')
    else:
        subevents = SubEvent.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        # Handle creating new subevent
        if 'create_subevent' in request.POST:
            form = SubEventForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Sub-event created successfully!")
                if event_id:
                    return redirect('manager_subevents', event_id=event_id)
                return redirect('manager_subevents')
        
        # Handle updating subevent
        elif 'update_subevent' in request.POST:
            subevent_id = request.POST.get('subevent_id')
            subevent = get_object_or_404(SubEvent, id=subevent_id)
            form = SubEventForm(request.POST, request.FILES, instance=subevent)
            if form.is_valid():
                form.save()
                messages.success(request, "Sub-event updated successfully!")
                if event_id:
                    return redirect('manager_subevents', event_id=event_id)
                return redirect('manager_subevents')
        
        # Handle deleting subevent
        elif 'delete_subevent' in request.POST:
            subevent_id = request.POST.get('subevent_id')
            subevent = get_object_or_404(SubEvent, id=subevent_id)
            subevent_name = subevent.name
            # If we were viewing subevents for a specific event, redirect back to that filtered view
            redirect_url = 'manager_subevents_by_event' if event_id else 'manager_subevents'
            redirect_params = {'event_id': event_id} if event_id else {}
            
            subevent.delete()
            messages.success(request, f"Sub-event '{subevent_name}' deleted successfully!")
            
            if event_id:
                return redirect(redirect_url, event_id)
            else:
                return redirect(redirect_url)
    else:
        initial_data = {'event': event} if event else {}
        form = SubEventForm(initial=initial_data)
    
    context = {
        'event': event,
        'subevents': subevents,
        'form': form,
        'all_events': Event.objects.all(),
    }
    
    return render(request, 'events/manager/subevents.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def manager_bookings(request):
    """Manager bookings management page"""
    bookings = Booking.objects.all().order_by('-created_at')
    
    # Filter bookings if requested
    status_filter = request.GET.get('status')
    if status_filter and status_filter != 'all':
        bookings = bookings.filter(status=status_filter)
    
    context = {
        'bookings': bookings,
    }
    
    return render(request, 'events/manager/bookings.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def manager_update_booking(request, booking_id):
    """Update booking status"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'confirmed', 'cancelled']:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking status updated to {new_status}")
        
        # If sending a message to the user
        message = request.POST.get('message')
        if message:
            # Logic for sending a notification to the user would go here
            # For now, we'll just add it as a note to the booking
            booking.notes = f"{booking.notes}\n\nMessage from manager ({timezone.now().strftime('%Y-%m-%d %H:%M')}): {message}"
            booking.save()
            messages.success(request, "Message sent to user")
            
    return redirect('manager_bookings')

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def manager_users(request):
    """Manager users management page"""
    users = User.objects.filter(is_staff=False, is_superuser=False).order_by('-date_joined')
    
    context = {
        'users': users,
    }
    
    return render(request, 'events/manager/users.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def manager_user_detail(request, user_id):
    """View and manage a specific user"""
    user = get_object_or_404(User, id=user_id)
    
    # Get user's profile, bookings, and reviews
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None
    
    bookings = Booking.objects.filter(user=user).order_by('-created_at')
    reviews = Review.objects.filter(user=user).order_by('-created_at')
    
    # Handle sending message to user
    if request.method == 'POST' and 'send_message' in request.POST:
        message = request.POST.get('message')
        if message:
            # Logic for sending a notification would go here
            # For now, just show a success message
            messages.success(request, f"Message sent to {user.username}")
    
    context = {
        'user_detail': user,
        'profile': profile,
        'bookings': bookings,
        'reviews': reviews,
    }
    
    return render(request, 'events/manager/user_detail.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def manager_contacts(request):
    """Manager view for contact messages"""
    contact_messages = ContactMessage.objects.all().order_by('-created_at')
    
    context = {
        'contact_messages': contact_messages,
    }
    
    return render(request, 'events/manager/contacts.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def manager_messages(request):
    """Manager view for sending and viewing messages to users"""
    messages_sent = UserMessage.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = UserMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.created_by = request.user
            message.save()
            messages.success(request, "Message sent successfully!")
            return redirect('manager_messages')
    else:
        form = UserMessageForm()
    
    context = {
        'form': form,
        'messages_sent': messages_sent,
    }
    
    return render(request, 'events/manager/messages.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def delete_message(request, message_id):
    """Delete a message"""
    message = get_object_or_404(UserMessage, id=message_id)
    message.delete()
    messages.success(request, "Message deleted successfully!")
    return redirect('manager_messages')

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def manager_gallery(request, subevent_id=None):
    """Manager gallery management page"""
    subevent = None
    if subevent_id:
        subevent = get_object_or_404(SubEvent, id=subevent_id)
        gallery_items = GalleryItem.objects.filter(subevent=subevent).order_by('order', 'created_at')
    else:
        gallery_items = GalleryItem.objects.all().order_by('subevent', 'order', 'created_at')
    
    if request.method == 'POST':
        # Handle creating new gallery item
        if 'create_gallery_item' in request.POST:
            form = GalleryItemForm(request.POST, request.FILES, subevent_id=subevent_id)
            if form.is_valid():
                form.save()
                messages.success(request, "Gallery item added successfully!")
                if subevent_id:
                    return redirect('manager_gallery', subevent_id=subevent_id)
                return redirect('manager_gallery')
        
        # Handle updating gallery item
        elif 'update_gallery_item' in request.POST:
            item_id = request.POST.get('item_id')
            gallery_item = get_object_or_404(GalleryItem, id=item_id)
            form = GalleryItemForm(request.POST, request.FILES, instance=gallery_item)
            if form.is_valid():
                form.save()
                messages.success(request, "Gallery item updated successfully!")
                if subevent_id:
                    return redirect('manager_gallery', subevent_id=subevent_id)
                return redirect('manager_gallery')
        
        # Handle deleting gallery item
        elif 'delete_gallery_item' in request.POST:
            item_id = request.POST.get('item_id')
            gallery_item = get_object_or_404(GalleryItem, id=item_id)
            gallery_item.delete()
            messages.success(request, "Gallery item deleted successfully!")
            if subevent_id:
                return redirect('manager_gallery', subevent_id=subevent_id)
            return redirect('manager_gallery')
    else:
        form = GalleryItemForm(subevent_id=subevent_id)
    
    # Get all subevents for filtering
    subevents = SubEvent.objects.all().order_by('event__name', 'name')
    
    context = {
        'gallery_items': gallery_items,
        'form': form,
        'subevent': subevent,
        'subevents': subevents,
    }
    
    return render(request, 'events/manager/gallery.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def manager_categories(request, subevent_id=None):
    """Manager categories management page"""
    subevent = None
    if subevent_id:
        subevent = get_object_or_404(SubEvent, id=subevent_id)
        categories = SubEventCategory.objects.filter(subevent=subevent).order_by('order', 'name')
    else:
        categories = SubEventCategory.objects.all().order_by('subevent', 'order', 'name')
    
    if request.method == 'POST':
        # Handle creating new category
        if 'create_category' in request.POST:
            form = SubEventCategoryForm(request.POST, request.FILES, subevent_id=subevent_id)
            if form.is_valid():
                form.save()
                messages.success(request, "Category added successfully!")
                if subevent_id:
                    return redirect('manager_categories', subevent_id=subevent_id)
                return redirect('manager_categories')
        
        # Handle updating category
        elif 'update_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(SubEventCategory, id=category_id)
            form = SubEventCategoryForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, "Category updated successfully!")
                if subevent_id:
                    return redirect('manager_categories', subevent_id=subevent_id)
                return redirect('manager_categories')
        
        # Handle toggling category active status
        elif 'toggle_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(SubEventCategory, id=category_id)
            category.is_active = not category.is_active
            category.save()
            status = "activated" if category.is_active else "deactivated"
            messages.success(request, f"Category {status} successfully!")
            if subevent_id:
                return redirect('manager_categories', subevent_id=subevent_id)
            return redirect('manager_categories')
        
        # Handle deleting category
        elif 'delete_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(SubEventCategory, id=category_id)
            category_name = category.name
            category.delete()
            messages.success(request, f"Category '{category_name}' deleted successfully!")
            if subevent_id:
                return redirect('manager_categories', subevent_id=subevent_id)
            return redirect('manager_categories')
    else:
        form = SubEventCategoryForm(subevent_id=subevent_id)
    
    # Get all subevents for filtering
    subevents = SubEvent.objects.all().order_by('event__name', 'name')
    
    context = {
        'categories': categories,
        'form': form,
        'subevent': subevent,
        'subevents': subevents,
    }
    
    return render(request, 'events/manager/categories.html', context)

# API ViewSets
class EventViewSet(viewsets.ModelViewSet):
    """API endpoint for events"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SubEventViewSet(viewsets.ModelViewSet):
    """API endpoint for sub-events"""
    queryset = SubEvent.objects.all()
    serializer_class = SubEventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    """API endpoint for reviews"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Authentication views
def signup(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('user_dashboard')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'authentication/signup.html', context)

# Review and Booking actions
@login_required
def add_review(request, event_id):
    """Add a review for an event"""
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.event = event
            review.save()
            messages.success(request, "Review added successfully!")
            return redirect('event_detail', slug=event.slug)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'events/add_review.html', context)

@login_required
def add_booking(request, subevent_id):
    """Add a booking for a subevent"""
    subevent = get_object_or_404(SubEvent, id=subevent_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.subevent = subevent
            
            # Calculate base price (subevent price * guests)
            base_price = subevent.price * booking.guests
            
            # Get selected categories
            selected_categories = request.POST.getlist('categories')
            categories_total = 0
            
            # Calculate total price including categories
            if selected_categories:
                categories = SubEventCategory.objects.filter(id__in=selected_categories)
                categories_total = sum(category.price for category in categories)
            
            # Calculate total amount with tax
            subtotal = base_price + categories_total
            tax = subtotal * Decimal('0.1')  # 10% tax
            booking.total_amount = subtotal + tax
            
            booking.save()
            
            # Save the selected categories to the booking
            if selected_categories:
                for category_id in selected_categories:
                    booking.categories.add(category_id)
            
            messages.success(request, "Your booking has been confirmed! You can view your bookings in your dashboard.")
            return redirect('user_bookings')
    else:
        form = BookingForm()
    
    context = {
        'form': form,
        'subevent': subevent,
        'categories': SubEventCategory.objects.filter(subevent=subevent, is_active=True),
    }
    return render(request, 'events/add_booking.html', context)
