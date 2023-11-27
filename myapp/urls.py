from django.urls import path

from . import views

urlpatterns = [
    # path("", views.redirect_to_login, name="redirect_to_login"),
    path("login/", views.login_view, name="login"),
    path("", views.home, name="home"),
    path("service_page/", views.service_page, name="service_page"),
    path("vehicles/", views.vehicles, name="vehicles"),
    path("vehicles/register", views.register_vehicle, name="register_vehicle"),
    path("vehicles/assign", views.assign_vehicle, name="assign_vehicle"),
    path('vehicles/delete/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path("personnel/", views.personnel, name="personnel"),
    path("contacts/", views.contacts, name="contacts"),
    path("about_us/", views.about_us, name="about_us"),
    path("make_an_appointment/", views.make_an_appointment, name="make_an_appointment"),
    path("logout/", views.logout_view, name="logout"),
    path('personnel/select_role/', views.select_role, name='select_role'),
    path('personnel/register/', views.register_personnel, name='register_personnel'),
    path('personnel/delete/<int:user_id>/', views.delete_personnel, name='delete_personnel'),
    path('personnel/search/', views.search_personnel, name='search_personnel'),
    path('create_task/', views.create_task, name='create_task'),
]