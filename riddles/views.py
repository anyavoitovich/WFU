from datetime import date

from django.views.decorators.http import require_POST

from .models import User, Vacancy, Resume, Employer, VacancyApplication, ResumeApplication, EducationalInstitution
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import User, Employer, JobSeeker, Resume, Message, Education
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .forms import EmployerRegistrationForm, JobSeekerRegistrationForm
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from django.db.models import Count
from django.views import View


@login_required
def index(request):
    vacancies = Vacancy.objects.all()
    jobseekers = JobSeeker.objects.all()
    resumes = Resume.objects.all()
    context = {'vacancies': vacancies, 'resumes': resumes, 'jobseekers':jobseekers, 'current_user': request.user}
    return render(request, 'index.html', context)

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

def register(request):
    if request.method == 'POST':
        role = request.POST.get('role')

        if role == 'Employer':
            form = EmployerRegistrationForm(request.POST)
        elif role == 'JobSeeker':
            form = JobSeekerRegistrationForm(request.POST)

            # Переместите проверку валидности сюда
            if form.is_valid():
                birthdate = form.cleaned_data.get('birthdate')
                if birthdate:
                    age = (date.today() - birthdate).days // 365
                    if age < 18 or age > 65:
                        return HttpResponse("Возраст должен быть от 18 до 65 лет")
        else:
            return HttpResponse("Недопустимая роль")

        # Переместите проверку form.is_valid() сюда
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
                                      birthdate=request.POST['birthdate'])
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
        education = Education(
            resume=new_resume,
            edu_institution=EducationalInstitution.objects.get(pk=request.POST['edu_institution']),
            level=request.POST['edu_level'],
            graduation_year=request.POST['graduation_year'],
        )
        education.save()

        return render(request, 'jobSeekerAccount.html')

        # Получение данных для выпадающего списка учебных учреждений
    edu_institutions = EducationalInstitution.objects.all()

    # Возвращаем форму добавления резюме (GET запрос)
    return render(request, 'add_resume.html', context={'current_user': request.user, 'edu_institutions': edu_institutions})

@login_required
def vacancy_detail(request, vacancy_id):
    # Retrieve the vacancy using the vacancy_id
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    employer = vacancy.employer
    # Pass the vacancy to the template context
    applications = VacancyApplication.objects.filter(vacancy=vacancy, sender=request.user)
    context = {'vacancy': vacancy, 'current_user': request.user, 'employer': employer, 'applications': applications}

    return render(request, 'vacancy_detail.html', context)


@login_required
def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)
    job_seeker = resume.job_seeker
    education = Education.objects.filter(resume=resume)
    applications = ResumeApplication.objects.filter(resume=resume, sender=request.user)
    context = {'resume': resume, 'current_user': request.user, 'job_seeker': job_seeker, 'education': education,
               'applications': applications, 'user': request.user}

    return render(request, 'resume_detail.html', context)

@login_required
def chat_view(request, other_user_id):
    try:
        other_user = get_object_or_404(User, UserID=other_user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest("User not found")

    chat_messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')

    if other_user.role == 'Employer':
        employer = get_object_or_404(Employer, EmployerID=other_user)
        context = {'other_user': employer, 'other_user_id': other_user_id, 'chat_messages': chat_messages, 'user': request.user}
    elif other_user.role == 'JobSeeker':
        job_seeker = get_object_or_404(JobSeeker, JobSeekerID=other_user)
        context = {'other_user': job_seeker, 'other_user_id': other_user_id, 'chat_messages': chat_messages, 'user': request.user}
    else:
        return HttpResponseBadRequest("Invalid user type")

    return render(request, 'chat.html', context)

@login_required
@require_POST
def send_message(request, other_user_id):
    if request.method == 'POST':
        other_user_id = int(other_user_id)
        other_user = get_object_or_404(User, UserID=other_user_id)

        message_text = request.POST.get('message')

        if message_text:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                text=message_text,
                timestamp=timezone.now()
            )

    return redirect(reverse('chat_view', kwargs={'other_user_id': other_user_id}))
@login_required
def chat_view(request, other_user_id):
    other_user = get_object_or_404(User, UserID=other_user_id)
    chat_messages = Message.objects.filter(
        (Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)),
    ).order_by('timestamp')

    context = {'other_user': other_user, 'other_user_id': other_user_id, 'chat_messages': chat_messages}
    return render(request, 'chat.html', context)
@login_required
def chat_list(request):
    user_chats_sender = Message.objects.filter(
        sender=request.user
    ).values('receiver').annotate(num_unread=Count('MessageID', filter=Q(is_read=False)))

    user_chats_receiver = Message.objects.filter(
        receiver=request.user
    ).values('sender').annotate(num_unread=Count('MessageID', filter=Q(is_read=False)))

    user_chats = user_chats_sender.union(user_chats_receiver)

    context = {'user_chats': user_chats, 'user': request.user}
    return render(request, 'chat_list.html', context)

