from django.contrib import admin
from .models import Event, SubEvent, Review, Booking, UserProfile, ContactMessage

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
