from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Event, SubEvent, Review, Booking

class EventForm(forms.ModelForm):
    """Form for creating and updating events"""
    class Meta:
        model = Event
        fields = ['name', 'description', 'image']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('event_form', 'Save Event', css_class='btn-primary'))
        self.fields['description'].widget.attrs = {'rows': 4}
        

class SubEventForm(forms.ModelForm):
    """Form for creating and updating sub-events"""
    class Meta:
        model = SubEvent
        fields = ['event', 'name', 'description', 'price', 'image']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('subevent_form', 'Save Sub-Event', css_class='btn-primary'))
        self.fields['description'].widget.attrs = {'rows': 4}


class ReviewForm(forms.ModelForm):
    """Form for creating reviews"""
    class Meta:
        model = Review
        fields = ['rating', 'comment', 'image']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1, 
                'max': 5, 
                'class': 'form-range',
                'step': 1
            }),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'rating',
            'comment',
            'image',
            Submit('submit', 'Submit Review', css_class='btn-primary mt-3')
        )


class BookingForm(forms.ModelForm):
    """Form for creating bookings"""
    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time', 'notes']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('booking_date', css_class='form-group col-md-6'),
                Column('booking_time', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'notes',
            Submit('submit', 'Book Now', css_class='btn-primary mt-3')
        )


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'email',
            Submit('submit', 'Update Profile', css_class='btn-primary mt-3')
        )
