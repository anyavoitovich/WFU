from django.views.decorators.http import require_POST

from .models import User, Vacancy, Resume, VacancyApplication, Employer
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import User, Employer, JobSeeker, Resume, Message
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from .forms import EmployerRegistrationForm, JobSeekerRegistrationForm
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from django.views import View


@login_required
def index(request):
    vacancies = Vacancy.objects.all()
    jobseekers = JobSeeker.objects.all()
    resumes = Resume.objects.all()
    context = {'vacancies': vacancies, 'resumes': resumes, 'jobseekers':jobseekers, 'current_user': request.user}
    return render(request, 'index.html', context)


# ...


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse("Invalid login credentials!")

        if check_password(password, user.password):
            auth_login(request, user)
            context = {'current_user': request.user}
            if user.role == 'Admin':
                return redirect('adminAccount')
            elif user.role == 'Employer':
                return render(request, 'employerAccount.html', context)
            elif user.role == 'JobSeeker':
                return render(request, 'jobSeekerAccount.html', context)
        else:
            print("Authentication failed")
            return HttpResponse("Invalid login credentials!")

    return render(request, "login.html")

@login_required
def logout(request):
    auth_logout(request)
    return redirect('index')

# def registerEmployer(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')
#         role = request.POST.get('role')
#
#         if password != password2:
#             return HttpResponse("Your password and confrom password are not the same!!")
#         else:
#             # Создаем пользователя
#             hashed_password = make_password(password)
#             user = User.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 email=email,
#                 password=hashed_password,
#                 role=role
#             )
#             return redirect('/login')
#
#     return render(request, "register.html")


def register(request):
    if request.method == 'POST':
        role = request.POST.get('role')

        if role == 'Employer':
            form = EmployerRegistrationForm(request.POST)
        elif role == 'JobSeeker':
            form = JobSeekerRegistrationForm(request.POST)
        else:
            return HttpResponse("Неверная роль")

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password1'])
            user.save()

            if role == 'Employer':
                employer = Employer(EmployerID=user,
                                    company_name=request.POST['company_name'],
                                    company_description=request.POST['company_description'])
                employer.save()

            elif role == 'JobSeeker':
                jobseeker = JobSeeker(JobSeekerID=user,
                                      birthdate=request.POST['birthdate'],
                                      education=request.POST['education'],
                                      experience=request.POST['experience'])
                jobseeker.save()

            context = {'current_user': user}

            return render(request, 'login.html', context)
    else:
        form = EmployerRegistrationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def employerAccount(request):
    context = {'current_user': request.user}
    return render(request, 'employerAccount.html', context)

@login_required
def jobSeekerAccount(request):
    context = {'current_user': request.user}
    return render(request, 'jobSeekerAccount.html', context)


# @login_required
# def add_vacancy(request):
#     # Проверяем, является ли пользователь работодателем
#     if request.user.role != 'Employer':
#         print("Пользователь не является работодателем. Доступ запрещен.")
#         return HttpResponse("Вы не авторизованы для добавления вакансий.")
#
#     if request.method == 'POST':
#         try:
#             employer = request.user.employer
#             print(f"Пользователь: {request.user}, Работодатель: {employer}")
#
#             new_vacancy = Vacancy(
#                 employer=employer,
#                 title=request.POST['title'],
#                 description=request.POST['description'],
#                 requirements=request.POST['requirements'],
#                 salary=request.POST['salary']
#             )
#             new_vacancy.save()
#
#             print("Вакансия успешно добавлена.")
#             return render(request, 'employerAccount.html')
#         except Employer.DoesNotExist:
#             print("У пользователя нет объекта работодателя.")
#             return render(request, 'add_vacancy.html', {'warning': True})
#
#     return render(request, 'add_vacancy.html')


@login_required
def add_vacancy(request):
    # Проверяем, является ли пользователь работодателем
    if request.user.role != 'Employer':
        print("Пользователь не является работодателем. Доступ запрещен.")
        return HttpResponse("Вы не авторизованы для добавления вакансий.")
    employer = request.user.employer
    # Ваш остальной код добавления вакансии
    if request.method == 'POST':
        # Обработка добавления вакансии
        new_vacancy = Vacancy(
            employer=employer,
            title=request.POST['title'],
            description=request.POST['description'],
            requirements=request.POST['requirements'],
            salary=request.POST['salary']
        )
        new_vacancy.save()
        return render(request, 'employerAccount.html')

    # Возвращаем форму добавления вакансии (GET запрос)
    return render(request, 'add_vacancy.html', context={'current_user': request.user})

@login_required
def add_resume(request):
    # Проверяем, является ли пользователь работодателем
    if request.user.role != 'JobSeeker':
        print("Пользователь не является соискателем. Доступ запрещен.")
        return HttpResponse("Вы не авторизованы для добавления вакансий.")
    job_seeker = request.user.jobseeker
    # Ваш остальной код добавления вакансии
    if request.method == 'POST':
        # Обработка добавления вакансии
        new_resume = Resume(
            job_seeker=job_seeker,
            profession=request.POST['profession'],
            skills=request.POST['skills'],
            experience=request.POST['experience'],
        )
        new_resume.save()
        return render(request, 'jobSeekerAccount.html')

    # Возвращаем форму добавления вакансии (GET запрос)
    return render(request, 'add_resume.html', context={'current_user': request.user})
def vacancy_detail(request, vacancy_id):
    # Retrieve the vacancy using the vacancy_id
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    employer = vacancy.employer
    # Pass the vacancy to the template context
    context = {'vacancy': vacancy,'current_user': request.user, 'employer': employer}

    return render(request, 'vacancy_detail.html', context)


@login_required
def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)
    job_seeker = resume.job_seeker
    context = {'resume': resume, 'current_user': request.user, 'job_seeker': job_seeker}
    return render(request, 'resume_detail.html', context)



@login_required
def chat_view(request, other_user_id):
    print("Other User ID:", other_user_id)

    try:
        other_user = get_object_or_404(User, UserID=other_user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest("User not found")

    print("Other User:", other_user)
    chat_messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')


    if other_user.role == 'Employer':
        employer = get_object_or_404(Employer, EmployerID=other_user)
        context = {'other_user': employer, 'other_user_id': other_user_id, 'chat_messages': chat_messages}
    elif other_user.role == 'JobSeeker':
        job_seeker = get_object_or_404(JobSeeker, JobSeekerID=other_user)
        context = {'other_user': job_seeker, 'other_user_id': other_user_id, 'chat_messages': chat_messages}
    else:
        # Handle cases where the user type is not defined
        return HttpResponseBadRequest("Invalid user type")

    return render(request, 'chat.html', context)



import logging

logger = logging.getLogger(__name__)

@login_required
@require_POST
def send_message(request, other_user_id):
    logger.info("send_message view is called.")

    if request.method == 'POST':
        other_user_id = int(other_user_id)
        other_user = get_object_or_404(User, UserID=other_user_id)

        # Используйте 'UserID' вместо 'id'
        message_text = request.POST.get('message')

        if message_text:
            # Create a new message
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                text=message_text,
                timestamp=timezone.now()
            )

    # Используйте reverse для создания URL с именем 'chat' и параметром other_user_id
    return redirect(reverse('chat_view', kwargs={'other_user_id': other_user_id}))

