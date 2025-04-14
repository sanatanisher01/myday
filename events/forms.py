from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Event, SubEvent, Review, Booking, GalleryItem, SubEventCategory, CartItem, UserMessage, Newsletter

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

    def clean_image(self):
        """Validate and process the uploaded image"""
        image = self.cleaned_data.get('image')
        if image:
            # Validate file type
            if not image.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise forms.ValidationError("Unsupported image format. Please use PNG, JPG, JPEG, or GIF.")

            # Validate file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file is too large. Maximum size is 5MB.")

        return image


class SubEventForm(forms.ModelForm):
    """Form for creating and updating sub-events"""
    class Meta:
        model = SubEvent
        fields = ['event', 'name', 'description', 'price', 'image', 'slug']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'slug': forms.TextInput(attrs={'placeholder': 'Will be auto-generated if left blank'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter out deleted events by checking if they exist
        self.fields['event'].queryset = Event.objects.all().order_by('name')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('subevent_form', 'Save Sub-Event', css_class='btn-primary'))

        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Make slug optional
        self.fields['slug'].required = False

    def clean_image(self):
        """Validate and process the uploaded image"""
        image = self.cleaned_data.get('image')
        if image:
            # Validate file type
            if not image.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise forms.ValidationError("Unsupported image format. Please use PNG, JPG, JPEG, or GIF.")

            # Validate file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file is too large. Maximum size is 5MB.")

        return image


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
        fields = ['booking_date', 'booking_time', 'address', 'mobile_number', 'notes']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter your full address', 'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Enter your mobile number', 'class': 'form-control'}),
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
            'address',
            'mobile_number',
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


class GalleryItemForm(forms.ModelForm):
    """Form for creating and updating gallery items"""
    class Meta:
        model = GalleryItem
        fields = ['subevent', 'image', 'caption', 'order']
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Brief description of the image'}),
            'order': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Display order (lower numbers appear first)'}),
        }

    def __init__(self, *args, **kwargs):
        subevent_id = kwargs.pop('subevent_id', None)
        super().__init__(*args, **kwargs)

        if subevent_id:
            self.fields['subevent'].initial = subevent_id
            self.fields['subevent'].widget = forms.HiddenInput()

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'subevent',
            'image',
            'caption',
            'order',
            Submit('submit', 'Save Gallery Item', css_class='btn-primary mt-3')
        )


class SubEventCategoryForm(forms.ModelForm):
    """Form for creating and updating subevent categories"""
    class Meta:
        model = SubEventCategory
        fields = ['name', 'description', 'image', 'price', 'is_active', 'order', 'subevent']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        subevent_id = kwargs.pop('subevent_id', None)
        super().__init__(*args, **kwargs)

        # If a specific subevent_id is provided, filter the subevent field
        if subevent_id:
            self.fields['subevent'].initial = subevent_id
            self.fields['subevent'].widget = forms.HiddenInput()
        else:
            # Otherwise, show all subevents in a dropdown
            self.fields['subevent'].queryset = SubEvent.objects.all().order_by('event__name', 'name')
            self.fields['subevent'].label_from_instance = lambda obj: f"{obj.event.name} - {obj.name}"


class UserMessageForm(forms.ModelForm):
    """Form for sending messages to users"""
    class Meta:
        model = UserMessage
        fields = ['user', 'subject', 'message', 'message_type', 'section']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show regular users (not staff or superusers)
        self.fields['user'].queryset = User.objects.filter(is_staff=False, is_superuser=False)
        self.fields['user'].label_from_instance = lambda obj: f"{obj.username} ({obj.email})"


class AddToCartForm(forms.ModelForm):
    """Form for adding items to cart"""
    class Meta:
        model = CartItem
        fields = ['category', 'quantity', 'booking_date', 'booking_time', 'guests', 'notes']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time'}),
            'quantity': forms.NumberInput(attrs={'min': 1, 'value': 1}),
            'guests': forms.NumberInput(attrs={'min': 1, 'value': 1}),
            'notes': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Any special requests or notes'}),
        }

    def __init__(self, *args, **kwargs):
        subevent_id = kwargs.pop('subevent_id', None)
        categories = kwargs.pop('categories', None)
        super().__init__(*args, **kwargs)

        if categories:
            self.fields['category'].queryset = categories

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'category',
            Row(
                Column('quantity', css_class='form-group col-md-6'),
                Column('guests', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('booking_date', css_class='form-group col-md-6'),
                Column('booking_time', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'notes',
            Submit('submit', 'Add to Cart', css_class='btn-primary mt-3')
        )


class NewsletterForm(forms.ModelForm):
    """Form for newsletter subscription"""
    class Meta:
        model = Newsletter
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Your email address', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'placeholder': 'Your name (optional)', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('newsletter_form', 'Subscribe', css_class='btn-primary'))

        # Make name field optional
        self.fields['name'].required = False
