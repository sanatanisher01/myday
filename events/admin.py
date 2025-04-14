from django.contrib import admin
from .models import Event, SubEvent, Review, Booking, UserProfile, ContactMessage, Newsletter, NewsletterTemplate, NewsletterCampaign

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
        from django.utils import timezone

        count = 0
        for subscriber in queryset:
            try:
                # Create HTML content
                html_message = f'''
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                        .header {{ background-color: #4e73df; color: white; padding: 20px; text-align: center; }}
                        .content {{ padding: 20px; background-color: #f9f9f9; }}
                        .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #777; }}
                        ul {{ padding-left: 20px; }}
                        .button {{ display: inline-block; background-color: #4e73df; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>Welcome to MyDay Events Newsletter!</h1>
                        </div>
                        <div class="content">
                            <p>Hello {subscriber.name or "there"},</p>
                            <p>Thank you for subscribing to the MyDay Events newsletter!</p>
                            <p>You will now receive updates about:</p>
                            <ul>
                                <li>Our latest event offerings</li>
                                <li>Special promotions and discounts</li>
                                <li>Seasonal packages and themes</li>
                                <li>Event planning tips and inspiration</li>
                            </ul>
                            <p>If you have any questions or need assistance with planning your event, feel free to reply to this email or contact our support team at +91 6397664902.</p>
                            <p><a href="https://myday-kokr.onrender.com/events/" class="button">Explore Our Events</a></p>
                        </div>
                        <div class="footer">
                            <p>Best regards,<br>Aryan Sanatani<br>MyDay Events Team</p>
                            <p>&copy; 2025 MyDay Events. All rights reserved.</p>
                        </div>
                    </div>
                </body>
                </html>
                '''

                # Plain text version
                plain_message = f'''Hello {subscriber.name or "there"},

Thank you for subscribing to the MyDay Events newsletter!

You will now receive updates about:
- Our latest event offerings
- Special promotions and discounts
- Seasonal packages and themes
- Event planning tips and inspiration

If you have any questions or need assistance with planning your event, feel free to reply to this email or contact our support team at +91 6397664902.

Best regards,
Aryan Sanatani
MyDay Events Team'''

                # Send email
                send_mail(
                    subject='Welcome to MyDay Events Newsletter!',
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                    html_message=html_message
                )

                # Update last_sent timestamp
                subscriber.last_sent = timezone.now()
                subscriber.save(update_fields=['last_sent'])
                count += 1
            except Exception as e:
                self.message_user(request, f"Error sending email to {subscriber.email}: {str(e)}", level='ERROR')

        self.message_user(request, f"Welcome email sent to {count} subscriber(s).")
    send_welcome_email.short_description = "Send welcome email to selected subscribers"


@admin.register(NewsletterTemplate)
class NewsletterTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'is_default', 'created_at', 'updated_at')
    list_filter = ('is_default', 'created_at', 'updated_at')
    search_fields = ('name', 'subject', 'content')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'subject', 'is_default')
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NewsletterCampaign)
class NewsletterCampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'status', 'scheduled_at', 'sent_at', 'sent_count')
    list_filter = ('status', 'created_at', 'sent_at')
    search_fields = ('name', 'subject', 'content')
    readonly_fields = ('created_at', 'updated_at', 'sent_at', 'sent_count', 'error_message')
    fieldsets = (
        (None, {
            'fields': ('name', 'subject', 'template')
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('wide',)
        }),
        ('Status', {
            'fields': ('status', 'scheduled_at')
        }),
        ('Results', {
            'fields': ('sent_at', 'sent_count', 'error_message'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['send_campaign', 'mark_as_draft']

    def send_campaign(self, request, queryset):
        from django.core.mail import send_mail
        from django.conf import settings
        from django.utils import timezone
        from django.template import Template, Context

        count = 0
        for campaign in queryset:
            if campaign.status in ['draft', 'scheduled', 'failed']:
                try:
                    # Update status to sending
                    campaign.status = 'sending'
                    campaign.save(update_fields=['status'])

                    # Get all active subscribers
                    subscribers = Newsletter.objects.filter(is_active=True)

                    # Prepare template
                    template_content = campaign.content
                    if campaign.template:
                        template_content = campaign.template.content

                    # Send to each subscriber
                    for subscriber in subscribers:
                        # Create context for template
                        context = Context({
                            'name': subscriber.name or 'there',
                            'email': subscriber.email,
                            'subject': campaign.subject,
                            'custom_message': campaign.content,
                            'unsubscribe_url': f"{request.scheme}://{request.get_host()}/newsletter/unsubscribe/?email={subscriber.email}"
                        })

                        # Render template
                        template = Template(template_content)
                        html_message = template.render(context)

                        # Send email
                        send_mail(
                            subject=campaign.subject,
                            message=campaign.content,  # Plain text version
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[subscriber.email],
                            fail_silently=False,
                            html_message=html_message
                        )

                        # Update subscriber's last_sent timestamp
                        subscriber.last_sent = timezone.now()
                        subscriber.save(update_fields=['last_sent'])

                    # Update campaign status
                    campaign.status = 'sent'
                    campaign.sent_at = timezone.now()
                    campaign.sent_count = subscribers.count()
                    campaign.save(update_fields=['status', 'sent_at', 'sent_count'])
                    count += 1
                except Exception as e:
                    campaign.status = 'failed'
                    campaign.error_message = str(e)
                    campaign.save(update_fields=['status', 'error_message'])
                    self.message_user(request, f"Error sending campaign '{campaign.name}': {str(e)}", level='ERROR')

        self.message_user(request, f"{count} campaign(s) sent successfully.")
    send_campaign.short_description = "Send selected campaigns"

    def mark_as_draft(self, request, queryset):
        queryset.update(status='draft')
        self.message_user(request, f"{queryset.count()} campaign(s) marked as draft.")
    mark_as_draft.short_description = "Mark selected campaigns as draft"
