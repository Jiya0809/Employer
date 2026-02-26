from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('register')

urlpatterns = [

    path('', home_redirect, name='home'),

    path('register/', views.register_view, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(template_name='auth/login.html'),
        name='login'
    ),

    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('employees/', views.index, name='index'),
    path('add/', views.add_employee, name='add_employee'),
    path('update/<int:id>/', views.update_employee, name='update_employee'),
    path('delete/<int:id>/', views.delete_employee, name='delete_employee'),
]