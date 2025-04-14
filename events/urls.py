from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/events', views.EventViewSet, basename='event-api')
router.register(r'api/subevents', views.SubEventViewSet, basename='subevent-api')
router.register(r'api/reviews', views.ReviewViewSet, basename='review-api')

urlpatterns = [
    # Main page routes
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('event/<slug:slug>/', views.event_detail, name='event_detail'),
    path('event/<slug:event_slug>/subevent/<slug:subevent_slug>/', views.subevent_detail, name='subevent_detail'),
    path('contact/', views.contact, name='contact'),

    # User dashboard routes
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/bookings/', views.user_bookings, name='user_bookings'),
    path('dashboard/bookings/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('dashboard/profile/', views.user_profile, name='user_profile'),
    path('dashboard/messages/', views.user_messages, name='user_messages'),
    path('dashboard/messages/read/<int:message_id>/', views.mark_message_read, name='mark_message_read'),
    path('dashboard/settings/', views.user_settings, name='user_settings'),
    path('dashboard/settings/change-password/', views.change_password, name='change_password'),
    path('dashboard/settings/notifications/', views.update_notification_settings, name='update_notification_settings'),
    path('dashboard/settings/privacy/', views.update_privacy_settings, name='update_privacy_settings'),
    path('dashboard/settings/setup-2fa/', views.setup_2fa, name='setup_2fa'),
    path('dashboard/settings/delete-account/', views.delete_account, name='delete_account'),

    # Admin routes
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/events/', views.admin_events, name='admin_events'),
    path('admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin/reviews/', views.admin_reviews, name='admin_reviews'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/add/', views.admin_add_user, name='admin_add_user'),
    path('admin/test-email/', views.test_email, name='test_email'),
    # Use admin_dashboard as a temporary replacement for admin_login
    path('admin/login/', views.admin_dashboard, name='admin_login'),
    path('owner-portal/', views.admin_dashboard, name='admin_login_page'),

    # Manager routes
    path('manager-login/', views.manager_login, name='manager_login'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/events/', views.manager_events, name='manager_events'),
    path('manager/subevents/', views.manager_subevents, name='manager_subevents'),
    path('manager/subevents/<int:event_id>/', views.manager_subevents_by_event, name='manager_subevents_by_event'),
    path('manager/gallery/', views.manager_gallery, name='manager_gallery'),
    path('manager/gallery/<int:subevent_id>/', views.manager_gallery, name='manager_gallery_by_subevent'),
    path('manager/categories/', views.manager_categories, name='manager_categories'),
    path('manager/categories/<int:subevent_id>/', views.manager_categories, name='manager_categories_by_subevent'),
    path('manager/messages/', views.manager_messages, name='manager_messages'),
    path('manager/messages/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('manager/bookings/', views.manager_bookings, name='manager_bookings'),
    path('manager/bookings/<int:booking_id>/update/', views.manager_update_booking, name='manager_update_booking'),
    path('manager/users/', views.manager_users, name='manager_users'),
    path('manager/users/<int:user_id>/', views.manager_user_detail, name='manager_user_detail'),
    path('manager/contacts/', views.manager_contacts, name='manager_contacts'),

    # Authentication routes
    path('signup/', views.signup, name='signup'),
    path('review/<int:event_id>/add/', views.add_review, name='add_review'),
    path('booking/<int:subevent_id>/add/', views.add_booking, name='add_booking'),

    # Newsletter routes
    path('newsletter/subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),

    # API routes
    path('', include(router.urls)),
]
