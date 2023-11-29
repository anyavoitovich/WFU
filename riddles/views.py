import pdb

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login,  get_user_model
from django.contrib.auth.hashers import make_password
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
            print("Authentication failed")
            return HttpResponse("не нашёл пользователя с такой комбинацией email и пароля!")

    return render(request, "login.html")


def registerEmployer(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')

        if password != password2:
            return HttpResponse("Your password and confrom password are not the same!!")
        else:
            # Создаем пользователя
            hashed_password = make_password(password)
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hashed_password,
                role=role
            )
            return redirect('/login')

    return render(request, "registerEmployer.html")


# def adminAccount(request):
#     return render(request, 'adminAccount.html')
@login_required
def employerAccount(request):
    return render(request, 'employerAccount.html')
@login_required
def jobSeekerAccount(request):
    return render(request, 'jobSeekerAccount.html')
