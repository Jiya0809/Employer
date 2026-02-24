from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # First page when server starts
    path('', views.register_view, name='register'),

    # Login (Django built-in)
    path('login/', auth_views.LoginView.as_view(template_name='employee/login.html'), name='login'),

    # Logout
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Employee CRUD
    path('employees/', views.index, name='index'),
    path('add/', views.add_employee, name='add_employee'),
    path('update/<int:id>/', views.update_employee, name='update_employee'),
    path('delete/<int:id>/', views.delete_employee, name='delete_employee'),
]