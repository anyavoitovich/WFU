"""
URL configuration for WFU project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.contrib.auth import views as auth_views


from riddles import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from riddles.views import login, employerAccount, jobSeekerAccount, add_vacancy, register, add_resume, logout, \
    vacancy_detail, resume_detail, chat_view, send_message, apply_vacancy, apply_resume, view_vacancy, edit_vacancy, \
    delete_vacancy, chat_list, jobseeker_applications, jobseeker_jobs, employer_applications, employer_candidates, \
    change_candidate_status, change_job_status

urlpatterns = [
    path("", views.index, name='index'),
    path("admin/", admin.site.urls),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('employerAccount/', employerAccount, name='employerAccount'),
    path('jobSeekerAccount/', jobSeekerAccount, name='jobSeekerAccount'),
    path('add_vacancy/', add_vacancy, name='add_vacancy'),
    path('add_resume/', add_resume, name='add_resume'),
    path('logout/', logout, name='logout'),
    path('vacancy/<int:vacancy_id>/', vacancy_detail, name='vacancy_detail'),
    path('resume/<int:resume_id>/', resume_detail, name='resume_detail'),
    path('chat/<int:other_user_id>/', chat_view, name='chat_view'),
    path('send_message/<int:other_user_id>/', views.send_message, name='send_message'),
    path('apply/vacancy/<int:vacancy_id>/', apply_vacancy, name='apply_vacancy'),
    path('apply/resume/<int:resume_id>/', apply_resume, name='apply_resume'),
    path('view_vacancy/<int:vacancy_id>/', views.view_vacancy, name='view_vacancy'),
    path('vacancy/<int:vacancy_id>/edit/', edit_vacancy, name='edit_vacancy'),
    path('vacancy/<int:vacancy_id>/delete/', delete_vacancy, name='delete_vacancy'),
    path('apply/vacancy/<int:vacancy_id>/', apply_vacancy, name='apply_vacancy'),
    path('view_resume/<int:resume_id>/', views.view_resume, name='view_resume'),
    path('edit_resume/<int:resume_id>/', views.edit_resume, name='edit_resume'),
    path('delete_resume/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('chat/list/', chat_list, name='chat_list'),
    path('chat/<int:other_user_id>/', chat_view, name='chat_view'),
    path('jobseeker/applications/', jobseeker_applications, name='jobseeker_applications'),
    path('jobseeker/jobs/', jobseeker_jobs, name='jobseeker_jobs'),
    path('employer/applications/', employer_applications, name='employer_applications'),
    path('employer/candidates/', employer_candidates, name='employer_candidates'),
    path('change_candidate_status/<int:candidate_id>/', change_candidate_status, name='change_candidate_status'),
    path('change_job_status/<int:job_id>/', change_job_status, name='change_job_status'),
]
