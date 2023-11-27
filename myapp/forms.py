# forms.py in your Django app
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Driver, Admin, MaintenancePersonnel, FuelingPerson, Vehicle, Route

# Base form for User model
class BaseUserRegistrationForm(UserCreationForm):
    role = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'surname', 'phone_number', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the role field from the form
        del self.fields['role']

class DriverRegistrationForm(BaseUserRegistrationForm):
    # Add extra fields for Driver
    driving_license = forms.CharField(max_length=50)
    # vehicle = forms.CharField(max_length=50)

class FuelingPersonRegistrationForm(BaseUserRegistrationForm):
    gas_station_name = forms.CharField(max_length=50)

class AdminRegistrationForm(BaseUserRegistrationForm):
    pass  # Admin doesn't have any additional fields

class MaintenancePersonnelRegistrationForm(BaseUserRegistrationForm):
    pass  # MaintenancePersonnel doesn't have any additional fields

class VehicleRegistrationForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'

    widgets = {
        'make': forms.TextInput(attrs={'class': 'form-control'}),
        'model': forms.TextInput(attrs={'class': 'form-control'}),
        'year': forms.NumberInput(attrs={'class': 'form-control'}),
        'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
        'type': forms.TextInput(attrs={'class': 'form-control'}),
        'sitting_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        'status': forms.TextInput(attrs={'class': 'form-control'}),
    }

class VehicleAssignmentForm(forms.Form):
    driver = forms.ModelChoiceField(queryset=Driver.objects.all())
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all())

    def __init__(self, *args, **kwargs):
        super(VehicleAssignmentForm, self).__init__(*args, **kwargs)
        self.fields['driver'].label_from_instance = lambda obj: f'Driver ID: {obj.user.id} - {obj.user.first_name} {obj.user.surname}'
        self.fields['vehicle'].label_from_instance = lambda obj: f'Vehicle ID: {obj.id} - {obj.make} {obj.model} {obj.year}'

class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['task_name', 'driver_user', 'start_location', 'end_location']

    def __init__(self, *args, **kwargs):
        super(TaskCreationForm, self).__init__(*args, **kwargs)
        # Customize the form fields here, e.g., for the driver selection field:
        self.fields['driver_user'].queryset = User.objects.filter(role='Driver')