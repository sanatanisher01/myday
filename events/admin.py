from django.contrib import admin
from .models import Event, SubEvent, Review, Booking, UserProfile, ContactMessage, Newsletter

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')

@admin.register(SubEvent)
class SubEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'price', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description', 'event__name')
    list_filter = ('event', 'created_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'rating', 'created_at')
    search_fields = ('user__username', 'event__name', 'comment')
    list_filter = ('rating', 'created_at', 'event')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'subevent', 'booking_date', 'booking_time', 'status')
    search_fields = ('user__username', 'subevent__name', 'notes')
    list_filter = ('status', 'booking_date', 'created_at')
    date_hierarchy = 'booking_date'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'country', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'city', 'country')
    list_filter = ('country', 'city')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'created_at'

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} message(s) marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f"{queryset.count()} message(s) marked as unread.")
    mark_as_unread.short_description = "Mark selected messages as unread"


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'subscribed_at', 'last_sent')
    list_filter = ('is_active', 'subscribed_at', 'last_sent')
    search_fields = ('email', 'name')
    readonly_fields = ('subscribed_at', 'last_sent')

    actions = ['mark_as_active', 'mark_as_inactive', 'send_welcome_email']

    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} subscriber(s) marked as active.")
    mark_as_active.short_description = "Mark selected subscribers as active"

    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} subscriber(s) marked as inactive.")
    mark_as_inactive.short_description = "Mark selected subscribers as inactive"

    def send_welcome_email(self, request, queryset):
        from django.core.mail import send_mail
        from django.conf import settings

        count = 0
        for subscriber in queryset:
            try:
                send_mail(
                    subject='Welcome to MyDay Events Newsletter',
                    message=f'Hello {subscriber.name or "there"},\n\nThank you for subscribing to our newsletter! You will now receive updates about our latest events and special offers.\n\nBest regards,\nMyDay Events Team',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )
                count += 1
            except Exception as e:
                self.message_user(request, f"Error sending email to {subscriber.email}: {str(e)}", level='ERROR')

        self.message_user(request, f"Welcome email sent to {count} subscriber(s).")
    send_welcome_email.short_description = "Send welcome email to selected subscribers"
