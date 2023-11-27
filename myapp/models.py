from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    role = models.CharField(max_length=50)      # 'Driver', 'Maintenance', 'Admin', 'FuelingPerson'
    phone_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",
        blank=True,
    )
class Vehicle(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    license_plate = models.CharField(max_length=20)
    type = models.CharField(max_length=50)
    sitting_capacity = models.IntegerField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.id}'

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.OneToOneField(Vehicle, on_delete=models.SET_NULL, null=True)
    driving_license = models.CharField(max_length=50, unique=True, null=True)

    def __str__(self):
        return f'{self.user.id}'

class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class MaintenancePersonnel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class FuelingPerson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gas_station_name = models.CharField(max_length=50)

class MaintenanceRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    maintenance_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    service_type = models.CharField(max_length=50)
    date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

class FuelRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver_user = models.ForeignKey(User, on_delete=models.CASCADE)
    fuel_date = models.DateField()
    amount_of_fuel = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    gas_station_name = models.CharField(max_length=50)
    fueling_person = models.ForeignKey(FuelingPerson, on_delete=models.SET_NULL, null=True, blank=True, related_name='fuel_records')

class Route(models.Model):
    driver_user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    task_name = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50)
