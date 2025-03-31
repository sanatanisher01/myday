from rest_framework import serializers
from .models import Event, SubEvent, Review, Booking

class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model"""
    avg_rating = serializers.FloatField(read_only=True, required=False)
    
    class Meta:
        model = Event
        fields = ['id', 'name', 'slug', 'description', 'image', 'created_at', 'updated_at', 'avg_rating']
        read_only_fields = ['slug', 'created_at', 'updated_at']

class SubEventSerializer(serializers.ModelSerializer):
    """Serializer for SubEvent model"""
    event_name = serializers.CharField(source='event.name', read_only=True)
    
    class Meta:
        model = SubEvent
        fields = ['id', 'name', 'slug', 'event', 'event_name', 'description', 'price', 'image', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    event_name = serializers.CharField(source='event.name', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'user_username', 'event', 'event_name', 'rating', 'comment', 'image', 'created_at']
        read_only_fields = ['user', 'created_at']

class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    subevent_name = serializers.CharField(source='subevent.name', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'user_username', 'subevent', 'subevent_name', 'booking_date', 
                 'booking_time', 'status', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
