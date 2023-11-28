from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login as auth_login
# Create your views here.

def index(request):
    return render(request, "index.html")

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            # Пользователь с таким email и паролем не найден
            return HttpResponse("Invalid login credentials!")


        request.session['user_id'] = user.UserID
        request.session['user_email'] = user.email
        request.session['user_role'] = user.role
        if user.role == 'Admin':
            return redirect('adminAccount')
        elif user.role == 'Employer':
            return redirect('employerAccount')
        elif user.role == 'JobSeeker':
            return redirect('jobSeekerAccount')
        else:
            return HttpResponse("Invalid login credentials!")

    return render(request, "login.html")

def registrationJobSeeker(request):
    return render(request, "registerJobSeeker.html")

def registerEmployer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')

        if password != password2:
            return HttpResponse("Your password and confrom password are not the same!!")
        else:
            # Создаем пользователя
            user = User.objects.create(
                name=name,
                surname=surname,
                email=email,
                password=password,
                role=role
            )
            return redirect('/login')

    return render(request, "registerEmployer.html")

@user_passes_test(lambda u: u.role == 'Admin')
@login_required
def adminAccount(request):
    return render(request, 'adminAccount.html')

@user_passes_test(lambda u: u.role == 'Employer')
@login_required
def employerAccount(request):
    return render(request, 'employerAccount.html')
def is_job_seeker(user):
    return user.role == 'JobSeeker'

@user_passes_test(is_job_seeker)
def jobSeekerAccount(request):
    return render(request, 'jobSeekerAccount.html')

