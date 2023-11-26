from django.shortcuts import render,HttpResponse,redirect
from .models import User
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

        # Вход успешен
        request.session['user_id'] = user.UserID
        request.session['user_email'] = user.email
        request.session['user_role'] = user.role
        return redirect('/')  # Замените '/dashboard' на URL вашей целевой страницы после входа

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
