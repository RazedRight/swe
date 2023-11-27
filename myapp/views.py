from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import (
    CustomAuthenticationForm,
    BaseUserRegistrationForm,
    AdminRegistrationForm,
    DriverRegistrationForm,
    MaintenancePersonnelRegistrationForm,
    FuelingPersonRegistrationForm
)
from django.contrib.auth import login, authenticate
from django.contrib.auth import authenticate, login as auth_login  # ensure correct import
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next') or request.GET.get('next')
                print(next_url)
                if next_url:
                    return redirect(next_url)
                return redirect('home')  # Replace with your home view's URL name
    else:
        form = CustomAuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

@login_required
def home(request):
    return render(request, "myapp/home.html", {})

@login_required
def service_page(request):
    return render(request, "myapp/service_page.html", {})

@login_required
def vehicles(request):
    return render(request, "myapp/vehicles.html", {})

@login_required
def personnel(request):
    selected_role = request.GET.get('role')
    personnel_data = None

    if selected_role == 'Driver':
        personnel_data = Driver.objects.select_related('user').all()
    elif selected_role == 'Maintenance':
        personnel_data = MaintenancePersonnel.objects.select_related('user').all()
    elif selected_role == 'FuelingPerson':
        personnel_data = FuelingPerson.objects.select_related('user').all()

    return render(request, 'myapp/personnel.html', {'personnel_data': personnel_data, 'selected_role': selected_role})

@login_required
def contacts(request):
    return render(request, "myapp/contacts.html", {})

@login_required
def about_us(request):
    return render(request, "myapp/about_us.html", {})

@login_required
def make_an_appointment(request):
    return render(request, "myapp/appointment.html", {})

@login_required
def logout_view(request):
    logout(request)
    return redirect('../login')

from django.shortcuts import render, redirect
from .forms import (BaseUserRegistrationForm, DriverRegistrationForm, 
                    AdminRegistrationForm, MaintenancePersonnelRegistrationForm, 
                    FuelingPersonRegistrationForm, VehicleRegistrationForm, VehicleAssignmentForm, TaskCreationForm)
from .models import User, Driver, Admin, MaintenancePersonnel, FuelingPerson, Vehicle

from django.shortcuts import render

def select_role(request):
    return render(request, 'myapp/select_role.html')

def register_personnel(request):
    # Get the role from the URL parameter
    selected_role = request.GET.get('role')
    # Choose the appropriate form based on the selected role
    form_class = get_form_class_for_role(selected_role)

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            # Create the User instance
            new_user = form.save(commit=False)
            new_user.role = selected_role
            new_user.save()

            # Create the role-specific profile
            create_related_profile(new_user, form.cleaned_data)

            # Redirect to success view
            return redirect('personnel')
    else:
        form = form_class()

    return render(request, 'myapp/register_personnel.html', {'form': form, 'role': selected_role})

def get_form_class_for_role(role, *args, **kwargs):
    if role == 'Driver':
        return DriverRegistrationForm
    elif role == 'Admin':
        return AdminRegistrationForm
    elif role == 'FuelingPerson':
        return FuelingPersonRegistrationForm
    elif role == 'Maintenance':
        return MaintenancePersonnelRegistrationForm
    else:
        print("You have to choose a role to register new user")

def create_related_profile(user, cleaned_data):
    print(user.role)
    if user.role == 'Driver':
        driving_license = cleaned_data.get('driving_license', None)
        print(driving_license)
        Driver.objects.create(user=user, driving_license=driving_license)
    elif user.role == 'Admin':
        Admin.objects.create(user=user)
    elif user.role == 'FuelingPerson':
        gas_station_name = cleaned_data.get('gas_station_name', None)
        FuelingPerson.objects.create(user=user, gas_station_name=gas_station_name)
    elif user.role == 'Maintenance':
        MaintenancePersonnel.objects.create(user=user)

def personnel_home(request):
    selected_role = request.GET.get('role')
    form_class = get_form_class_for_role(selected_role)

    # Assuming you have a model for each personnel type, adjust accordingly
    if selected_role == 'Driver':
        personnel_list = Driver.objects.all()
    elif selected_role == 'Admin':
        personnel_list = Admin.objects.all()
    elif selected_role == 'FuelingPerson':
        personnel_list = FuelingPerson.objects.all()
    elif selected_role == 'Maintenance':
        personnel_list = MaintenancePersonnel.objects.all()
    else:
        personnel_list = User.objects.all()  # Display all personnel

    return render(request, 'myapp/personnel.html', {'form': form_class(), 'role': selected_role, 'personnel_list': personnel_list})

def delete_personnel(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('personnel')  # Redirect back to the personnel page after deletion

def search_personnel(request):
    query = request.GET.get('q', '')
    personnel_data = []

    # Search in the User table based on the query
    users = User.objects.filter(first_name__icontains=query) | \
            User.objects.filter(surname__icontains=query)

    for user in users:
        user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'surname': user.surname,
            'email': user.email,
            'phone_number': user.phone_number,
            'role': user.role,
            'created_at': user.created_at
        }
        # Check the user's role and get additional data from related models
        if user.role == 'Driver':
            driver = Driver.objects.get(user=user)
            user_data['vehicle'] = driver.vehicle
            user_data['driving_license'] = driver.driving_license
        elif user.role == 'FuelingPerson':
            fueling_person = FuelingPerson.objects.get(user=user)
            user_data['gas_station_name'] = fueling_person.gas_station_name
            # Add additional fields specific to FuelingPerson
        personnel_data.append(user_data)
    return render(request, 'myapp/search_personnel.html', {'personnel_data': personnel_data, 'search_query': query})

def register_vehicle(request):
    if request.method == 'POST':
        form = VehicleRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicles')  # Redirect to the vehicle list page after successful registration
    else:
        form = VehicleRegistrationForm()

    return render(request, 'myapp/register_vehicle.html', {'form': form})
def vehicles(request):
    vehicles = Vehicle.objects.all()
    print(vehicles)
    return render(request, 'myapp/vehicles.html', {'vehicles': vehicles})

def assign_vehicle(request):
    if request.method == 'POST':
        form = VehicleAssignmentForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            driver_id = form.cleaned_data['driver'].id
            vehicle_id = form.cleaned_data['vehicle'].id

            # Update the Driver table to assign the vehicle to the driver
            driver = Driver.objects.get(id=driver_id)
            driver.vehicle = Vehicle.objects.get(id=vehicle_id)
            driver.save()

            return redirect('vehicles')  # Redirect to the vehicles list page
    else:
        form = VehicleAssignmentForm()

    return render(request, 'myapp/assign_vehicle.html', {'form': form})

def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    vehicle.delete()
    return redirect('vehicles')  # Replace 'vehicles_list' with the URL name of your vehicle list page

import json  # Import JSON module to parse location data

def create_task(request):
    if request.method == 'POST':
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            route = form.save(commit=False)

            # Process start_location and end_location from Google Maps
            start_location_data = json.loads(request.POST.get('start_location', '{}'))
            end_location_data = json.loads(request.POST.get('end_location', '{}'))

            route.start_location = f"{start_location_data.get('lat')}, {start_location_data.get('lng')}"
            route.end_location = f"{end_location_data.get('lat')}, {end_location_data.get('lng')}"

            route.save()  # Save the route with updated locations
            return redirect('home')
    else:
        form = TaskCreationForm()

    return render(request, 'myapp/create_task.html', {'form': form})