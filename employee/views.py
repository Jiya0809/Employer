import re
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django import forms

def home(request):
    # If user already logged in → dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    # If no users exist → show register page
    if not User.objects.exists():
        return redirect('register')

    # If user exists but not logged in → show login
    return redirect('login')

# Custom Register Form
class RegisterForm(UserCreationForm):

    username = forms.CharField(
        max_length=150,
        required=True,
        help_text="Only alphabets and spaces allowed.",
        validators=[]   # Remove default Django validators
    )

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()

        # Only alphabets and spaces allowed
        if not re.fullmatch(r"[A-Za-z ]+", username):
            raise forms.ValidationError(
                "Username must contain only alphabets and spaces."
            )

        return username

# Register View
def register_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")   # Go to login after register
    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})

# Logout View
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    
    return render(request, "employee/logout.html")

# Dashboard View
@login_required
def dashboard(request):
    total_employees = Employee.objects.count()
    total_departments = Employee.objects.values('department').distinct().count()
    total_salary = Employee.objects.aggregate(Sum('salary'))['salary__sum'] or 0

    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'total_salary': total_salary,
    }
    return render(request, 'employee/dashboard.html', context)


# Show All Employees
@login_required
def index(request):
    query = request.GET.get('q')

    if query:
        employees = Employee.objects.filter(name__icontains=query)
    else:
        employees = Employee.objects.all()

    total_employees = employees.count()
    total_salary = employees.aggregate(Sum('salary'))['salary__sum'] or 0

    context = {
        'employees': employees,
        'total_employees': total_employees,
        'total_salary': total_salary,
        'query': query
    }

    return render(request, 'employee/index.html', context)


# Add Employee
@login_required
def add_employee(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        salary = request.POST['salary']
        department = request.POST['department']

        Employee.objects.create(
            name=name,
            email=email,
            salary=salary,
            department=department
        )
        return redirect('index')

    return render(request, 'employee/add.html')


# Update Employee
@login_required
def update_employee(request, id):
    employee = Employee.objects.get(id=id)

    if request.method == "POST":
        employee.name = request.POST.get('name')
        employee.email = request.POST.get('email')
        employee.department = request.POST.get('department')
        employee.salary = request.POST.get('salary')
        employee.save()
        return redirect('index')

    return render(request, 'employee/update_employee.html', {'employee': employee})

# Delete Employee
@login_required
def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('index')