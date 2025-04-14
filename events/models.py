from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

class Event(models.Model):
    """
    Main event category model (e.g. Wedding, Birthday, Anniversary)
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', max_length=500)  # Increased max_length for full paths
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class SubEvent(models.Model):
    """
    Sub-events under each main event (e.g. Wedding Photography, Birthday Cake)
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='subevents')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='subevents/', max_length=500)  # Increased max_length for full paths
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.event.name}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event.name} - {self.name}"

    class Meta:
        ordering = ['event', 'name']


class SubEventCategory(models.Model):
    """Model for subevent categories (add-ons or options)"""
    subevent = models.ForeignKey(SubEvent, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Sub-event categories'

    def __str__(self):
        return f"{self.subevent.name} - {self.name}"


class Booking(models.Model):
    """Model for event bookings"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    subevent = models.ForeignKey(SubEvent, on_delete=models.CASCADE, related_name='bookings')
    categories = models.ManyToManyField(SubEventCategory, blank=True, related_name='bookings')
    booking_date = models.DateField()
    booking_time = models.TimeField()
    guests = models.PositiveIntegerField(default=1)
    address = models.CharField(max_length=255, null=True, blank=True)  # Temporarily allowing null
    mobile_number = models.CharField(max_length=20, null=True, blank=True)  # Temporarily allowing null
    notes = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.subevent.name} - {self.booking_date}"


class Review(models.Model):
    """
    User reviews for events
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.event.name}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'event']


class UserProfile(models.Model):
    """Extended user profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # Address information
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    email_promotions = models.BooleanField(default=False)
    email_system_updates = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)

    # Privacy settings
    profile_visibility = models.CharField(
        max_length=10,
        choices=[
            ('public', 'Public'),
            ('limited', 'Limited'),
            ('private', 'Private')
        ],
        default='limited'
    )
    allow_data_collection = models.BooleanField(default=True)
    allow_third_party_sharing = models.BooleanField(default=False)

    # Security settings
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class ContactMessage(models.Model):
    """Model for storing contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject[:30]}"


class GalleryItem(models.Model):
    """Model for subevent gallery images"""
    subevent = models.ForeignKey(SubEvent, on_delete=models.CASCADE, related_name='gallery_items')
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Gallery item for {self.subevent.name}"


class CartItem(models.Model):
    """Model for storing items in a user's cart"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    subevent = models.ForeignKey(SubEvent, on_delete=models.CASCADE)
    category = models.ForeignKey(SubEventCategory, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    booking_date = models.DateField(null=True, blank=True)
    booking_time = models.TimeField(null=True, blank=True)
    guests = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.category:
            return f"{self.user.username} - {self.subevent.name} - {self.category.name}"
        return f"{self.user.username} - {self.subevent.name}"

    def get_total_price(self):
        """Calculate the total price for this cart item"""
        base_price = self.subevent.price * self.guests
        category_price = self.category.price * self.quantity if self.category else 0
        return base_price + category_price


class UserMessage(models.Model):
    """Model for messages from managers to users"""
    MESSAGE_TYPES = (
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('danger', 'Danger'),
    )

    SECTION_CHOICES = (
        ('general', 'General'),
        ('bookings', 'Bookings'),
        ('events', 'Events'),
        ('gallery', 'Gallery'),
        ('categories', 'Categories'),
        ('support', 'Support'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='info')
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default='general')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_messages')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.user.username}"


class ActivityLog(models.Model):
    """Model for tracking system activities"""
    ACTION_TYPES = (
        ('booking_created', 'Booking Created'),
        ('booking_updated', 'Booking Updated'),
        ('booking_cancelled', 'Booking Cancelled'),
        ('booking_completed', 'Booking Completed'),
        ('user_registered', 'User Registered'),
        ('user_updated', 'User Updated'),
        ('event_created', 'Event Created'),
        ('event_updated', 'Event Updated'),
        ('event_deleted', 'Event Deleted'),
        ('subevent_created', 'Subevent Created'),
        ('subevent_updated', 'Subevent Updated'),
        ('subevent_deleted', 'Subevent Deleted'),
        ('gallery_updated', 'Gallery Updated'),
        ('message_sent', 'Message Sent'),
        ('review_posted', 'Review Posted'),
        ('admin_action', 'Admin Action'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    description = models.TextField()
    target_model = models.CharField(max_length=50, blank=True, null=True)
    target_id = models.PositiveIntegerField(blank=True, null=True)
    additional_data = models.JSONField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'

    def __str__(self):
        return f"{self.action_type} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    @classmethod
    def log_activity(cls, user, action_type, description, target_model=None, target_id=None, additional_data=None, request=None):
        """
        Helper method to create activity log entries
        """
        ip_address = None
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')

        return cls.objects.create(
            user=user,
            action_type=action_type,
            description=description,
            target_model=target_model,
            target_id=target_id,
            additional_data=additional_data,
            ip_address=ip_address
        )
