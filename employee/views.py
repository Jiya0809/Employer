from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee

# Show all employees
def index(request):
    query = request.GET.get('q')
    
    if query:
        employees = Employee.objects.filter(name__icontains=query)
    else:
        employees = Employee.objects.all()

    total_employees = employees.count()
    total_salary = sum(emp.salary for emp in employees)

    context = {
        'employees': employees,
        'total_employees': total_employees,
        'total_salary': total_salary,
        'query': query
    }

    return render(request, 'employee/index.html', context)


# Add employee
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


# Update employee
def update_employee(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":
        employee.name = request.POST['name']
        employee.email = request.POST['email']
        employee.salary = request.POST['salary']
        employee.department = request.POST['department']
        employee.save()
        return redirect('index')

    return render(request, 'employee/update.html', {'employee': employee})


# Delete employee
def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('index')