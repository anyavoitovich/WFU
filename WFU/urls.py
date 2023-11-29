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
    vacancy_detail, resume_detail

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
    path('resume/<int:resume_id>/', resume_detail, name='resume_detail')
]