@login_required
@require_POST
def apply_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)

    existing_application = VacancyApplication.objects.filter(vacancy=vacancy, sender=request.user).first()
    if existing_application:
        return HttpResponseBadRequest("Вы уже подавали заявку на эту вакансию.")

    VacancyApplication.objects.create(vacancy=vacancy, sender=request.user, status='Pending')

    return redirect('vacancy_detail', vacancy_id=vacancy_id)

@login_required
@require_POST
def apply_resume(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)

    existing_application = ResumeApplication.objects.filter(resume=resume, sender=request.user).first()
    if existing_application:
        return HttpResponseBadRequest("Вы уже подавали заявку на это резюме.")

    ResumeApplication.objects.create(resume=resume, sender=request.user, status='Pending')

    return redirect('resume_detail', resume_id=resume_id)

@login_required
def view_resume(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)
    job_seeker = resume.job_seeker
    education = Education.objects.filter(resume=resume)
    context = {'resume': resume, 'current_user': request.user, 'job_seeker': job_seeker, 'education': education, 'user': request.user}

    return render(request, 'view_resume.html', context)
@login_required
def edit_resume(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)

    if request.method == 'POST':
        resume.profession = request.POST['profession']
        resume.skills = request.POST['skills']
        resume.experience = request.POST['experience']
        resume.save()

        education = resume.education
        education.edu_institution = EducationalInstitution.objects.get(pk=request.POST['edu_institution'])
        education.level = request.POST['edu_level']
        education.graduation_year = request.POST['graduation_year']
        education.save()
        return redirect('jobSeekerAccount')

    context = {'resume': resume, 'user': request.user}
    return render(request, 'edit_resume.html', context)

@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)

    if request.method == 'POST':
        resume.delete()
        return redirect('jobSeekerAccount')

    context = {'resume': resume, 'user': request.user}
    return render(request, 'delete_resume.html', context)

@login_required
def view_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    context = {'vacancy': vacancy, 'user': request.user}
    return render(request, 'view_vacancy.html', context)

@login_required
def edit_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)

    if request.method == 'POST':
        vacancy.title = request.POST['title']
        vacancy.description = request.POST['description']
        vacancy.requirements = request.POST['requirements']
        vacancy.salary = request.POST['salary']
        vacancy.save()
        return redirect('employerAccount')

    context = {'vacancy': vacancy, 'user': request.user}
    return render(request, 'edit_vacancy.html', context)

@login_required
def delete_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)

    if request.method == 'POST':
        vacancy.delete()
        return redirect('employerAccount')

    context = {'vacancy': vacancy, 'user': request.user}
    return render(request, 'delete_vacancy.html', context)

@login_required
def jobseeker_applications(request):
    applications = VacancyApplication.objects.filter(sender=request.user)
    context = {'applications': applications, 'user': request.user}
    return render(request, 'jobseeker_applications.html', context)

@login_required
def jobseeker_jobs(request):
    job_applications = ResumeApplication.objects.filter(resume__job_seeker=request.user.jobseeker)
    context = {'job_applications': job_applications, 'user': request.user}
    print(context)  # Добавьте этот отладочный вывод
    return render(request, 'jobseeker_jobs.html', context)

@login_required
def employer_applications(request):
    applications = ResumeApplication.objects.filter(sender=request.user)
    employer_applications = VacancyApplication.objects.filter(vacancy__employer=request.user.employer)
    context = {'applications': applications, 'candidates': employer_applications,'user': request.user}
    return render(request, 'employer_applications.html', context)

@login_required
def employer_candidates(request):
    employer_applications = VacancyApplication.objects.filter(vacancy__employer=request.user.employer)
    context = {'candidates': employer_applications, 'user': request.user}
    return render(request, 'employer_candidates.html', context)

@login_required
@require_POST
def change_candidate_status(request, candidate_id):
    candidate = get_object_or_404(VacancyApplication, pk=candidate_id)
    new_status = request.POST.get('new_status')

    # Validate that the new_status is one of the allowed choices
    if new_status in ['Accepted', 'Rejected', 'Pending']:
        candidate.status = new_status
        candidate.save()

    # Вернуться на страницу с кандидатами работодателя
    return redirect('employer_candidates')

@login_required
@require_POST
def change_job_status(request, job_id):
    job_application = get_object_or_404(ResumeApplication, pk=job_id)
    new_status = request.POST.get('new_status')

    # Проверка, что new_status - это один из разрешенных вариантов
    if new_status in ['Accepted', 'Rejected', 'Pending']:
        job_application.status = new_status
        job_application.save()

    # Вернуться на страницу с кандидатами работодателя
    return redirect('jobseeker_jobs')